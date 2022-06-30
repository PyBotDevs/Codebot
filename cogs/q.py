import discord, base64, brainfuck #pip install brainfuck-interpreter
from discord.ext import commands
from discord.ext.commands import *

class ex(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.command(name="decode")
    async def a(self, ctx, c, *, data):
        if c == "bin" or c == "binary":
            d = str()
            for i in data.split():
                a = int(i, 2)
                d += chr(a)
            return await ctx.reply(d)
        elif c == "hex" or c == "hexadecimal":
            return await ctx.reply(bytearray.fromhex(data).decode())
        elif c == "base32" or c == "b32":
            return await ctx.reply(base64.b32decode(data).decode("UTF-8"))
        elif c == "base64" or c == "b64":
            return await ctx.reply(base64.b64decode(data).decode("UTF-8"))
        elif c == "bf" or c == "brainfk" or c == "brainfuck":
            return await ctx.reply(brainfuck.evaluate(data))
        else: raise BadArgument

def setup(client:commands.Bot): client.add_cog(ex(client))
