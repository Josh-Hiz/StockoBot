#import os
import os

#discord import 
import discord
from discord.ext import commands

#import dotenv 
from dotenv import load_dotenv

#import data science tools
from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import kaleido
import plotly.express as px
import requests

#Time tooling
from datetime import datetime
from requests import *
import json


months = ['January','Febuary','March',
          'April','May','June','July',
          'August', 'September', 'October',
          'November','December']

yf.pdr_override()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NEWS_TOKEN = os.getenv('NEWS_API_TOKEN')
ALPACA_TOKEN = os.getenv('ALPACA_TOKEN')
ALPACA_SECRET = os.getenv('ALPACA_SECRET')


clientIntents = discord.Intents.all()

helpCommand = commands.DefaultHelpCommand(no_category='Avaliable Commands')

client = commands.Bot(command_prefix='!stocko ', intents=clientIntents,help_command=helpCommand)

@client.event
async def on_ready():
    await client.wait_until_ready()
    for guild in client.guilds:
            if guild.name == GUILD:
                break    
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

def get_data(stock, start_date, end_date):
    df = pdr.get_data_yahoo(stock, start = start_date, end = end_date)
    return df

def convert_timestamp(date_time):
    ALLOWED_STRING_FORMATS = ["%Y/%m/%d-%H:%M:%S", "%Y/%m/%d"]
    for format in ALLOWED_STRING_FORMATS:
        try:
            d = datetime.strptime(date_time, format)
            return d
        except ValueError:
            pass

def validate_time(left_time_point, right_time_point):
    if(left_time_point > right_time_point or right_time_point > datetime.today() or left_time_point > datetime.today()):
        return False
    else: 
        return True

@client.command(name='Graph-Performance',help='Returns a chart of stock performance over a time interval')
async def performance_graph(ctx, 
                     date1=commands.parameter(description="Date in %Y/%m/%d-%H:%M:%S or %Y/%m/%d"), 
                     date2=commands.parameter(description="Date in %Y/%m/%d-%H:%M:%S or %Y/%m/%d"), 
                     stock=commands.parameter(description="Stock ticker, AAPL, GOOGL, etc"), 
                     chart_type=commands.parameter(description="Line, Candle, Renko, Point-Figure, OHLC"),
                     mav_set=commands.parameter(default=10,description="Moving average setting 2-20")):
    
    if(stock == None or chart_type == None):
        await ctx.send("ERROR: Cannot have stock=Nonetype or chart_type=Nonetype please type !stocko help Graph-Performance to see a list of chart types")
        raise discord.DiscordException("ERROR: Cannot have null stock or chart_type, please type !stocko help Graph-Performance to see a list of chart types")
    
    if(date2 == "Present"): 
        right_time_point = datetime.today()
        left_time_point = convert_timestamp(date1)
    else:
        try:
            right_time_point = convert_timestamp(date2)
            left_time_point = convert_timestamp(date1)
        except ValueError:
            await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d")
            raise discord.DiscordException("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d")
    
    if validate_time(left_time_point, right_time_point):
        await ctx.send(f'Years selected: {left_time_point.year}-{right_time_point.year}, stock selected: {stock}, first time point: {left_time_point}, second time point: {right_time_point}')
            
        data = get_data(stock, left_time_point, right_time_point)
        
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
    
@client.command(name="Graph-MACD",help="Returns the full MACD of a given stock including S&P500")
async def chart_macd(ctx,date1,date2,stock):
    if(stock == None):
        await ctx.send("ERROR: Cannot have stock=Nonetype")
        raise discord.DiscordException("ERROR: Cannot have stock=Nonetype")
    
    if(date2 == "Present"): 
        right_time_point = datetime.today()
        left_time_point = convert_timestamp(date1)
    else:
        try:
            right_time_point = convert_timestamp(date2)
            left_time_point = convert_timestamp(date1)
        except ValueError:
            await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d")
            raise discord.DiscordException("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d")
    
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

@client.command(name="Graph-Volatility",help='Showcases historical volatility or provides volatility prediction using GARCH')
async def chart_volatility(ctx, 
                           date1=commands.parameter(description="Date in %Y/%m/%d-%H:%M:%S or %Y/%m/%d"), 
                           date2=commands.parameter(description="Date in %Y/%m/%d-%H:%M:%S or %Y/%m/%d"), 
                           option=commands.parameter(description="Either Historical or Predict"), 
                           chart_type=commands.parameter(description="Historical use Line or Histogram, for Predict use GARCH"), 
                           stock=commands.parameter(description="Stock ticker, AAPL, GOOGL, etc")):
    
    if(stock == None or option == None):
        await ctx.send("ERROR: Cannot have stock or option = Nonetype")
        raise discord.DiscordException("ERROR: Cannot have stock or option = Nonetype")
    
    if(date2 == "Present"): 
        right_time_point = datetime.today()
        left_time_point = convert_timestamp(date1)
    else:
        try:
            right_time_point = convert_timestamp(date2)
            left_time_point = convert_timestamp(date1)
        except ValueError:
            await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d")
            raise discord.DiscordException("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d")
        
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
                        trace = px.line(vol,title="Historical volatility over a rolling window")
                        trace.write_image("output.png")
                    case 'Histogram':
                        trace = px.histogram(log_returns,title=f"{stock} Annualized Volatility: {str(round(annualized_vol,1))}")
                        trace.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)
                        trace.write_image("output.png")
            case "Predict":
                match chart_type:
                    # Predict will only have Line for GARCH model
                    case 'GARCH':
                        trace = px.line(log_returns * 100,title="Volatility with prediction")
                        trace.update_layout(yaxis_title="Frequency")
                        trace.write_image("output.png")

        file = discord.File("output.png", filename="output.png")
        embed = discord.Embed(colour=0xFF8300,title=f"Stock Volatility {chart_type} Plot")
        embed.set_image(url="attachment://output.png")
        await ctx.send(embed=embed, file=file)
        
        os.remove("output.png")
    else:
        await ctx.send("ERROR: Cannot have the first time point greater than the second time point OR any time thats greater than today")
        raise discord.DiscordException("ERROR: Cannot have the first time point greater than the second time point")

@client.command(name="Graph-Ratio",help='Showcases the specific ratio of a stock')
async def chart_volatility(ctx, date1, date2, option, stock):
    
    if(stock == None):
        await ctx.send("ERROR: Cannot have stock=Nonetype")
        raise discord.DiscordException("ERROR: Cannot have stock=Nonetype")
    
    if(date2 == "Present"): 
        right_time_point = datetime.today()
        left_time_point = convert_timestamp(date1)
    else:
        try:
            right_time_point = convert_timestamp(date2)
            left_time_point = convert_timestamp(date1)
        except ValueError:
            await ctx.send("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d")
            raise discord.DiscordException("ERROR: Invalid format, please use %Y/%m/%d-%H:%M:%S or %Y/%m/%d")
        
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
                trace = px.line(sharpe_ratio)
                trace.write_image("output.png")
            case "Sortino-Ratio":
                sortino_vol = log_returns[log_returns<0].rolling(window=TRADING_DAYS, center=True,min_periods=10).std() * np.sqrt(TRADING_DAYS)
                s_ratio = (log_returns.rolling(window=TRADING_DAYS).mean() - Rf)*TRADING_DAYS/sortino_vol
                trace = px.line(s_ratio.dropna())
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

def parse_json(data):
    '''Parse should grab: regularMarketDayRange, regularMarketDayHigh, regularMarketDayLow, regularMarketVolume'''
    data = data['quoteResponse']
    results=data['result']
    parsed_data = {}
    for entry in results:
        for k,v in entry.items():
            if k == 'regularMarketDayRange' or k == 'regularMarketDayHigh' or k == 'regularMarketDayLow' or k == 'regularMarketVolume':
                parsed_data[k] = v
            else: pass
    return parsed_data
    
        
@client.command(name='RealTime', help='Shows realtime statistics of a specified stock')
async def stock_realtime(ctx, symbol:str):
    url = f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}'
    count = 0
    
    response = requests.get(url,headers={'User-agent': 'Mozilla/5.0'})
    data = json.loads(response.text)
    pj = parse_json(data)
        
client.run(TOKEN)