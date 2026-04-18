from config.config import db
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

class Season(db.Model):
    __tablename__ = "season"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    episodes = relationship("Episode", back_populates="season", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Season {self.id}: {self.name}>'
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
