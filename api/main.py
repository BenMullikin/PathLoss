from fastapi import FastAPI

from api.core.towers.router import router as tower_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok"}


app.include_router(tower_router)
