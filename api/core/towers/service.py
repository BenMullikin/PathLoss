from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, text
from api.db.models.cell_tower import CellTower


async def get_towers_nearby(db: AsyncSession, lat: float, lon: float, radius_km: float):
    radius_m = radius_km * 1000
    point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
    stmt = (
        select(CellTower)
        .where(func.ST_DWithin(CellTower.geom, point, radius_m))
        .order_by(func.ST_Distance(CellTower.geom, point))
    )
    res = await db.execute(stmt)
    return res.scalars().all()
