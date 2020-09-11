#!/usr/bin/env python3

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
            colour=discord.Colour(0x4A90E2),
            description=self.bot_config["bot"]["description"],
        )

        prefixes = self.bot.user.name + " uses the following prefixes:\n"

        print(type(self.bot_config["bot"]["prefixes"]))

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
