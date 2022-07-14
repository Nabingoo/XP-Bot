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
async def level(ctx):
    v_db_level = None
    
    cursor = conn.execute('''SELECT Level from Rankings where xpneeded >= (select xpamount from UserInfo where DiscordID = 84854837288) and min <= (select xpamount from UserInfo where DiscordID = 84854837288)''')
    for row in cursor:
        v_db_level = row[0]
        print(v_db_level)
    embed=discord.Embed(title=v_db_level, description= 'Use - ?generate', color=discord.Color.dark_grey())
    embed.set_author(name=ctx.author.id)
    await ctx.channel.send(ctx.author.mention,embed=embed)

@bot.event
async def on_message(message):
    randomnum = random.randint(10, 25)
    
    if message.author.bot:
        return        
    v_mem_disc_id =  message.author.id
    print(v_mem_disc_id)
    v_db_discordID = None
    v_db_xp = None
    v_db_lasttime_db = None
    v_db_lastmessage = None
    cursor = conn.execute('select DiscordID , xpamount , lastmessage from UserInfo where DiscordID=? limit 1',[v_mem_disc_id])
    for row in cursor:
        v_db_discordID = row[0] 
        v_db_xp = row[1]
        v_db_lasttime_db = row[2]
    print (v_db_discordID)
    if v_db_discordID ==  None:
        embed=discord.Embed(title="The User Does not have past message", description= 'Use - ?generate', color=discord.Color.dark_grey())
        embed.set_author(name=v_mem_disc_id)
        await message.channel.send(message.author.mention,embed=embed)
        #Insert in Used List Table (dark_grey List) 
        #cursor = conn.execute('''update UserInfo set xpamount = xpamount + 1''')
        cursor = conn.execute('''INSERT INTO UserInfo (DiscordID,xpamount,lastmessage) VALUES (?,?,?)''',(v_mem_disc_id, v_db_xp,message.created_at))
        conn.commit()
        
        cursor = conn.execute('''update UserInfo set xpamount= (?) where DiscordID=?''',[randomnum,v_mem_disc_id])
        #cursor = conn.execute('''INSERT INTO UserInfo (DiscordID,xpamount,lastmessage) VALUES (?,?,?)''',(v_mem_disc_id, v_db_xp,message.created_at))
        conn.commit()        
    else:
        #if message.created_at - v_db_lasttime_db 
        print("ELSE")
        cursor = conn.execute('''select lastmessage from UserInfo where DiscordID=?''',[v_db_discordID])
        for row in cursor:
            v_db_lastmessage = row[0]
        
        difference = message.created_at - datetime.strptime(v_db_lastmessage, '%Y-%m-%d %H:%M:%S.%f')
        
        
        v_diff = difference.total_seconds()
        print(v_diff)
        timereq = "2022-02-13 00:00:05.000000"
        newtime = datetime.strptime(timereq, '%Y-%m-%d %H:%M:%S.%f')
        print(type(v_diff))
        timereq = float(5.0)
        if v_diff >= timereq:
            cursor = conn.execute('''update UserInfo set lastmessage=? , xpamount = xpamount + (?)  where DiscordID=?''',[message.created_at, randomnum, v_mem_disc_id])
            conn.commit()
            #cursor = conn.execute('''update UserInfo set xpamount = xpamount + 1 where DiscordID=?''',[v_mem_disc_id])
            #conn.commit()
            await message.channel.send("Yes")

        else:
            await message.channel.send("no")
               # if difference > newtime:
      #      message.channel.send("Nice!")
       #     cursor = conn.execute('''update UserInfo set xpamount = xpamount + 15 where DiscordID=?''',[v_db_discordID])
       #     conn.commit()
       # else:
        #    message.channel.send("Hey, Thats too soon!")
        
        #embed=discord.Embed(title=TimeDiff, description= 'Use - ?generate', color=discord.Color.dark_grey())
        #embed.set_author(name=v_mem_disc_id)
        #await message.channel.send(message.author.mention,embed=embed)
    
  

#cursor = conn.execute('''SELECT Level from Rankings where xpneeded >= (select xpamount from UserInfo where DiscordID = 84854837288) and min <= (select xpamount from UserInfo where DiscordID = 84854837288)''')

bot.run("ODUyMTU3MzM2ODU1NTExMDcw.YMCvXQ.LoXwzM1Ps3vgaLAGq0wXgSabSko")