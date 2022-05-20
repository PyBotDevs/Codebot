# modules
import os
import discord
from discord.errors import InvalidArgument
from discord.ext import commands
from discord.ext.commands import *
from keep_alive import keep_alive
# end of modules

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)
owner = ["αrchιshα#5518", "notsniped#4573", "thatOneArchUser#5794"]
oid = [706697300872921088, 738290097170153472, 705462972415213588]
bot.remove_command('help')

# when ready
@bot.event
async def on_ready():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(f'\n> {bot.user} HAS CONNECTED TO DISCORD.\n\n>')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Visual Studio Code"))
    print(f'[log] Log is loading...')
    print(f'[log] {bot.user} changed its activity.')

#@bot.event
#async def on_guild_join(guild):
#    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"codes"))
#    print(f'[log] {bot.user} changed its activity.')

#@bot.event
#async def on_guild_remove(guild):
#    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"codes"))
#    print(f'[log] {bot.user} changed its activity.')
# end of startup

@bot.command()
async def load(ctx, *, arg1):
    if ctx.message.author.id in oid:
        pass
    else:
        await ctx.reply(f"You can\'t use this command")
        print(f"[Cog] {ctx.author} returned an error: User Missing Permission.")
        return
    try:
        bot.load_extension(f'cogs.{arg1}')
        await ctx.send("Loaded Cog")
        print(f"[Cog] {ctx.author} loaded cog.")
        return
    except Exception as e:
        await ctx.send(e)
        print(f"[Cog] An unexpected error has occurred: {e}")

@bot.command()
async def unload(ctx, *, arg1):
    if ctx.message.author.id in oid:
        pass
    else:
        await ctx.reply(f"You can\'t use this command")
        print(f"[Cog] {ctx.author} returned an error: User Missing Permission.")
        return
    try:
        bot.unload_extension(f'cogs.{arg1}')
        await ctx.send("Unloaded Cog")
        print(f"[Cog] {ctx.author} unloaded cog.")
        return
    except Exception as e:
        await ctx.send(e)
        print(f"[Cog] An unexpected error has occurred: {e}")
        
@bot.command()
async def reload(ctx, *, arg1):
    if ctx.message.author.id in oid:
        pass
    else:
        await ctx.reply(f"You can\'t use this command")
        print(f"[Cog] {ctx.author} returned an error: User Missing Permission.")
        return
    try:
        bot.unload_extension(f'cogs.{arg1}')
        bot.load_extension(f'cogs.{arg1}')
        await ctx.send("Reloaded Cog")
        print(f"[log] {ctx.author} reloaded cog.")
        return
    except Exception as e:
        await ctx.send(e)
        print(f"[Cog] An unexpected error has occurred: {e}")

bot.load_extension("cogs.cexec")
bot.load_extension("cogs.eval")
keep_alive()
bot.run('token')



# btw i use arch
