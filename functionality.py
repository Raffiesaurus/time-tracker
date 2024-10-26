from datetime import datetime
import pytz
import discord
import json
from collections import OrderedDict
from tabulate import tabulate

server_data = {}

# File path for saving the data
DATA_FILE = "server_data.json"

# Save data to JSON file
def save_data():
    with open(DATA_FILE, "w") as file:
        # Convert OrderedDict to regular dictionary to save in JSON format
        json.dump(server_data, file, default=dict)
        
# Load data from JSON file
def load_data():
    global server_data
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            # Reconvert to OrderedDict to preserve the order when loading
            server_data = {
                int(guild_id): OrderedDict(users)
                for guild_id, users in data.items()
            }
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is corrupted, start with an empty dictionary
        server_data = {}

# Modify set_timezone to store per-server data
async def set_timezone(author: discord.User, guild_id: int, timezone: str, country: str) -> str:
    """Sets the user's timezone and country, specific to their server (guild)."""

    if not country:
        return f"{author.mention}, invalid country! Please mention a country or city after the timezone."
    
    if timezone in pytz.all_timezones:
        # Initialize server data if it doesn't exist
        if guild_id not in server_data:
            server_data[guild_id] = OrderedDict()
            save_data()
        
        # Store user data within the specific server context
        if guild_id in server_data and server_data[guild_id] and author.id in server_data[guild_id]:
            # Update the existing user's timezone and country
            server_data[guild_id][f'{author.id}']["timezone"] = timezone
            server_data[guild_id][f'{author.id}']["country"] = country
            server_data[guild_id][f'{author.id}']["set_at"] = datetime.now().isoformat()  # Update timestamp
            save_data()
            return f"{author.mention}, your timezone has been updated to {timezone} ({country})."
        else:
            # Store user data within the specific server context
            server_data[guild_id][author.id] = {
                "name": author.display_name,
                "timezone": timezone,
                "country": country,
                "set_at": datetime.now().isoformat()  # Use ISO format to store in JSON
            }
            save_data()
            return f"{author.mention}, your timezone has been set to {timezone} ({country})."

    else:
        return f"{author.mention}, invalid timezone! Please refer to a list of IANA time zones."

async def list_users(guild_id: int, num_entries: int) -> str:
    """Displays the last `num_entries` added users for the specific server."""

    # Check if the server has data
    if guild_id not in server_data or not server_data[guild_id]:
        return "No timezones have been set yet in this server."

    # Get the last `num_entries` items from the specific server's data
    recent_entries = list(server_data[guild_id].values())[-num_entries:]
    
    # Prepare data for tabulate
    table_data = []
    for data in recent_entries:
        user_timezone = pytz.timezone(data["timezone"])
        current_time = datetime.now(user_timezone).strftime("%I:%M %p")
        current_date = datetime.now(user_timezone).strftime("%d/%m")
        
        # Add row to table data
        table_data.append([
            data["name"][:10],  # Limit name to 15 characters if desired
            data["timezone"][:10],  # Limit timezone to 15 characters if desired
            current_time,
            current_date
        ])

    # Format the table with a fancy grid
    table = tabulate(
        table_data,
        headers=["User", "Timezone", "Current Time", "Date"],
        tablefmt="fancy_grid"
    )

    return f"```\n{table}\n```"


# Command to get a user's current time, timezone, and country
async def check_time(author: discord.User, guild_id: int) -> str:
    """Fetches the time of the mentioned user."""
    
    # Check if guild and user data exist in server_data
    if guild_id in server_data and server_data[guild_id] and server_data[guild_id][f'{author.id}']:
        user_data = server_data[guild_id][f'{author.id}']

        timezone = user_data.get("timezone")
        country = user_data.get("country")
        
        # Convert the timezone and fetch current time
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz).strftime("%I:%M %p")
            current_date = datetime.now(tz).strftime("%d/%m")
        except Exception as e:
            print(f"Error with timezone {timezone}: {e}")
            return f"{author.mention}, there was an error retrieving your timezone. Please re-enter it."

        # Format and return the response
        return (
            f"**Current Time for {author.mention}:**\n"
            f"```Timezone: {timezone} ({country})\n"
            f"Date: {current_date}\n"
            f"Time: {current_time}```"
        )

    else:
        # Notify user if timezone is not set
        return (
            f"{author.mention} has not set a timezone. They can set it using the command `!setTZ <timezone> <country>`."
        )


# Help command to display usage instructions
async def help_command() -> str:
    """Provides instructions for using the bot."""
    timezone_link = "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
    return (
        "**Bot Commands:**\n"
        "`!setTZ <timezone> <country>` - Set your timezone. Use an IANA time zone code like `Europe/London` or `America/New_York`.\n"
        "`Example: !setTZ Europe/London Scotland`\n"
        "`!time @user` - Get the current time of the mentioned user.\n"
        "`!list <number>` - Get the last <number> of people times added.\n"
        f"**Time Zone List:** For a full list of IANA time zones, visit [this link]({timezone_link})."
    )


# Processing responses and commands
async def process_response(client: discord.Client,
                           message: discord.Message) -> None:
    if message.author == client.user:
        return

    load_data()
    if message.content.startswith('!setTZ'):
        try:
            contents = message.content.split('!setTZ ')[1]
            contentTZ, contentCountry = contents.split(' ')
            await message.channel.send(await
                                       set_timezone(message.author, message.guild.id,contentTZ,
                                                    contentCountry))
        except ValueError:
            await message.channel.send(
                "Please use the correct format: `!setTZ <timezone> <country>`")

    elif message.content.startswith('!time'):
        if message.mentions:
            user = message.mentions[0]
            await message.channel.send(await check_time(user,  message.guild.id))
        else:
            await message.channel.send(
                "Please mention a user to get their current time.")

    elif message.content.startswith('!help'):
        await message.channel.send(await help_command())

    elif message.content.startswith('!list'):
        try:
            num_entries = int(message.content.split('!list ')[1])
        except (IndexError, ValueError):
            num_entries = 10  # Default to 10 if no number is provided

        await message.channel.send(await list_users(message.guild.id, num_entries))