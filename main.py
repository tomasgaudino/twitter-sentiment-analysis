from constants.twitter_accounts import TWITTER_ACCOUNTS
from connector.database import Database
from processor.twitter_processor import TwitterProcessor
from utils.logger import logger
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()


class TwitterClient:
    def __init__(self, db_name, db_user, db_password, db_host, db_port,
                 buffer_size, openai_api_key, max_retries=3, retry_interval=5):
        self.twitter_accounts = TWITTER_ACCOUNTS
        self.buffer_size = buffer_size
        self.db = Database(db_name, db_user, db_password, db_host, db_port, max_retries, retry_interval)
        self.processor = TwitterProcessor(TWITTER_ACCOUNTS, buffer_size, openai_api_key)

        # TODO: Set up authentication with your Twitter API credentials
        auth = tweepy.OAuth1UserHandler(
            consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
            consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
            access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        )
        self.api = tweepy.API(auth)

    def retrieve_tweets(self):
        for account in self.twitter_accounts:
            logger.info(f"Getting tweets from {account}...")
            try:
                tweets = self.api.user_timeline(screen_name=account, count=10)
            except tweepy.TweepError as e:
                logger.error(f"Error retrieving tweets for {account}: {str(e)}")
                continue

            # Process the tweets and buffer them for insertion into the connector
            self.processor.buffer_tweets(tweets)

        # Insert any remaining tweets in the buffer into the connector
        if self.processor.tweets_buffer:
            try:
                self.db.insert_tweets(self.processor.tweets_buffer)
            except Exception as e:
                logger.error(f"Error inserting tweets into database: {str(e)}")

        # Disconnect from the connector when done
        self.db.disconnect()


if __name__ == '__main__':
    # Set up the TwitterClient and retrieve the latest tweets
    client = TwitterClient(db_name=os.environ.get('DB_NAME'),
                           db_user=os.environ.get('DB_USER'),
                           db_password=os.environ.get('DB_PASSWORD'),
                           db_host=os.environ.get('DB_HOST'),
                           db_port=os.environ.get('DB_PORT'),
                           max_retries=3,
                           retry_interval=5,
                           buffer_size=100,
                           openai_api_key=os.environ.get('OPENAI_TOKEN'))
    client.retrieve_tweets()
