from dataclasses import dataclass
from typing import Text, List
from datetime import datetime, timedelta

DEFAULT_REMINDER_DELTA = timedelta(hours=12)
DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


@dataclass
class Turns:
    guild_id: Text
    channel_id: Text
    current_order: List[Text]
    original_order: List[Text]
    created_time: datetime
    check_time: datetime

    def __post_init__(self):
        self.id = f"{self.guild_id}:{self.channel_id}"

    def next_turn(self):
        self.check_time += DEFAULT_REMINDER_DELTA
        # rotate magic
        self.current_order.append(self.current_order.pop(0))

    @property
    def current(self) -> Text:
        return self.current_order[0]

