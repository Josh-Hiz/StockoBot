# FinanceCog.py
from discord.ext import commands
from client.query_handler.query import QueryHandler
from client.statistics_handler.statistics_handler import StatisticsHandler
from client.options_handler.options_handler import OptionHandler
from client.news_handler.news_handler import NewsHandler
# from client.realtime_handler.realtime_handler import RealtimeHandler

class FinanceCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot 
        self.stat_client = StatisticsHandler(bot)
        self.option_client = OptionHandler(bot)
        self.news_client = NewsHandler(bot)
        self.data_query_client = QueryHandler(bot)
        # self.realtime_client = RealtimeHandler(bot)
    
    @commands.command(name='Graph-Performance',help='Returns a chart of stock performance over a time interval',aliases=['gp'])
    async def performance_graph(self, ctx, date1, date2, stock, chart_type="Line", mav_set=10):
        await self.stat_client.graph_performance(ctx, date1, date2, stock, chart_type, mav_set)
    
    @commands.command(name="Graph-MACD",help="Returns the full MACD of a given stock including S&P500",aliases=['gm'])
    async def chart_macd(self,ctx,date1,date2,stock):
        await self.stat_client.chart_macd(ctx,date1,date2,stock)
    
    @commands.command(name="Graph-Volatility",help='Showcases historical volatility or provides volatility prediction using GARCH',aliases=['gv'])
    async def chart_volatility(self,ctx, date1,date2,stock,chart_type="Line",trading_days=60):
        await self.stat_client.chart_volatility(ctx,date1,date2,stock,chart_type,trading_days)
        
    @commands.command(name="Graph-Ratio",help='Showcases the specific ratio of a stock',aliases=['gr'])
    async def chart_ratio(self,ctx, date1, date2,stock,option="Sharpe",trading_days=60):
        await self.stat_client.chart_ratio(ctx,date1,date2,stock,option,trading_days)

    @commands.command(name='Graph-Indicators',help='Outputs a graph of 3 technical indicators, RSI, BBands, and VWAP for a selected time range and stock',aliases=['gi'])
    async def graph_indicators(self, ctx, left_time_point, right_time_point,stock):
        await self.stat_client.graph_indicators(ctx,left_time_point,right_time_point,stock)

    @commands.command(name='Options-Chain-Call',help='Outputs the call options chain for a selected stock',aliases=['opc'])
    async def get_call(self,ctx,stock,num_rows=10):
        await self.option_client.get_call(ctx,stock,num_rows)
        
    @commands.command(name='Options-Chain-Put',help='Outputs the put options chain for a selected stock',aliases=['opp'])
    async def get_put(self,ctx,stock,num_rows=10):
        await self.option_client.get_put(ctx,stock,num_rows)

    @commands.command(name="news",
                      help='Outputs financial news based on a prompt\nTopics:\n- blockchain\n- earnings\n- ipo\n- mergers_and_acquisitions\n- financial_markets\n- economy_fiscal\n- economy_monetary\n- economy_macro\n- energy_transportation\n- finance\n- life_sciences\n- manufacturing\n- real_estate\n- retail_wholesale\n- technology\n',
                      aliases=['nw'])
    async def get_news(self,ctx, stock, topics=None, num_articles=5):
        await self.news_client.get_news(ctx, stock, topics, num_articles)
        
    # @commands.command(name='RealTime', help='Shows realtime statistics of a specified stock',aliases=['rt'])
    # async def stock_realtime(self, ctx, symbol):
    #     await self.realtime_client.stock_realtime(ctx, symbol)

    @commands.command(name="Query-Equity",help="Outputs the overall comprehensive summary of a given valid equity",aliases=["q"])
    async def get_summary(self,ctx,stock):
        await self.stat_client.stock_summary(ctx, stock)
        
def setup(bot):
    bot.add_cog(FinanceCog(bot))