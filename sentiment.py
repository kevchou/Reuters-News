import reutersnews
import nltk

aapl = reutersnews.get_all_stories('AAPL', '2018-07-01', '2018-08-14')



test_article = aapl[0]['top_story']['body']

# Break up article into sentences
from nltk import tokenize
article_lines = tokenize.sent_tokenize(test_article)


from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

sid.polarity_scores(test_article)


news_day = aapl[0]

for news_day in aapl:
    print(news_day['date'])
    print("Top Story", news_day['top_story']['headline'])
    print(sid.polarity_scores(news_day['top_story']['body'])['compound'])

    print("Other Stories")
    if news_day.get('other_stories'):
        for news in news_day['other_stories']:
            print(news['headline'], sid.polarity_scores(news['body'])['compound'])