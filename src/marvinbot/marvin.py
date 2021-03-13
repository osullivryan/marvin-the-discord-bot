import os
from collections import defaultdict
from datetime import timedelta
from typing import Any, Text, List, Dict

import discord
from marvinbot.helpers.helpers import make_ordinal
from marvinbot.marvin_types import Turns
from marvinbot.messages.parsers import PARSERS

token = os.getenv("DISCORD_TOKEN")


def _pre_parse(command: str) -> str:
    # TODO: This should be an enum
    command = 'roll' if 'roll' in command else command
    command = 'turns' if 'turns' in command else command
    command = 'turn end' if 'turn end' in command else command
    command = 'turn end' if 'take turn' in command else command
    return command


class Marvin(discord.Client):
    def __init__(self):
        super(Marvin, self).__init__()
        self.turns: Dict[Text, Turns] = dict()

    async def on_ready(self):
        print(
            f"{self.user} is connected to {len(self.guilds)} guilds"
        )

    async def on_error(self, event: Any, *args: Any, **kwargs: Any) -> None:
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                f.write(f'Unhandled event: {event}\n')

    async def on_message(self, message: discord.Message) -> None:
        author = message.author
        # Don't send the message if it's us
        if author == self.user:
            return
        else:
            message_content: str = message.content.lower()
            if not message_content.startswith("!Marvin") and not message_content.startswith("!marvin"):
                return
            message_command = message_content.removeprefix("!Marvin").removeprefix("!marvin").lstrip()
            message_command = _pre_parse(message_command)

            if 'turn end' in message_command:
                await self._take_turn(message)
                return

            if 'turns' in message_command:
                await self._start_turns(message)
                return
            if message_command not in PARSERS:
                await message.channel.send(f"{author.mention}, I don't support your request. Go away.")
                return

            await PARSERS[message_command](message)

    async def _start_turns(self, message: discord.Message) -> None:
        message_content: str = message.content.lower()
        users = message_content.split('turns')[-1].split(',')
        if len(users) == 0:
            await message.channel.send(f"Seems lonely")
            return
        user_lines = ''.join([f'\n{make_ordinal(i + 1)}:{u}' for i, u in enumerate(users)])
        await message.channel.send(f"Okay. The turn order is... {user_lines}")

        # The user string comes to use messy when in a message
        users = [u.strip().replace('!', '') for u in users]
        new_turns = Turns(
            guild_id=message.guild.id,
            channel_id=message.channel.id,
            current_order=users,
            original_order=users,
            created_time=message.created_at,
            check_time=message.created_at

        )
        self.turns[new_turns.id] = new_turns
        await self._add_turns(message, new_turns)

    async def _ping_user_about_their_turn(self, channel: discord.TextChannel, user_id: Text):
        await channel.send(f"{user_id} it's your turn. Would you hurry up?")

    async def _add_turns(self, message: discord.Message, new_turns: Turns) -> None:
        await self._ping_user_about_their_turn(message.channel, new_turns.current)
        print('new turn is happening')

    async def _take_turn(self, message: discord.Message) -> None:
        author = message.author.mention
        guild_id = message.guild.id
        channel_id = message.channel.id

        potential_turn_id = f"{guild_id}:{channel_id}"
        turns = self.turns.get(potential_turn_id)
        if turns is None:
            await message.channel.send(f"You don't have any turns set up yet...")
            return

        if turns.current == author:
            turns.next_turn()
            await self._ping_user_about_their_turn(message.channel, turns.current)






marvin_bot = Marvin()
marvin_bot.run(token)
