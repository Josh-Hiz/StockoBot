import yfinance as yf
yf.set_tz_cache_location("cache/")

embed_colors = [0xff5733,0x43d4e9,0xdf27f1,0xf60c54,0xf5f109,0x09f51d,
                0xffffff,0x000000,0xff8300,0xdaf7a6,0xff5733,0xc70039,
                0x581845]

class QueryHandler:
    
    def __init__(self,bot) -> None:
        self.bot = bot
        
    async def hello_world(self,ctx):
        await ctx.send("Query Client activated")