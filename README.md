# Streaming tweets from two different hashtags into a slack-bot app: Data Pipeline

This project was written during Spiced Academy Data Science Bootcamp. 
It is one of the weekly projects.

The recent tweets are streamed from #Ukraine and #Rojava, stored in MongoDB, processed for sentiment analysis.
The tweets and their sentiment analysis scores are loaded in PostgreSQL. 
The tweets are randomly stremed into the Slack-bot App together with the evaluation of their sentiment and an image taken either from Ukraine or Rojava.
The whole process is dockerized.

The contents include 
- tweet collector
    - Dockerfile and requirements for the tweeter.py to work with docker.
    - tweeter.py
- etl transformer
    - Dockerfile and requirements for the etl.py to work with docker.
    - etl.py
- slack bot
    - Dockerfile and requirements for the etl.py to work with docker.
    - slack_with_formatting.py

### Important note
    For all the folders a separate keys.py file that includes the essential passwords and tokens should be created. 

The followings should be written in different keys.py in each folder:
- tweet collector keys.py:
    - Bearer_Token = *`Bearer_Token`*
        1. This should be obtained from Tweeter developer 
        2. Register your application on apps.twitter.com.
        3. Navigate to the Twitter App dashboard and open the Twitter App for which you would like to generate access tokens.
        4. Navigate to the “keys and tokens” page.
        5. You’ll find the API keys, user Access Tokens, and Bearer Token on this page.
        6. Write down the Bearer Token in the keys.py.

- etl transformer keys.py:
    - postgres = 'postgresql://postgres:12345@postgresdb:5432'

    If you have initiated the postgres docker container before, you might have to enter the user name and the password that were initally used
    - postgres = 'postgresql://user:password@host:5432'

- slack bot keys.py:
    - webhook_url = *`webhook_url`*

        1. Get your webhook_url from slack
        2. Go to [your_app](https://api.slack.com/apps)
        3. If you don't have one, create a new app. 
        4. Click on your app.
        5. Go to 'Add Features and Functionality'
        6. Click on Incoming Webhooks and activate it.
        7. Click on 'Add New Webhook to Workspace'
        8. Select the channel you want to post your app. 
        9. Copy the Webohook URL into the keys.py

    - postgres = 'postgresql://postgres:12345@postgresdb:5432'


## Usage 

### General
Go to the [Docker_Documentation](https://docs.docker.com/), find the installation instructions and install Docker CE.
In your terminal, go to the folder that contains docker-compose.yml file.
Run: `docker compose up --build`

### Tweet Collector

Connects to MongoDB and tweeter API. 
Creates two separate databases with the tweets extracted from #Ukraine and #Rojava. 
After 60 minutes, the tweets are deleted from the databases and new tweets are inserted.

### ETL transformer

Connects to MongoDB and PostgreSQL. 
Cleans the tweets from punctuation, links, and 'breaking news', and performs sentiment analysis using vaderSentiment.
Creates a database in PostgreSQL with the original tweet, sentiment analysis compound score, date of tweet, and number of likes.
After 60 minutes, the database is renewed.
*It is important to put a time sleep of ~10 s. 
MongoDB requires time to initialize, which might lead to an empty database in PostgreSQL if not waited.*

### Slack bot

Connects to PostgreSQL and Slack-Bot. 
The sentiment of the tweet is evaluated as exclamation ranging from pretty good to quite negative.
Randomly selects the tweets from either #Ukraine or #Rojava PostreSQL databases. 
The tweet is posted with an image representing either Ukraine or Rojava based on the tweet.
For formatting the slack post, please refer to [slack-block-kit-builder](https://app.slack.com/block-kit-builder/T036UAB10E5)

## License

(c) 2022 Gülçin Vardar

Distributed under the conditions of the MIT License. See LICENSE for details.