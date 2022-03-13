import uvicorn
import os

from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"Content": "Hello World"}


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
