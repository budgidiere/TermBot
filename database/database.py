#!/usr/bin/env python3

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
