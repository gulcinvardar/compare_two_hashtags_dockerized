from sqlalchemy import create_engine
import requests
import json
import psycopg2
import keys
import time
import random

def postgres_connection():
    '''
    Connects to postgres and creates a new tables.
    Create a key file for postgres connection using your own name and password that way:
    postgres = 'postgresql://{USERNAME}:{PASSWORD}@postgresdb:5432'
    '''
    engine = create_engine(keys.postgres, echo=True) 

    return engine

def post_to_slack(hashtag, tweet, sentiment, date, likes, evaluate):
    '''Create the message to be posted. 
    The message includes the dbname, tweet, sentiment analysis, creation date, and an image corresponding to the dbname.
    '''
    images = {'ukraine': 'https://static.dw.com/image/60695176_303.jpg', 
    'rojava' : 'https://mondediplo.com/local/cache-vignettes/L890xH593/lmd_1218_05_getty_1060194448_-c6909.jpg?1583762245' }

    payload = {
	    "blocks": [
            {
			    "type": "header",
			    "text": {
				    "type": "plain_text",
				    "text": f"This tweet has appeared at #{hashtag}",
				    "emoji": True
			    }
		    },
		    {
			    "type": "section",
			    "text": {
				    "type": "plain_text",
				    "text": f"\n \n {tweet}",
				    "emoji": True
			    },
			    "accessory": {
				    "type": "image",
				    "image_url": images.get(hashtag),
				    "alt_text": "alt text for image"
			    }
		    },
            {
			    "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": f"Created at: *{date}* The number of :+1: : *{likes}*",
			    }
		    },
		    {
			    "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": f"The sentiment score of this twit is *{sentiment}*.\n This seems to be *{evaluate}*:exclamation:"
		        }
            },
            {
		    	"type": "section",
    			"text": {
	    			"type": "mrkdwn",
		    		"text": "*Would you like to talk about it?* :speech_balloon:"
			    },
    			"accessory": {
	    			"type": "multi_conversations_select",
		    		"placeholder": {
			    		"type": "plain_text",
				    	"text": "Select conversations",
					    "emoji": True
	    			},
		    		"action_id": "multi_conversations_select-action"
			    }
            }
        ]
    }
    return payload

def twits_query(query):
    result = engine.execute(query).fetchall()
    tweet = dict(result[0]).get('text')
    sentiment = float(dict(result[0]).get('sentiment'))
    date = dict(result[0]).get('date')
    likes = dict(result[0]).get('likes')

    return tweet, sentiment, date, likes

def evaluate_the_sentiment(sentiment):
    evaluate = sentiment
    if evaluate < -0.75:
        evaluate = 'quite negative'
    elif evaluate < -0.5:
        evaluate = 'negative'
    elif evaluate < -0.25:
        evaluate = 'not so negative'
    elif evaluate == -0:
        evaluate = 'quite neutral'
    elif evaluate < 0.25:
        evaluate = 'mayyyyybe positive'
    elif evaluate < 0.5:
        evaluate = 'positive.'
    elif evaluate < 0.75:
        evaluate = 'quite positive'
    else:
        evaluate = 'super positive'
    
    return evaluate





engine = postgres_connection()
db_names = ['ukraine_twits', 'rojava_twits']
while True:
    db_random = random.choice(db_names)
    hashtag = db_random.split('_')[0]
    query = f'SELECT * FROM {db_random} ORDER by RANDOM() LIMIT 1;'
    tweet, sentiment, date, likes = twits_query(query)
    evaluate = evaluate_the_sentiment(sentiment)
    payload = post_to_slack(hashtag, tweet, sentiment, date, likes, evaluate)
    requests.post(url=keys.webhook_url, json = payload)
    time.sleep(15)
