import discord
import requests
from bs4 import BeautifulSoup
import asyncio
import logging
from config import DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID, TWITTER_USERNAME

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Function to fetch latest tweets using web scraping
def fetch_latest_tweet(username):
    url = f'https://twitter.com/{username}'
    response = requests.get(url)
    logging.info(f"Fetching tweets from {url}")
    if response.status_code == 200:
        logging.info("Successfully fetched the Twitter page")
        soup = BeautifulSoup(response.text, 'html.parser')
        tweets = soup.find_all('div', {'data-testid': 'tweet'})
        if tweets:
            tweet = tweets[0]
            tweet_id = tweet.get('data-tweet-id')
            tweet_text = tweet.find('div', {'lang': True}).text
            logging.info(f"Found tweet ID: {tweet_id}")
            logging.info(f"Tweet text: {tweet_text}")
            return tweet_id, tweet_text
        else:
            logging.error("No tweets found on the page")
    else:
        logging.error(f"Failed to fetch tweets: {response.status_code}")
        logging.error(f"Response content: {response.content}")

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
        tweet_id, tweet_text = fetch_latest_tweet(TWITTER_USERNAME)
        if tweet_id and tweet_text and tweet_id != last_tweet_id:
            tweet_url = f"https://x.com/{TWITTER_USERNAME}/status/{tweet_id}"
            message = f"New tweet from {TWITTER_USERNAME}: {tweet_url}\n{tweet_text}"
            await discord_channel.send(message)
            last_tweet_id = tweet_id
        else:
            logging.info("No new tweets found or failed to fetch tweets.")

        # Wait for 60 seconds before checking for new tweets again
        await asyncio.sleep(10)

client.run(DISCORD_BOT_TOKEN)
