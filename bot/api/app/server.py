import os
import uvicorn

from fastapi import FastAPI

from ...db.models import Guild

app = FastAPI()


@app.get("/")
async def root():
    return {"Message": "Hello World"}


@app.get("/guild/{id}")
async def get_guild(id: int):
    guild = await Guild.get(discord_id=id).values()
    return guild


if __name__ == "__main__":
    app_name = os.path.basename(__file__).replace(".py", "")
    uvicorn.run(
        app=f"{app_name}:app",
        host="127.0.0.1",
        port=7777,
        workers=1,
        reload=True,
        debug=True,
    )
