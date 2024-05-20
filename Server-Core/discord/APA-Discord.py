# SPDX-License-Identifier: MIT
import asyncio
import random
import os
import config
import re
import external
import database
import disnake
from disnake.ext import commands
from datetime import datetime, timezone

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

#======================================================================================================================
def is_authorized(user):
    authorized = False
    for role in user.roles:
        if str(role) == config.authorized_role:
            authorized = True

    return authorized

def isAdmin(user):
    authorized = False
    for role in user.roles:
        if str(role) == config.admin_role:
            authorized = True
    return authorized

#======================================================================================================================
@bot.command(brief='!pzadd \"user name\" password', description='Create a player in the whitelist.')
async def pzadd(ctx, *args):
    print("pzadd")
    if not is_authorized(ctx.author):
        await ctx.send('Not authorized.')
        return

    if len(args) != 2:
        await ctx.send('Usage: pzadd \"username\" password.')
        return

    result = external.execute_adduser(args[0],args[1])
    print(result)
    await ctx.send(f'{result}.')

#======================================================================================================================
@bot.command(brief='!pzban steamid', description='Ban a steam ID from Zomboid Server.')
async def pzban(ctx, *args):
    print("pzban")
    if not is_authorized(ctx.author):
        await ctx.send('Not authorized.')
        return

    if len(args) != 1:
        await ctx.send('Usage: pzban steam_id.')
        return

    if not args or not args[0].isdigit():
        await ctx.send('Invalid Steam ID.')
        return

    result = external.execute_banid(args[0])
    await ctx.send(f'{result}.')

#======================================================================================================================
@bot.command(brief='!pzunban steamid', description='Unban a steam ID from Zomboid Server.')
async def pzunban(ctx, *args):
    if not is_authorized(ctx.author):
        await ctx.send('Not authorized.')
        return

    if len(args) != 1:
        await ctx.send('Usage: pzunban steam_id.')
        return

    if not args or not args[0].isdigit():
        await ctx.send('Invalid Steam ID.')
        return

    result = external.execute_unbanid(args[0])
    await ctx.send(f'{result}.')

#======================================================================================================================
@bot.command(brief='!pzkick \"user name\"', description='Kick a user from Zomboid Server.')
async def pzkick(ctx, *args):
    if not is_authorized(ctx.author):
        await ctx.send('Not authorized.')
        return

    if len(args) > 1:
        await ctx.send('Usage: pzkick \"user\".')
        return

    result = external.execute_pzkick(args[0])
    await ctx.send(f'{result}.')

#======================================================================================================================
@bot.command(brief='!pzplayers', description='Returns a list of online players.')
async def pzplayers(ctx):
    if not is_authorized(ctx.author):
        await ctx.send('Not authorized.')
        return
    try:
        await ctx.send('\n'.join(external.execute_pzplayers()))
    except:
        await ctx.send('Unable to return a list at this time.')

#======================================================================================================================
@bot.command(brief='!pzlookup steamid|\"username\"', description='Returns a player whitelist entry.')
async def pzlookup(ctx, *args):
    if not is_authorized(ctx.author):
        await ctx.send('Not authorized.')
        return
    
    if len(args) != 1:
        await ctx.send('Usage: pzlookup steamid|\"username\"')
        return
    
    connection, cursor = database.main_db_connect()

    if re.match(r"765\d{14}", f"{args[0]}"):
        row = database.steam_id(cursor,args[0]).fetchone()
    else:
        print(args[0])
        row = database.username(cursor,args[0]).fetchone()

    if row == None:
        await ctx.send("No records found.")
    else:
        await ctx.send(f"Username {row[0]}, SteamID: {row[1]}, Last Login: {row[2]}")

    database.close_connections(connection, cursor)

#======================================================================================================================
@bot.command(brief='!pzgunrunner [number]', description='generates a random list of 10 guns, unless a number is specificed')
async def pzgunrunner(ctx, *args):
    if not is_authorized(ctx.author):
        await ctx.send('Not authorized.')
        return
    
    gunRunnerList = []
    finalList = []
    try:
        with open(config.gunList) as guns:
            gunRunnerList = guns.readline().split(",")

        if len(args) > 0:
            try:
                int(args[0])
                finalList = random.choices(gunRunnerList, k=int(args[0]))
            except:
                await ctx.send("You need to supply a number.")
                return
        else:
            finalList = random.choices(gunRunnerList, k=10)

        if finalList:
            await ctx.send('\n'.join(finalList))
            return
    except:
        print("Unable to open file")

#======================================================================================================================
@bot.command(brief='!pzrestart message time', description='default message "an unplanned reboot", default time "15", requires at least one value')
async def pzrestart(ctx, *args):
    if not isAdmin(ctx.author):
        await ctx.send('Not authorized.')
        return
    
    if len(args) == 2:
        await external.execute_pzrestart(args[0], args[1], bot)
    elif len(args) == 1:
        try:
            value = int(args[0])
            await external.execute_pzrestart("an unplanned reboot", value, bot)
        except ValueError:
            await external.execute_pzrestart(args[0], 15, bot)
    else:
        await ctx.send('Usage: pzrestart message time')
        return

#======================================================================================================================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\n------")

#======================================================================================================================
if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))