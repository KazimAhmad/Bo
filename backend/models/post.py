from config.config import db
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
import datetime
import enum

class MediaType(enum.Enum):
    image = "Image"
    video = "Video"

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Interger, primary_key = True)
    media_url = db.Column(db.String, unique = True, nullable = False)
    description = db.Column(db.String(180), nullable = True)
    date = db.Column(db.DateTime, nullable = False, default= datetime.datetime.now(datetime.timezone.utc))
    media_type = db.Column(db.Enum(MediaType))

    episode_id = Column(Integer, ForeignKey("episode.id"))
    episode = relationship("Episode", back_populates="posts")

    def to_json(self):
        return {
            "id": self.id,
            "title": self.media_url,
            "description": self.description,
            "episode": self.episode.to_json()
        }
