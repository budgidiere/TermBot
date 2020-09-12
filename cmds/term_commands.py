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

import datetime
import discord
from discord.ext import commands


class TermCommands(commands.Cog):
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn
        self.blacklist = conn.channel_not_blacklisted

    @commands.command(aliases=["e", "ex"])
    async def explain(self, ctx, *args):
        await ctx.trigger_typing()
        if args:
            args = args[0].lower()
            explanation = await self.conn.get_explanation(args)
            if explanation:
                await ctx.send(explanation[1])
            else:
                await self.listtopics(ctx)
        else:
            await self.listtopics(ctx)

    @commands.command(aliases=["list"])
    async def listtopics(self, ctx):
        await ctx.trigger_typing()
        topics = await self.conn.get_topics()
        message = "Available topics:\n"
        for topic in topics:
            message += "• `" + topic[0] + "`\n"
        await ctx.send(message)

    @commands.command(aliases=["d"])
    async def define(self, ctx, *, args):
        if await self.blacklist(ctx):
            await ctx.trigger_typing()
            args = args.lower()
            term = await self.conn.get_term(args)
            if term:
                embed = self.definition_embed_builder(term)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Term not found!")

    def definition_embed_builder(self, term):
        embed = discord.Embed(
            title=term[1].title(),
            colour=discord.Colour(0x9013FE),
            description=term[2],
            timestamp=term[4],
        )
        embed.set_footer(text="ID: {}".format(term[0]))
        if term[5]:
            synonyms = ""
            for synonym in term[5]:
                synonyms += "• " + synonym + "\n"
            embed.add_field(name="Synonyms", value=synonyms, inline=False)
        embed.add_field(name="Source", value=term[3], inline=False)
        return embed
