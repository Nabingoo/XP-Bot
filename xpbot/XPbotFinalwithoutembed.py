#from asyncio.windows_events import NULL
import os
import discord
from discord.ext import commands
from discord import Embed
import time
import datetime
from datetime import timedelta
#from datetime import timezone
from datetime import datetime
import sqlite3
import random
from typing import Optional
intents = discord.Intents.default()

#connec to our DB XP
conn = sqlite3.connect( 'xp.db')
print ("XP DB Opened Successfully")
print (os.getcwd())
bot = commands.Bot(command_prefix = "+", intents = intents)

@bot.command()
async def test(ctx):
    await ctx.send("test")
@bot.command()
async def rank(ctx, member: Optional[discord.User]): 
    if member is None:
        v_disc_mem_ID = ctx.author.id
        v_surname = ctx.author.display_name
        v_avatar_url = ctx.author.avatar_url
        
    else:
        v_disc_mem_ID = member.id
        v_surname = member.display_name
        v_avatar_url = member.avatar_url
    v_db_level = None
    v_db_databasexp = None
    v_db_currxp = None
    v_db_needxp = None
    
        
    cursor = conn.execute('''SELECT Level from Rankings where xpneeded >= (select xpamount from UserInfo where DiscordID = ?) and min <= (select xpamount from UserInfo where DiscordID = ?)''',[v_disc_mem_ID,v_disc_mem_ID])
    for row in cursor:
        v_db_level = row[0]
        print(v_db_level)
    cursor = conn.execute('''select xpamount from UserInfo where DiscordID = ?''',[v_disc_mem_ID])
    for row in cursor:
        v_db_currxp = row[0]
        print(v_db_currxp)
    cursor = conn.execute('''SELECT XPneeded from Rankings where XPneeded >= ? and min <= ?''',[v_db_currxp,v_db_currxp])
    for row in cursor:
        v_db_needxp = row[0]
        print(v_db_needxp)
    embed=discord.Embed(title="Level: " + str(v_db_level), description= 'Current XP= ' + str(v_db_currxp) + '/' + str(v_db_needxp), color=discord.Color.dark_grey())
    embed.set_author(name=v_surname, icon_url=v_avatar_url)
    await ctx.channel.send(ctx.author.mention,embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def givexp(ctx, message, member: Optional[discord.User]): 
    if member is None:
        v_disc_mem_ID = ctx.author.id
        v_surname = ctx.author.display_name
        v_avatar_url = ctx.author.avatar_url
        
    else:
        v_disc_mem_ID = member.id
        v_surname = member.display_name
        v_avatar_url = member.avatar_url
    
    cursor = conn.execute('''update UserInfo set xpamount = xpamount + ? where DiscordID = ?''',[int(message),v_disc_mem_ID])
    conn.commit()

@bot.command()
@commands.has_permissions(administrator=True)
async def removexp(ctx, message, member: Optional[discord.User]): 
    if member is None:
        v_disc_mem_ID = ctx.author.id
        v_surname = ctx.author.display_name
        v_avatar_url = ctx.author.avatar_url
        
    else:
        v_disc_mem_ID = member.id
        v_surname = member.display_name
        v_avatar_url = member.avatar_url
    
    cursor = conn.execute('''update UserInfo set xpamount = xpamount - ? where DiscordID = ?''',[int(message),v_disc_mem_ID])
    conn.commit()
@bot.event
async def on_message(message):
    randomnum = random.randint(15, 25)
    
    if message.author.bot:
        return        
    v_mem_disc_id =  message.author.id
    
    v_db_discordID = None
    v_db_xp = None
    v_db_lasttime_db = None
    v_db_lastmessage = None
    cursor = conn.execute('select DiscordID , xpamount , lastmessage from UserInfo where DiscordID=? limit 1',[v_mem_disc_id])
    for row in cursor:
        v_db_discordID = row[0] 
        v_db_xp = row[1]
        v_db_lasttime_db = row[2]
    
    if v_db_discordID ==  None:
        
        
        cursor = conn.execute('''INSERT INTO UserInfo (DiscordID,xpamount,lastmessage) VALUES (?,?,?)''',(v_mem_disc_id, v_db_xp,message.created_at))
        conn.commit()
        
        cursor = conn.execute('''update UserInfo set xpamount= (?) where DiscordID=?''',[randomnum,v_mem_disc_id])
        
        conn.commit()   
        await bot.process_commands(message)     
    else:
        
        
        cursor = conn.execute('''select lastmessage from UserInfo where DiscordID=?''',[v_db_discordID])
        for row in cursor:
            v_db_lastmessage = row[0]
        
        difference = message.created_at - datetime.strptime(v_db_lastmessage, '%Y-%m-%d %H:%M:%S.%f')
        
        
        v_diff = difference.total_seconds()
        
        timereq = float(60.0)
        if v_diff >= timereq:
            cursor = conn.execute('''update UserInfo set lastmessage=? , xpamount = xpamount + (?)  where DiscordID=?''',[message.created_at, randomnum, v_mem_disc_id])
            conn.commit()
            
            print(v_mem_disc_id)
            print("yes")
            await bot.process_commands(message)

        else:
            print(v_mem_disc_id)
            print("no")
            await bot.process_commands(message)
       
    
  



bot.run("ODUyMTU3MzM2ODU1NTExMDcw.YMCvXQ.LoXwzM1Ps3vgaLAGq0wXgSabSko")