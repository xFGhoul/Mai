import os
import aioredis
import uvicorn
import secrets

from typing import List
from pathlib import Path

from fastapi import Depends, FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.requests import Request

from fastapi_discord import DiscordOAuthClient, RateLimited, Unauthorized, User
from fastapi_discord.models import GuildPreview

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from fastapi_events.dispatcher import dispatch
from fastapi_events.middleware import EventHandlerASGIMiddleware
from fastapi_events.handlers.local import local_handler

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from starlette.middleware.sessions import SessionMiddleware

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


app = FastAPI()
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


@app.get("/auth/discord/login")
@cache(expire=60)
async def discord_login():
    return RedirectResponse(discord.oauth_login_url)


@app.get("/auth/discord/redirect")
@cache(expire=60)
async def discord_callback(request: Request, code: str):
    token, refresh_token = await discord.get_access_token(code)
    request.session["discord_token"] = token
    return RedirectResponse("/api/v1/users/me")


@app.get(
    "/authenticated",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=bool,
)
async def isAuthenticated(token: str = Depends(discord.get_token)):
    try:
        auth = await discord.isAuthenticated(token)
        return auth
    except Unauthorized:
        return False


@app.exception_handler(Unauthorized)
async def unauthorized_error_handler(_, __):
    return JSONResponse({"error": "Unauthorized"}, status_code=401)


@app.exception_handler(RateLimited)
async def rate_limit_error_handler(_, e: RateLimited):
    return JSONResponse(
        {"error": "RateLimited", "retry": e.retry_after, "message": e.message},
        status_code=429,
    )


@app.get(
    "/api/v1/users/me",
    # dependencies=[Depends(discord.requires_authorization)],
    # response_model=User,
)
@cache(expire=60)
async def get_user(request: Request):

    token = request.session.get("discord_token")

    if token:
        request.headers.__dict__["_list"].append(
            (b"authorization", f"Bearer {token}".encode())
        )
        return token
    else:
        return RedirectResponse("/auth/discord/login")


@app.get(
    "/api/v1/guilds",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=List[GuildPreview],
)
@cache(expire=60)
async def get_guilds(guilds: List = Depends(discord.guilds)):
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
    app_name = os.path.basename(__file__).replace(".py", "")
    uvicorn.run(
        app=f"{app_name}:app",
        host="127.0.0.1",
        port=6969,
        workers=1,
        reload=True,
        debug=True,
    )
