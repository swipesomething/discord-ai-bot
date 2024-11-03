# ©2024 Swipe - https://github.com/swipesomething - https://baconwood.net

import configparser
from bot import DiscordBot

config = configparser.ConfigParser()
config.read('config.ini')

bot = DiscordBot()
bot.config = config

if __name__ == "__main__":
    bot.run(config['CONFIG']['token'])
    print("Slash commands synced globally.")

