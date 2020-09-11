#!/usr/bin/env python3

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
    async def addterm(self, ctx, term, desc, source, *synonyms):
        term = term.lower()
        await self.conn.add_term(term, desc, source, list(synonyms))
        await ctx.send("✅ Term added.")

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
