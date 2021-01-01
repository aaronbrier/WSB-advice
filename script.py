import re
from creds import *
from tickerslist import *
import praw
from textblob import TextBlob
from collections import defaultdict


def clean(comment):  
	return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())

def analyze(all_comments, tickers):
	for comment in all_comments:
		if not isinstance(comment, praw.models.MoreComments):
			comment = clean(comment.body)
			word_list = comment.split()
			for word in word_list:
				if len(word) <= 6 and word.isupper():
					tickers[word] += TextBlob(comment).sentiment.polarity

def main():
	reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)
	tickers = defaultdict(float)
	for submission in reddit.subreddit("wallstreetbets").hot(limit=10):
		analyze(submission.comments.list(), tickers)
	with open("output.txt","w") as file:
		for ticker, sentiment in sorted(tickers.items(), key = lambda x : x[1]):
			print(f"{ticker}: {sentiment}")
			if sentiment > 0:
				file.write(f"{ticker}: {sentiment}\n")


if __name__ == "__main__":
	main()