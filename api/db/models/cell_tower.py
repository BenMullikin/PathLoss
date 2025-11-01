from sqlalchemy import Column, Integer, BigInteger, SmallInteger, String, Float, Index, DateTime, func, CheckConstraint, UniqueConstraint
from geoalchemy2 import Geometry
from api.db.base import Base


class CellTower(Base):
    __tablename__ = "cell_towers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    radio = Column(String(16), nullable=False)
    mcc = Column(SmallInteger, nullable=False)
    mnc = Column(SmallInteger, nullable=False)
    area_code = Column(Integer, nullable=True)
    cid = Column(BigInteger, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    geom = Column(Geometry("POINT", srid=4326), nullable=False)
    elevation_m = Column(Float, nullable=True)
    source = Column(String(32), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),  onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("radio", "mcc", "mnc", "area_code", "cid", name="uq_cell_tower_identity"),
        Index("ix_cell_towers_identity", "radio", "mcc", "mnc", "area_code", "cid"),
        Index("ix_cell_towers_geom", "geom", postgresql_using="gist"),
        CheckConstraint("radio IN ('GSM','UMTS','LTE','NR')", name="ck_cell_towers_radio"),
        CheckConstraint("lat BETWEEN -90 AND 90", name="ck_cell_towers_lat"),
        CheckConstraint("lon BETWEEN -180 AND 180", name="ck_cell_towers_lon"),
        CheckConstraint("mcc BETWEEN 1 AND 999", name="ck_cell_towers_mcc"),
        CheckConstraint("mnc BETWEEN 0 AND 999", name="ck_cell_towers_mnc"),
    )

    def __repr__(self):
        return f"<CellTower {self.radio} {self.mcc}-{self.mnc} LAC/TAC={self.area_code} CID={self.cid} @ ({self.lat:.5f},{self.lon:.5f})>"
