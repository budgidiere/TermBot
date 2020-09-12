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


def is_bot_owner():
    async def predicate(ctx):
        return ctx.author.id in bot_config["bot"]["bot_owners"]

    return commands.check(predicate)


class AdminCommands(commands.Cog):
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn

    @commands.command()
    @is_bot_owner()
    async def addterm(self, ctx, term, category, desc, source, *synonyms):
        term = term.lower()
        category = category.lower()
        synonyms = [synonym.lower() for synonym in synonyms]
        await self.conn.add_term(term, desc, source, list(synonyms), category)
        await ctx.send("✅ Term added.")

    @commands.command()
    @is_bot_owner()
    async def setcategories(self, ctx, term, *categories):
        term = term.lower()
        categories = [category.lower() for category in categories]
        await self.conn.set_categories(term, categories)
        await ctx.send(
            "✅ Added {} to the categories {}.".format(term, ", ".join(categories))
        )

    @commands.command()
    @is_bot_owner()
    async def delterm(self, ctx, term_id):
        await self.conn.del_term(term_id)
        await ctx.send("✅ Term deleted.")

    @commands.command()
    @is_bot_owner()
    async def addtopic(self, ctx, topic, *, explanation):
        await self.conn.add_explanation(topic, explanation)
        await ctx.send("✅ Explanation added.")

    @commands.command()
    @is_bot_owner()
    async def makeadmin(self, ctx, user_id: discord.User):
        await self.conn.add_bot_admin(user_id.id, ctx.message.author.id)
        await ctx.send("✅ Gave admin perms to **{}**.".format(str(user_id)))
