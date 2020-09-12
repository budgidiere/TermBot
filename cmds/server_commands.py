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

import re
import discord
from discord.ext import commands


class ServerCommands(commands.Cog):
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn

    @commands.command()
    async def perms(self, ctx):
        await ctx.trigger_typing()
        embed = discord.Embed(
            title="Permissions",
            colour=discord.Colour(0x9013FE),
            description=f"{self.bot.user.name} requires the following permissions to function:\n- `View Channels`, `Read Message History`: see channels and messages to respond.\n- `Send Messages`: respond to commands.\n- `Embed Links`: create embeds for term definitions and the help commands.\n- `Add Reactions`",
        )
        embed.add_field(
            name="Denying Permissions",
            value="Without `Manage Messages`, the bot will still function, but reactions have to be removed manually when moving between pages of search results.\nBy denying the bot the `Send Messages` permission in a channel, it will not respond to any commands in said channel. (However, in most cases, it is better to use the `disable` command to disable all commands except `explain` in a channel)",
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx, *args):
        await ctx.trigger_typing()

        current_blacklist = await self.conn.get_blacklist(ctx.message.guild.id)
        channels = await self.get_channel_ids(args)
        message = ""

        for channel in channels:
            if not channel in current_blacklist:
                await self.conn.add_to_blacklist(channel, ctx.message.guild.id)
                message += (
                    "✅ Channel <#" + str(channel) + "> added to command blacklist.\n"
                )
            else:
                message += (
                    "⚠ Channel <#"
                    + str(channel)
                    + "> is already on the blacklist. Use `"
                    + ctx.prefix
                    + "enable` to remove it from the blacklist.\n"
                )

        await ctx.send(message)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx, *args):
        await ctx.trigger_typing()

        current_blacklist = await self.conn.get_blacklist(ctx.message.guild.id)
        channels = await self.get_channel_ids(args)
        message = ""

        for channel in channels:
            if channel in current_blacklist:
                await self.conn.remove_from_blacklist(channel, ctx.message.guild.id)
                message += (
                    "✅ Channel <#" + str(channel) + "> removed from the blacklist.\n"
                )
            else:
                message += (
                    "⚠ Channel <#"
                    + str(channel)
                    + "> is not blacklisted. Use `"
                    + ctx.prefix
                    + "disable` to add it to the blacklist.\n"
                )

        await ctx.send(message)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def blacklist(self, ctx):
        await ctx.trigger_typing()

        blacklist = await self.conn.get_blacklist(ctx.message.guild.id)
        blacklist_message = ""

        for channel in blacklist:
            blacklist_message += "<#" + str(channel) + ">\n"

        embed = discord.Embed(
            title="Command blacklist",
            colour=discord.Colour(0x9013FE),
            description=blacklist_message,
        )
        embed.set_footer(
            text="Use `{}enable` to remove channels from the blacklist.".format(
                ctx.prefix
            )
        )

        await ctx.send(embed=embed)

    async def get_channel_ids(self, args):
        channels = []
        for item in args:
            m = re.search(r"<#(?P<ID>\d{3,25})>", item)
            channel = m.group("ID")
            channels.append(int(channel))
        return channels
