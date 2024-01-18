# statistics_handler.py
import matplotlib.pyplot as plt
from date_handler.date_verify import verify_range, validate_time
from .Statistics.Indicators import IndicatorsTA
import yfinance as yf
import mplfinance as mpf
import discord
import os
from pandas_datareader import data as pdr
import numpy as np
import plotly.express as px

# Months list
months = ['January','Febuary','March',
          'April','May','June','July', 
          'August', 'September', 'October',
          'November','December']

yf.pdr_override()

def get_data(stock, start_date, end_date):
    df = pdr.get_data_yahoo(stock, start = start_date, end = end_date)
    return df

class StatisticsHandler:

    def __init__(self, bot):
        self.bot = bot
        
    async def graph_performance(self, ctx, date1, date2, stock, chart_type="Line", mav_set=10):
        try:
            ranges = verify_range(date1, date2)
            left_time_point = ranges[0]
            right_time_point = ranges[1]
        except ValueError:
            await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d for the left time point")
        
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
            raise discord.DiscordException("ERROR: Cannot have the first time point greater than the second time point")

    async def chart_macd(self, ctx,date1,date2,stock):
        if(stock == None):
            await ctx.send("ERROR: Cannot have stock=Nonetype")
            raise discord.DiscordException("ERROR: Cannot have stock=Nonetype")
        
        try:
            ranges = verify_range(date1,date2)
            left_time_point = ranges[0]
            right_time_point = ranges[1]
        except ValueError:
            await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d for the left time point")
        
        if validate_time(left_time_point, right_time_point):
            await ctx.send(f'Years selected: {left_time_point.year}-{right_time_point.year}, stock selected: {stock}, first time point: {left_time_point}, second time point: {right_time_point}')
                
            data = get_data(stock, left_time_point, right_time_point)
            exp12 = data['Close'].ewm(span=12, adjust=False).mean()
            exp26 = data['Close'].ewm(span=26, adjust=False).mean()
            
            macd = exp12 - exp26
            
            signal = macd.ewm(span=9, adjust=False).mean()
            histogram = macd - signal
            
            apds = [mpf.make_addplot(exp12,color='lime'),
                mpf.make_addplot(exp26,color='c'),
                mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,
                color='dimgray',alpha=1,secondary_y=False),
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
            raise discord.DiscordException("ERROR: Cannot have the first time point greater than the second time point")

    async def chart_volatility(self, ctx,date1,date2,stock,option='Historical',chart_type='Line'):
        if(stock == None):
            await ctx.send("ERROR: Cannot have stock or option = Nonetype")
            raise discord.DiscordException("ERROR: Cannot have stock or option = Nonetype")
        
        try:
            ranges = verify_range(date1,date2)
            left_time_point = ranges[0]
            right_time_point = ranges[1]
        except ValueError:
            await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d for the left time point")
            
        if validate_time(left_time_point, right_time_point):
            await ctx.send(f'Years selected: {left_time_point.year}-{right_time_point.year}, stock selected: {stock}, first time point: {left_time_point}, second time point: {right_time_point}')
            data = get_data(stock, left_time_point, right_time_point)
            log_returns = np.log(data.Close/data.Close.shift(1)).dropna()
            daily_std = log_returns.std()
            annualized_vol = daily_std*np.sqrt(252) * 100
            match option:
                case "Historical":
                    match chart_type:
                        case 'Line':
                            TRADING_DAYS = 60
                            vol = log_returns.rolling(window=TRADING_DAYS).std() * np.sqrt(TRADING_DAYS)
                            trace = px.line(vol,title="Historical volatility over a rolling window",template='plotly_dark',width=600,height=400)
                            trace.write_image("output.png")
                        case 'Histogram':
                            trace = px.histogram(log_returns,title=f"{stock} Annualized Volatility: {str(round(annualized_vol,1))}",template='plotly_dark')
                            trace.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)
                            trace.write_image("output.png")
                case "Predict":
                    match chart_type:
                        # Predict will only have Line for GARCH model
                        case 'GARCH':
                            trace = px.line(log_returns * 100,title="Daily Returns over time",template='plotly_dark',width=800,height=400)
                            trace.write_image("output.png")

            file = discord.File("output.png", filename="output.png")
            embed = discord.Embed(colour=0xFF8300,title=f"Stock Volatility {chart_type} Plot")
            embed.set_image(url="attachment://output.png")
            await ctx.send(embed=embed, file=file)
            
            os.remove("output.png")
        else:
            await ctx.send("ERROR: Cannot have the first time point greater than the second time point OR any time thats greater than today")
            raise discord.DiscordException("ERROR: Cannot have the first time point greater than the second time point")

    async def chart_ratio(self, ctx, date1, date2,stock,option="Sharpe-Ratio"):
        if(stock == None):
            await ctx.send("ERROR: Cannot have stock=Nonetype")
            raise discord.DiscordException("ERROR: Cannot have stock=Nonetype")
        
        try:
            ranges = verify_range(date1,date2)
            left_time_point = ranges[0]
            right_time_point = ranges[1]
        except ValueError:
            await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d for the left time point")
            
        if validate_time(left_time_point, right_time_point):
            await ctx.send(f'Years selected: {left_time_point.year}-{right_time_point.year}, stock selected: {stock}, first time point: {left_time_point}, second time point: {right_time_point}')

            data = get_data(stock, left_time_point, right_time_point)
            log_returns = np.log(data.Close/data.Close.shift(1)).dropna()
            TRADING_DAYS = 60
            Rf = 0.01/252
            vol = log_returns.rolling(window=TRADING_DAYS).std() * np.sqrt(TRADING_DAYS)
            
            match option:
                case "Sharpe-Ratio":
                    sharpe_ratio = (log_returns.rolling(window=TRADING_DAYS).mean() - Rf)*TRADING_DAYS/vol
                    trace = px.line(sharpe_ratio,template='plotly_dark')
                    trace.write_image("output.png")
                case "Sortino-Ratio":
                    sortino_vol = log_returns[log_returns<0].rolling(window=TRADING_DAYS, center=True,min_periods=10).std() * np.sqrt(TRADING_DAYS)
                    s_ratio = (log_returns.rolling(window=TRADING_DAYS).mean() - Rf)*TRADING_DAYS/sortino_vol
                    trace = px.line(s_ratio.dropna(),template='plotly_dark')
                    trace.write_image("output.png")
            
            file = discord.File("output.png", filename="output.png")
            embed = discord.Embed(colour=0xFF8300,title=f"Stock {option} Plot")
            embed.set_image(url="attachment://output.png")
            await ctx.send(embed=embed, file=file)
            
            os.remove("output.png")
        else:
            await ctx.send("ERROR: Cannot have the first time point greater than the second time point OR any time thats greater than today")
            raise discord.DiscordException("ERROR: Cannot have the first time point greater than the second time point")
    
    async def graph_indicators(self,ctx,left_time_point,right_time_point,stock):
        if(stock == None):
            await ctx.send("ERROR: Cannot have stock=Nonetype")
            raise discord.DiscordException("ERROR: Cannot have stock=Nonetype")
        
        indicator = IndicatorsTA(stock,left_time_point,right_time_point)
        indicator.plotIndicators()
        file = discord.File("output.png", filename="output.png")
        embed = discord.Embed(colour=0xFF8300,title=f"Stock RSI, BBands, and VWAP for {stock} Plot")
        embed.set_image(url="attachment://output.png")
        await ctx.send(embed=embed, file=file)