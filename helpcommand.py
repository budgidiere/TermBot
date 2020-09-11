#!/usr/bin/env python3

import discord
from discord.ext import commands

bot.remove_command("help")


async def createHelpCommand():
    embed = discord.Embed(
        title="Help",
        colour=discord.Colour(0x4A90E2),
        description=bot_config["bot"]["description"],
    )

    prefixes = bot.user.name + " uses the following prefixes:\n"

    for index, prefix in enumerate(bot_config["bot"]["prefixes"]):
        if index != len(bot_config["bot"]["prefixes"]) - 1:
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
        value="`help`: Shows the command list and an invite to the support server.\n`invite`: Invite TermBot to your server.",
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
        value="These commands require the `Manage Server` permission to use.\n`perms`: Explain the permissions TermBot needs to function.\n`disable`: Disable all commands *except* `explain` in a given channel(s).\n`enable`: Enable all commands except `explain` in a given channel(s).\nTo disable ***all*** commands in a channel, deny the bot the `Send Messages` permission in that channel.",
        inline=False,
    )
    embed.add_field(
        name="Support server",
        value="Our support server is here: <link>",
        inline=False,
    )

    return embed


@bot.command()
async def help(ctx):
    await ctx.trigger_typing()
    embed = await createHelpCommand()
    await ctx.send(embed=embed)
