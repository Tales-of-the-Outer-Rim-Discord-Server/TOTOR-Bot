from random import choice, randint
from typing import Optional
from ..db import db

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown


class Bounty(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="set-bounty", aliases=["new-bounty", "bounty-n", "bounty-s"])
	async def New_Bounty(self, ctx, target, alive=1000, dead="Not to be brought in dead", *, OtherInfo="No Other Info"):
		if target:
			print(f" ---> Author={ctx.author}")
			print(f" ---> Target= {target}")
			print(f" ---> Alive={alive}")
			print(f" ---> Dead={dead}")
			print(f" ---> OtherInfo={OtherInfo}")
			await ctx.send(f"Author={ctx.author}\nTarget= {target}\nDead={dead}\nAlive={alive}\nOtherInfo={OtherInfo}")

		

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("Bounty")


def setup(bot):
	bot.add_cog(Bounty(bot))
