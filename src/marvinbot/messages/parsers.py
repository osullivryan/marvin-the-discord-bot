from typing import Dict, Callable
from discord import Message
from marvinbot.messages.message_parser import flip_a_coin, roll_dice

# TODO: Type this Callable fully.
PARSERS: Dict[str, Callable] = {
    "flip a coin": flip_a_coin,
    "roll": roll_dice,
}