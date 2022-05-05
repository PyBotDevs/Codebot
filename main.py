# modules
import os
import discord
import asyncio
import datetime
import time
from discord.errors import InvalidArgument
from discord.ext import commands
from discord.ext.commands import *
from keep_alive import keep_alive
# end of modules

intents = discord.Intents(messages=True, members=True, guilds=True)
bot = commands.Bot(command_prefix=']', intents=intents)
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
    print(f'\n> {bot.user} HAS CONNECTED TO DISCORD.\n\n> OWNER:\n')
    for i in owner:
        print(f"{i}\n")
    print("OWNER\'S ID:\n")
    for s in oid:
        print(f"{s}\n")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"everyone in {str(len(bot.guilds))} guilds | ]help"))
    print(f'[log] Log is loading...')
    print(f'[log] {bot.user} changed its activity.')

@bot.event
async def on_guild_join(guild):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"everyone in {str(len(bot.guilds))} guilds | ]help"))
    print(f'[log] {bot.user} changed its activity.')

@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"everyone in {str(len(bot.guilds))} guilds | ]help"))
    print(f'[log] {bot.user} changed its activity.')
# end of startup

# sudo
@bot.event
async def on_message(message):
    embed=discord.Embed(title='**admin command list of iso6.9**', description='admin prefix: `sudo\{space\}`', color=discord.Color.green())
    embed.add_field(name='control:', value='shutdown', inline=False)
    embed.set_footer(text='you\'re an admin, wow')
    await bot.process_commands(message) # add this if you're also using cmd decorators
    if message.content.startswith("sudo help") and not message.author.bot:
        if message.author.id in oid:
            await message.reply(embed=embed)
            print(f'[{message.author.name}@iso6.9 ~] requested sudo command.')
        else:
            await message.reply(f'{message.author.name} you are not an admin!')
            print(f'[log] Beware! Non-admin using sudo command detected. Requested by: {message.author}')
    if message.content.startswith("sudo shutdown") and not message.author.bot:
        def check(msg): return msg.author == message.author and msg.channel == message.channel and (msg.content)
        if message.author.id in oid:
            await message.reply('You sure?')
            msg = await bot.wait_for("message", check=check)
            if msg.content == 'y' or msg.content == 'yes':
                await message.reply('Shutting down the bot...')
                time.sleep(0.5)
                print(f'[{message.author.name}@iso6.9 ~] SystemExit triggered in sudo command.')
                raise SystemExit('Bot shutdown')
            elif msg.content == 'n' or msg.content == 'no': await message.reply('ok')
            else:
                await message.reply(f'What is {msg.content}? You are supposed to reply with yes or no')
                print(f'[log] {message.author} returned an error: Bad argument.')
        else:
            await message.reply(f'hOW AboUt nO :eyes:')
            print(f'[log] {message.author} returned an error: User not admin.')
    # swear filter
    # var
    bad = ["fuck", "bitch", "nigga", "nigger", "shit", "motherfucker", "cunt", "dickhead"]
    nsfw = ["sex", "cock", "dick", "penis", "pussy"]
    for word in bad:
        if word in message.content and not message.author.bot:
            await message.reply("ayo no bad words!")
            await message.delete()
            print(f"[filter] {bot.user} blocked a message by {message.author} which contains bad words.")
    for word in nsfw:
        if word in message.content and not message.author.bot:
            await message.reply("nO nsfW")
            await message.delete()
            print(f"[filter] {bot.user} blocked a message by {message.author} which contains nsfw words.")
        
# snipe
snipe_message_author = {}
snipe_message_content = {}

@bot.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    await asyncio.sleep(60)
    del snipe_message_author[message.channel.id]
    del snipe_message_content[message.channel.id]

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def snipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(title = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
        em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed = em)
        print(f'[log] {ctx.author} requested ]snipe.')
    except:
        await ctx.send(f"There are no recently deleted messages in #{channel.name}")
        print(f'[log] {ctx.author} returned an error: No recently deleted messages.')
# end of snipe

# edit_snipe
@bot.event
async def on_message_edit(message_before, message_after):
    if not message_after.author.bot:
        global author
        author = message_before.author
        guild = message_before.guild.id
        channel = message_before.channel
        global before
        before = message_before.content
        global after
        after = message_after.content

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def edit_snipe(ctx):
    try:
        em = discord.Embed(description=f'**Message before**: {before}\n**Message after**:{after}')
        em.set_footer(text=f'This message was edited by {author}')
        await ctx.send(embed = em)
        print(f'[log] {ctx.author} requested ]edit_snipe.')
    except:
        await ctx.reply('No recently edited messages here :eyes:')
        print(f'[log] {ctx.author} returned an error: No recently edited messages.')
# end of edit_snipe

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

bot.load_extension("cogs.Main")
keep_alive()
bot.run('token')



# btw i use arch
