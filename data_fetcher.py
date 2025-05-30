
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def fetch_price_data(ticker):
    data = yf.download(ticker, period="1d", interval="15m")
    return data

def fetch_news_sentiment(ticker):
    query = f"{ticker} stock news"
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = [h.get_text() for h in soup.find_all("div", {"class": "BNeawe vvjwJb AP7Wnd"})]
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(h)['compound'] for h in headlines]
    return sum(scores) / len(scores) if scores else 0
