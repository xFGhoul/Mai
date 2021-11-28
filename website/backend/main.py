import os
import aioredis
import uvicorn
import secrets

from pathlib import Path

from fastapi import Depends, FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from starlette_discord.client import DiscordOAuthClient
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse, JSONResponse
from starlette.requests import Request
from starlette.exceptions import HTTPException

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from fastapi_events.dispatcher import dispatch
from fastapi_events.middleware import EventHandlerASGIMiddleware
from fastapi_events.handlers.local import local_handler

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from config.ext.parser import config

from exceptions.exceptions import UserIsBlacklisted, GuildIsBlacklisted
from helpers.classes import EmailTemplates
from models.schemas import EmailSchema, EmailContent


conf = ConnectionConfig(
    MAIL_USERNAME=config["MAIL_USERNAME"],
    MAIL_PASSWORD=config["MAIL_PASSWORD"],
    MAIL_FROM=config["MAIL_FROM"],
    MAIL_PORT=config["MAIL_PORT"],
    MAIL_SERVER=config["MAIL_SERVER"],
    MAIL_TLS=config["MAIL_TLS"],
    MAIL_SSL=config["MAIL_SSL"],
    USE_CREDENTIALS=config["MAIL_USE_CREDENTIALS"],
    VALIDATE_CERTS=config["MAIL_VALIDATE_CERTS"],
    TEMPLATE_FOLDER=Path(__file__).parent / "templates/emails",
)


app = FastAPI(debug=True)

CLIENT_ID = str(config["DISCORD_CLIENT_ID"])
CLIENT_SECRET = config["DISCORD_CLIENT_SECRET"]
REDIRECT_URL = config["DISCORD_REDIRECT_URL"]

discord = DiscordOAuthClient(
    CLIENT_ID, CLIENT_SECRET, REDIRECT_URL, scopes=("identify", "email")
)


@cache()
async def get_cache():
    return 1


# -- PATHS


@app.post("api/v1/email")
async def send_email(
    background_tasks: BackgroundTasks, email: EmailSchema, content: EmailContent
) -> JSONResponse:

    message = MessageSchema(
        subject=content.subject,
        recipients=email.recipients,  # List of recipients, as many as you can pass
        html=content.html,
        subtype="html",
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message)

    return JSONResponse(
        status_code=200, content={"message": "email has been sent"}
    )


@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
@cache(expire=60)
async def root(request: Request) -> JSONResponse:
    return JSONResponse({"message": "Hello World"})


@app.get("/api/v1/login")
@cache(expire=60)
async def login():
    return discord.redirect()


@app.get("/auth/discord/redirect")
@cache(expire=60)
async def redirect(request: Request, code: str):
    user = await discord.login(code)
    request.session["discord_user"] = user
    return RedirectResponse("/api/v1/users/me")


@app.get("/api/v1/users/me")
@cache(expire=60)
async def get_user(request: Request):
    user = request.session.get("discord_user")

    # dispatch("on_discord_get_user", payload={"id": user.id})
    return user.json()


@app.get("/api/v1/guilds")
@cache(expire=60)
async def get_guilds(guilds):
    return guilds


# -- Events


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await FastAPILimiter.init(redis)


if __name__ == "__main__":
    app.add_middleware(EventHandlerASGIMiddleware, handlers=[local_handler])
    app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(64))
    origins = ["http://localhost:3000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app_name = os.path.basename(__file__).replace(".py", "")
    uvicorn.run(
        app=f"{app_name}:app",
        host="127.0.0.1",
        port=6969,
        workers=1,
        reload=True,
        debug=True,
    )
