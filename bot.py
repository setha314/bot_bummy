import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents,help_command=None)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


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



@bot.command()
async def help(ctx):
    """Shows all available commands."""
    embed = discord.Embed(
        title="Bot Commands",
        description="Here are all the commands you can use:",
        color=discord.Color.blue()
    )

    embed.add_field(name="$add <a> <b>", value="Adds two numbers.", inline=False)
    embed.add_field(name="$roll NdN", value="Rolls dice in NdN format (e.g., 2d6).", inline=False)
    embed.add_field(name="$choose option1 option2 ...", value="Chooses between multiple options.", inline=False)
    embed.add_field(name="$repeat <times> <message>", value="Repeats a message several times.", inline=False)
    embed.add_field(name="$joined <member>", value="Shows when a member joined.", inline=False)
    embed.add_field(name="$cool", value="Checks coolness.", inline=False)
    embed.add_field(name="$cool bot", value="Checks if the bot is cool.", inline=False)

    await ctx.send(embed=embed)


bot.run("")