import asyncio
from pathlib import Path

from src.use_httpx import get_asins_by_httpx
from src.use_zendriver import get_asins_by_zendriver

async def main():
    asin: str = 'B0BLYSGFRW'
    dst_folder: Path = Path(__file__).parent

    # 并发运行
    task2 = asyncio.create_task(get_asins_by_zendriver(asin, dst_folder))
    task1 = asyncio.create_task(get_asins_by_httpx(asin, dst_folder))

    # 主线程等待所有 task 执行完毕
    await asyncio.gather(task1, task2)

if __name__ == '__main__':
    asyncio.run(main())
