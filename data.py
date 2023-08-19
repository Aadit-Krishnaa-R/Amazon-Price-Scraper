import sqlite3
import pandas as pd

conn = sqlite3.connect('amztracker.db')

data = pd.read_sql_query('''SELECT * FROM tracked_prices ''',conn)

print(data)
# import asyncio
# import aiohttp
# async def fetch_url(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.text()

# async def main():
#     search = "laptop"
#     url = f"https://www.amazon.in/s?k={search}"
#     html_content = await fetch_url(url)
#     print(html_content)

# asyncio.run(main())