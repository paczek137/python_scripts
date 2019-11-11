#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import concurrent
import datetime
import random
import discord
from discord.ext import commands, tasks
import os
import asyncio
from concurrent.futures import ProcessPoolExecutor
import p11_facebook_parser as wagon

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\n" + os.path.basename(__file__)
print(s)

client = commands.Bot(command_prefix= '.')

@client.event
async def on_ready():
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

@client.command(pass_context=True)
async def wagon(ctx):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    loop = asyncio.get_event_loop()
    menu = await loop.run_in_executor(executor, wagon.wagon_find_menu)
    #result = await sync_to_async(get_chat_id)("django")
    #menu = wagon.wagon_find_menu()
    await ctx.send(f' Wagonowa menu:' + menu)

client.run('NjI2NTIxNzYxNTk2NTcxNjUw.XZKKTQ.6nFzoJCeI1xZWHEHMlqj_ni8eh4')