import httpx
from typing import Optional

from api.db.models.cell_tower import CellTower
from api.db.schemas.cell_tower import CellTowerCreate
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.crud.cell_tower import create_or_update


class OpenCellIDClient:
    BASE_URL = "https://opencellid.org/cell/getInArea"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def fetch_bbox(
        self,
        lat_min: float,
        lon_min: float,
        lat_max: float,
        lon_max: float,
        mcc: Optional[int] = None,
        mnc: Optional[int] = None,
        radio: str = "LTE",
        limit: int = 1000,
        offset: int = 0,
        fmt: str = "json",
    ):
        params = {
            "key": self.api_key,
            "BBOX": f"{lat_min},{lon_min},{lat_max},{lon_max}",
            "radio": radio,
            "limit": limit,
            "offset": offset,
            "format": fmt,
        }
        if mcc:
            params["mcc"] = mcc
        if mnc:
            params["mnc"] = mnc

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(self.BASE_URL, params=params)
            resp.raise_for_status()
            return resp.json()

    async def sync_to_db(self, db: AsyncSession, data: dict):
        towers = []
        for item in data.get("cells", []):
            tower = CellTowerCreate(
                radio=item["radio"],
                mcc=item["mcc"],
                mnc=item["mnc"],
                lac=item.get("lac") or item.get("tac") or 0,
                cid=item.get("cellid") or item.get("cid") or 0,
                lat=item["lat"],
                lon=item["lon"],
            )
            towers.append(await create_or_update(db, tower))
        await db.commit()
        return towers
