from random import choice, randint
from typing import Optional
from ..db import db

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown

# gets rule number from database of server rules and prints the rule back as an embed.

class Rules(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="rules", aliases=["rule", "server_rules"])
	async def server_rules(self, ctx):
		"""THIS IS NOT A COMMAND YET!"""
		print("		--> the rules cog is functional")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("rules")


def setup(bot):
	bot.add_cog(Rules(bot))