from datetime import datetime
from resources import resource


class event:

    def __init__(
        self,
        type: str,
        beginning: datetime,
        end: datetime,
        needed_resources: dict[resource:int] = {},
        description=None,
    ):
        self.type = type
        self.beginning = beginning
        self.end = end
        self.needed_resources = needed_resources
        self.description = description

    def to_dict(self):
        return {
            "type": self.type,
            "beginning": self.beginning.isoformat(),
            "end": self.end.isoformat(),
            "needed_resources": self.needed_resources,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data):
        data["beginning"] = datetime.fromisoformat(data["beginning"])
        data["end"] = datetime.fromisoformat(data["end"])

        return cls(
            data["type"],
            data["beginning"],
            data["end"],
            data["needed_resources"],
            data["description"],
        )

    def __str__(self):
        start = self.beginning.replace(second=0, microsecond=0)
        end = self.end.replace(second=0, microsecond=0)
        return f"{self.type} fijada desde {start} hasta {end}"
