from typing import List

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_discord import DiscordOAuthClient, RateLimited, Unauthorized, User
from fastapi_discord.models import GuildPreview

from config.ext.parser import config

app = FastAPI()

CLIENT_ID = config["DISCORD_CLIENT_ID"]
CLIENT_SECRET = config["DISCORD_CLIENT_SECRET"]
REDIRECT_URL = config["DISCORD_REDIRECT_URL"]

discord = DiscordOAuthClient(
    CLIENT_ID, CLIENT_SECRET, REDIRECT_URL, ("identify", "guilds", "email")
)  # scopes

app.get("/")


async def read_root():
    return {"message": "Hello World"}


@app.get("/login")
async def login():
    return RedirectResponse(discord.oauth_login_url)


@app.get("/callback")
async def callback(code: str):
    token, refresh_token = await discord.get_access_token(code)
    return {"access_token": token, "refresh_token": refresh_token}


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
    "/user",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=User,
)
async def get_user(user: User = Depends(discord.user)):
    return user


@app.get(
    "/guilds",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=List[GuildPreview],
)
async def get_guilds(guilds: List = Depends(discord.guilds)):
    return guilds
