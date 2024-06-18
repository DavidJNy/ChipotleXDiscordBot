import discord
import tweepy
import asyncio
import logging
from config import DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID, TWITTER_USERNAME, TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up Tweepy
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

# Set up Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def fetch_latest_tweet(username):
    tweets = twitter_api.user_timeline(screen_name=username, count=1, tweet_mode='extended')
    if tweets:
        tweet = tweets[0]
        tweet_id = tweet.id_str
        tweet_text = tweet.full_text
        return tweet_id, tweet_text
    return None, None

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    discord_channel = client.get_channel(int(DISCORD_CHANNEL_ID))
    if not discord_channel:
        logging.error("Invalid channel ID")
        return

    last_tweet_id = None

    while True:
        tweet_id, tweet_text = await fetch_latest_tweet(TWITTER_USERNAME)
        if tweet_id and tweet_text and tweet_id != last_tweet_id:
            tweet_url = f"https://twitter.com/{TWITTER_USERNAME}/status/{tweet_id}"
            message = f"New tweet from {TWITTER_USERNAME}: {tweet_url}\n{tweet_text}"
            await discord_channel.send(message)
            last_tweet_id = tweet_id
        else:
            logging.info("No new tweets found or failed to fetch tweets.")

        # Wait for 60 seconds before checking for new tweets again
        await asyncio.sleep(60)

client.run(DISCORD_BOT_TOKEN)
