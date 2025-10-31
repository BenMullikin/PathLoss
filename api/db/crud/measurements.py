from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from geoalchemy2.shape import from_shape
from shapely.geometry import Point # type: ignore

from api.db.models.measurements import Measurement
from api.db.schemas.measurements import MeasurementCreate, MeasurementUpdate


async def get_all(db: AsyncSession, limit=100, offset=0):
    result = await db.execute(
        select(Measurement).order_by(Measurement.id).limit(limit).offset(offset)
    )
    return result.scalars().all()


async def get_by_id(db: AsyncSession, measurement_id):
    result = await db.execute(
        select(Measurement).where(Measurement.id == measurement_id)
    )
    return result.scalar_one_or_none()

async def create(db: AsyncSession, measurement_in: MeasurementCreate):
    measurement = Measurement(**measurement_in.model_dump())
    measurement.geom = from_shape(Point(measurement.lon, measurement.lat), srid=4326) # type: ignore
    db.add(measurement)
    await db.commit()
    await db.refresh(measurement)
    return measurement

async def update(db: AsyncSession, measurement_id, measurement_in: MeasurementUpdate):
    existing = await get_by_id(db, measurement_id)
    if not existing:
        return None
    for field, value in measurement_in.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    await db.commit()
    await db.refresh(existing)
    return existing

async def delete(db: AsyncSession, measurement_id: int) -> bool:
    measurement = await get_by_id(db, measurement_id)
    if not measurement:
        return False
    await db.delete(measurement)
    await db.commit()
    return True