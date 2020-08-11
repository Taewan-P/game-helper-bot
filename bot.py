import os, json
import discord, asyncio

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse

app = discord.Client()


json_data = open(os.getcwd() + "/token/.config.json", encoding='utf-8').read()
config_json = json.loads(json_data)
token = config_json["token"]

@app.event
async def on_ready():
    print('Logged in as')
    print(app.user.name)
    print(app.user.id)
    print('------')
    game = discord.Game("Game Helper | !help")
    await app.change_presence(status=discord.Status.online, activity=game)


app.run(token)