"""SQLAlchemy models and utility functions for Twitoff Application"""
from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


class User(DB.Model):
    """Twitter User Table that will correspond to tweets - SQLAlchemy syntax"""
    id = DB.Column(DB.BigInteger, primary_key=True) #id column (primary key)
    name = DB.Column(DB.String, nullable=False) #name column
#    newest_tweet_id = DB.Column(DB.BigInteger) #keeps track of recent user tweet

    def __repr__(self):
      return f'<User: {self.name}>'

class Tweet(DB.Model):
    """Tweet text data associated with Users Table"""
    id = DB.Column(DB.BigInteger, primary_key=True) #id column (primary key)
    text = DB.Column(DB.Unicode(300)) # text column
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'))
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
      return f'<Tweet: {self.text}>'