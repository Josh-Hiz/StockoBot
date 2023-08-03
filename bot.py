#import os
import asyncio
import os

from Statistics.Indicators import *
from news_handler.news import parse_news
from date_handler.date_verify import verify_range, validate_time
from Statistics.Quote import parse_json

#discord imports
import discord
from discord.ext import commands

#import dotenv 
from dotenv import load_dotenv

#import data science tools and API's 
from pandas_datareader import data as pdr
import numpy as np
import dataframe_image as dfi
from pytz import timezone
import yfinance as yf
from yahoo_fin import options as op
import matplotlib.pyplot as plt
import mplfinance as mpf
import plotly.express as px

#Time and Data parsing tooling
import json
import requests

months = ['January','Febuary','March',
          'April','May','June','July', 
          'August', 'September', 'October',
          'November','December']

yf.pdr_override()

load_dotenv()

FINANCE_TOKEN = os.getenv('FINANCE_API_TOKEN')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

clientIntents = discord.Intents.all()

helpCommand = commands.DefaultHelpCommand(no_category='Avaliable Commands')

client = commands.Bot(command_prefix='!stocko ', intents=clientIntents,help_command=helpCommand)

@client.event
async def on_ready():
    await client.wait_until_ready()

def get_data(stock, start_date, end_date):
    df = pdr.get_data_yahoo(stock, start = start_date, end = end_date)
    return df

@client.command(name='Graph-Performance',help='Returns a chart of stock performance over a time interval',aliases=['gp'])
async def performance_graph(ctx, 
                     date1=commands.parameter(description="Date in %Y/%m/%d-%H:%M:%S or %Y/%m/%d"), 
                     date2=commands.parameter(description="Date in %Y/%m/%d-%H:%M:%S or %Y/%m/%d"), 
                     stock=commands.parameter(description="Stock ticker, AAPL, GOOGL, etc"), 
                     chart_type=commands.parameter(description="Line, Candle, Renko, Point-Figure, OHLC",default="Line"),
                     mav_set=commands.parameter(default=10,description="Moving average setting 2-20")):
    
    if(stock == None):
        await ctx.send("ERROR: Cannot have stock=Nonetype or chart_type=Nonetype please type !stocko help Graph-Performance to see a list of chart types")
        raise discord.DiscordException("ERROR: Cannot have null stock or chart_type, please type !stocko help Graph-Performance to see a list of chart types")
    
    try:
        ranges = verify_range(date1,date2)
        left_time_point = ranges[0]
        right_time_point = ranges[1]
    except ValueError:
        await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d for the left time point")
    
    if validate_time(left_time_point, right_time_point):
        await ctx.send(f'Years selected: {left_time_point.year}-{right_time_point.year}, stock selected: {stock}, first time point: {left_time_point}, second time point: {right_time_point}')
            
        data = get_data(stock, left_time_point, right_time_point)
        print(data)
        
        plt.clf()
        
        colors = mpf.make_marketcolors(up="#00ff00",
                                       down="#ff0000",
                                       wick="inherit",
                                       edge="inherit",
                                       volume="white",
                                       ohlc='orange')
        
        mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors = colors,mavcolors=['#ff00ff'])
        
        match chart_type:
            case 'Line':
                mpf.plot(data,mav=mav_set,volume=True,type='line',style=mpf_style,title=f'\nStock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png')
            case 'Candle':
                mpf.plot(data,mav=mav_set,volume=True,type='candle',style=mpf_style,title=f'\nStock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png')
            case 'Renko':
                mpf.plot(data,mav=mav_set,volume=True,type='renko',style=mpf_style,title=f'\nStock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png',renko_params=dict(brick_size='atr',atr_length=2))
            case 'Point-Figure':
                print(left_time_point,right_time_point)
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
    
@client.command(name="Graph-MACD",help="Returns the full MACD of a given stock including S&P500",aliases=['gm'])
async def chart_macd(ctx,date1,date2,stock):
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

@client.command(name="Graph-Volatility",help='Showcases historical volatility or provides volatility prediction using GARCH',aliases=['gv'])
async def chart_volatility(ctx, 
                           date1=commands.parameter(description="Date in %Y/%m/%d-%H:%M:%S or %Y/%m/%d"), 
                           date2=commands.parameter(description="Date in %Y/%m/%d-%H:%M:%S or %Y/%m/%d"),
                           stock=commands.parameter(description="Stock ticker, AAPL, GOOGL, etc"), 
                           option=commands.parameter(description="Either Historical or Predict",default="Historical"), 
                           chart_type=commands.parameter(description="Historical use Line or Histogram, for Predict use GARCH",default="Line")):
    
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

@client.command(name="Graph-Ratio",help='Showcases the specific ratio of a stock',aliases=['gr'])
async def chart_volatility(ctx, date1, date2,stock,option="Sharpe-Ratio"):
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
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): 
        await ctx.send("Unknown command, please type !stocko help for a list of commands.")
            
@client.command(name='RealTime', help='Shows realtime statistics of a specified stock',aliases=['rt'])
async def stock_realtime(ctx, symbol:str):
    
    colors = [0xFF8300,0xDAF7A6,0xFF5733,0xC70039,0x581845]
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={FINANCE_TOKEN}'
    count = 0
    real_embed = discord.Embed(colour=0xFF8300, title=f"{symbol} Realtime Data:")
    user_msg = await ctx.send(embed=real_embed)
    while not client.is_closed():
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
        

@client.command(name='Graph-Indicators',help='Outputs a graph of 3 technical indicators, RSI, BBands, and VWAP for a selected time range and stock',aliases=['gi'])
async def graph_indicators(ctx, 
                           left_time_point=commands.parameter(description="Date in %Y/%m/%d-%H:%M:%S or %Y/%m/%d"), 
                           right_time_point=commands.parameter(description="Date in %Y/%m/%d-%H:%M:%S or %Y/%m/%d"),
                           stock=commands.parameter(description="Stock ticker, AAPL, GOOGL, etc")):
    if(stock == None):
        await ctx.send("ERROR: Cannot have stock=Nonetype")
        raise discord.DiscordException("ERROR: Cannot have stock=Nonetype")
    
    indicator = IndicatorsTA(stock,left_time_point,right_time_point)
    indicator.plotIndicators()
    file = discord.File("output.png", filename="output.png")
    embed = discord.Embed(colour=0xFF8300,title=f"Stock RSI, BBands, and VWAP for {stock} Plot")
    embed.set_image(url="attachment://output.png")
    await ctx.send(embed=embed, file=file)
        
@client.command(name='Options-Chain-Call',help='Outputs the call options chain for a selected stock',aliases=['opc'])
async def get_call(ctx, stock:str, num_rows=10):
    if(stock == None):
        await ctx.send("ERROR: Cannot have stock=Nonetype")
        raise discord.DiscordException("ERROR: Cannot have stock=Nonetype")
    elif num_rows>20:
        await ctx.send("ERROR: Cannot exceed 20 rows!")
        raise discord.DiscordException("ERROR: Cannot exceed 20 rows!")
    else:
        expirationDates = op.get_expiration_dates(stock)
        callData = op.get_calls(stock,date=expirationDates[0])
        callData = callData.tail(num_rows)
        callData = callData.reset_index(drop=True)
        callData = callData.drop(columns=['Contract Name'])
        dfi.export(callData,'output.png',table_conversion='matplotlib',fontsize=8)
        file = discord.File("output.png", filename="output.png")
        embed = discord.Embed(colour=0xFF8300,title=f"Stock call options for {stock}")
        embed.set_image(url="attachment://output.png")
        await ctx.send(embed=embed, file=file)
        os.remove('output.png')
        
@client.command(name='Options-Chain-Put',help='Outputs the put options chain for a selected stock',aliases=['opp'])
async def get_put(ctx, stock:str,num_rows=10):
    if(stock == None):
        await ctx.send("ERROR: Cannot have stock=Nonetype")
        raise discord.DiscordException("ERROR: Cannot have stock=Nonetype")
    elif num_rows>20:
        await ctx.send("ERROR: Cannot exceed 20 rows!")
        raise discord.DiscordException("ERROR: Cannot exceed 20 rows!")
    else:
        expirationDates = op.get_expiration_dates(stock)
        putData = op.get_puts(stock,date=expirationDates[0])
        putData = putData.tail(num_rows)
        putData = putData.reset_index(drop=True)
        putData = putData.drop(columns=['Contract Name'])
        dfi.export(putData,'output.png',table_conversion='matplotlib',fontsize=8)
        file = discord.File("output.png", filename="output.png")
        embed = discord.Embed(colour=0xFF8300,title=f"Stock put options for {stock}")
        embed.set_image(url="attachment://output.png")
        await ctx.send(embed=embed, file=file)
        os.remove('output.png')
        
@client.command(name="news",help='Outputs financial news based on a prompt',alias='nw')
async def get_news(ctx, stock, topics=None, num_articles=5):
    if num_articles > 10:
        await ctx.send("ERROR: Cannot exceed 10 articles!")
    else:
        await ctx.send("The news command can do alot more than you think! Type !stocko help news for a comprehensive list of all options you can do!")
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock}&apikey={FINANCE_TOKEN}' if topics == None else f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={topics}&tickers={stock}&apikey={FINANCE_TOKEN}'
        r = requests.get(url)
        data = r.json()
        emb = parse_news(data, num_articles)
        await ctx.send(embed=emb)
    
client.run(TOKEN)