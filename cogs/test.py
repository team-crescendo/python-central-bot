from discord.ext.commands import command

class BasicCommands:
    def __init__(self, bot):
        self.bot = bot
        self.session = {}

    async def on_ready(self):
        print(" [BCs] Successfully loaded. ")

    @command('테스트', pass_context=True)
    async def test(self, ctx):
        await ctx.bot.say(f"{ctx.message.author.mention} Yes!")

def setup(bot):
    bot.add_cog(BasicCommands(bot))
