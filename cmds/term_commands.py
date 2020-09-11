#!/usr/bin/env python3

import discord
from discord.ext import commands
import datetime


class TermCommands(commands.Cog):
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn

    @commands.command(aliases=["e", "ex"])
    async def explain(self, ctx, *, args):
        await ctx.trigger_typing()
        args = args.lower()
        explanation = await self.conn.get_explanation(args)
        if explanation:
            await ctx.send(explanation[1])

    @commands.command(aliases=["d"])
    async def define(self, ctx, *, args):
        await ctx.trigger_typing()
        args = args.lower()
        term = await self.conn.get_term(args)
        if term:
            embed = self.definition_embed_builder(term)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Term not found! {}".format(type(args)))

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
