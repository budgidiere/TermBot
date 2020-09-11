#!/usr/bin/env python3

from pathlib import Path
import sys
import psycopg2
import tomlkit

config_file = Path("config.toml")

if not config_file.is_file():
    raise FileNotFoundError(
        "Config file not found! Try using the sample config in config.sample.toml"
    )

config = tomlkit.parse(config_file.read_text())

conn = psycopg2.connect(config["db"]["database_url"])

cur = conn.cursor()

sql_file = open(sys.argv[-1], "r")
cur.execute(sql_file.read())
conn.commit()

conn.commit()
cur.close()
conn.close()
