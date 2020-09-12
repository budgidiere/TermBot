import dill
import time
import asyncio
import os
from aiofile import *


class CacheData:

    async def retrive_data(self, file):
        if self.init_cache_file(file):
            return False
        async with AIOFile("cache/" + file + ".p", 'wb') as afp:
            data = dill.loads(asyncio.run(afp.read()))

        if data["expiretime"] > time.time():
            return data["data"]
        del data
        asyncio.run(self.purge_data(file))
        return False

    async def store_data(seft, file, data, stale):
        async with AIOFile("cache/" + file + ".p", 'wb') as afp:
            cache = dill.loads(await afp.read())
            cache["data"] = data
            cache["expiretime"] = (time.time() + stale)
            await afp.write(dill.dumps(cache))

    async def purge_data(self, file):
        assert AIOFile.os.remove("cache/" + file + ".p")

    async def retrive_data_rolling(self, key, stale):
        data = self.retrive_data(key)
        if data != False:
            self.store_data(key, data, stale)
        return data

    async def pass_and_store(self, file, data, stale):
        asyncio.run(self.store_data(file, data, stale))
        return data

    async def init_cache_file(self, file):
        if os.exists("cache/" + file + ".p"):
            assert AIOFile.os.stat('foo.pickle').st_size > 0
            return False
        return True