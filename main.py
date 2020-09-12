#!/usr/bin/env python3

# TermBot: Discord bot to make glossaries of terms
# Copyright (C) 2020 Starshine113 (Starshine System)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from pathlib import Path
import discord
from discord.ext import commands
import tomlkit
from cmds import static_commands, server_commands, admin_commands, term_commands
from database import database as botdb

config_file = Path("config.toml")

if not config_file.is_file():
    raise FileNotFoundError(
        "Config file not found! Try using the sample config in config.sample.toml"
    )

bot_config = tomlkit.parse(config_file.read_text())

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

description = bot_config["bot"]["description"]

bot = commands.AutoShardedBot(
    command_prefix=bot_config["bot"]["prefixes"],
    description=description,
    case_insensitive=True,
)

conn = botdb.DatabaseConn(bot_config["db"]["database_url"])


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

    activity = "{}help | in {} servers".format(
        bot_config["bot"]["prefixes"][0], len(bot.guilds)
    )

    await bot.change_presence(activity=discord.Game(name=activity))


@bot.event
async def on_guild_join(guild):
    activity = "{}help | in {} servers".format(
        bot_config["bot"]["prefixes"][0], len(bot.guilds)
    )

    await bot.change_presence(activity=discord.Game(name=activity))


@bot.event
async def on_guild_remove(guild):
    activity = "{}help | in {} servers".format(
        bot_config["bot"]["prefixes"][0], len(bot.guilds)
    )

    await bot.change_presence(activity=discord.Game(name=activity))


bot.add_cog(static_commands.StaticCommands(bot, bot_config, conn))
bot.add_cog(server_commands.ServerCommands(bot, conn))
bot.add_cog(admin_commands.AdminCommands(bot, conn))
bot.add_cog(term_commands.TermCommands(bot, conn))

bot.run(bot_config["bot"]["token"])
