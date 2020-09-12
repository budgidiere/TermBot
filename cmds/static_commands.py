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

import discord
from discord.ext import commands


class StaticCommands(commands.Cog):
    def __init__(self, bot, bot_config):
        self.bot = bot
        self.bot_config = bot_config
        self.bot.remove_command("help")

    async def createHelpCommand(self):
        embed = discord.Embed(
            title="Help",
            colour=discord.Colour(0x9013FE),
            description=self.bot_config["bot"]["description"],
        )

        prefixes = self.bot.user.name + " uses the following prefixes:\n"

        for index, prefix in enumerate(self.bot_config["bot"]["prefixes"]):
            if index != len(self.bot_config["bot"]["prefixes"]) - 1:
                prefixes += prefix + ", "
            else:
                prefixes += prefix

        embed.add_field(
            name="Prefix",
            value=prefixes,
            inline=False,
        )
        embed.add_field(
            name="Info",
            value=f"`help`: Shows the command list and an invite to the support server.\n`invite`: Invite {self.bot.user.name} to your server.",
            inline=False,
        )
        embed.add_field(
            name="Terms",
            value="`define`: Show the definition for a term. (Alias: `d`)\n`search`: Search for a term. (Alias: `s`)",
            inline=False,
        )
        embed.add_field(
            name="Explain",
            value="`explain`: Show a list of all explanations. (Aliases: `e`, `ex`)\n`explain <topic>`: Show a short explanation about a topic.",
            inline=False,
        )
        embed.add_field(
            name="Management commands",
            value=f"These commands require the `Manage Server` permission to use.\n`perms`: Explain the permissions {self.bot.user.name} needs to function.\n`disable`: Disable all commands *except* `explain` in a given channel(s).\n`enable`: Enable all commands except `explain` in a given channel(s).\nTo disable ***all*** commands in a channel, deny the bot the `Send Messages` permission in that channel.",
            inline=False,
        )
        embed.add_field(
            name="Source code",
            value="The bot is open source, licensed under the GNU Affero General Public License 3.0 or later. The source code is available here: https://github.com/Starshine113/TermBot",
            inline=False,
        )

        if self.bot_config["bot"]["support_server"]:
            embed.add_field(
                name="Support server",
                value="Our support server is here: {}".format(
                    self.bot_config["bot"]["support_server"]
                ),
                inline=False,
            )

        return embed

    @commands.command()
    async def help(self, ctx):
        await ctx.trigger_typing()
        embed = await self.createHelpCommand()
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.trigger_typing()
        await ctx.send(
            "Use this link to invite me to your server!\n<{}>".format(
                self.bot_config["bot"]["invite_link"]
            )
        )

    @commands.command(aliases=["hi"])
    async def hello(self, ctx):
        await ctx.trigger_typing()
        await ctx.send("Hello " + ctx.message.author.mention + "!")

    @commands.command()
    async def pronouns(self, ctx):
        await ctx.trigger_typing()
        await ctx.send(
            f"Hi, I'm {self.bot.user.name}! I'm non-binary, and my preferred pronouns are they/them."
        )
