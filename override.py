from discord.ext.commands.bot import _get_variable, Bot
from settings import Config
from i18n import t

import i18n

conf = Config("config.ini")

trans_conf = conf.get("Translation")
i18n.set("locale", trans_conf['default_locale'])
i18n.set("file_type", "json")
i18n.load_path.append(trans_conf['path'])


class CrescBot(Bot):
    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.get("suffix", t("messages.reply_suffix"))
        super().__init__(*args, **kwargs)

    def reply(self, content, *args, **kwargs):
        """|coro|

        A helper function that is equivalent to doing

        .. code-block:: python

            msg = '{0.mention}{1}, {2}'.format(message.author, self.suffix, content)
            self.send_message(message.channel, msg, *args, **kwargs)

        The following keyword arguments are "extensions" that augment the
        behaviour of the standard wrapped call.

        Parameters
        ------------
        delete_after: float
            Number of seconds to wait before automatically deleting the
            message.

        See Also
        ---------
        :meth:`Client.send_message`
        """
        author = _get_variable('_internal_author')
        destination = _get_variable('_internal_channel')
        fmt = '{0.mention}{1}, {2}'.format(author, self.suffix, content)

        extensions = ('delete_after',)
        params = {
            k: kwargs.pop(k, None) for k in extensions
        }

        coro = self.send_message(destination, fmt, *args, **kwargs)
        return self._augmented_msg(coro, **params)
