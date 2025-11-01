from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.core.towers.router import router as tower_router
from api.core.measurements.router import router as measurements_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok"}


app.include_router(tower_router)
app.include_router(measurements_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)