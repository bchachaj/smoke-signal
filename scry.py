import sys
import os 
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA 
import praw 
# import math 
# import datetime as dt 
# import pandas as pd 
# import numpy as np 

# nltk.download('vader_lexicon')
# nltk.download('stopwords')

from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
username = os.getenv('username')
password = os.getenv('password')
user_agent = os.getenv('user_agent')

def scry():
    keyword = "GME"
    # sia = SIA()
    # scores = sia.polarity_scores("line was really good and amazing nice")
    # print(scores)
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         password=password,
                         user_agent=user_agent,
                         username=username)

    sub = reddit.subreddit('wallstreetbets')


    posts = sub.new(limit=10)
    for post in posts:
        title = post.title 
        print(title)

    return 'Hello from AWS Lambda using Python' + sys.version + '!' 

