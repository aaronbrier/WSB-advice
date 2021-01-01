# WSB-advice
A program that gives me financial advice straight from /r/wallstreetbets

Looks at all comments from posts from the last 2 days to find the stocks that have the highest sentiment value

Dependencies:
* pip3 install praw
* pip3 install -U textblob
* python3 -m textblob.download_corpora
* CLIENT_ID and CLIENT_SECRET obtained from https://www.reddit.com/prefs/apps