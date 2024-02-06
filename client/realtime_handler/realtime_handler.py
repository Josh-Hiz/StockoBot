import discord
import os 
import requests
import json
import asyncio
from quote import parse_json
from bot import FINANCE_TOKEN
class RealtimeHandler:
    
    def __init__(self,bot):
        self.bot = bot
        
    async def stock_realtime(self,ctx,symbol:str):
    
        colors = [0xff5733,0x43d4e9,0xdf27f1,0xf60c54,0xf5f109,0x09f51d,
                0xffffff,0x000000,0xff8300,0xdaf7a6,0xff5733,0xc70039,
                0x581845]
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
                break