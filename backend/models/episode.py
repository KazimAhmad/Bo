from config.config import db
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
import datetime

class Episode(db.Model):
    __tablename__ = "episode"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date = db.Column(db.DateTime, nullable = False, default= datetime.datetime.now(datetime.timezone.utc))
    rating = Column(Float, nullable = False)
    image_url = db.Column(db.String, unique = True, nullable = False)

    season_id = Column(Integer, ForeignKey("season.id"))
    season = relationship("Season", back_populates="episode")

    posts = relationship("Post", back_populates="episode", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "rating": self.rating,
            "image_url": self.image_url,
            "season": self.season.to_json()
        }
