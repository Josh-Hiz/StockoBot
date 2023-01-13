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
import requests
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

#Time tooling
from datetime import datetime
from newsapi.newsapi_client import NewsApiClient
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
    ALLOWED_STRING_FORMATS = ["%Y-%m-%d-%H:%M:%S", "%Y-%m-%d"]
    for format in ALLOWED_STRING_FORMATS:
        try:
            d = datetime.strptime(date_time, format)
            return d
        except ValueError:
            pass

@client.command(name='Graph-Performance',help='Returns a chart of stock performance over a time interval')
async def graph_test(ctx, 
                     date1=commands.parameter(description="Date in %Y-%m-%d-%H:%M:%S or %Y-%m-%d"), 
                     date2=commands.parameter(description="Date in %Y-%m-%d-%H:%M:%S or %Y-%m-%d"), 
                     stock=commands.parameter(description="Stock ticker, AAPL, GOOGL, etc"), 
                     chart_type=commands.parameter(description="Line, Candle, Renko, Point-Figure, OHLC")):
    
    if(date2 == "Present"): 
        right_time_point = datetime.today()
        left_time_point = convert_timestamp(date1)
    else:
        try:
            right_time_point = convert_timestamp(date2)
            left_time_point = convert_timestamp(date1)
        except ValueError:
            await ctx.send("ERROR: Invalid format, please use %Y-%m-%d-%H:%M:%S or %Y-%m-%d")
            raise discord.DiscordException("ERROR: Invalid format, please use %Y-%m-%d-%H:%M:%S or %Y-%m-%d")
    
    if(left_time_point > right_time_point or right_time_point > datetime.today() or left_time_point > datetime.today()):
        await ctx.send("ERROR: Cannot have the first time point greater than the second time point OR any time thats greater than today")
        raise discord.DiscordException("ERROR: Cannot have the first time point greater than the second time point")
    else:
        await ctx.send(f'Years selected: {left_time_point.year}-{right_time_point.year}, stock selected: {stock}, first time point: {left_time_point}, second time point: {right_time_point}')

        data = get_data(stock, left_time_point, right_time_point)
        
        plt.clf()
        
        colors = mpf.make_marketcolors(up="#00ff00",
                                       down="#ff0000",
                                       wick="inherit",
                                       edge="inherit",
                                       volume="orange",
                                       ohlc='orange')
        
        mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors = colors)
        
        match chart_type:
            case 'Line':
                mpf.plot(data,type='line',style=mpf_style,title=f'Stock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png')
            case 'Candle':
                mpf.plot(data,type='candle',style=mpf_style,title=f'Stock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png')
            case 'Renko':
                mpf.plot(data,type='renko',style=mpf_style,title=f'Stock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png',renko_params=dict(brick_size=0.75))
            case 'Point-Figure':
                mpf.plot(data,type='pnf',style=mpf_style,title=f'Stock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png')
            case 'OHLC':
                mpf.plot(data,type='ohlc',style=mpf_style,title=f'Stock Price between {months[left_time_point.month-1]} {left_time_point.day} and {months[right_time_point.month-1]} {right_time_point.day} within {left_time_point.year}-{right_time_point.year}',savefig='output.png')
            
        filename = 'output.png'
        await ctx.send(file=discord.File(filename))
        os.remove("output.png")
    
@client.command(name="Graph-MACD",help="Returns the full MACD of a given stock including S&P500")
async def chart_volatility(ctx,date1,date2,stock):
    
    if(date2 == "Present"): 
        right_time_point = datetime.today()
        left_time_point = convert_timestamp(date1)
    else:
        try:
            right_time_point = convert_timestamp(date2)
            left_time_point = convert_timestamp(date1)
        except ValueError:
            await ctx.send("ERROR: Invalid format, please use %Y-%m-%d-%H:%M:%S or %Y-%m-%d")
            raise discord.DiscordException("ERROR: Invalid format, please use %Y-%m-%d-%H:%M:%S or %Y-%m-%d")
    
    if(left_time_point > right_time_point or right_time_point > datetime.today() or left_time_point > datetime.today()):
        await ctx.send("ERROR: Cannot have the first time point greater than the second time point OR any time thats greater than today")
        raise discord.DiscordException("ERROR: Cannot have the first time point greater than the second time point")
    else:
        await ctx.send(f'Years selected: {left_time_point.year}-{right_time_point.year}, stock selected: {stock}, first time point: {left_time_point}, second time point: {right_time_point}')

        data = get_data(stock, left_time_point, right_time_point)
        print(data['Close'])
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

        mpf.plot(data,type='candle',addplot=apds,figscale=1.1,figratio=(8,5),title='\nMACD',
                style='blueskies',volume=True,volume_panel=2,panel_ratios=(6,3,2),savefig='output.png')
        
        filename = 'output.png'
        await ctx.send(file=discord.File(filename))
        os.remove("output.png")
        

        

# def parse_json(stockJson):
#     '''Should only have Close, Open, Volume, Low, High'''
#     pass
  
# @client.command(name='RealTime', help='Shows realtime statistics of a specified stock')
# async def stock_realtime(ctx, symbol:str):
#     url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m&range=1d&close=adjusted'
    
#     response = requests.get(url,headers={'User-agent': 'Mozilla/5.0'})
#     d = response.json()
#     data = parse_json(d) 
        
        
client.run(TOKEN)