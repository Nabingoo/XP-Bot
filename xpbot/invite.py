from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="&", intents=intents)
invites = {}

@bot.event
async def on_ready(): 
    # Getting all the guilds our bot is in
    for guild in bot.guilds:
        # Adding each guild's invites to our dict
        invites[guild.id] = await guild.invites()

def find_invite_by_code(invite_list, code):
    
    # Simply looping through each invite in an
    # invite list which we will get using guild.invites()
    
    for inv in invite_list:
        
        # Check if the invite code in this element
        # of the list is the one we're looking for
        
        if inv.code == code:
            
            # If it is, we return it.
            
            return inv

@bot.event
async def on_member_join(member):
    memberid = member.id
    role = discord.utils.get(member.guild.roles, name = "whitelist")
    # Getting the invites before the user joining
    # from our cache for this specific guild

    invites_before_join = invites[member.guild.id]

    # Getting the invites after the user joining
    # so we can compare it with the first one, and
    # see which invite uses number increased

    invites_after_join = await member.guild.invites()

    # Loops for each invite we have for the guild
    # the user joined.

    for invite in invites_before_join:

        # Now, we're using the function we created just
        # before to check which invite count is bigger
        # than it was before the user joined.
        
        if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
            
            # Now that we found which link was used,
            # we will print a couple things in our console:
            # the name, invite code used the the person
            # who created the invite code, or the inviter.
            
            print(f"Member {member.name} Joined")
            print(f"Invite Code: {invite.code}")
            print(f"Inviter: {invite.inviter}")
            if invite.code == "jm7nVWJe4U":
                await member.add_roles(role)
            else:
                pass
            
            # We will now update our cache so it's ready
            # for the next user that joins the guild

            invites[member.guild.id] = invites_after_join
            
            # We return here since we already found which 
            # one was used and there is no point in
            # looping when we already got what we wanted
            return
@bot.event
async def on_member_remove(member):
    
    # Updates the cache when a user leaves to make sure
    # everything is up to date
    
    invites[member.guild.id] = await member.guild.invites()
bot.run("OTE2ODcwMzY3MzYzMDkyNTIw.YawcEg.5xXxCuapZF1ijW3AiHMS8nuN8fU")