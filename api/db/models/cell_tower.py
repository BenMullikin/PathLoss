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


class CellTower(Base):
    __tablename__ = "cell_towers"

    id = Column(Integer, primary_key=True)
    radio = Column(String(16), nullable=False)
    mcc = Column(SmallInteger, nullable=False)
    mnc = Column(SmallInteger, nullable=False)
    lac = Column(Integer, nullable=True)
    cid = Column(BigInteger, nullable=False)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    seen_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    geom = Column(Geometry("POINT", srid=4326))

    __table_args__ = (
        Index("ix_cell_towers_identity", "radio", "mcc", "mnc", "lac", "cid"),
        # Index("ix_cell_towers_geom", "geom", postgresql_using="gist"),
        CheckConstraint("lat BETWEEN -90 AND 90", name="ck_cell_towers_lat"),
        CheckConstraint("lon BETWEEN -180 AND 180", name="ck_cell_towers_lon"),
    )

    def __repr__(self):
        return f"<CellTower {self.radio} {self.mcc}-{self.mnc} LAC/TAC={self.lac} CID={self.cid} @ ({self.lat:.5f},{self.lon:.5f})>"
