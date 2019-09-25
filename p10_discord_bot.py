#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

import datetime
import random
import discord
from discord.ext import commands, tasks

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\np9_discord_bot.py"
print(s)

client = commands.Bot(command_prefix= '.')

@client.event
async def on_read():
    print("Bot is ready")

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain',
                 'Yes',
                 'My reply is no']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def repeat(ctx):
    send_msg.start(ctx)

@tasks.loop(seconds=2)
async def send_msg(ctx):
    await ctx.send("hello")

@client.command()
async def check(ctx):
    await ctx.send(f'Hi {ctx.author}')

client.run('NjI2NTIxNzYxNTk2NTcxNjUw.XYvWVw.uUJ1JGMyNFFT-6eXX3Acra1Gxzs')