# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv
from googlesearch import search

from helper import readFromJson,writeToJson

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# creating bot command to reply hello
@bot.command(name='hello', help='Responds with hi')
async def hello(ctx):
    await ctx.send("Hi "+ ctx.author.name)

# creating bot command for google search
@bot.command(name='google', help='Responds with top 5 links from google search')
async def google_search(ctx, keyword):

    print("this keyword to search for",keyword)
    # search on google.com to get top5 results
    for j in search(keyword, tld="com", num=5, stop=5, pause=2):
        await ctx.send(j)

    # adding new search keyword for user in json file
    search_history = readFromJson('search_history.json')
    userId = str(ctx.author.id)

    # if userid present in keys then append to list of previous search keywords
    # else store keyword in a list for current user id
    if userId in search_history.keys():
        search_history[userId].append(keyword)
    else:
        search_history[userId] = [keyword]

    # removing duplicate searchs
    search_history[userId] = list(dict.fromkeys(search_history[userId]))

    # writing to json file. we can use any other storage method of storing this (database table, cloud storage)
    writeToJson('search_history.json',search_history)

# creating bot command for recent searchs
@bot.command(name='recent', help='Responds with search history')
async def recent_searchs(ctx, keyword):
    print("current user",ctx.author, ctx.author.id)

    # read json file to check recent searchs
    search_history = readFromJson('search_history.json')
    userId = str(ctx.author.id)

    responseStatus = False

    # check if user has search history
    if userId in search_history.keys():
        # check each keyword in stored list with current keywords
        # if it matches will send that keyword
        for i in search_history[userId]:
            if keyword.lower() in i.lower():
                await ctx.send(i)
                responseStatus = True

    # if response is not sent that means no past searches for this keyword
    if responseStatus == False:
        await ctx.send("No recent search with keyword- "+ keyword)

print("starting server")
bot.run(TOKEN)
