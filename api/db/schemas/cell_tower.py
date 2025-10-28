from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class CellTowerBase(BaseModel):
    radio: str
    mcc: int = Field(ge=0, le=999)
    mnc: int = Field(ge=0, le=999)
    lac: Optional[int] = Field(default=None, ge=0)
    cid: int = Field(ge=0)
    lon: float
    lat: float

    @field_validator("lat")
    @classmethod
    def _lat_range(cls, v):
        if not (-90.0 <= v <= 90.0):
            raise ValueError("Invalid Latitude")
        return v

    @field_validator("lon")
    @classmethod
    def _lon_range(cls, v):
        if not (-180.0 <= v <= 180.0):
            raise ValueError("Invalid Longitude")
        return v


class CellTowerCreate(CellTowerBase):
    pass


class CellTowerRead(CellTowerBase):
    id: int
    seen_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CellTowerUpdate(CellTowerBase):
    radio: Optional[str] = None
    mcc: Optional[int] = Field(ge=0, le=999)
    mnc: Optional[int] = Field(ge=0, le=999)
    lac: Optional[int] = Field(default=None, ge=0)
    cid: Optional[int] = Field(ge=0)
    lon: Optional[float] = None
    lat: Optional[float] = None
