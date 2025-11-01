from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.models.cell_tower import CellTower
from api.db.schemas.cell_tower import CellTowerCreate, CellTowerUpdate


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
    tower.geom = func.ST_SetSRID(func.ST_MakePoint(tower.lon, tower.lat), 4326) # type: ignore
    db.add(tower)
    await db.commit()
    await db.refresh(tower)
    return tower


async def update(db: AsyncSession, tower_id, tower_in: CellTowerUpdate):
    existing = await get_by_id(db, tower_id)
    if not existing:
        return None
    changed = tower_in.model_dump(exclude_unset=True)
    for field, value in changed.items():
        setattr(existing, field, value)
    if {"lat", "lon"} & changed.keys():
        existing.geom = func.ST_SetSRID(func.ST_MakePoint(existing.lon, existing.lat), 4326) # type: ignore
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
        CellTower.area_code == tower_in.area_code,
        CellTower.cid == tower_in.cid,
    )
    result = await db.execute(stmt)
    tower = result.scalar_one_or_none()

    if tower:
        # update lat/lon if changed
        tower.lat = tower_in.lat # type: ignore
        tower.lon = tower_in.lon # type: ignore
        tower.geom = func.ST_SetSRID( # type: ignore
            func.ST_MakePoint(tower_in.lon, tower_in.lat), 4326
        )
    else:
        tower = CellTower(
            **tower_in.model_dump(),
            geom=func.ST_SetSRID(func.ST_MakePoint(tower_in.lon, tower_in.lat), 4326),
        )
        db.add(tower)
    await db.commit()
    await db.refresh(tower)
    return tower
