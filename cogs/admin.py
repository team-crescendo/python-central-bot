from discord import User, Message
from discord.ext.commands import command, group, CheckFailure, Context
from settings import Config
from db import PostgreSQL

from .utils import checks, users, interact

import i18n
t = i18n.t


class Administration:
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
        print(" [ADm] Successfully loaded.")

    @command('종료', pass_context=True)
    async def ad_shutdown(self, ctx):
        Y = t('emojis.t')
        N = t('emojis.f')

        async def callback():
            await self.bot.close()
            exit(1)

        await interact.interact_with_reaction(
            self.bot,
            ctx.message.author,
            t('admin.shutdown_really'),
            callback,
            emojis=[Y, N]
        )
    
    @group('관리', invoke_without_command=True)
    @checks.is_crescendo()
    async def administration(self, *_):
        pass

    @administration.group('유저', invoke_without_command=True)
    @checks.is_crescendo()
    async def ad_user(self, *_):
        pass

    @ad_user.command("조회", pass_context=True)
    @checks.is_crescendo()
    async def ad_view(self, ctx, *args):
        if not args:
            user = ctx.message.author.id
        else:
            user, *remains = args

        user = users.parse_mention(user)

        user, uuid = users.get_uuid(self.DB, user)

        if uuid is None:
            await ctx.bot.reply(t("admin.no_uuid_found"))
            return

        point = users.get_point(self.DB, uuid)

        _fake_ctx = Context(prefix="\0", message=Message(reactions=[], author={"id": user}))
        print(_fake_ctx.message.author.id)
        valid = checks.is_valid(self.DB, False)(_fake_ctx)
        await ctx.bot.reply(t("admin.view_point") \
            .format(
                _target=user, 
                _dsid=user,
                _uuid=uuid, 
                _active=valid,
                _point=point
            )
        )

    @ad_user.command("가입", pass_context=True)
    @checks.is_crescendo()
    async def ad_member(self, ctx, *args):
        bot = ctx.bot
        if not args:
            return

        user, *_ = args

        user = users.parse_mention(user)
        if not len(user) == 18:
            await bot.reply(t('admin.invalid_discord_id'))
            return 

        _, uuid = users.get_uuid(self.DB, user)

        if uuid:
            await bot.reply(t("admin.remote_register_already"))
            return

        _, data = self.DB.rnf(f"INSERT INTO uuid (point) VALUES (0) RETURNING uuid;")
        uuid = data[0][0]
        _, data = self.DB.rnf(f"INSERT INTO discord (uuid, discord_id) VALUES ('{uuid}', '{user}') RETURNING uuid;")

        if data:
            await bot.reply(t('admin.remote_register_success').format(_discord=user, _uuid=uuid))
        else:
            await bot.reply(t('admin.remote_register_failed'))

    @ad_user.command("탈퇴", pass_context=True)
    @checks.is_crescendo()
    async def ad_unregister(self, ctx, *args):
        bot = ctx.bot

        user = users.parse_mention(ctx.message.author.id)
        _, uuid = users.get_uuid(self.DB, user)

        if not uuid:
            await bot.reply(t('admin.remote_unregister_not_user'))
            return

        Y = t("emojis.t")
        N = t("emojis.f")

        if not len(user) == 18:
            await bot.reply(t('admin.invalid_discord_id'))
            return

        async def callback():
            self.DB.run(f"DELETE FROM attendance WHERE uuid='{uuid}';")
            self.DB.run(f"DELETE FROM discord WHERE uuid='{uuid}';")
            self.DB.run(f"DELETE FROM uuid WHERE uuid='{uuid}';")

            await bot.reply(t('admin.remote_unregister_success'))

        await interact.interact_with_reaction(
            ctx.bot,
            ctx.message.author,
            t("admin.remote_unregister_really"),
            callback,
            emojis=[Y, N]
        )

    @administration.error
    @ad_user.error
    @ad_view.error
    async def perm_error(self, error, ctx):
        if isinstance(error, CheckFailure):
            await ctx.bot.reply(t("messages.less_permission"))

        ctx.bot.send_message(
            ctx.bot.get_channel("459291184146153482"),
            t("error_remote_report").format(
                _server=ctx.message.server,
                _channel=ctx.message.channel.id,
                _error=repr(error)
            )
        )

    
def setup(bot):
    bot.add_cog(Administration(bot))
