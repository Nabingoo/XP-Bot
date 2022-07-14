import os
import discord
from discord.ext import commands
from discord import Embed
import sqlite3
intents = discord.Intents.default()
conn = sqlite3.connect( 'xp.db')
conn2 = sqlite3.connect( 'referral.db')
print ("XP DB Opened Successfully")
print (os.getcwd())
bot = commands.Bot(command_prefix = "+", intents = intents)

@bot.command()
async def test(ctx):
    await ctx.send("test")

@bot.command()
async def whitelist(ctx):
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, name = "whitelist")
    #role = get(member.server.roles, name="whitelist")
    v_db_level = None
    v_db_invites = None
    cursor = conn.execute('''SELECT Level from Rankings where xpneeded >= (select xpamount from UserInfo where DiscordID = ?) and min <= (select xpamount from UserInfo where DiscordID = ?)''',[ctx.author.id,ctx.author.id])
    for row in cursor:
        v_db_level = row[0]
        print(v_db_level)
    cursor = conn2.execute('''SELECT Ref_count from Referral_Log where Discord_ID = ?''',[ctx.author.id])
    for row in cursor:
        v_db_invites = row[0]
        print(v_db_level)

    if v_db_level >= 11:
        if v_db_invites >= 5:
            #give role
            embed=discord.Embed(title="Congrats on Whitelist! Welcome to the OGC!", description= "You meet the requirements!", color=discord.Color.green())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await member.add_roles(role)
        else:
            embed=discord.Embed(title="Whitelist Failed", description= "You do NOT meet the invite requirement!", color=discord.Color.red())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    else:
        if v_db_invites >= 9:
            #give role
            embed=discord.Embed(title="Congrats on Whitelist! Welcome to the OGC!", description= "You meet the requirements!", color=discord.Color.green())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await member.add_roles(role)
        else:
            embed=discord.Embed(title="Whitelist Failed", description= "You do NOT meet both requirements!", color=discord.Color.red())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)



bot.run("ODUyMTU3MzM2ODU1NTExMDcw.YMCvXQ.e25wsaeCHwQf-m2xX16UgBo1gRM")