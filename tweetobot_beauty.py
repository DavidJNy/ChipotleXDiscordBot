import requests
from bs4 import BeautifulSoup
import discord
import asyncio
from config import DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID

# Set up Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)



# Function to fetch latest tweets using web scraping
def fetch_latest_tweet(username):
    url = f'https://x.com/{username}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)
        tweets = soup.find_all('div', {'data-testid': 'tweet'})
        if tweets:
            tweet = tweets[0]
            tweet_id = tweet.get('data-tweet-id')
            tweet_text = tweet.find('div', {'lang': True}).text
            return tweet_id, tweet_text
        else:
            print("No tweets found on the page")
    else:
        print(f"Failed to fetch tweets: {response.status_code}")

    return None, None

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    discord_channel = client.get_channel(int(DISCORD_CHANNEL_ID))
    if not discord_channel:
        print("Invalid channel ID")
        return

    last_tweet_id = None

    while True:
        tweet_id, tweet_text = fetch_latest_tweet('PsykoMcNasty')  # Replace with your desired Twitter username
        if tweet_id and tweet_text and tweet_id != last_tweet_id:
            tweet_url = f"https://x.com/example_username/status/{tweet_id}"  # Replace with your desired Twitter username
            message = f"New tweet from example_username: {tweet_url}\n{tweet_text}"
            await discord_channel.send(message)
            last_tweet_id = tweet_id
        else:
            print("No new tweets found or failed to fetch tweets.")

        # Wait for x seconds before checking for new tweets again
        await asyncio.sleep(5)

client.run(DISCORD_BOT_TOKEN)
