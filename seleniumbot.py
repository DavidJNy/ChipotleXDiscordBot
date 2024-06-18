import discord
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import asyncio
import logging
from config import DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID, TWITTER_USERNAME

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Function to fetch latest tweets using Selenium
def fetch_latest_tweet(username):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = f'https://twitter.com/{username}'
        logging.info(f"Fetching tweets from {url}")
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        tweets = driver.find_elements(By.CSS_SELECTOR, 'article[role="article"]')
        if tweets:
            tweet = tweets[0]
            tweet_text = tweet.text
            tweet_id = tweet.get_attribute('data-tweet-id')
            logging.info(f"Found tweet ID: {tweet_id}")
            logging.info(f"Tweet text: {tweet_text}")
            return tweet_id, tweet_text
        else:
            logging.error("No tweets found on the page")
    except Exception as e:
        logging.error(f"Failed to fetch tweets: {str(e)}")
    finally:
        driver.quit()

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
            tweet_url = f"https://twitter.com/{TWITTER_USERNAME}/status/{tweet_id}"
            message = f"New tweet from {TWITTER_USERNAME}: {tweet_url}\n{tweet_text}"
            await discord_channel.send(message)
            last_tweet_id = tweet_id
        else:
            logging.info("No new tweets found or failed to fetch tweets.")

        # Wait for 60 seconds before checking for new tweets again
        await asyncio.sleep(60)

client.run(DISCORD_BOT_TOKEN)
