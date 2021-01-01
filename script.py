import re
from creds import *
import praw
from textblob import TextBlob

def clean(comment): 
	#clean comments by removing links, special characters  
	return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())

def analyze(all_comments):
	total = 0
	for comment in all_comments:
		if not isinstance(comment, praw.models.MoreComments):
			total += TextBlob(clean(comment.body)).sentiment.polarity
	return total

total = 0
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)
for submission in reddit.subreddit("wallstreetbets").hot(limit=10):
	print(submission.title)
	all_comments = submission.comments.list()
	total += analyze(all_comments)
	print(total)