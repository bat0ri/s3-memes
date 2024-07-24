from dataclasses import dataclass, field
from uuid import uuid4

from domain.models.memes import Meme as MemeModel


@dataclass
class Meme:
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True
        )

    title: str
    content_type: str
    content_size: int

    def to_model(self):
        return MemeModel(
            oid=self.oid,
            title=self.title,
            content_type=self.content_type,
            content_size=self.content_size
        )

    def to_dict(self):
        return {
            "oid": self.oid,
            "title": self.title,
            "content_type": self.content_type,
            "content_size": self.content_size
        }
