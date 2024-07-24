from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer


Base = declarative_base()


class Meme(Base):
    __tablename__ = "memes"

    oid = Column(String, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    content_type = Column(String)
    content_size = Column(Integer)

    def to_dict(self):
        return {
            "oid": self.oid,
            "title": self.title,
            "content_type": self.content_type,
            "content_size": self.content_size
        }