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

import psycopg2


class DatabaseConn:
    def __init__(self, database_url):
        self.conn = psycopg2.connect(database_url)
        self.cur = self.conn.cursor()

    async def add_term(self, term, description, source, synonyms, category):
        if synonyms:
            self.cur.execute(
                "INSERT INTO terms (term, description, source, synonyms, categories) VALUES (%s, %s, %s, %s, %s)",
                (term, description, source, synonyms, [category]),
            )
        else:
            self.cur.execute(
                "INSERT INTO terms (term, description, source, categories) VALUES (%s, %s, %s, %s)",
                (term, description, source, [category]),
            )
        self.conn.commit()

    async def set_categories(self, term, categories):
        self.cur.execute(
            "UPDATE terms SET categories = %s WHERE term = %s OR %s = ANY (synonyms)",
            (categories, term, term),
        )
        self.conn.commit()

    async def del_term(self, term_id):
        self.cur.execute("DELETE FROM terms WHERE id = %s", (int(term_id),))

    async def get_term(self, term):
        if isinstance(term, int):
            self.cur.execute("SELECT * FROM terms WHERE id = %s", (int(term),))
        elif isinstance(term, str):
            self.cur.execute(
                "SELECT * FROM terms WHERE term = %s OR %s = ANY (synonyms)",
                (term, term),
            )
        return self.cur.fetchone()

    async def add_explanation(self, topic, explanation):
        self.cur.execute(
            "INSERT INTO explanations (topic, explanation) VALUES (%s, %s)",
            (topic, explanation),
        )
        self.conn.commit()

    async def get_explanation(self, topic):
        self.cur.execute("SELECT * FROM explanations WHERE topic = %s", (topic,))
        return self.cur.fetchone()

    async def get_topics(self):
        self.cur.execute("SELECT * FROM explanations")
        return self.cur.fetchall()

    async def add_to_blacklist(self, channel, guild_id):
        self.cur.execute(
            "INSERT INTO blacklisted_channels (channel_id, server_id) VALUES (%s, %s)",
            (channel, guild_id),
        )
        self.conn.commit()

    async def remove_from_blacklist(self, channel, guild_id):
        self.cur.execute(
            "DELETE FROM blacklisted_channels WHERE channel_id = %s AND server_id = %s",
            (int(channel), int(guild_id)),
        )
        self.conn.commit()

    async def get_blacklist(self, guild_id):
        self.cur.execute(
            "SELECT channel_id FROM blacklisted_channels WHERE server_id = %s",
            (int(guild_id),),
        )
        channels = self.cur.fetchall()
        channel_list = []
        for channel in channels:
            channel_list.append(channel[0])

        return channel_list

    async def channel_not_blacklisted(self, ctx):
        if ctx.message.guild.id:
            blacklist = await self.get_blacklist(ctx.message.guild.id)
            return ctx.message.channel.id not in blacklist

    async def add_bot_admin(self, user_id, user):
        self.cur.execute(
            "INSERT INTO admins (user_id, added_by_id) VALUES (%s, %s)", (user_id, user)
        )
        self.conn.commit()
