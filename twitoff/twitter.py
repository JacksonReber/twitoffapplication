import sqlalchemy
import tweepy
import spacy
import requests
from os import getenv
from .models import DB, Tweet, User


#TODO - 
TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)

TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load('my_model')

def vectorize_tweet(tweet_text):
  return nlp(tweet_text).vector

def add_or_update_user(username):
    try:
        resp = requests.get(
            f'https://lambda-ds-twit-assist.herokuapp.com/user/{username}')
        user = resp.json()
        user_id = user['twitter_handle']['id']

        db_user = (User.query.get(user_id)) or User(id=user_id, name=username)

        DB.session.add(db_user)

        tweets = user['tweets']
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet['full_text'])
            db_tweet = Tweet(
                id=tweet['id'], text=tweet['full_text'], vect=tweet_vector)
            db_user.tweets.append(db_tweet)
            exists = Tweet.query.filter(Tweet.id == db_tweet.id).all()
            if not exists:
                DB.session.add(db_tweet)

    
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
#    else:

    DB.session.commit()
    
def insert_example_users():
    DB.session.execute(sqlalchemy.delete(Tweet).where(Tweet.id.isnot(None)))
    DB.session.execute(sqlalchemy.delete(User).where(User.id.isnot(None)))
    DB.session.commit()
    # users = ["mcuban", "nasa"]
    # for user in users:
#add_or_update_user(user)
