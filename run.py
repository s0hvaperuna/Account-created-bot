from bot import BaseBot
import json

with open('config.json', 'r') as f:
    config = json.load(f)

bot = BaseBot(config, config['prefix'])
bot.run(config['token'])
