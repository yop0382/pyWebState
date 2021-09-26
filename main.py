import uvicorn as uvicorn
from fastapi import FastAPI

from Pg import Pg

app = FastAPI()
pg = Pg()


@app.get("/status/{command_id}")
async def root(command_id: int):
    return pg.get_command_progress(command_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
