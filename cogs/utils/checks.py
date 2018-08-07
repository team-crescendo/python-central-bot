from discord.ext import commands
from settings import Config
from db import PostgreSQL

def is_in_guild(guild_id):
    def predicate(ctx):
        return ctx.bot.get_server(guild_id).get_member(ctx.message.author.id)
        
    return commands.check(predicate)

def is_crescendo():
    return is_in_guild("399121287504723970")

def is_user(db):
    def predicate(ctx):
        _, data = db.rnf(f"SELECT uuid FROM discord WHERE discord_id='{ctx.message.author.id}';")

        return bool(data)

    return commands.check(predicate)

def is_not_user(db):
    def predicate(ctx):
        print(ctx.message.author.id)
        _, data = db.rnf(f"SELECT uuid FROM discord WHERE discord_id='{ctx.message.author.id}';")

        return not bool(data)

    return commands.check(predicate)
