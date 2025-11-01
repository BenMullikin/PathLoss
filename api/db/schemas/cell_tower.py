from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class CellTowerBase(BaseModel):
    radio: str
    mcc: int = Field(ge=0, le=999)
    mnc: int = Field(ge=0, le=999)
    area_code: Optional[int] = Field(default=None, ge=0)
    cid: int = Field(ge=0)
    lat: float
    lon: float
    elevation_m: Optional[float]
    source: Optional[str]

    @field_validator("radio")
    @classmethod
    def _radio_type(cls, v):
        radios = ["GSM", "UMTS", "LTE", "NR"]
        if v not in radios:
            raise ValueError("Invalid Radio")
        return v
    
    @field_validator("mcc")
    @classmethod
    def _mcc_range(cls, v):
        if not (1 <= v <= 999):
            raise ValueError("Invalid MCC")
        return v
    
    @field_validator("mnc")
    @classmethod
    def _mnc_range(cls, v):
        if not (0 <= v <= 999):
            raise ValueError("Invalid MNC")
        return v

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
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CellTowerUpdate(CellTowerBase):
    radio: Optional[str] = None
    mcc: Optional[int] = Field(ge=0, le=999)
    mnc: Optional[int] = Field(ge=0, le=999)
    area_code: Optional[int] = Field(default=None, ge=0)
    cid: Optional[int] = Field(ge=0)
    lat: Optional[float] = None
    lon: Optional[float] = None
    elevation_m: Optional[float] = None
    source: Optional[str] = None