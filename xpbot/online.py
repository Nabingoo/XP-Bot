import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix=':', self_bot=True, help_command=None)

async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game("Modding."))

client.run(("mfa.C7dCu86F8wLb-Z2xb_tdC5j01_ech0-KkTuDEmT008umW4aboEl1NUFxWeYUq3EK1KxitzejD-8Abfuff0nV"), bot=False)