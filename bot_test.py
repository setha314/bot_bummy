
import os
import random
from PIL import Image
import pytesseract
import discord
from discord.ext import commands
import requests
TOKEN = "###"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
@bot.command()
async def meme(ctx):
    memes_folder = "mems"

    images = [
        file for file in os.listdir(memes_folder)
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
    ]

    if not images:
        await ctx.send("No images found in the mems folder!")
        return

    random_image = random.choice(images)
    image_path = os.path.join(memes_folder, random_image)

    await ctx.send(file=discord.File(image_path))
def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Once we call the duck command, the program calls the get_duck_image_url function'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)
@bot.command()
async def weather(ctx, *, city):
    api_key = "035132d3ec6c2307fbe55d9b7ddd93fa"

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        await ctx.send("City not found.")
        return

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    description = data["weather"][0]["description"]

    await ctx.send(
        f"🌤 Weather in {city}\n"
        f"Temperature: {temp}°C\n"
        f"Feels like: {feels_like}°C\n"
        f"Conditions: {description}"
    )
    await ctx.send(random.choice(tips))


import random

# Waste database
waste_data = {
    "paper": "♻️ Recycle: Paper can be recycled.",
    "newspaper": "♻️ Recycle: Newspapers belong in the recycling bin.",
    "cardboard": "♻️ Recycle: Cardboard can be recycled.",
    "plastic bottle": "♻️ Recycle: Plastic bottles belong in recycling.",
    "glass bottle": "♻️ Recycle: Glass bottles can be recycled.",
    "aluminium can": "♻️ Recycle: Aluminium cans belong in recycling.",
    "food waste": "🗑️ Rubbish: Put food waste in the rubbish or compost if available.",
    "chip packet": "🗑️ Rubbish: Most chip packets cannot be recycled.",
    "dirty pizza box": "🗑️ Rubbish: Greasy pizza boxes are not recyclable.",
    "tissue": "🗑️ Rubbish: Used tissues belong in the rubbish bin.",
    "battery": "⚠️ Special Disposal: Batteries should be taken to a battery recycling point.",
    "light bulb": "⚠️ Special Disposal: Take light bulbs to a designated recycling centre."
}

# Random tips
tips = [
    "💡 Tip: Reuse shopping bags instead of taking new ones.",
    "💡 Tip: Rinse recyclable containers before recycling them.",
    "💡 Tip: Use a reusable water bottle to reduce plastic waste.",
    "💡 Tip: Batteries should never be thrown into normal bins.",
    "💡 Tip: Compost food scraps whenever possible.",
    "💡 Tip: Reduce waste by buying products with less packaging."
    "💡 Energy Tip: Turn off lights when leaving a room.",
    "💡 Energy Tip: Unplug chargers when they're not being used.",
    "💡 Energy Tip: Use LED bulbs. They use less energy and last longer.",
    "💡 Energy Tip: Make use of natural daylight before switching on lights.",
    "💡 Energy Tip: Turn off your computer instead of leaving it on overnight.",
    "💡 Energy Tip: Lower your thermostat by 1°C to save energy.",
    "💡 Energy Tip: Close doors and windows when heating is on.",
    "💡 Energy Tip: Wash clothes at 30°C instead of higher temperatures.",
    "💡 Energy Tip: Only boil the amount of water you need in a kettle.",
    "💡 Energy Tip: Air-dry clothes when possible instead of using a tumble dryer.",
    "💡 Energy Tip: Keep your fridge door closed as much as possible.",
    "💡 Energy Tip: Switch electronics off at the wall instead of leaving them on standby.",
    "💡 Energy Tip: Clean dust from vents and fans to improve efficiency.",
    "💡 Energy Tip: Use power-saving mode on laptops and phones.",
    "💡 Energy Tip: Take shorter showers to save water and energy.",
    "💡 Energy Tip: Open curtains during sunny days to naturally warm your home.",
    "💡 Energy Tip: Close curtains at night to keep heat inside.",
    "💡 Energy Tip: Use rechargeable batteries instead of disposable ones.",
    "💡 Energy Tip: Run dishwashers and washing machines only when full.",
    "💡 Energy Tip: Plant trees or shrubs to help cool buildings naturally.",
    "🌍 Eco Tip: Reduce, Reuse, Recycle.",
    "🌍 Eco Tip: Bring a reusable bottle instead of buying bottled water.",
    "🌍 Eco Tip: Reuse shopping bags to reduce plastic waste.",
    "🌍 Eco Tip: Compost food scraps whenever possible.",
    "🌍 Eco Tip: Repair items before replacing them."
]

@bot.command()
async def sort(ctx, *, item):
    item = item.lower()

    if item in waste_data:
        await ctx.send(waste_data[item])
    else:
        await ctx.send(
            "❓ I don't know that item yet. Try another item or ask a local recycling authority."
        )

    # Random tip
    await ctx.send(random.choice(tips))


@bot.command()
async def help_sort(ctx):
    await ctx.send(
        "**Waste Sorting Bot**\n"
        "Use `!sort <item>` to find out where an item should go.\n"
        "Example: `!sort plastic bottle`"
    )

    # Random tip
    await ctx.send(random.choice(tips))







bot.run(TOKEN)