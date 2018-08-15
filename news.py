import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime as dt

ticker = 'AAPL'

# Generate list of dates
dates = pd.date_range(start='2018-08-01', end='2018-08-14', freq='D').tolist()
dates = [f"{str(d.month).zfill(2)}{str(d.day).zfill(2)}{d.year}" for d in dates]

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
