from discord.ext.commands import Cog, cog


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        # await self.bot.stdout.send("Fun Cog Ready")
        print('Fun Cog Ready')
        


def setup(bot):
	bot.add_cog(Fun(bot))
