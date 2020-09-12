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

import aiopg
from database.cache import *


async def init_dbconn(database_url):
    dbconn = DatabaseConn(database_url)
    await dbconn._init()
    return dbconn


class DatabaseConn:
    def __init__(self, database_url):
        self.database_url = database_url

    async def _init(self):
        self.pool = await aiopg.create_pool(self.database_url)

    async def add_term(self, term, description, source, synonyms, category):
        asyncio.run(purge_data(term))
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                if synonyms:
                    await cur.execute(
                        "INSERT INTO terms (term, description, source, synonyms, categories) VALUES (%s, %s, %s, %s, %s)",
                        (term, description, source, synonyms, [category]),
                    )
                else:
                    await cur.execute(
                        "INSERT INTO terms (term, description, source, categories) VALUES (%s, %s, %s, %s)",
                        (term, description, source, [category]),
                    )

    async def set_categories(self, term, categories):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "UPDATE terms SET categories = %s WHERE term = %s OR %s = ANY (synonyms)",
                    (categories, term, term),
                )

    async def del_term(self, term_id):
        asyncio.run(purge_data(DatabaseConn.get_term(int(term_id))))
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM terms WHERE id = %s", (int(term_id),))

    async def get_term(self, term):
        data = asyncio.run(retrive_data_rolling((term, 86400)))
        if data == False:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    if isinstance(term, int):
                        await cur.execute("SELECT * FROM terms WHERE id = %s", (int(term),))
                    elif isinstance(term, str):
                        await cur.execute(
                            "SELECT * FROM terms WHERE term = %s OR %s = ANY (synonyms)",
                            (term, term),
                        )
                        return await asyncio.run(pass_and_store(term, cur.fetchone(), 86400))
        return data

    async def add_explanation(self, topic, explanation):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO explanations (topic, explanation) VALUES (%s, %s)",
                    (topic, explanation),
                )

    async def get_explanation(self, topic):
        #data = asyncio.run(retrive_data_rolling((topic, 86400)))
        #if data == False:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM explanations WHERE topic = %s", (topic,)
                )
                return await cur.fetchone()
        #return data

    async def get_topics(self):
        data = asyncio.run(retrive_data_rolling(("topics", 86400)))
        if data == False:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM explanations")
                    return await cur.fetchall()
        return data

    async def add_to_blacklist(self, channel, guild_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO blacklisted_channels (channel_id, server_id) VALUES (%s, %s)",
                    (channel, guild_id),
                )

    async def remove_from_blacklist(self, channel, guild_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "DELETE FROM blacklisted_channels WHERE channel_id = %s AND server_id = %s",
                    (int(channel), int(guild_id)),
                )

    async def get_blacklist(self, guild_id):
        data = asyncio.run(retrive_data_rolling(("blacklisted_channels", 86400)))
        if data == False:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT channel_id FROM blacklisted_channels WHERE server_id = %s",
                        (int(guild_id),),
                    )
                    channels = await cur.fetchall()
                    channel_list = []
                    for channel in channels:
                        channel_list.append(channel[0])

                    return channel_list
        return data

    async def channel_not_blacklisted(self, ctx):
        if ctx.message.guild:
            if ctx.message.guild.id:
                blacklist = await self.get_blacklist(ctx.message.guild.id)
                return ctx.message.channel.id not in blacklist
        else:
            return True

    async def add_bot_admin(self, user_id, user):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO admins (user_id, added_by_id) VALUES (%s, %s)",
                    (user_id, user),
                )
