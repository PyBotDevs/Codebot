# modules
import io
import inspect
import traceback
import textwrap
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
from contextlib import redirect_stdout
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

    @commands.command(name='evaluate', aliases=['eval', 'e'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _eval(self, ctx, *, body):
        if ctx.message.author.id not in oid: return
        blocked_words = ['while', 'quit', 'exit', 'SystemExit', 'open', '.delete()', 'os', 'subprocess', 'history()', '("token")', "('token')",
                        'aW1wb3J0IG9zCnJldHVybiBvcy5lbnZpcm9uLmdldCgndG9rZW4nKQ==', 'aW1wb3J0IG9zCnByaW50KG9zLmVudmlyb24uZ2V0KCd0b2tlbicpKQ==']
        if ctx.message.author.id != 705462972415213588:
            for x in blocked_words:
                if x in body:
                    return await ctx.send('Your code contains certain blocked words.')
        env = {
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource,
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text)-1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != '', pages))
        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try: 
                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                self.client._last_result = ret
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await ctx.message.add_reaction('\u2705')
        elif err:
            await ctx.message.add_reaction('\u2049')
        else:
            await ctx.message.add_reaction('\u2705')

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
    bot.add_cog(MainCog(bot))
