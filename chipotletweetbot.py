import discord
import requests
import asyncio
import logging
from config import (
    TWITTER_BEARER_TOKEN,
    DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID, TWITTER_USERNAME
)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Function to fetch tweets
def fetch_tweets(username, bearer_token):
    headers = {
        'Authorization': f'Bearer {bearer_token}',
    }
    params = {
        'tweet.fields': 'created_at',
        'expansions': 'author_id',
        'usernames': username,
    }
    url = 'https://api.twitter.com/2/tweets/search/recent'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to fetch tweets: {response.status_code}, {response.text}")
        return None

@client.event
async def on_ready():
    try:
        print(f'Logged in as {client.user}')
        for guild in client.guilds:
            for channel in guild.channels:
                print(f'Channel: {channel.name}, ID: {channel.id}, Type: {channel.type}')

        discord_channel = client.get_channel(int(DISCORD_CHANNEL_ID))
        if not discord_channel:
            raise ValueError("Invalid channel ID")

        while True:
            tweets = fetch_tweets(TWITTER_USERNAME, TWITTER_BEARER_TOKEN)
            if tweets and 'data' in tweets:
                for tweet in tweets['data']:
                    tweet_url = f"https://twitter.com/{TWITTER_USERNAME}/status/{tweet['id']}"
                    message = f"New tweet from {TWITTER_USERNAME}: {tweet_url}"
                    await discord_channel.send(message)
            else:
                logging.error("Failed to fetch tweets")

            # Wait for 60 seconds before fetching tweets again
            await asyncio.sleep(60)

    except Exception as e:
        logging.error(f"Error in on_ready: {e}")

client.run(DISCORD_BOT_TOKEN)
