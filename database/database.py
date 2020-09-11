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

    async def add_term(self, term, description, source, synonyms):
        self.cur.execute(
            "INSERT INTO terms (term, description, source, synonyms) VALUES (%s, %s, %s, %s)",
            (term, description, source, synonyms),
        )
        self.conn.commit()

    async def del_term(self, term_id):
        self.cur.execute("DELETE FROM terms WHERE id = %s", (int(term_id)))

    async def get_term(self, term):
        self.cur.execute("SELECT * FROM terms WHERE term = %s", (term,))
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
