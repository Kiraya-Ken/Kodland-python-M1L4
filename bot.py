# import discord
# from bot_logic import flip_coin, gen_emodji, gen_pass
# from setting import settings   
# # Variabel intents menyimpan hak istimewa bot
# intents = discord.Intents.default()
# # Mengaktifkan hak istimewa message-reading
# intents.message_content = True
# # Membuat bot di variabel klien dan mentransfernya hak istimewa
# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print(f'Kita telah masuk sebagai {client.user}')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith('$halo'):
#         await message.channel.send("Hi!")
#     elif message.content.startswith('$bye'):
#         await message.channel.send("\U0001f642")
#     elif message.content.startswith('$check'):
#         await message.channel.send("test")
#     elif message.content.startswith('$fc'):
#         await message.channel.send(flip_coin())
#     elif message.content.startswith('$emodji'):
#         await message.channel.send(gen_emodji())    
#     else:
#         await message.channel.send("Password Kamu "+ gen_pass(10))

# client.run(settings["YOUR_TOKEN"])

# This example requires the 'members' and 'message_content' privileged intents to function.

from bot_logic import gen_pass
import discord
from discord.ext import commands
import random
from bot_logic import flip_coin, gen_emodji, gen_pass
from setting import settings  

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def pass_gen(ctx, pass_length: int):
    await ctx.send(gen_pass(pass_length))

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


bot.run(settings['TOKEN'])