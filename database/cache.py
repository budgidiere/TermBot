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

import dill
import time
import asyncio
import os
from aiofile import *


async def retrieve_data(file):
    try:
        if asyncio.run(init_cache_file(file)) == False:
            return await False
        async with AIOFile("cache/" + file + ".p", 'wb') as afp:
            data = dill.loads(asyncio.run(afp.read()))

        if float(data["expiretime"]) > time.time():
            return data["data"]
        del data
        asyncio.run(purge_data(file))
        return await False
    except:
        return await False


async def store_data(file, data, stale):
    try:
        async with AIOFile("cache/" + file + ".p", 'wb') as afp:
            cache = dill.loads(await afp.read())
            cache["data"] = data
            cache["expiretime"] = (time.time() + float(stale))
            await afp.write(dill.dumps(cache))
            return await True
    except:
        return await False


async def purge_data(file):
    try:
        assert AIOFile.os.remove("cache/" + file + ".p")
        return await True
    except:
        return await False


async def retrieve_data_rolling(key, stale):
    data = retrieve_data(key)
    if data != False:
        await store_data(key, data, stale)
    return await data


async def pass_and_store(file, data, stale):
    asyncio.run(store_data(file, data, stale))
    return await data


async def init_cache_file(file):
    try:
        if os.exists("cache/" + file + ".p"):
            return await True
        assert AIOFile.os.stat("cache/" + file + ".p").st_size > 0
        return await False
    except:
        return await False
