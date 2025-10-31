from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    SmallInteger,
    String,
    Float,
    Index,
    DateTime,
    func,
    CheckConstraint,
)
from geoalchemy2 import Geometry
from api.db.base import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    rsrp_dBm = Column(Float, nullable=False)
    mcc = Column(SmallInteger, nullable=False)
    mnc = Column(SmallInteger, nullable=False)
    lac = Column(Integer, nullable=True)
    cid = Column(BigInteger, nullable=False)
    source = Column(String(64), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    geom = Column(Geometry("POINT", srid=4326))

    __table_args__ = (
        Index("ix_measurements_identity", "mcc", "mnc", "lac", "cid", "lat", "lon"),
        CheckConstraint("lat BETWEEN -90 AND 90", name="ck_measurements_lat"),
        CheckConstraint("lon BETWEEN -180 AND 180", name="ck_measurements_lon")
    )
    
    def __repr__(self):
        return f"<Measurement {self.source} {self.mcc}-{self.mnc} LAC/TAC={self.lac} CID={self.cid} @ ({self.lat:.5f},{self.lon:.5f})>"