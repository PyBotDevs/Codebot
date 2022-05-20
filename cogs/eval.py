# this code is being used by @Archbot , @isobot , and their alternative versions, this is being use with cogs for Discord bots.

# modules
import datetime
import inspect
import io
import math
import os
import sys
import textwrap
import traceback
from contextlib import redirect_stdout
import discord
#import pyduktape
import requests
from discord import TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import *
from discord.utils import get
from interpreter.interpreter.interpreter import Interpreter

# end of modules

owner = ["αrchιshα#5518", "notsniped#4573", "thatOneArchUser#5794"]
oid = [706697300872921088, 738290097170153472, 705462972415213588]

#now = datetime.now()
#current_time = now.strftime("%H:%M:%S")

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

class EvalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'): return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(name='evaluate', aliases=['eval', 'e'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _eval(self, ctx, *, body):
        if ctx.message.author.id not in oid: return
        blocked_words = ['while', 'quit', 'exit', 'SystemExit', 'open', '.delete()', 'os', 'subprocess', 'history()', '("token")', "('token')"]
        if ctx.message.author.id != 706697300872921088:
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
        print(f'[log] {ctx.author} executed .eval.')

#    @commands.command()
#    async def cexec(self, ctx, *, body):
#        self.log(f"{self.gettime()}{ctx.author} executed {ctx.command}")
#        if ctx.message.author.id not in oid: return
#        if body.startswith("```c") and body.endswith("```"):
#            body = body.replace("```c", "")
#            body = body.replace("```", "")
#        elif body.startswith("```") and body.endswith("```"):
#            body = body.replace("```", "")
#        def _cexec(code):
#            oldstd = sys.stdout
#            sys.stdout = open("out.txt", "w")
#            Interpreter.run(code)
#            sys.stdout.close()
#            sys.stdout = oldstd
#            with open("out.txt", "r") as f: data = f.read()
#            return data
#        await ctx.send(f"{_cexec(body)}")
            
def setup(bot):
    bot.add_cog(ErrorHandler(bot))
    bot.add_cog(EvalCog(bot))
