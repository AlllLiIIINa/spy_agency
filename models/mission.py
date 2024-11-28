from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Mission(Base):
    __tablename__ = 'missions'

    id = Column(Integer, primary_key=True, index=True)
    spy_cat_id = Column(Integer, ForeignKey('spy_cats.id'))
    spy_cat = relationship("SpyCat", back_populates="missions")
    targets = relationship("Target", back_populates="mission", cascade="all, delete-orphan")
    complete = Column(Boolean, default=False)
