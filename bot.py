from override import CrescBot
from settings import Config


cogs = [
    "cogs.test",
    "cogs.vip",
    "cogs.members",
    "cogs.attendance",
    "cogs.admin"
]

_conf = Config("config.ini")
_token = _conf.get("Credential.token")

bot = CrescBot(command_prefix="크센아 ")

for cog in cogs:
    bot.load_extension(cog)

bot.run(_token)
