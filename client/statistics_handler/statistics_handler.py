import pandas as pd
import matplotlib.pyplot as plt
from .Statistics.Indicators import IndicatorsTA
from ..date_handler.date_verify import verify_range, validate_time
import yfinance as yf
import mplfinance as mpf
import discord
import os
from pandas_datareader import data as pdr
import numpy as np
import plotly.express as px

months = ['January','Febuary','March',
          'April','May','June','July', 
          'August', 'September', 'October',
          'November','December']

# Override pdr and set cache location
yf.pdr_override()
yf.set_tz_cache_location("client/statistics_handler/")

def get_data(stock:str, start_date:str, end_date:str) -> pd.DataFrame:
    """Global function to generate a data frame using Pandas Data Reader for Yahoo

    Args:
        stock (str): Stock ticker symbol that can be found on https://finance.yahoo.com/
        start_date (str): Left time point to be used for data scrape
        end_date (str): Right time point to be used for data scrape

    Returns:
        pd.DataFrame: Dataframe containing the OHLC Adjusted Close and Volume of a stock
    """
    return pdr.get_data_yahoo(stock, start = start_date, end = end_date)

class StatisticsHandler:

    def __init__(self, bot):
        self.bot = bot
        
    async def graph_performance(self, ctx:None, date1:str, date2:str, stock:str, chart_type:int="Line", mav_set:int=10) -> None:
        """Graphs the overall performance of a given stock as well as the MAV line as a compliment

        Args:
            ctx (None): Discord Context
            date1 (str): Left time point to be used for data scrape
            date2 (str): Right time point to be used for data scrape
            stock (str): Stock ticker symbol that can be found on https://finance.yahoo.com/
            chart_type (int, optional): What type of chart you want: Line, Candle, Renko, Point-Figure, OHLC. Defaults to "Line".
            mav_set (int, optional): Value to use for MAV line. Defaults to 10.
        """
        if stock == None:
            await ctx.send("ERROR: Cannot have stock=Nonetype")
        else:
            try:
                left_time_point,right_time_point = verify_range(date1, date2)
            except ValueError:
                await ctx.send("ERROR: Invalid format, please use '%Y/%m/%d-%H:%M:%S' or '%Y/%m/%d' for the left time point")
            
            if validate_time(left_time_point, right_time_point):
                await ctx.send(f'Years selected: {left_time_point.year}-{right_time_point.year}, stock selected: {stock}, first time point: {left_time_point}, second time point: {right_time_point}')
                    
                data = get_data(stock, left_time_point, right_time_point)
                
                plt.clf()
                
                colors = mpf.make_marketcolors(up="#00ff00",down="#ff0000",wick="inherit",edge="inherit",volume="white",ohlc='orange')
                
                mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors = colors,mavcolors=['#ff00ff'])
                
                match chart_type:
                    case 'Line':
                        mpf.plot(data,mav=mav_set,volume=True,type='line',style=mpf_style,title=f'\nStock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png')
                    case 'Candle':
                        mpf.plot(data,mav=mav_set,volume=True,type='candle',style=mpf_style,title=f'\nStock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png')
                    case 'Renko':
                        mpf.plot(data,mav=mav_set,volume=True,type='renko',style=mpf_style,title=f'\nStock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png',renko_params=dict(brick_size='atr',atr_length=2))
                    case 'Point-Figure':
                        mpf.plot(data,volume=True,type='pnf',style=mpf_style,title=f'\nStock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png',pnf_params=dict(box_size='atr',atr_length=2))
                    case 'OHLC':
                        mpf.plot(data,mav=mav_set,volume=True,type='ohlc',style=mpf_style,title=f'\nStock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png')
                
                file = discord.File("output.png", filename="output.png")
                embed = discord.Embed(colour=0xFF8300,title=f"Stock {chart_type} Performance Plot")
                embed.set_image(url="attachment://output.png")
                await ctx.send(embed=embed, file=file)
                os.remove("output.png")
            else:
                await ctx.send("ERROR: Cannot have the first time point greater than the second time point OR any time thats greater than today")

    async def chart_macd(self, ctx:None,date1:str,date2:str,stock:str,slow:int=12,fast:int=26,signal:int=9) -> None:
        """Plots the MACD(slow,fast,signal) for a given stock, the default is MACD(12,26,9)

        Args:
            ctx (None): Discord Context
            date1 (str): Left time point to be used for data scrape
            date2 (str): Right time point to be used for data scrape
            stock (str): Stock ticker symbol that can be found on https://finance.yahoo.com/
            slow (int, optional): Value for slow EMA. Defaults to 12.
            fast (int, optional): Value for fast EMA. Defaults to 26.
            signal (int, optional): Value for signal EMA. Defaults to 9.
        """
        if stock == None:
            await ctx.send("ERROR: Cannot have stock=Nonetype")
        else:        
            try:
                left_time_point,right_time_point = verify_range(date1,date2)
            except ValueError:
                await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d for the left time point")
            
            if validate_time(left_time_point, right_time_point):
                await ctx.send(f'Years selected: {left_time_point.year}-{right_time_point.year}, stock selected: {stock}, first time point: {left_time_point}, second time point: {right_time_point}')
                    
                data = get_data(stock, left_time_point, right_time_point)
                exp12 = data['Close'].ewm(span=slow, adjust=False).mean()
                exp26 = data['Close'].ewm(span=fast, adjust=False).mean()
                
                macd = exp12 - exp26
                
                signal = macd.ewm(span=signal, adjust=False).mean()
                histogram = macd - signal
                
                apds = [mpf.make_addplot(exp12,color='lime'),
                    mpf.make_addplot(exp26,color='c'),
                    mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,color='dimgray',alpha=1,secondary_y=False),
                    mpf.make_addplot(macd,panel=1,color='fuchsia',secondary_y=True),
                    mpf.make_addplot(signal,panel=1,color='b',secondary_y=True),
                ]

                mpf.plot(data,type='candle',addplot=apds,figscale=1.1,figratio=(8,5),title=f'\nMACD of {stock}',
                    style='blueskies',volume=True,volume_panel=2,panel_ratios=(6,3,2),savefig='output.png')

                file = discord.File("output.png", filename="output.png")
                embed = discord.Embed(colour=0xFF8300,title=f"{stock} MACD Plot")
                embed.set_image(url="attachment://output.png")
                await ctx.send(embed=embed, file=file)
                os.remove("output.png")
            else:
                await ctx.send("ERROR: Cannot have the first time point greater than the second time point OR any time thats greater than today")

    async def chart_volatility(self, ctx:None,date1:str,date2:str,stock:str,chart_type:str ='Line',trading_days:int=60) -> None:
        """Graphs the historical volatility of a stock as well as its histogram with annualized historical volatility

        Args:
            ctx (None): Discord context
            date1 (str): Left time point to be used for data scrape
            date2 (str): Right time point to be used for data scrape
            stock (str): Stock ticker symbol that can be found on https://finance.yahoo.com/
            chart_type (str, optional): Graphing option, either Line or Histogram. Defaults to 'Line'.
            trading_days (int, optional): Number of trading days to be used in rolling window. Defaults to 60.
        """
        if stock == None:
            await ctx.send("ERROR: Cannot have stock or option = Nonetype")
        else:        
            try:
                left_time_point,right_time_point = verify_range(date1,date2)
            except ValueError:
                await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d for the left time point")
                
            if validate_time(left_time_point, right_time_point):
                await ctx.send(f'Years selected: {left_time_point.year}-{right_time_point.year}, stock selected: {stock}, first time point: {left_time_point}, second time point: {right_time_point}')
            
                data = get_data(stock, left_time_point, right_time_point)
                log_returns = np.log(data.Close/data.Close.shift(1)).dropna()
                daily_std = log_returns.std()
                annualized_vol = daily_std*np.sqrt(252) * 100
                match chart_type:
                    case 'Line':
                        vol = log_returns.rolling(window=trading_days).std() * np.sqrt(trading_days)
                        trace = px.line(vol,title=f"Historical volatility over a {trading_days}-day rolling window",template='plotly_dark',width=600,height=400)
                        trace.write_image("output.png")
                    case 'Histogram':
                        trace = px.histogram(log_returns,title=f"{stock} Annualized Volatility: {str(np.round(annualized_vol,1))}",template='plotly_dark')
                        trace.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)
                        trace.write_image("output.png")
                file = discord.File("output.png", filename="output.png")
                embed = discord.Embed(colour=0xFF8300,title=f"Stock Volatility {chart_type} Plot")
                embed.set_image(url="attachment://output.png")
                await ctx.send(embed=embed, file=file)
                
                os.remove("output.png")
            else:
                await ctx.send("ERROR: Cannot have the first time point greater than the second time point OR any time thats greater than today")

    async def chart_ratio(self, ctx:None, date1 : str, date2 : str,stock : str,option : str ="Sharpe",trading_days:int=60) -> None:
        """Graphs the Risk-Return ratio for a given stock, currently the only ones supported are Sharpe and Sortino

        Args:
            ctx (None): Discord context
            date1 (str): Left time point to be used for data scrape
            date2 (str): Right time point to be used for data scrape
            stock (str): Stock ticker symbol that can be found on https://finance.yahoo.com/
            option (str, optional): What ratio you want to view, either Sharpe or Sortino for now. Defaults to "Sharpe".
            trading_days (int, optional): Number of trading days to be used in rolling window. Defaults to 60.
        """
        if stock == None:
            await ctx.send("ERROR: Cannot have stock=Nonetype")
        else:        
            try:
                left_time_point,right_time_point = verify_range(date1,date2)
            except ValueError:
                await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d for the left time point")
                
            if validate_time(left_time_point, right_time_point):
                await ctx.send(f'Years selected: {left_time_point.year}-{right_time_point.year}, stock selected: {stock}, first time point: {left_time_point}, second time point: {right_time_point}')

                data = get_data(stock, left_time_point, right_time_point)
                log_returns = np.log(data.Close/data.Close.shift(1)).dropna()
                Rf = 0.01/252
                vol = log_returns.rolling(window=trading_days).std() * np.sqrt(trading_days)
                
                match option:
                    case "Sharpe":
                        sharpe_ratio = (log_returns.rolling(window=trading_days).mean() - Rf)*trading_days/vol
                        trace = px.line(sharpe_ratio,template='plotly_dark')
                        trace.write_image("output.png")
                    case "Sortino":
                        sortino_vol = log_returns[log_returns<0].rolling(window=trading_days, center=True,min_periods=10).std() * np.sqrt(trading_days)
                        sortino_ratio = (log_returns.rolling(window=trading_days).mean() - Rf)*trading_days/sortino_vol
                        trace = px.line(sortino_ratio.dropna(),template='plotly_dark')
                        trace.write_image("output.png")
                    
                
                file = discord.File("output.png", filename="output.png")
                embed = discord.Embed(colour=0xFF8300,title=f"Stock {option} Plot")
                embed.set_image(url="attachment://output.png")
                await ctx.send(embed=embed, file=file)
                os.remove("output.png")
            else:
                await ctx.send("ERROR: Cannot have the first time point greater than the second time point OR any time thats greater than today")
    
    async def graph_indicators(self,ctx:None,left_time_point:str,right_time_point:str,stock:str) -> None:
        """Graphs the RSI, Bollinger Bands, and VWAP of a given stock in one graph

        Args:
            ctx (None): Discord Context
            left_time_point (str): Left time point to be used for data scrape
            right_time_point (str): Right time point to be used for data scrape
            stock (str): Stock ticker symbol that can be found on https://finance.yahoo.com/

        Raises:
            discord.DiscordException: Raises a discord exception if a stock was not given
        """
        if stock == None:
            await ctx.send("ERROR: Cannot have stock=Nonetype")
        else:
            indicator = IndicatorsTA(stock,left_time_point,right_time_point)
            indicator.plotIndicators()
            file = discord.File("output.png", filename="output.png")
            embed = discord.Embed(colour=0xFF8300,title=f"Stock RSI, BBands, and VWAP for {stock} Plot")
            embed.set_image(url="attachment://output.png")
            await ctx.send(embed=embed, file=file)