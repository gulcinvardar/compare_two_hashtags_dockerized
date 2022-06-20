import pandas as pd
import psycopg2
import pymongo
import regex as re
from sqlalchemy import create_engine
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import keys

def connections():
    '''Connects to mongo database'''
    client = pymongo.MongoClient(host="mongodb", port=27017)
    engine = create_engine(keys.postgres, echo=True)

    return client, engine

def create_mongo_db():
    mongo_db_ro = client.rojava_twit
    mongo_db_uk = client.ukraine_twit                                   
    twits_ro = mongo_db_ro.twit.find()
    twits_uk = mongo_db_uk.twit.find()                                     

    return twits_ro, twits_uk


def clean_tweets(twit):
    '''
    This will be used in the method to insert the data into Postgres db
    Cleans the tweets
    '''
    twit = re.sub('@[A-Za-z0-9]+', '', twit)                        
    twit = re.sub('https?:\/\/\S+', '', twit)                       
    twit = re.sub('#\w+', '', twit)                                
    twit = re.sub('RT\s', '', twit)                                 
    twit = re.sub('(?i)breaking[ ]?(news)?', '', twit)              
    
    return twit


def to_postgres(engine, twits, postgres_db_name, query):
    '''
    Loads the cleaned text and the sentiment compound score 
    based on Vader analysis into postgres db
    '''
    engine.execute(f'DROP TABLE IF EXISTS {postgres_db_name};')                                
    engine.execute(f'''
                    CREATE TABLE {postgres_db_name} 
                    (text VARCHAR(500),
                    sentiment NUMERIC,
                    date DATE,
                    likes NUMERIC); 
                    ''') 
    analyzer = SentimentIntensityAnalyzer()                                   
    for twit in twits:
        text = twit['text']
        text_clean = clean_tweets(text)
        date = twit['created_at']                        
        score = analyzer.polarity_scores(text_clean).get('compound')
        likes = dict(twit['metric']).get('like_count')       
        engine.execute(query, (text, score, date, likes))
    

    


client, engine = connections()
time.sleep(10)

while True:
    twits_ro, twits_uk = create_mongo_db()
    postgres_db_name_uk = 'ukraine_twits' 
    query_uk = "INSERT INTO ukraine_twits VALUES (%s, %s, %s, %s);" 
    to_postgres(engine, twits_uk, postgres_db_name_uk, query_uk)
    postgres_db_name_ro = 'rojava_twits' 
    query_ro = "INSERT INTO rojava_twits VALUES (%s, %s, %s, %s);" 
    to_postgres(engine, twits_ro, postgres_db_name_ro, query_ro)
    time.sleep(60)