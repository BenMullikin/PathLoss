import asyncio
from api.db.session import async_session
from api.db.crud.cell_tower import create, get_all
from api.db.schemas.cell_tower import CellTowerCreate


async def main():
    async with async_session() as db:
        tower = CellTowerCreate(
            radio="LTE", mcc=310, mnc=260, lac=12345, cid=67890, lon=-82.5, lat=34.5
        )
        await create(db, tower)
        all_towers = await get_all(db)
        print(all_towers)


asyncio.run(main())
