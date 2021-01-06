from random import choice, randint
from typing import Optional

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown

# gives a paginated shop list for the server and the price of the items
# # Arms Dealers shop (weapons, armor)
# # Ship Dealer shop (Ship hulls)
# # Other dealer (spice coaxium etc... )

class Shop(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="shops", aliases=["shop", "items"])
	async def server_shops(self, ctx):
            print("		--> the shop cog is functional")
        

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("reset")


def setup(bot):
	bot.add_cog(Shop(bot))