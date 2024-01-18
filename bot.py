# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!stocko "),
            case_insensitive=True,
            intents=discord.Intents.all()
        )
    async def on_ready(self):
        await client.wait_until_ready()
        await self.setup_hook()

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                name = filename[:-3]
                client.load_extension(f"cogs.{name}")
        
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound): 
            await ctx.send("Unknown command, please type !stocko help for a list of commands.")
            
client = Client()
client.run(TOKEN)