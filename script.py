import re
import requests
import openpyxl 
import concurrent.futures
from bs4 import BeautifulSoup

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Output'
sheet.append(['Name', 'Email'])

def scrape_gibsondunn(page):
    global excel, sheet, names, emails
    url = f'https://www.gibsondunn.com/?paged1={page}&search=lawyer&type=lawyer&s&office%5B0%5D=1722&office%5B1%5D=1721&office%5B2%5D=1720&office%5B3%5D=1719&office%5B4%5D=1718&office%5B5%5D=1717&office%5B6%5D=1716&office%5B7%5D=1715&office%5B8%5D=1714&office%5B9%5D=1713&school'
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        cards = soup.find('div', 'container').find_all('div', class_=re.compile('col-xs-12 col-sm-12 col-md-12 search-content xs-sm-hidden'))
        
        for card in cards:
            name = email = None
            try:
                name = card.find('h2').text.strip()
            except Exception as error:
                print(f'page: {page}; error in name: {error}')
            try:
                email = card.find('a', 'print-btn').text.strip()
            except Exception as error:
                print(f'page: {page}; error in email: {error}')
            sheet.append([name, email])
        excel.save('gibsondunn.xlsx')
    except Exception as error:
        print(f'page: {page}; error: {error}')
        
counter = []
i = 1
while i <= 70:
    counter.append(i)
    i += 1
    
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(scrape_gibsondunn, counter)
