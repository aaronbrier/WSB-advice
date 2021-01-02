import re
from creds import *
from tickerslist import TICKER_LIST
import praw
from textblob import TextBlob
from collections import defaultdict

POST_LIMIT = 100

def clean(comment):  
	return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())

#uses textblob for sentiment analysis of the entire comment
#if there is a stock ticker in the comment, it adds that comments sentiment analysis to the tickers[ticker]
def analyze_sentiment(all_comments, tickers):
	for comment in all_comments:
		if not isinstance(comment, praw.models.MoreComments):
			comment = clean(comment.body)
			word_list = comment.split()
			for word in word_list:
				if word in TICKER_LIST:
					tickers[word] += TextBlob(comment).sentiment.polarity

#it will look for the word buy and any stock tickers within 1 words of the mention of buy
#does the same thing for sell
def analyze_naive(all_comments, tickers):
	for comment in all_comments:
		if not isinstance(comment, praw.models.MoreComments):
			comment = clean(comment.body)
			word_list = comment.split()
			for index in range(len(word_list)):
				if "buy" in word_list[index].lower():
					if index-1 >=0 and word_list[index-1] in TICKER_LIST:
						tickers[word_list[index-1]] += 1
					if index+1 < len(word_list) and word_list[index+1] in TICKER_LIST:
						tickers[word_list[index+1]] += 1
				if "sell" in word_list[index].lower():
					if index-1 >=0 and word_list[index-1] in TICKER_LIST:
						tickers[word_list[index-1]] -= 1
					if index+1 < len(word_list) and word_list[index+1] in TICKER_LIST:
						tickers[word_list[index+1]] -= 1

def main():
	reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)
	tickers_sentiment = defaultdict(float)
	tickers_naive = defaultdict(int)

	for submission in reddit.subreddit("wallstreetbets").hot(limit=POST_LIMIT):
		analyze_sentiment(submission.comments.list(), tickers_sentiment)
		analyze_naive(submission.comments.list(), tickers_naive)

	with open("sentiment_output.txt","w") as file:
		for ticker, sentiment in sorted(tickers_sentiment.items(), key = lambda x : x[1]):
			print(f"{ticker}: {sentiment}")
			if sentiment > 0:
				file.write(f"{ticker}: {sentiment}\n")
	with open("buy_sell_output.txt","w") as file:
		for ticker, sentiment in sorted(tickers_naive.items(), key = lambda x : x[1]):
			print(f"{ticker}: {sentiment}")
			if sentiment > 0:
				file.write(f"{ticker}: {sentiment}\n")


if __name__ == "__main__":
	main()