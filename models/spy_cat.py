from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class SpyCat(Base):
    __tablename__ = 'spy_cats'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    years_of_experience = Column(Integer)
    breed = Column(String)
    salary = Column(Integer)
    missions = relationship("Mission", back_populates="spy_cat")
