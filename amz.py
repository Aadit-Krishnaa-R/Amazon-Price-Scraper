from requests_html import HTMLSession, AsyncHTMLSession
import threading
import csv
import datetime
import sqlite3
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import requests
from flask import Flask, url_for, redirect, render_template, request
import asyncio
import aiohttp
import json
import os
global search



# def load_auth():
#     FILE = "./auth.json"
#     with open(FILE, "r") as f:
#         return json.load(f)

# # place your bright data credentials in auth.json file with keys: "username", "password" and "host"
# cred = load_auth()
# auth = f'{cred["username"]}:{cred["password"]}'
# browser_url = f'wss://{auth}@{cred["host"]}'
# def amz_scraper(search):

#     loop = asyncio.new_event_loop()  # Create a new event loop
#     asyncio.set_event_loop(loop)  # Set the event loop for this thread
    
#     from playwright.sync_api import sync_playwright

#     url = "https://www.amazon.in/"
#     with sync_playwright() as p:
#         url = "https://www.amazon.in/"
#         browser = p.chromium.launch()
#         page = browser.new_page()
#         page.goto(url)
#         page.fill('input#twotabsearchtextbox', search)
#         page.click('input[type=submit]')
#         page.wait_for_selector('div.s-main-slot.s-result-list.s-search-results.sg-row')
#         html = page.inner_html('div.s-main-slot.s-result-list.s-search-results.sg-row')
#         soup = BeautifulSoup(html, 'lxml')
#         asins = []
#         for product in soup.find_all("div", {"data-asin": True}):
#             asin = product["data-asin"]
#             asins.append(asin)
        
#     while "" in asins:
#         asins.remove("")
        
#     asins_new = asins[:4]
#     print(asins_new)
    
#     conn = sqlite3.connect('amztracker.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS prices8(date DATE, asin TEXT, price FLOAT, title TEXT, dealer TEXT)''')
#     s = HTMLSession()
#     for asin in asins_new:
#         r = s.get(f'https://www.amazon.in/dp/{asin}')
#         r.html.render(sleep=5) 
#         price = r.html.find('span.a-price-whole')[0].text
#         title = r.html.find('#productTitle')[0].text.strip()
#         dealer = r.html.find('#merchant-info')[0].text.strip()
#         date = datetime.datetime.today()
#         c.execute('''INSERT INTO prices8 VALUES(?,?,?,?,?)''', (date, asin, price, title, dealer))
#         print(f'Added data for {asin}, {price}')
        
#     conn.commit()
#     print('Committed new entries to database')

#     c.close()
#     conn.close()
#     loop.close()


# app = Flask(__name__)

# @app.route("/",methods=("GET", "POST"), strict_slashes=False)
# def index():
#     if(request.method == "POST"):
#         search=request.form['search']
#         thread = threading.Thread(target=amz_scraper, args=(search,))
#         thread.start()
#         return redirect("/list", code=302)
#     return render_template("index.html")

app = Flask(__name__)

# async def amz_scraper(search):
#     try:
#         url = "https://www.amazon.in/"
#         async with async_playwright() as p:
#             browser = await p.chromium.launch()
#             page = await browser.new_page()
#             await page.goto(url)
#             await page.fill('input#twotabsearchtextbox', search)
#             await page.click('input[type=submit]')
#             await page.wait_for_selector('div.s-main-slot.s-result-list.s-search-results.sg-row')
#             html = await page.inner_html('div.s-main-slot.s-result-list.s-search-results.sg-row')
#             soup = BeautifulSoup(html, 'lxml')
#             asins = []
#             for product in soup.find_all("div", {"data-asin": True}):
#                 asin = product["data-asin"]
#                 asins.append(asin)
#         while "" in asins:
#             asins.remove("")
#         asins_new = asins[:4]
#         print(asins_new)
        
#         conn = sqlite3.connect('amztracker.db')
#         c = conn.cursor()
#         c.execute('''CREATE TABLE IF NOT EXISTS prices8(date DATE, asin TEXT, price FLOAT, title TEXT, dealer TEXT)''')
        
#         s = AsyncHTMLSession()
#         for asin in asins_new:
#             page = await browser.new_page()
#             await page.goto(url)
#             await asyncio.sleep(5)  # Use asyncio.sleep for asynchronous sleep
            
#             price = await page.inner_text('span.a-price-whole')
#             title = await page.inner_text('#productTitle')
#             dealer = await page.inner_text('#merchant-info')
#             date = datetime.datetime.today()
#             c.execute('''INSERT INTO prices8 VALUES(?,?,?,?,?)''', (date, asin, price, title, dealer))
#             print(f'Added data for {asin}, {price}')
#         conn.commit()
#         print('Committed new entries to database')
#     except Exception as e:
#             print(f"An error occurred: {str(e)}")
#     finally:
#         if 'browser' in locals():
#             await browser.close()

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        header={
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        async with session.get(url, headers=header) as response:
            return await response.text()
asins = []
asins_new = []


# async def test():
#     asins_new.append("B0BDL2DPSS")
#     asins_new.append("B0BV2XWZML")
async def amz_scraper(search):
    
    url = f"https://www.amazon.in/s?k={search}"
    html_content = await fetch_url(url)
    # print(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    asins = []
    for product in soup.find_all("div", {"data-asin": True}):
        asin = product["data-asin"]
        asins.append(asin)
    while "" in asins:
        asins.remove("")
    asins_new = asins[:6]
    # print(asins_new)
    # for i in range(6):
    #     asins_new_1[i]=asins_new[i]

    
    conn = sqlite3.connect('amztracker.db')
    c = conn.cursor()
    # c.execute('''CREATE TABLE prices10(sno INTEGER, date DATE, asin TEXT, price FLOAT, title TEXT, dealer TEXT)''')
    c.execute(''' DELETE FROM prices10 ''')
    tasks = []
    for asin in asins_new:
        url = f'https://www.amazon.in/dp/{asin}'
        tasks.append(fetch_url(url))
    # c.execute(''' DELETE FROM prices9 ''')
    html_responses = await asyncio.gather(*tasks)
    # print(html_responses)
    for i in range(len(html_responses)):
        r = BeautifulSoup(html_responses[i], 'lxml')
        # print(r)
        # price=90
        # price = r.select_one('span.a-offscreen').get_text(strip=True)
        price_element = r.find('span', {'class': 'a-price-whole'})
        price = price_element.text.strip()
        title = r.select_one('#productTitle').get_text(strip=True)
        dealer = r.select_one('#merchant-info').get_text(strip=True)
        print(dealer)
        date = datetime.datetime.today()
        # price=90
        c.execute('''INSERT INTO prices10 VALUES(?,?,?,?,?,?)''', (i+1, date, asins_new[i], price, title, dealer))
        print(f'Added data for {asins_new[i]}, {price}')
    # return asins_new
    conn.commit()
    print('Committed new entries to database')
    c.close()
    conn.close()
print(asins_new)    
async def tracked_products(asin_array):
    conn = sqlite3.connect('amztracker.db')
    c = conn.cursor()
    # c.execute('''CREATE TABLE tracked_prices(sno INTEGER, date DATE, asin TEXT, price FLOAT, title TEXT, dealer TEXT)''')
    tasks=[]
    for asin in asin_array:
        url = f'https://www.amazon.in/dp/{asin}'
        tasks.append(fetch_url(url))
    # c.execute(''' DELETE FROM prices9 ''')
    html_responses = await asyncio.gather(*tasks)
    # print(html_responses)
    for i in range(len(html_responses)):
        r = BeautifulSoup(html_responses[i], 'lxml')
        # print(r)
        # price=90
        price = r.select_one('span.a-offscreen').get_text(strip=True)
        # price_element = r.find('span', {'class': 'a-price-whole'})
        # price = price_element.text.strip()
        title = r.select_one('#productTitle').get_text(strip=True)
        dealer = r.select_one('#merchant-info').get_text(strip=True)
        print(dealer)
        date = datetime.datetime.today()
        # price=90
        c.execute('''INSERT INTO tracked_prices VALUES(?,?,?,?,?,?)''', (i+1, date, asin_array[i], price, title, dealer))
        print(f'Added data for {asin_array}, {price}')
    # return asins_new
    conn.commit()
    print('Committed new entries to database')
    c.close()
    conn.close()



@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    if request.method == "POST":
        search = request.form['search']
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(amz_scraper(search))
        finally:
            loop.close()
        # print(search)

        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        
        # try:
        #     loop.run_until_complete(test())
        # finally:
        #     loop.close()
        
        return redirect("/list", code=302)
    return redirect("/",code=302)
@app.route('/list')
def list():
    con = sqlite3.connect("amztracker.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute('''select * from prices10''')

    rows = cur.fetchall(); 
    return render_template("list.html",rows = rows)
  
asins_track=[]
@app.route('/track', methods=("GET", "POST"), strict_slashes=False)
def track():
    if request.method == "POST":
        # test()
        id1 = request.form.get('id', False)
        id_act=int(id1)
        asins_track.append(asins_new[id_act-1])


        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(tracked_products(asins_track))
        finally:
            loop.close()
        # print(search)


        print(asins_track)
        # print(asins_new)
        return redirect("/tracked_list", code=302)

print(asins_new)


@app.route('/tracked_list')
def tracked_list():
    con1 = sqlite3.connect("amztracker.db")
    con1.row_factory = sqlite3.Row

    cur1 = con1.cursor()
    cur1.execute('''select * from prices8''')

    rows = cur1.fetchall(); 
    return render_template("list1.html",rows = rows)


if (__name__ == '__main__'):
    app.run(debug=True)


# search1 = input("Enter commodity name")

# url = "https://www.amazon.in/"
# # params = {"k": "iphone"}

# # response = requests.get(url, params=params)
# # r = requests.post(url = 'https://async.scraperapi.com/jobs', json={ 'apiKey': '5ae8defa7539ee3b929363d648522e50', 'url': 'https://www.amazon.in/' })
# # json_dict = r.text

# # act_url = json_dict.get("statusUrl")

# # print(r.content)

# # soup = BeautifulSoup(response.content, "html.parser")

# # asins = []
# # for product in soup.find_all("div", {"data-asin": True}):
# #     asin = product["data-asin"]
# #     asins.append(asin)
# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.goto(url)
#     page.fill('input#twotabsearchtextbox', search)
#     page.click('input[type=submit]')
#     page.wait_for_selector('div.s-main-slot.s-result-list.s-search-results.sg-row')
#     html = page.inner_html('div.s-main-slot.s-result-list.s-search-results.sg-row')
#     soup = BeautifulSoup(html, 'lxml')
#     asins = []
#     for product in soup.find_all("div", {"data-asin": True}):
#         asin = product["data-asin"]
#         #print(asin)
#         asins.append(asin)

# while("" in asins):
#     asins.remove("")
# # print(asins[:4])

# asins_new=asins[:4]
# # i=0
# print(asins_new)
# # while(i<3):
# #     asins_new[i]=asins[i]
# #     i+=1
# # print(asins_new)
# # #connect to/create database
# conn = sqlite3.connect('amztracker.db')
# c = conn.cursor()

# #only create the table once, then comment out or delete the line
# # c.execute('''CREATE TABLE prices6(date DATE, asin TEXT, price FLOAT, title TEXT, dealer TEXT)''')

# #start session and create lists
# s = HTMLSession()

# # #read csv to list
# # with open('asins.csv', 'r') as f:
# #     csv_reader = csv.reader(f)
# #     for row in csv_reader:
# #         asins.append(row[0])

# # # #scrape data
# for asin in asins_new:
#     r = s.get(f'https://www.amazon.in/dp/{asin}')
#     r.html.render(sleep=5) 
#     price = r.html.find('span.a-price-whole')[0].text
#     title = r.html.find('#productTitle')[0].text.strip()
#     dealer = r.html.find('#merchant-info')[0].text.strip()
#     asin = asin
#     date = datetime.datetime.today()
#     c.execute('''INSERT INTO prices6 VALUES(?,?,?,?,?)''', (date, asin, price, title, dealer))
#     print(f'Added data for {asin}, {price}')

# conn.commit()
# print('Committed new entries to database')




