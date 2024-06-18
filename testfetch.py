import tweepy
from config import TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

# Set up Tweepy with your credentials
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

def fetch_latest_tweet(username):
    try:
        # Fetch the latest tweet from the specified user
        tweets = twitter_api.user_timeline(screen_name=username, count=1, tweet_mode='extended')
        if tweets:
            tweet = tweets[0]
            tweet_id = tweet.id_str
            tweet_text = tweet.full_text
            return tweet_id, tweet_text
        else:
            print("No tweets found for this user.")
            return None, None
    except tweepy.TweepError as e:
        print(f"Failed to fetch tweets: {e}")
        return None, None

if __name__ == "__main__":
    twitter_username = 'your_twitter_username'  # Replace with the username you want to fetch the latest tweet from
    tweet_id, tweet_text = fetch_latest_tweet(twitter_username)
    if tweet_id and tweet_text:
        print(f"Latest tweet from @{twitter_username}:")
        print(f"Tweet ID: {tweet_id}")
        print(f"Tweet Text: {tweet_text}")
    else:
        print("No tweet found or failed to fetch tweet.")
