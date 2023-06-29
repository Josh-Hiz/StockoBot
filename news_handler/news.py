# Main python file for news handler module
# to be used in the main bot file 
import os
import discord
from discord.ext import commands

def parse_news(data):
    '''
    Parses news and grabs the following data:
    - Title
    - Summary
    - URL
    - Sentiment
    '''
    data["feed"] = data["feed"][:5]
    print(data)
    news_emb = discord.Embed(colour=0x338AFF)
    for i in range(len(data["feed"])):
        news_emb.add_field(name=f'{data["feed"][i]["title"]}',value=f'{data["feed"][i]["summary"]}\n[Read More]({data["feed"][i]["url"]})\nSentiment: {data["feed"][i]["overall_sentiment_label"]}',inline=False)
        
    return news_emb
