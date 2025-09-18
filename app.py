import discord
from discord.ext import commands
import json
from nighthawks import UIDBypass, Handler
from threading import Thread
import os
import logging

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

def get_token() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bot_json_file = os.path.join(base_dir, "bot.json")
    with open(bot_json_file, 'r') as token_file:
        data = json.load(token_file)

    return str(data['token']) 



discord_token = get_token()


# intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# create bot
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 
    
    await bot.process_commands(message)



@bot.command()
async def bypass(ctx, *, command):
    bypass = UIDBypass()
    handler = Handler()

    await ctx.send(f'{ctx.author.mention} - Please wait...')
    
    uid, username, password = command.split(" ")

    # first attempt login
    login_response = handler.LoginAccount(username, password, is_bot_request=True)
    
    if login_response == "Login Success":
        bypass_response = bypass.whitelistUid(uid, username, password)
        await ctx.send(f'{ctx.author.mention} - \nUID: {uid}\nUsername: {username}\nPassword: {password}\nStatus: {login_response}\nWhitelist Status: {bypass_response}')
    else:
        await ctx.send(f'{ctx.author.mention} - \nUID: {uid}\nUsername: {username}\nPassword: {password}\nStatus: {login_response}')


@bypass.error
async def bypass_error(ctx, error):
    await ctx.send(f'{ctx.author.mention} - {error}')


bot.run(discord_token, log_handler=handler, log_level=logging.DEBUG)