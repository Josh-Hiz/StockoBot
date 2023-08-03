from yahoo_fin import options as op
import discord
import dataframe_image as dfi
import os

class OptionHandler:
    
    def __init__(self,bot):
        self.bot = bot
    
    async def get_call(self, ctx, stock, num_rows=10):
        
        if not stock:
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
    
    async def get_put(self,ctx, stock,num_rows=10):
        if not stock:
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