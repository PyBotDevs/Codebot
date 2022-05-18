# modules
import random
import json
import os
import discord
import asyncio
import datetime
import time
import cmath
import math
import string
import praw
import prawcore
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from datetime import datetime
from random import randint
from discord.errors import InvalidArgument
from discord.ext import commands
from discord.ext.commands import *
# end of modules

owner = ["αrchιshα#5518", "notsniped#4573", "thatOneArchUser#5794"]
oid = [706697300872921088, 738290097170153472, 705462972415213588]

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# error handler
class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        ignored = (commands.CommandNotFound)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required argument(s).')
            print(f'[log] {ctx.author} returned an error: {error}.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have the permission to do that. :eyes:")
            print(f'[log] {ctx.author} returned an error: {error}.')
        if isinstance(error, BotMissingPermissions):
            await ctx.send('I don\'t have the required permissions to use this.')
            print(f'[log] {ctx.author} returned an error: {error}.')
        if isinstance(error, BadArgument):
            await ctx.send('Invalid argument')
            print(f'[log] {ctx.author} returned an error: {error}.')
        if isinstance(error, commands.CommandOnCooldown):
            if math.ceil(error.retry_after) < 60:
                await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(error.retry_after)} seconds')
                print(f'[log] {ctx.author} returned an error: {error}.')
            elif math.ceil(error.retry_after) < 3600:
                ret = math.ceil(error.retry_after) / 60
                await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(ret)} minutes')
                print(f'[log] {ctx.author} returned an error: {error}.')
            elif math.ceil(error.retry_after) >= 3600:
                ret = math.ceil(error.retry_after) / 3600
                if ret >= 24:
                    r = math.ceil(ret) / 24
                    await ctx.reply(f"This command is on cooldown. Please try after {r} days")
                    print(f'[log] {ctx.author} returned an error: {error}.')
                else:
                    await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(ret)}')
                    print(f'[log] {ctx.author} returned an error: {error}.')
                # How to use cooldowns:
                # after @commands.command() add @commands.cooldown(1, cooldown, commands.BucketType.user)
# end of error handler

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#    @commands.command(name='evaluate', aliases=['eval', 'e'])
#    @commands.cooldown(1, 5, commands.BucketType.user)
#    async def

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
    bot.add_cog(MainCog(bot))
