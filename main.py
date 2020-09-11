#!/usr/bin/env python3

import logging
from pathlib import Path
import discord
from discord.ext import commands
import tomlkit

config_file = Path("config.toml")

if not config_file.is_file():
    raise FileNotFoundError(
        "Config file not found! Try using the sample config in config.sample.toml"
    )

bot_config = tomlkit.parse(config_file.read_text())

activity = bot_config["bot"]["prefixes"][0] + "help"

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

description = bot_config["bot"]["description"]

bot = commands.AutoShardedBot(
    command_prefix=bot_config["bot"]["prefixes"], description=description
)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

    await bot.change_presence(activity=discord.Game(name=activity))


bot.run(bot_config["bot"]["token"])
