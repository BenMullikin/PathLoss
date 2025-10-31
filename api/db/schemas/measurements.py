from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class MeasurementBase(BaseModel):
    lat: float
    lon: float
    rsrp_dBm: float
    mcc: int = Field(ge=0, le=999)
    mnc: int = Field(ge=0, le=999) 
    lac: Optional[int] = Field(default=None, ge=0)
    cid: int = Field(ge=0)
    source: str

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

class MeasurementCreate(MeasurementBase):
    pass

class MeasurementRead(MeasurementBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class MeasurementUpdate(MeasurementBase):
    lat: Optional[float] = None
    lon: Optional[float] = None
    rsrp_dBm: Optional[float] = None
    mcc: Optional[int] = Field(ge=0, le=999)
    mnc: Optional[int] = Field(ge=0, le=999) 
    lac: Optional[int] = Field(default=None, ge=0)
    cid: Optional[int] = Field(ge=0)
    source: Optional[str] = None