import uvicorn
import os

from typing import Optional

from fastapi import FastAPI

from ..db.models import Guild

app = FastAPI()


@app.get("/")
async def root():
    guild = await Guild.get_or_none(discord_id=806599466604953641).values()
    return {"Guild Information": guild}


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
