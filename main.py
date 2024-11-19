import discord
from discord.ext import tasks, commands
import random
from collections import Counter
import os  # To load the token from .env
import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from the .env file

discord_token = os.getenv("DISCORD_TOKEN")


# Initialize the activity counter
activity_counter = Counter()

# Load the token from the .env file
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up intents (required for message tracking and tagging members)
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# List of random messages
MESSAGES = [
    "Hey remember to level up your heroes!",
    "Don't forget to buy everything I have for sale in the tavern!",
    "Not sure but I'm not a gamer!",
    "Mythic Vibes my friend!",
    "Make sure to check Crypto Tro latest video!",
    "An Ancient proverb says: Each of us has two beavers inside....",
    "I like this Weekly reset show, but I kinda miss Office Hours!",
    "Every Mythic Dread Knight you make, will keep you a step ahead of the game. Two steps, if you consider Dread Knights will be released in 2084!",
    "Let me tell you a secret, yesterday I One Small Stoned frosty...."
    "Who's the mad man selling all those SPELL hats so cheap??"
    "If one archer is not enough, try three!"
    "Everybody wants to be a Beaver!"
    "You now how much i hate to play against my guildmates!"
    
]

# When the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} is now online and ready!')
    # Start the periodic task
    send_random_message.start()

# Track user activity
@bot.event
async def on_message(message):
    # Debugging: Print message details
    print(f"Received message from {message.author}: {message.content}")

    # Ignore bot messages to avoid counting them
    if message.author.bot:
        return

    # Track activity for non-bot members
    activity_counter[message.author] += 1

    # Debugging: print every time a message is tracked
    print(f"Tracking {message.author.name}: {activity_counter[message.author]} messages")

    # Print current state of the activity counter to ensure it's being updated
    print(f"Current activity counter: {activity_counter}")

    # Make sure the bot processes commands too (so !ping works)
    await bot.process_commands(message)

# Periodic task to send random messages every 30 minutes
@tasks.loop(minutes=30)
async def send_random_message():
    for guild in bot.guilds:
        # Replace with the correct channel ID
        general_channel_id = 1024108042205274223  # Replace this with your channel ID
        general_channel = guild.get_channel(general_channel_id)

        if not general_channel:
            print(f"Channel with ID {general_channel_id} not found in {guild.name}")
            continue

        # Print out the entire activity_counter to see what's tracked
        print(f"Activity Counter: {activity_counter}")

        # Get the 30 most active members, excluding bots
        active_members = [member for member, _ in activity_counter.most_common(30) if not member.bot]

        # Debugging: Print active members and their counts
        print(f"Active members found: {active_members}")
        if active_members:
            for member in active_members:
                print(f"{member.name}: {activity_counter[member]} messages")
        else:
            print("No active members found")

        if not active_members:
            print(f"No active members found in {guild.name}")
            continue

        selected_member = random.choice(active_members)
        random_message = random.choice(MESSAGES)

        # Send the message to the general chat
        await general_channel.send(f"Skiller Bot Says: {selected_member.mention}, {random_message}")


# Simple ping command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Test command to see current activity count
@bot.command()
async def test(ctx):
    # Create a readable string for activity count
    activity_report = "\n".join([f"{member.name}: {count} messages" for member, count in activity_counter.items()])
    if activity_report:
        await ctx.send(f"Current activity count:\n{activity_report}")
    else:
        await ctx.send("No activity recorded yet.")



# Run the bot with the loaded token
bot.run(TOKEN)


