import os

import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import numpy as np

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='!')



@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
         f'{bot.user} has connected to the following guild:\n'
         f'{guild.name}(id: {guild.id})'
         )

@bot.command(name='99', help='Responds with a quote from Brooklynn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='roll', help='Rolls a dice of specified side numbers')
async def roll(ctx, roll_code):

    # Get number of dice nd 
    num_dice = roll_code.split('d')[0]
    num_sides = int(roll_code.split('d')[1])
    if num_dice == '':
        num_dice = 1
    else:
        num_dice = int(num_dice)

    # Roll each dice
    dice = [str(random.choice(range(1, num_sides + 1))) for _ in range(num_dice)]
    total = int(np.sum([int(die) for die in dice]))

    await ctx.send(', '.join(dice))
    await ctx.send('Total: {total}'.format(total=total))

@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.command(name='delete-channel')
@commands.has_role('admin')
async def delete_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel:
        print(f'Deleting channel: {channel_name}')
        await existing_channel.delete()
        await ctx.send(f'Deleted channel: {channel_name}')
    else:
        m = f'Channel {channel_name} does not exist.'
        print(m)
        await ctx.send(m)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)