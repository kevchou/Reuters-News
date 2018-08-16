import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import re

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

    date_text = soup.find('div', {'class': 'ArticleHeader_date'}).text
    time_re = re.search("([0-9]+:[0-9]+ [a-zA-Z]{2})", date_text)
    time = time_re.groups()[0]

    article_body = soup.find("div", {"class": "StandardArticleBody_body"})
    body = "".join([p.text for p in article_body.find_all('p')])

    return body, time


def parse_story(story, date):
    header = story.find('h2')

    article_url = header.find('a').get('href')
    headline = header.text

    body, post_time = get_story_body(BASEURL + article_url)

    return {
        'headline': headline,
        'body': body,
        'url': article_url,
        'post_date': dt.datetime.strptime(date + ' ' + post_time, '%m%d%Y %I:%M %p')
    }



def get_story(ticker, date):
    """Gets all stories for input company $ticker for $date
    """
    url = f'https://www.reuters.com/finance/stocks/company-news/{ticker}.O?date={date}'

    # Get html from URL and create soup object
    request = urllib.request.urlopen(url)
    raw = request.read()
    soup = BeautifulSoup(raw, 'html.parser')

    company_news = {
        'date': dt.datetime.strptime(date, '%m%d%Y'),
        'url': url
    }

    # Finds the company news articles
    news = soup.findAll("div", {"id": "companyNews"})

    # Top Story
    top_story = news[0]
    if top_story.find('h2'):
        company_news['top_story'] = parse_story(top_story, date)

    # Other Stories
    other_stories = news[1].findAll('div', {'class': 'feature'})
    if len(other_stories) > 0:
        company_news['other_stories'] = []
        
        for s in other_stories:
            company_news['other_stories'].append(parse_story(s, date))

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