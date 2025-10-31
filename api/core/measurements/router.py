from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.db.session import get_db
from api.db.crud import measurements
from api.db.schemas.measurements import MeasurementCreate, MeasurementRead, MeasurementUpdate

# import os

router = APIRouter(prefix="/measurements", tags=['Measurements'])

@router.get("/", response_model=List[MeasurementRead])
async def list_measurements(
    limit: int = 100, offset: int = 0, db: AsyncSession = Depends(get_db)
):
    return await measurements.get_all(db, limit=limit, offset=offset)

@router.get("/{measurement_id}", response_model=MeasurementRead)
async def get_measurement(measurement_id: int, db: AsyncSession = Depends(get_db)):
    measurement = await measurements.get_by_id(db, measurement_id)
    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement no found :(")
    return measurement

# @router.get("/nearby", response_model=List[MeasurementRead])
# async def nearby_measurements(
#     lat: float = Query(..., description="Latitude in decimal degrees"),
#     lon: float = Query(..., description="Longitude in decimal degrees"),
#     radius_km: float = Query(1.0, description="Radius in kilometers"),
#     db: AsyncSession = Depends(get_db),
# ):
#     measurements = await get_measurements_nearby(db, lat, lon, radius_km) # Need to actually implement this
#     return measurements

@router.post("/", response_model=MeasurementRead)
async def create_measurement(measurement_in: MeasurementCreate, db: AsyncSession = Depends(get_db)):
    measurement = await measurements.create(db, measurement_in)
    return measurement