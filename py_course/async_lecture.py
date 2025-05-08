import asyncio
import time


def slow_function():
    print('slow_function started')
    time.sleep(5)
    print('slow_function ended')
    return 0

async def sync_to_async_executor():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, slow_function)


async def main():
    result = await asyncio.gather(sync_to_async_executor(), sync_to_async_executor(), sync_to_async_executor())

    print(result)


if __name__ == '__main__':
    asyncio.run(main())
