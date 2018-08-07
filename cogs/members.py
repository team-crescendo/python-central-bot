from discord.ext.commands import command, CheckFailure
from settings import Config
from db import PostgreSQL

from .utils import checks

import i18n
t = i18n.t


class Member:
    def __init__(self, bot):
        self.bot = bot
        self.session = {}

        conf = Config("config.ini")

        trans_conf = conf.get("Translation")
        i18n.set("locale", trans_conf['default_locale'])
        i18n.set("file_type", "json")
        i18n.load_path.append(trans_conf['path'])

    DB = PostgreSQL(**Config("config.ini").get("Database"))
    
    async def on_ready(self):
        print(" [Mmb] Successfully loaded.")

    @command("가입", pass_context=True)
    @checks.is_not_user(DB)
    async def register(self, ctx):
        bot = ctx.bot

        Y = t("emojis.t")
        N = t("emojis.f")

        o = await bot.reply(
            t("messages.agreements")
        )

        await bot.add_reaction(o, Y)
        await bot.add_reaction(o, N)

        r = await bot.wait_for_reaction(emoji=[Y, N], timeout=60, message=o, user=ctx.message.author)

        await bot.delete_message(o)

        if r and str(r.reaction.emoji) == Y:
            _, data = self.DB.rnf(f"INSERT INTO uuid (point) VALUES (0) RETURNING uuid;")
            _, data = self.DB.rnf(f"INSERT INTO discord (uuid, discord_id) VALUES ('{data[0][0]}', '{ctx.message.author.id}') RETURNING uuid;")

            if data:
                await bot.reply(t('messages.register_success'))
            else:
                await bot.reply(t('messages.error_call_admin'))

    @register.error
    async def register_error(self, error, ctx):
        if isinstance(error, CheckFailure):
            await ctx.bot.reply(t('messages.register_already'))


def setup(bot):
    bot.add_cog(Member(bot))
