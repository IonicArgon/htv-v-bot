import discord
import os
import requests
import json
import firstAid

from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'),
                   description="First aid bot!")
bot.remove_command('help')

# bot stuff


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name=" .help"))


@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        title="Heal-A-Bot: Commands",
        description="The Discord bot that provides first aid help!",
        color=0x0096FF)

    embed.add_field(name="help", value="Shows this message.", inline=False)
    embed.add_field(
        name="addCondition",
        value="Adds new conditions to the condition database.\n" + \
              "Usage: `.addCondition (Condition Name); (List of Symptoms); (List of Treatment)`\n" + \
              "Example: `.addCondition Heart attack; Chest pains, difficulty breathing; Call 911, Aspirin`\n" + \
              "Aliases: `add, ac`",
        inline=False)
    embed.add_field(
        name="removeCondition",
        value="Removes a condition from the condition database.\n" + \
              "Usage: `.removeCondition (Condition Name)`\n" + \
              "Example: `.removeCondition heart attack`\n" + \
              "Aliases: `rm, remove, delete`",
        inline=False)
    embed.add_field(
        name="list",
        value="List all conditions currently in the database.\n" + \
              "Usage: `.list`\n" + \
              "Aliases: `ls`",
        inline=False)
    embed.add_field(
        name="search",
        value="Looks for a condition by name.\n" + \
              "Usage: `.search (Condition Name)`\n" + \
              "Example: `.search heart attack`\n" + \
              "Aliases: `none`",
        inline=False)
    embed.add_field(
        name="compare",
        value="Compare Symptoms to Database to Find Conditions.\n" + \
              "Usage: `.compare (Symptom Name)`\n" + \
              "Example: `.compare chest pain`\n" + \
              "Aliases: `c, comp`",
        inline=False)
    embed.add_field(
        name="cpr",
        value="Shows CPR instructions.\n" + \
              "Usage: `.cpr`\n" + \
              "Aliases: `none`",
        inline=False)

    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def easterEgg(ctx):
    embed = discord.Embed(title=os.getenv('easter'))
    embed.set_image(url="https://placekitten.com/500/300")
    await ctx.send(embed=embed)
  
@bot.command(pass_context=True)
async def randomTestCommand(ctx):
    embed = discord.Embed(title=os.getenv('LOGGER_NAME'))
    embed.set_image(url=os.getenv('LOGGER'))
    await ctx.send(embed=embed)
    embed.set_image(url=os.getenv('DEBUG'))
    await ctx.send(embed=embed)


bot.load_extension("firstAid")
bot.run(os.getenv('TOKEN'))
