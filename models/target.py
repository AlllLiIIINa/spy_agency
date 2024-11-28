from sqlalchemy import Integer, String, Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Target(Base):
    __tablename__ = 'targets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)
    notes = Column(String)
    complete = Column(Boolean, default=False)
    mission_id = Column(Integer, ForeignKey('missions.id'))
    mission = relationship("Mission", back_populates="targets")
