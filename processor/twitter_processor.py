import openai
import re
from constants.openai_pricing import API_COST_PER_1000_TOKENS


class TwitterProcessor:
    def __init__(self, twitter_accounts, buffer_size, openai_api_key):
        self.twitter_accounts = twitter_accounts
        self.buffer_size = buffer_size
        self.tweets_buffer = []

        openai.api_key = openai_api_key

    @staticmethod
    def calculate_tweet_cost(self, base_prompt, tweet):
        price = ((len(base_prompt) + len(tweet)) / 4) * (API_COST_PER_1000_TOKENS / 1000)
        return price

    def process_tweet(self, tweet):
        # TODO: Improve base_prompt to get better results
        base_prompt = "Analyze the sentiment of this tweet about Bitcoin:\n\n"
        # Use OpenAI's API to generate a response to the tweet
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=base_prompt+tweet,
            temperature=0.5,
            max_tokens=50,
            n=1,
            stop=None,
            timeout=10.0,
        )

        # Calculate tweet processing price
        cost = self.calculate_tweet_cost(base_prompt, tweet)

        # Extract the response text from the OpenAI API response
        response_text = response.choices[0].text

        # TODO: Analyze the response text more accurately to determine the sentiment towards Bitcoin
        if re.search(r'\b(bullish|buy)\b', response_text, re.IGNORECASE):
            sentiment = 'positive'
        elif re.search(r'\b(bearish|sell)\b', response_text, re.IGNORECASE):
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        # Return a dictionary containing the tweet ID, creation time, text, and sentiment
        return {
            'id': tweet.id,
            'created_at': tweet.created_at,
            'text': tweet.text,
            'sentiment': sentiment,
            'cost': cost
            }

    def buffer_tweets(self, tweets):
        for tweet in tweets:
            processed_tweet = self.process_tweet(tweet)
            self.tweets_buffer.append(processed_tweet)

            if len(self.tweets_buffer) == self.buffer_size:
                self.db.insert_tweets(self.tweets_buffer)
                self.tweets_buffer = []
