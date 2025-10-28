from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.models.cell_tower import CellTower
from api.db.schemas.cell_tower import CellTowerCreate, CellTowerUpdate
from typing import List, Optional


async def get_all(db: AsyncSession, limit=100, offset=0):
    result = await db.execute(
        select(CellTower).order_by(CellTower.id).limit(limit).offset(offset)
    )
    return result.scalars().all()


async def get_by_id(db: AsyncSession, tower_id):
    result = await db.execute(select(CellTower).where(CellTower.id == tower_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, tower_in: CellTowerCreate):
    tower = CellTower(**tower_in.model_dump())
    db.add(tower)
    await db.commit()
    await db.refresh(tower)
    return tower


async def update(db: AsyncSession, tower_id, tower_in: CellTowerUpdate):
    existing = await get_by_id(db, tower_id)
    if not existing:
        return None
    for field, value in tower_in.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete(db: AsyncSession, tower_id: int) -> bool:
    tower = await get_by_id(db, tower_id)
    if not tower:
        return False
    await db.delete(tower)
    await db.commit()
    return True


async def create_or_update(db: AsyncSession, tower_in: CellTowerCreate):
    stmt = select(CellTower).where(
        CellTower.radio == tower_in.radio,
        CellTower.mcc == tower_in.mcc,
        CellTower.mnc == tower_in.mnc,
        CellTower.lac == tower_in.lac,
        CellTower.cid == tower_in.cid,
    )
    result = await db.execute(stmt)
    tower = result.scalar_one_or_none()

    if tower:
        # update lat/lon if changed
        tower.lat = tower_in.lat
        tower.lon = tower_in.lon
        tower.geom = func.ST_SetSRID(
            func.ST_MakePoint(tower_in.lon, tower_in.lat), 4326
        )
    else:
        tower = CellTower(
            **tower_in.model_dump(),
            geom=func.ST_SetSRID(func.ST_MakePoint(tower_in.lon, tower_in.lat), 4326),
        )
        db.add(tower)
    return tower
