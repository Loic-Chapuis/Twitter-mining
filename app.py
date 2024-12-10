# caling API to get the data needed

import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# Authenticate with the Twitter API
def authenticate_twitter():
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    return client

# Function to fetch the latest tweet from a specific user
def get_latest_tweet(client, username):
    try:
        # Utilisation de l'API v2
        user = client.get_user(username=username)
        if not user.data:
            return {"error": "User not found"}
            
        user_id = user.data.id
        tweets = client.get_users_tweets(id=user_id, 
                                       max_results=1,
                                       tweet_fields=['created_at', 'public_metrics'])
        
        if tweets.data:
            tweet = tweets.data[0]
            return {
                "text": tweet.text,
                "created_at": tweet.created_at.isoformat(),
                "likes": tweet.public_metrics['like_count'],
                "retweets": tweet.public_metrics['retweet_count']
            }
        else:
            return {"error": "No tweets found for this user."}
    except tweepy.TweepyException as e:
        return {"error": str(e)}

# Main entry point
if __name__ == "__main__":
    client = authenticate_twitter()
    username = "unusual_whales"
    tweet_data = get_latest_tweet(client, username)
    if "error" in tweet_data:
        print(f"Error: {tweet_data['error']}")
    else:
        print("Latest Tweet from @unusual_whales:")
        for key, value in tweet_data.items():
            print(f"{key.capitalize()}: {value}")
