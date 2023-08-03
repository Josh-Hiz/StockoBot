import discord
from bot import FINANCE_TOKEN 
from quote import parse_json
import requests
import json
import asyncio

class RealtimeHandler:
    
    def __init__(self,bot):
        self.bot = bot
        
    async def stock_realtime(self,ctx,symbol:str):
    
        colors = [0xFF8300,0xDAF7A6,0xFF5733,0xC70039,0x581845]
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={FINANCE_TOKEN}'
        count = 0
        real_embed = discord.Embed(colour=0xFF8300, title=f"{symbol} Realtime Data:")
        user_msg = await ctx.send(embed=real_embed)
        while not self.bot.is_closed():
            try:
                count+=1
                response = requests.get(url)
                data = json.loads(response.text)
                pj = parse_json(data)
                print(list(pj.values()))
                price = pj['price']
                volume = pj['volume']
                high = pj['high']
                low = pj['low']
                change = pj['change']
                change_percent = pj['change percent']
                ltd = pj['ltd']
                update_embed = discord.Embed(colour=colors[count%len(colors)],title=f"{symbol} Realtime Data:",description=f'```css\nPrice: ${price}\nVolume: {volume}\nHigh: ${high}\nLow: ${low}\nChange: {change}\nChange Percent: {change_percent}\nLatest Trading Day: {ltd}\n```')
                await user_msg.edit(embed=update_embed)
                await asyncio.sleep(15)
                if count == 25: break 
            except Exception:
                await ctx.send("ERROR: Invalid stock or Timeout!")
                raise discord.DiscordException("ERROR: Invalid stock! or Timeout!")