import discord
from discord.ext import commands
intents = discord.Intents.default()



print ("Bot Ready!")

bot = commands.Bot(command_prefix = "+", intents = intents)


@bot.event
async def on_message(message):
    
    reactions = ['👍','👎']
    if message.channel.id == 942153315549077669:
        for emoji in reactions: 
            await message.add_reaction("👍")
            await message.add_reaction("👎")
       

bot.run("ODc5Nzg0MzM2MDUwNzYxNzQ4.YSUxAw.BD6S_kkK8RU7iiwYAN64SIfj78g")
