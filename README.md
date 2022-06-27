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
    - Bearer_Token = < >
    This should be obtained from Tweeter developer 

    Step 1: Get a Twitter Bearer Token

    Register your application on apps.twitter.com.

    Navigate to the Twitter App dashboard and open the Twitter App for which you would like to generate access tokens.

    Navigate to the “keys and tokens” page.

    You’ll find the API keys, user Access Tokens, and Bearer Token on this page.

    Write down the Bearer Token.

- etl transformer keys.py:
    - postgres = 'postgresql://postgres:12345@postgresdb:5432'

    If you have initiated the postgres docker container before, you might have to enter the user name and the password that were initally used
    - postgres = 'postgresql://user:password@host:5432'

- slack bot keys.py:
    - webhook_url = <>
    - postgres = 'postgresql://postgres:12345@postgresdb:5432'

    get your webhook_url from slack

    Go to [your_app](https://api.slack.com/apps)

    If you don't have one, create a new app. 

    Click on your app.

    Go to 'Add Features and Functionality'

    Click on Incoming Webhooks and activate it.

    Click on 'Add New Webhook to Workspace'

    Select the channel you want to post your app. 

    Copy the Webohook URL into the keys.py

