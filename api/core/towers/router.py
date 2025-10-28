from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.db.session import get_db
from api.db.crud import cell_tower
from api.db.schemas.cell_tower import CellTowerCreate, CellTowerRead, CellTowerUpdate
from api.core.towers.service import get_towers_nearby
from api.core.towers.opencell_client import OpenCellIDClient

import os

router = APIRouter(prefix="/towers", tags=["Cell Towers"])


@router.get("/", response_model=List[CellTowerRead])
async def list_towers(
    limit: int = 100, offset: int = 0, db: AsyncSession = Depends(get_db)
):
    return await cell_tower.get_all(db, limit=limit, offset=offset)


@router.get("/{tower_id}", response_model=CellTowerRead)
async def get_tower(tower_id: int, db: AsyncSession = Depends(get_db)):
    tower = await cell_tower.get_by_id(db, tower_id)
    if not tower:
        raise HTTPException(status_code=404, detail="Tower not found")
    return tower


@router.get("/nearby", response_model=list[CellTowerRead])
async def nearby_towers(
    lat: float = Query(..., description="Latitude in decimal degrees"),
    lon: float = Query(..., description="Longitude in decimal degrees"),
    radius_km: float = Query(1.0, description="Radius in kilometers"),
    db: AsyncSession = Depends(get_db),
):
    towers = await get_towers_nearby(db, lat, lon, radius_km)
    return towers


@router.post("/", response_model=CellTowerRead)
async def create_tower(tower_in: CellTowerCreate, db: AsyncSession = Depends(get_db)):
    tower = await cell_tower.create(db, tower_in)
    return tower


@router.patch("/{tower_id}", response_model=CellTowerRead)
async def update_tower(
    tower_id: int, tower_in: CellTowerUpdate, db: AsyncSession = Depends(get_db)
):
    tower = await cell_tower.update(db, tower_id, tower_in)
    if not tower:
        raise HTTPException(status_code=404, detail="Tower not found")
    return tower


@router.delete("/{tower_id}")
async def delete_tower(tower_id: int, db: AsyncSession = Depends(get_db)):
    success = await cell_tower.delete(db, tower_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tower not found")
    return {"ok": True}


@router.post("/sync/opencellid")
async def sync_opencellid(
    lat_min: float,
    lon_min: float,
    lat_max: float,
    lon_max: float,
    db: AsyncSession = Depends(get_db),
):
    client = OpenCellIDClient(api_key=os.getenv("OPENCELLID_API_KEY"))
    data = await client.fetch_bbox(lat_min, lon_min, lat_max, lon_max)
    towers = await client.sync_to_db(db, data)
    return {"fetched": len(towers)}
