import sys
import os
import jsonpickle
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
nltk.download('vader_lexicon')
nltk.download('stop_words')

import praw
from praw.models import MoreComments
from datetime import datetime
from uuid import uuid4

from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
username = os.getenv('username')
password = os.getenv('password')
user_agent = os.getenv('user_agent')

class ScoredEntry:
    def __init__(self, id, scores, entry_date, total, title="default"):
        self.id = id
        self.scores = scores
        self.entry_date = entry_date
        self.total = total
        self.title = title
        
def scry(keyword, subreddit="all"):
    # keyword = "GME"  # searching post titles for match || discussion
    # alernatively load all available comments and look for match
    sia = SIA()
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         password=password,
                         user_agent=user_agent,
                         username=username)

    sub = reddit.subreddit(subreddit)
    posts = sub.new(limit=20)
    eventid = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

    result = []

    # TODO: create generator function to decouple below responsibilities 

    for post in posts:
        title = post.title

        if keyword in title:
            submission = reddit.submission(post)
            utc = submission.created_utc
            dt = datetime.fromtimestamp(utc)
            post_entry_date = dt.strftime("%m/%d/%Y, %H:%M:%S")

            total_com = len(submission.comments)
            if total_com == 0: 
                continue

            sentiment_scores = {
                "pos_aggregate": 0,
                "neg_aggregate": 0,
                "compound_aggregate": 0,
                "compound_average": 0
            }

            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments):
                    continue

                scores = sia.polarity_scores(top_level_comment.body)
                sentiment_scores["compound_aggregate"] += scores['compound']
                sentiment_scores["pos_aggregate"] += scores['pos']
                sentiment_scores["neg_aggregate"] += scores['neg']

            # Right now, only focused on compound score average. pos/neg included incase they
            # can also show interesting trends
            calc_avg = sentiment_scores["compound_aggregate"] / total_com

            # TODO: cap floating dec points
            sentiment_scores["compound_average"] = calc_avg

            entry = ScoredEntry(eventid, sentiment_scores,
                                post_entry_date, total_com, title)
            frozen = jsonpickle.encode(entry.__dict__)
            # print(frozen)
            result.append(frozen)

    return result
