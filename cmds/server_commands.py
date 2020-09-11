#!/usr/bin/env python3

import discord
from discord.ext import commands


class ServerCommands(commands.Cog):
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def perms(self, ctx):
        await ctx.send("You can manage this guild!")
