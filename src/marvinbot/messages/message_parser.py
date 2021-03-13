from typing import Dict, Text, Callable
import random
import discord


async def flip_a_coin(message: discord.Message) -> None:
    rand_int = random.randint(0, 1)
    if rand_int == 0:
        result = "Heads"
    else:
        result = "Tails"
    await message.channel.send(f"{message.author.mention}, your result is {result}")


async def roll_dice(message: discord.Message) -> None:
    message_content: str = message.content.lower()
    dice = message_content.split('roll')[-1].strip()
    if len(dice) == 0:
        await message.channel.send(f"{message.author.mention}, you rolled a {random.randint(1, 20)}")
        return

    iterator, die_size = dice.split('d')

    if int(iterator) > 10:
        await message.channel.send(f"{message.author.mention}, good try.")
        return
    elif int(die_size) > 100:
        await message.channel.send(f"{message.author.mention}, good try.")
        return

    if iterator is None:
        await message.channel.send(f"{message.author.mention}, you rolled {random.randint(1, int(die_size))}.")
        return
    else:
        total = [random.randint(1, int(die_size)) for _ in range(int(iterator))]
        str_total = [str(t) for t in total]
        await message.channel.send(f"{message.author.mention}, you rolled {sum(total)} ({', '.join(str_total)}).")
    return









