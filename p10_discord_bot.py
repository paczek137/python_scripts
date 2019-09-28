#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

import datetime
import random
import discord
from discord.ext import commands, tasks
import os
import p11_facebook_parser as wagon

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\n" + os.path.basename(__file__)
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

@client.command()
async def wagon(ctx):
    menu = wagon.wagon_find_menu()
    await ctx.send(f' Wagonowa menu:')

client.run('NjI2NTIxNzYxNTk2NTcxNjUw.XY6dag.I2O69wIf9VKEHIgv7t7RupcdIXQ')