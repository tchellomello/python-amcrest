import asyncio
import logging
import time


from gpscrest.helpers import assert_http_response

import aiohttp

_LOGGER = logging.getLogger(__name__)


class GPSCrestFetcher:

    def __init__(self, proxy=None):
        self.session =  aiohttp.ClientSession = self._make_aiohttp_session()
        self.proxy = proxy

    def _make_aiohttp_session(self) -> aiohttp.ClientSession:
        """Create aiohttp.ClientSession for scope."""
        return aiohttp.ClientSession()

    async def post(self, url, data=None, headers=None):
        start = time.perf_counter()

        async with self.session.post(url,
                                    data=data,
                                    headers=headers,
                                    proxy=self.proxy,
                                    verify_ssl=False) as response:

            resp = assert_http_response(await response.json())
            elapsed = time.perf_counter() - start
            print(f'{url} run took {elapsed:0.2f} seconds')
            return resp.get('data')