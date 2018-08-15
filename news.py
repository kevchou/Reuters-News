import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt



ticker = 'AAPL'

# Generate list of dates
start = '2018-01-01'
end = '2018-01-07'



def generate_date_list(start, end):
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    end_dt = dt.datetime.strptime(end, '%Y-%m-%d')

    dates = [start_dt + dt.timedelta(days=x) for x in range(0, (end_dt - start_dt).days)]
    return dates

dates = generate_date_list(start, end)



# Convert date to right format for url
dates = [f"{str(d.month).zfill(2)}{str(d.day).zfill(2)}{d.year}" for d in dates]

# Stores all news articles
all_news = []

for i, date in enumerate(dates):
    
    url = f'https://www.reuters.com/finance/stocks/company-news/{ticker}.O?date={date}'

    # Get html from URL and create soup object
    request = urllib.request.urlopen(url)
    raw = request.read()
    soup = BeautifulSoup(raw, 'html.parser')

    company_news = {
        'date': date
    }

    # Finds the company news articles
    news = soup.findAll("div", {"id": "companyNews"})

    # Top Story
    top_story = news[0]
    if top_story.find('h2'):
        top_header = top_story.find('h2')

        top_link = top_header.find('a').get('href')
        top_text = top_header.text

        company_news['top_story'] = {
            'text': top_text,
            'url': top_link
        }

    # Other Stories
    other_stories = news[1].findAll('div', {'class': 'feature'})
    if len(other_stories) > 0:
        company_news['other_stories'] = []
        
        for s in other_stories:
            story_header = s.find('h2')

            story_link = story_header.find('a').get('href')
            story_text = story_header.text

            company_news['other_stories'].append({
                'text': story_text,
                'url': story_link
            })

    all_news.append(company_news)
    if i % 25 == 0:
        print(i)


print(len(all_news))


##### Get full news article
url = all_news[2]['top_story']['url']
url2 = 'https://www.reuters.com/' + url

request = urllib.request.urlopen(url2)
raw = request.read()
soup = BeautifulSoup(raw, 'html.parser')

article_body = soup.find("div", {"class": "StandardArticleBody_body"})
article_body.text

