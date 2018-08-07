from discord import User
from discord.ext.commands import command, CheckFailure
from db import PostgreSQL
from settings import Config

from .utils import checks, users

import i18n
t = i18n.t


class VIP:
    def __init__(self, bot):
        self.bot = bot
        self.sessions = {}

        conf = Config("config.ini")
        self.DB = PostgreSQL(**conf.get("Database"))

        trans_conf = conf.get("Translation")
        i18n.set("locale", trans_conf['default_locale'])
        i18n.set("file_type", "json")
        i18n.load_path.append(trans_conf['path'])

    def __unload(self):
        self.DB.close()

    async def on_ready(self):
        print(f" [VIP] Successfully loaded.")

    @command('포인트', pass_context=True)
    async def vip_point(self, ctx):
        _, data = self.DB.rnf(f"SELECT uuid.point FROM uuid INNER JOIN discord ON (discord.uuid = uuid.uuid) WHERE discord.discord_id='{ctx.message.author.id}';")

        if not data:
            await ctx.bot.reply(t("messages.register_request"))
        else:
            await ctx.bot.reply(t("messages.vip_point").format(point=data[0][0]))

    @command('관리', pass_context=True)
    @checks.is_crescendo()
    async def admin(self, ctx, *args):
        menu, *remains = args

        if menu == "조회":
            user, *_ = remains

            if isinstance(user, User):
                user = user.id
            if user[:2] == "<@" and user[-1:] == ">":
                user = user[2:-1]

            uuid = users.get_uuid(self.DB, user)

            if uuid is None:
                await ctx.bot.reply(t("admin.no_uuid_found"))
                return

            point = users.get_point(self.DB, user)
            await ctx.bot.reply(t("admin.view_point").format(_target=f"<@{user}> ({user})", _uuid=uuid, _point=point))
                

    @admin.error
    async def perm_error(self, error, ctx):
        if isinstance(error, CheckFailure):
            await ctx.bot.reply(t("messages.less_permission"))

        print(error)


def setup(bot):
    bot.add_cog(VIP(bot))
