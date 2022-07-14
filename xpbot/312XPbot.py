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
import math
from typing import Optional
from discord.utils import get
intents = discord.Intents.default()

#connec to our DB XP
conn = sqlite3.connect( 'xp.db')
sqlite3
print ("XP DB Opened Successfully")
print (os.getcwd())
bot = commands.Bot(command_prefix = "+", intents = intents)
@bot.command(aliases=['inventory', 'invt'])
async def inv(ctx):
    v_db_currbox = None
    cursor = conn.execute('select NewBoxes from boxes where DiscordID=? limit 1',[ctx.author.id])
    for row in cursor:
        v_db_currbox = row[0] 
        
    print(v_db_currbox)
    embed=discord.Embed(title="Current Boxes", description= 'You have ' + str(v_db_currbox) +"!", color=discord.Color.dark_grey())
        
    await ctx.channel.send(ctx.author.mention,embed=embed)
@bot.command(aliases=['givebox', 'claimbox'])
async def getbox(ctx):
    v_mem_disc_id =  ctx.author.id
    #size2 = len(str(message.created_at))
    v_db_discordID = None
    v_db_nb = None
    v_db_ub = None
    v_db_var = None
    v_db_level = None
    cursor = conn.execute('select DiscordID , NewBoxes , UsedBoxes from boxes where DiscordID=? limit 1',[v_mem_disc_id])
    for row in cursor:
        v_db_discordID = row[0] 
        v_db_nb = row[1]
        v_db_ub = row[2]
    
    if v_db_discordID ==  None:
        
        v_db_nb = 0
        v_db_ub = 0
        
        cursor = conn.execute('''INSERT INTO boxes (DiscordID,NewBoxes,UsedBoxes) VALUES (?,?,?)''',(v_mem_disc_id, v_db_nb, v_db_ub))
        conn.commit()
          
          
    else:
        
        cursor = conn.execute('''select xpamount from UserInfo where DiscordID=?''',[v_db_discordID])
        for row in cursor:
            v_db_var = row[0]

        if v_db_var >= 12475:
            v_db_level == 45
            math = v_db_nb + v_db_ub
            giveboxes = 15
            if giveboxes >= math:
                math2 = giveboxes - math
            
            if math2 == 0:
                
                embed=discord.Embed(title="You haven't recieved boxes!", color=discord.Color.dark_grey())
        
                await ctx.channel.send(ctx.author.mention,embed=embed)
            else:
                cursor = conn.execute('''update boxes set NewBoxes= (?) where DiscordID=?''',[math2,v_mem_disc_id])
                conn.commit()
                embed=discord.Embed(title="You've got boxes!", description= 'You gained ' + str(math2) +" boxes!", color=discord.Color.dark_grey())
        
                await ctx.channel.send(ctx.author.mention,embed=embed)
        else:
        
            cursor = conn.execute('''SELECT Level from Rankings where xpneeded >= ? and min <= ?''',[v_db_var,v_db_var])
            for row in cursor:
                v_db_level = row[0]
        
            giveboxes = v_db_level // 3

            math = v_db_nb + v_db_ub

            if giveboxes >= math:
                math2 = giveboxes - math
            
                if math2 == 0:
                
                    embed=discord.Embed(title="You haven't recieved boxes!", color=discord.Color.dark_grey())
        
                    await ctx.channel.send(ctx.author.mention,embed=embed)
                else:
                    cursor = conn.execute('''update boxes set NewBoxes= (?) where DiscordID=?''',[math2,v_mem_disc_id])
                    conn.commit()
                    embed=discord.Embed(title="You've got boxes!", description= 'You gained ' + str(math2) +" boxes!", color=discord.Color.dark_grey())
        
                    await ctx.channel.send(ctx.author.mention,embed=embed)
        
        
        
        

        


@bot.command(aliases=['openbox', 'box'])
async def open(ctx):
    
    v_db_discordID = None
    v_db_nb = None
    v_db_ub = None
    v_db_var = None
    cursor = conn.execute('select DiscordID , NewBoxes , UsedBoxes from boxes where DiscordID=? limit 1',[ctx.author.id])
    for row in cursor:
        v_db_discordID = row[0] 
        v_db_nb = row[1]
        v_db_ub = row[2]
    
    if v_db_discordID ==  None:
        
        v_db_nb = 0
        v_db_ub = 0
        
        cursor = conn.execute('''INSERT INTO boxes (DiscordID,NewBoxes,UsedBoxes) VALUES (?,?,?)''',(ctx.author.id, v_db_nb, v_db_ub))
        conn.commit()

    else:
        
        if v_db_nb == 0:
            embed=discord.Embed(title="you cannot open any boxes.",description= "You are out of boxes.", color=discord.Color.red())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(ctx.author.mention,embed=embed) 
        else:
        
            cursor = conn.execute('''update boxes set NewBoxes= NewBoxes - 1 where DiscordID=?''',[ctx.author.id])
            conn.commit()
            cursor = conn.execute('''update boxes set UsedBoxes = UsedBoxes + 1 where DiscordID=?''',[ctx.author.id])
            conn.commit()

            out = random.randint(1, 10000)

            if out >= 1 and out <= 64: 
        
                embed=discord.Embed(title="Box Opened!",description= "You won tickets to a launch!", color=discord.Color.green())
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(ctx.author.mention,embed=embed) 
            elif out >= 65 and out <= 3300: 
                member = ctx.message.author
                role = discord.utils.get(member.guild.roles, name = "whitelist")
                
                
                embed=discord.Embed(title="Box Opened!",description= "You won whitelist!", color=discord.Color.blue())
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await member.add_roles(role)
                await ctx.send(ctx.author.mention,embed=embed) 
                
            elif out > 3300:
        
                embed=discord.Embed(title="Box Opened!",description= "You didn't win anything.", color=discord.Color.red())
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(ctx.author.mention,embed=embed) 
@bot.command()
async def rank(ctx, member: Optional[discord.User]): 
    if member is None:
        v_disc_mem_ID = ctx.author.id
        v_surname = ctx.author.display_name
        v_avatar_url = ctx.author.avatar.url
        
    else:
        v_disc_mem_ID = member.id
        v_surname = member.display_name
        v_avatar_url = member.avatar.url
    v_db_level = None
    v_db_databasexp = None
    v_db_currxp = None
    v_db_needxp = None
    v_db_minxp = None
    cursor = conn.execute('''select xpamount from UserInfo where DiscordID = ?''',[v_disc_mem_ID])
    for row in cursor:
        v_db_currxp = row[0]
        print(v_db_currxp)
    if v_db_currxp >= 12475:
        embed=discord.Embed(title="Level: MAX", description= 'Current XP= MAX', color=discord.Color.dark_grey())
        embed.add_field(name = "Progress Bar: " , value =  ":100:" + ":fire:" + ":triumph:" + ":ok_hand:", inline = False)
        embed.set_author(name=v_surname)
        embed.set_thumbnail(url=v_avatar_url)
        await ctx.channel.send(ctx.author.mention,embed=embed)
    else:
        cursor = conn.execute('''select min from Rankings where xpneeded >= (select xpamount from UserInfo where DiscordID = ?) and min <= (select xpamount from UserInfo where DiscordID = ?)''',[v_disc_mem_ID,v_disc_mem_ID])   
        for row in cursor:
            v_db_minxp = row[0]
            print(v_db_minxp)
        cursor = conn.execute('''SELECT Level from Rankings where xpneeded >= (select xpamount from UserInfo where DiscordID = ?) and min <= (select xpamount from UserInfo where DiscordID = ?)''',[v_disc_mem_ID,v_disc_mem_ID])
        for row in cursor:
            v_db_level = row[0]
            print(v_db_level)
    
        cursor = conn.execute('''SELECT XPneeded from Rankings where XPneeded >= ? and min <= ?''',[v_db_currxp,v_db_currxp])
        for row in cursor:
            v_db_needxp = row[0]
            print(v_db_needxp)
        xpgap = v_db_needxp - v_db_minxp
        xpgap2 = v_db_currxp - v_db_needxp
        xppercent3 = ((xpgap2 / xpgap) * -1 * 100) / 5
    ###
    
    
        embed=discord.Embed(title="Level: " + str(v_db_level), description= 'Current XP= ' + str(v_db_currxp) + '/' + str(v_db_needxp), color=discord.Color.dark_grey())
        embed.add_field(name = "Progress Bar: " + str(v_db_level), value = (20-math.trunc(xppercent3)) * ":red_square:" + math.trunc(xppercent3) * ":white_large_square:", inline = False)
        embed.set_author(name=v_surname)
        embed.set_thumbnail(url=v_avatar_url)
        await ctx.channel.send(ctx.author.mention,embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def givexp(ctx, message, member: Optional[discord.User]): 
    if member is None:
        v_disc_mem_ID = ctx.author.id
        v_surname = ctx.author.display_name
        v_avatar_url = ctx.author.avatar.url
        
    else:
        v_disc_mem_ID = member.id
        v_surname = member.display_name
        v_avatar_url = member.avatar.url
    
    cursor = conn.execute('''update UserInfo set xpamount = xpamount + ? where DiscordID = ?''',[int(message),v_disc_mem_ID])
    conn.commit()

@bot.command()
@commands.has_permissions(administrator=True)
async def removexp(ctx, message, member: Optional[discord.User]): 
    if member is None:
        v_disc_mem_ID = ctx.author.id
        v_surname = ctx.author.display_name
        v_avatar_url = ctx.author.avatar.url
        
    else:
        v_disc_mem_ID = member.id
        v_surname = member.display_name
        v_avatar_url = member.avatar.url
    
    cursor = conn.execute('''update UserInfo set xpamount = xpamount - ? where DiscordID = ?''',[int(message),v_disc_mem_ID])
    conn.commit()

@bot.command()
async def leaderboard(ctx):  
    
    cursor = conn.execute('select DiscordID, XPamount from  UserInfo order by XPamount desc  limit 10')
    v_description_info = ""
    v_rank = 0
    for row in cursor:
        v_rank = v_rank + 1
        v_description_info += "**" +str(v_rank) + ". " + f"<@"+str(row[0])+">" + "**\n" + str(row[1]) + " XP\n\n" 
    embed = discord.Embed(title="Leaderboard", description="Top 10", color=0x00ff00)
    embed=discord.Embed(description= v_description_info, color=discord.Color.dark_grey())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
    await ctx.send(ctx.author.mention,embed=embed) 
@bot.event
async def on_message(message):
    randomnum = random.randint(15,25)
    
    if message.author.bot:
        return        
    v_mem_disc_id =  message.author.id
    #size2 = len(str(message.created_at))
    v_db_discordID = None
    v_db_xp = None
    v_db_lasttime_db = None
    v_db_lastmessage = None
    #v_altmessagedate = str(message.created_at)[:size2 - 6]
    #altmsg = message.created_at.replace(tzinfo=None) 
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
        #v_dat = str(message.created_at)
        
        #size = len(v_dat)
        #lastmsg = (v_db_lastmessage).replace(tzinfo=None) 
        #mod_string = message.created_at[:size - 6]
        #dt_string = str(v_db_lastmessage)
        #new_dt = dt_string[:26]
        #difference = message.created_at - datetime.strptime(mod_string, '%Y-%m-%d %H:%M:%S.%f')
        difference = (message.created_at)  - (datetime.strptime(v_db_lastmessage, '%Y-%m-%d %H:%M:%S.%f%z'))
        
        
        v_diff = difference.total_seconds()
        
        timereq = float(60.0)
        if v_diff >= timereq:
            cursor = conn.execute('''update UserInfo set lastmessage=? , xpamount = xpamount + (?)  where DiscordID=?''',[message.created_at, randomnum, v_mem_disc_id])
            conn.commit()
            
            print(randomnum)
            print("yes")

            await bot.process_commands(message)

        else:
            
            print("no")
            await bot.process_commands(message)
       
    
  



bot.run("ODUyMTU3MzM2ODU1NTExMDcw.YMCvXQ.e25wsaeCHwQf-m2xX16UgBo1gRM")
