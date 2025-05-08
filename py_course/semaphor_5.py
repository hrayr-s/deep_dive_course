import asyncio

import aiohttp
import requests


async def handler(url, sem):
    results = None
    async with sem:
        print(f'Started handling {url}')
        # results = requests.get(url).text
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                results = await response.text()

        print(f'Finished handling {url}')

    return results


async def main():
    urls = [
        f'https://test.hrayr.am/timeout.php?t={_}' for _ in range(100)
    ]
    sem = asyncio.Semaphore(5)
    tasks = [asyncio.create_task(handler(url, sem)) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)

if __name__ == '__main__':
    asyncio.run(main())
