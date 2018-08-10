from discord.ext.commands import command, CheckFailure
from settings import Config
from db import PostgreSQL

from .utils import checks, users

import i18n
t = i18n.t


class Attendance:
    def __init__(self, bot):
        self.bot = bot
        self.session = {}

        conf = Config("config.ini")

        trans_conf = conf.get("Translation")
        i18n.set("locale", trans_conf['default_locale'])
        i18n.set("file_type", "json")
        i18n.load_path.append(trans_conf['path'])

    DB = PostgreSQL(**Config("config.ini").get("Database"))

    def __unload(self):
        self.DB.close()
    
    async def on_ready(self):
        print(" [ATd] Successfully loaded.")
    
    @checks.is_user(DB)
    @command("출석", pass_context=True)
    async def add_attendance(self, ctx):
        _, uuid = users.get_uuid(self.DB, ctx.message.author.id)

        if uuid is None:
            await ctx.bot.reply(t("messages.register_request"))
            return

        _, data = self.DB.rnf(f"SELECT date FROM attendance WHERE uuid='{uuid}' and date >= current_date;")

        if data:
            await ctx.bot.reply(t("messages.attendance_already"))
            return

        _, data = self.DB.rnf(f"INSERT INTO attendance (uuid) VALUES ('{uuid}') RETURNING date;")

        if data:
            await ctx.bot.reply(t("messages.attendance_success").format(time=data[0][0]))
            return
        
        await ctx.bot.reply(t("messages.error_call_admin"))

    @add_attendance.error
    async def error_add_attendance(self, error, ctx):
        if isinstance(error, CheckFailure):
            await ctx.bot.reply(t("messages.register_request"))

        print(error)


def setup(bot):
    bot.add_cog(Attendance(bot))
