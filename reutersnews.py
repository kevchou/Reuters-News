# TODO: clean news story body. it is currently getting image text too

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

BASEURL = 'https://www.reuters.com/'

def generate_date_list(start, end):
    """Returns a list of datetime objects (days) between from $start to $end.
    """
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    end_dt = dt.datetime.strptime(end, '%Y-%m-%d')

    dates = [start_dt + dt.timedelta(days=x) for x in range(0, (end_dt - start_dt).days+1)]
    return dates


def get_story_body(url):
    """Webscrapes the body text of input news article
    """
    request = urllib.request.urlopen(url)
    raw = request.read()
    soup = BeautifulSoup(raw, 'html.parser')

    article_body = soup.find("div", {"class": "StandardArticleBody_body"})
    body_text = "".join([p.text for p in article_body.find_all('p')])

    return body_text


def get_story(ticker, date):
    """Gets all stories for input company $ticker for $date
    """
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
            'url': top_link,
            'body': get_story_body(BASEURL + top_link)
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
                'url': story_link,
                'body': get_story_body(BASEURL + story_link)
            })

    return company_news


def get_all_stories(ticker, start, end):
    """Gets all stories for input $ticker, for every date between $start and $end
    """
    # Get and convert dates to right format for url
    dates = generate_date_list(start, end)
    dates = [f"{str(d.month).zfill(2)}{str(d.day).zfill(2)}{d.year}" for d in dates] # Date needs to be MMDDYYYY

    # Variable to stores all news articles
    all_news = []
    for i, date in enumerate(dates):
        all_news.append(get_story(ticker, date))

    # Filter out dates without stories
    all_news = [n for n in all_news if n.get('top_story')]

    return all_news