import discord, requests
import os

FINANCE_TOKEN = os.getenv('FINANCE_API_TOKEN')

class NewsHandler:
    def __init__(self,bot):
        self.bot = bot
        
    def parse_news(self, data, num_articles):
        '''
        Parses news and grabs the following data:
        - Title
        - Summary
        - URL
        - Sentiment
        '''
        data["feed"] = data["feed"][:num_articles]
        news_emb = discord.Embed(colour=0x338AFF)
        for i in range(len(data["feed"])):
            news_emb.add_field(name=f'{data["feed"][i]["title"]}',value=f'{data["feed"][i]["summary"]}\n[Read More]({data["feed"][i]["url"]})\nSentiment: {data["feed"][i]["overall_sentiment_label"]}',inline=False)
            
        return news_emb
        
    async def get_news(self,ctx, stock, topics=None, num_articles=5):
        if num_articles > 10:
            await ctx.send("ERROR: Cannot exceed 10 articles!")
        else:
            await ctx.send("The news command can do alot more than you think! Type !stocko help news for a comprehensive list of all options you can do!")
            url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock}&apikey={FINANCE_TOKEN}' if topics == None else f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={topics}&tickers={stock}&apikey={FINANCE_TOKEN}'
            r = requests.get(url)
            data = r.json()
            emb = self.parse_news(data, num_articles)
            await ctx.send(embed=emb)