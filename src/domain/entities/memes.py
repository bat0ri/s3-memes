from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Meme:
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kwonly=True
        )

    title: str
    content_type: str
    content_length: int

    def __dict__(self):
        return {
            "oid": self.oid,
            "title": self.title,
            "content_type": self.content_type,
            "content_length": self.content_length
        }