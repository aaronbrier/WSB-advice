# WSB-advice
A program that gives me financial advice straight from https://www.reddit.com/r/wallstreetbets/

Looks at comments from trending posts to find the stocks that have the highest sentiment value. Also looks at stock tickers that have mentions of "buy" nearby

Uses PRAW (Reddit API Wrapper) and Textblob for sentiment analysis

Dependencies:
* pip3 install praw
* pip3 install -U textblob
* python3 -m textblob.download_corpora
* CLIENT_ID and CLIENT_SECRET obtained from https://www.reddit.com/prefs/apps