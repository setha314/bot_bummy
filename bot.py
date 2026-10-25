import discord
from discord.ext import commands
import random
from sympy import symbols, Eq, solve, sympify
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
# /plus 3 4
@bot.command()
async def plus(ctx, a: float, b: float):
    await ctx.send(f"{a} + {b} = {a + b}")

# /minus 5 2
@bot.command()
async def minus(ctx, a: float, b: float):
    await ctx.send(f"{a} - {b} = {a - b}")

# /mult 3 4
@bot.command()
async def mult(ctx, a: float, b: float):
    await ctx.send(f"{a} × {b} = {a * b}")

# /divi 10 2
@bot.command()
async def divi(ctx, a: float, b: float):
    if b == 0:
        await ctx.send("You can't divide by zero.")
        return
    await ctx.send(f"{a} ÷ {b} = {a / b}")





@bot.command()
async def solvefor(ctx, variable: str, *, equation: str):
    """
    Solves algebra equations for ANY variable.
    Example:
    /solvefor x 2x + 4 = 10
    /solvefor y 3x + 2y = 10
    """
    try:
        # Replace ^ with ** for power
        equation = equation.replace("^", "**")

        # Insert * between number and variable (2x -> 2*x)
        import re
        equation = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", equation)

        # Split equation
        if "=" not in equation:
            await ctx.send("Please include '=' in your equation.")
            return

        left, right = equation.split("=")

        # Create variable symbol
        var = symbols(variable)

        # Convert text to SymPy expressions
        left_expr = sympify(left)
        right_expr = sympify(right)

        # Build equation
        eq = Eq(left_expr, right_expr)

        # Solve
        solutions = solve(eq, var)

        # Respond
        if len(solutions) == 0:
            await ctx.send(f"No solution found for {variable}.")
        elif len(solutions) == 1:
            await ctx.send(f"{variable} = {solutions[0]}")
        else:
            formatted = ", ".join(str(s) for s in solutions)
            await ctx.send(f"Solutions for {variable}: {formatted}")

    except Exception as e:
        await ctx.send("I couldn't solve that. Try: /solvefor x 2x+4=10")
from sympy import symbols, sympify
from sympy.plotting import plot

import matplotlib.pyplot as plt
import numpy as np
from sympy import sympify, symbols

@bot.command()
async def graph(ctx, *, expression: str):
    """
    Graphs a math expression in terms of x.
    Example:
    /graph x^2 + 3x + 2
    """
    try:
        # Replace ^ with ** for power
        expression = expression.replace("^", "**")

        # Insert * between number and variable (2x -> 2*x)
        import re
        expression = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", expression)

        # Prepare SymPy expression
        x = symbols('x')
        expr = sympify(expression)

        # Convert to a lambda function for numpy
        f = np.vectorize(lambda val: float(expr.subs(x, val)))

        # Generate x values
        xs = np.linspace(-10, 10, 400)

        # Compute y values
        ys = f(xs)

        # Plot
        plt.figure()
        plt.plot(xs, ys)
        plt.title(f"Graph of {expression}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)

        # Save graph
        filename = "graph.png"
        plt.savefig(filename)
        plt.close()

        # Send graph
        await ctx.send(file=discord.File(filename))

    except Exception as e:
        await ctx.send("I couldn't graph that. Try something like: /graph x^2+3x+2")










bot.run("")
