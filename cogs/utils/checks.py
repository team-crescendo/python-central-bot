from discord.ext import commands
from settings import Config
from db import PostgreSQL

from discord import User
from discord.ext.commands import Context

def is_in_guild(guild_id, is_decorator=True):
    def predicate(ctx):
        return ctx.bot.get_server(guild_id).get_member(ctx.message.author.id)
        
    if is_decorator:
        return commands.check(predicate)

    return predicate

def is_crescendo(is_decorator=True):
    return is_in_guild("399121287504723970", is_decorator)

def is_user(db, is_decorator=True):
    def predicate(ctx):
        _, data = db.rnf(f"SELECT uuid FROM discord WHERE discord_id='{ctx.message.author.id}';")

        return bool(data)

    if is_decorator:
        return commands.check(predicate)

    return predicate

def is_not_user(db, is_decorator=True):
    def predicate(ctx):
        _, data = db.rnf(f"SELECT uuid FROM discord WHERE discord_id='{ctx.message.author.id}';")

        return not(bool(data)) or not(is_valid(db, False)(ctx))

    if is_decorator:
        return commands.check(predicate)

    return predicate

def is_valid(db, is_decorator=True):
    def predicate(ctx):
        print(ctx.message.author.id)
        _, data = db.rnf(f"SELECT uuid.uuid FROM uuid INNER JOIN discord ON (discord.uuid = uuid.uuid) WHERE discord.discord_id='{ctx.message.author.id}' and uuid.valid=false;")
        print(data, bool(data), not bool(data))

        return not bool(data)

    if is_decorator:
        return commands.check(predicate)

    return predicate
