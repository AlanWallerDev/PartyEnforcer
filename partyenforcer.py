import os
from twitchio.ext import commands
import logging
import csv
import re

# Path to your data file
DATA_FILE_PATH = 'user_counts.csv'

class Bot(commands.Bot):
    
    def __init__(self):
    
        tokenID = 'oauth:kxisfn4wd520zb9siqomwa4f35jvo4'
        client = 'wnjvgeheymrrbq332w87h3mel4s99o'
        bot_n = 'PartyEnforcer'
        pref='!'
        chan = ['mrzancar', 'rath_bone']
        
        super().__init__(token=tokenID, client_id=client, nick=bot_n, prefix=pref, initial_channels=chan)
        self.user_counts = self.load_user_counts()

    def load_user_counts(self):
        """Load user counts from a file into a dictionary."""
        try:
            with open(DATA_FILE_PATH, mode='r', newline='') as file:
                reader = csv.reader(file)
                return {rows[0]: int(rows[1]) for rows in reader}
        except FileNotFoundError:
            return {}  # Return an empty dictionary if the file doesn't exist

    def save_user_counts(self):
        """Save the current user counts back to the file."""
        with open(DATA_FILE_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            for user, count in self.user_counts.items():
                writer.writerow([user, count])

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

 



    @commands.command(name='wall')
    async def wall_command(self, ctx, *, username: str = None):
        # Check if the user is a moderator or the broadcaster
        if ctx.author.is_mod or ctx.author.name.lower() == ctx.channel.name.lower():
            if username:
                # Remove leading @ from username if present
                username = username.lstrip('@')
                
                # Validate the cleaned username
                if re.match("^[a-zA-Z0-9_]{4,25}$", username):
                    # Update the user count
                    self.user_counts[username] = self.user_counts.get(username, 0) + 1

                    # Save the updated counts to the file
                    self.save_user_counts()

                    # Inform that the count was updated
                    await ctx.send(f"{username} Gets the wall! They have gotten the wall {self.user_counts[username]} times.")
           

            

    @commands.command(name='wallstats')
    async def wall_stats_command(self, ctx, *, username: str = None):
        # If a username is provided, check stats for that user; otherwise, for the command issuer
        target_user = username if username else ctx.author.name

        # Check if the user's stats exist
        user_count = self.user_counts.get(target_user, 0)

        # Respond with the user's wall stats
        if username:
            await ctx.send(f"{target_user} has gotten the wall {user_count} times.")
        else:
            await ctx.send(f"{ctx.author.name}, you have gotten the wall {user_count} times.")


if __name__ == "__main__":
    try:
        bot = Bot()
        bot.run()
    except Exception as e:
        logging.error("An error occurred", exc_info=True)

        
 