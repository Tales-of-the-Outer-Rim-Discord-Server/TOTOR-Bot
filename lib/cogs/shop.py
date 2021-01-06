from random import choice, randint
from typing import Optional

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown


class Reset(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="reset", aliases=["rs"])
	async def reset_user(self, ctx):
            pass
        

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("reset")


def setup(bot):
	bot.add_cog(Reset(bot))