
import tweepy
import keys
import pymongo
import time

def connections():
    '''
    Connect to mongodb and twitter
    Create your own Bearer Token through twitter
    '''
    client_mongo = pymongo.MongoClient(host="mongodb",port=27017)
    client_twit = tweepy.Client(bearer_token=keys.Bearer_Token)

    return client_mongo, client_twit


def create_mongodb(client_mongo):
    '''Create mongo databases. The names are optional'''  
    db_uk = client_mongo.ukraine_twit
    db_ro = client_mongo.rojava_twit
    dbcoll_uk = db_uk.twit
    dbcoll_ro = db_ro.twit  
    
    return db_uk, db_ro, dbcoll_uk, dbcoll_ro

def tweet_colection(search_query):
    '''Get tweets from anything you want, but here we use ukraine and rojava.'''
    cursor = tweepy.Paginator(
        method=client_twit.search_recent_tweets,
        query=search_query,
        tweet_fields=['author_id', 'created_at', 'public_metrics'],
        user_fields=['username', 'profile_image_url']
    ).flatten(limit=100)

    return cursor

def twits_to_mongo(db, cursor):
    '''Insert the twits into mongodb one by one'''
    for tweet in cursor:
        info = {'text': tweet.text, 'id': tweet.id, 'created_at': tweet.created_at, 'metric':tweet.public_metrics}
        db.twit.insert_one(info)



client_mongo, client_twit = connections()
db_uk, db_ro, dbcoll_uk, dbcoll_ro = create_mongodb(client_mongo)


while True:
    dbcoll_uk.delete_many({})
    search_query_uk = "#Ukraine lang:en -is:retweet -is:reply -is:quote -has:links"
    cursor_uk = tweet_colection(search_query_uk)
    twits_to_mongo(db_uk, cursor_uk)

    dbcoll_ro.delete_many({})
    search_query_ro = "#Rojava lang:en -is:retweet -is:reply -is:quote -has:links"
    cursor_ro = tweet_colection(search_query_ro)
    twits_to_mongo(db_ro, cursor_ro)
    print('one round done')
    time.sleep(60)


