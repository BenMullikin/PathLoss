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
    ForeignKey
)
from geoalchemy2 import Geometry
from api.db.base import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(BigInteger, primary_key=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    geom = Column(Geometry("POINT", srid=4326), nullable=False)
    elevation_m = Column(Float, nullable=True)
    source = Column(String(64), nullable=False)
    radio = Column(String(16), nullable=False)
    mcc = Column(SmallInteger, nullable=False)
    mnc = Column(SmallInteger, nullable=False)
    area_code = Column(Integer, nullable=True)
    tower_id = Column(BigInteger, ForeignKey("cell_towers.id", ondelete="SET NULL"), nullable=True)
    cid = Column(BigInteger, nullable=False)
    rsrp = Column(Float, nullable=True)
    rssi = Column(Float, nullable=True)
    rsrq = Column(Float, nullable=True)
    sinr = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),  onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_measurements_identity", "mcc", "mnc", "area_code", "cid"),
        Index("ix_measurements_geom", "geom", postgresql_using="gist"),
        CheckConstraint("radio IN ('GSM','UMTS','LTE','NR')", name="ck_measurements_radio"),
        CheckConstraint("lat BETWEEN -90 AND 90", name="ck_measurements_lat"),
        CheckConstraint("lon BETWEEN -180 AND 180", name="ck_measurements_lon"),
        CheckConstraint("mcc BETWEEN 1 AND 999", name="ck_measurements_mcc"),
        CheckConstraint("mnc BETWEEN 0 AND 999", name="ck_measurements_mnc"),
        CheckConstraint("rsrp BETWEEN -150 AND -40", name="ck_measurements_rsrp"),
        CheckConstraint("rssi BETWEEN -120 AND 0", name="ck_measurements_rssi"),
        CheckConstraint("sinr BETWEEN -20 AND 40", name="ck_measurements_sinr"),
    )
    
    def __repr__(self):
        return f"<Measurement {self.source} {self.mcc}-{self.mnc} LAC/TAC={self.area_code} CID={self.cid} @ ({self.lat:.5f},{self.lon:.5f})>"