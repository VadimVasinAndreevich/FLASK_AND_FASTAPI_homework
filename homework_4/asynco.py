import asyncio
import aiohttp
import time
import os
import argparse
from help import return_filename

"""
'https://w.forfun.com/fetch/96/9683f749b5bf3bcce70efbbcf078cb3a.jpeg' 
'https://w.forfun.com/fetch/86/8624a634267d67c9ec72699dd8b161f9.jpeg' 
'https://w.forfun.com/fetch/ad/adb100f66e77bf9fda6da7660e2e7050.jpeg' 
'https://kristallosofija.com/wp-content/uploads/17ki-full.jpg' 
'https://www.ccdc.cam.ac.uk/media/Python.png'
"""


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            direct = 'asynco'
            content = await response.read()
            filename = return_filename(url)
            if direct not in os.listdir():
                os.mkdir(direct)
            with open(f'{direct}/{filename}', "wb") as f:
                f.write(content)
            print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


async def main():
    tasks = []
    parser = argparse.ArgumentParser(description='My first argument parser')
    parser.add_argument('param', metavar='a b c', nargs='*', help='enter a b c separated by a space')
    urls = parser.parse_args()
    for url in urls.param:
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


start_time = time.time()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
