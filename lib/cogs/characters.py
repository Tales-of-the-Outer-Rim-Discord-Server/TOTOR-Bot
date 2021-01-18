from random import choice, randint
from typing import Optional
from ..db import db

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown


class Characters(Cog):
	def __init__(self, bot):
		self.bot = bot




	@command(name="bounty-hunter", aliases=["register-hunter"])
	async def Register_Hunter(self, ctx, name: Optional[str]):
            """Register a Bounty Hunter"""
            if name:
                    await ctx.send(f"Hunter Registered \n Owner: {ctx.author} \n Name: {name} \n Guild: None \n Completed Bounties: 0 \n Completed Bounty Value: 0")
            else:
                name = ctx.author.display_name
                await ctx.send(f"Hunter Registered \n Owner: {ctx.author.mention} \n Name: {name} \n Guild: None \n Completed Bounties: 0 \n Completed Bounty Value: 0")

	@command(name="assassin", aliases=["register-assassin"])
	async def Register_Assassin(self, ctx, name: Optional[str]):
            """Register an Assassin Character"""
            if name:
                    await ctx.send(f"Assassin Registered \n Owner: {ctx.author} \n Name: {name} \n Guild: None \n Completed Bounties: 0 \n Completed Bounty Value: 0")
            else:
                name = ctx.author.display_name
                await ctx.send(f"Assassin Registered \n Owner: {ctx.author.mention} \n Name: {name} \n Guild: None \n Completed Bounties: 0 \n Completed Bounty Value: 0")





	@command(name="list-hunters", aliases=["list-bounty-hunters", "hunters"])
	async def List_Hunters(self, ctx):
            """ Get a list of all bounty hunters in the server """
            pass

	@command(name="list-assassins", aliases=["assassins"])
	async def List_Assassins(self, ctx):
            """ Get a list of all assassins in the server """
            pass




	@command(name="hunter-search", aliases=["hunter-stats", "hunter-s"])
	async def Search_Hunters(self, ctx, name: Optional[str]):
            """Get the stats of a bounty hunter (default is yourself)"""
            if not name:
                name = ctx.author.display_name
                await ctx.send(f"Searched for {name} in the Galactic Archives.")
            else:
                    await ctx.send(f"Searched for {name} in the Galactic Archives")

	@command(name="assassin-search", aliases=["assassin-s"])
	async def Search_Assassins(self, ctx, name: Optional[str]):
            """Get the stats of an Assassin (default is yourself)"""
            if not name:
                name = ctx.author.display_name
                await ctx.send(f"Searched for {name} in the Galactic Archives.")
            else:
                    await ctx.send(f"Searched for {name} in the Galactic Archives")

	@Cog.listener()
	async def on_ready(self, ctx):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("Bounty")
			author = ctx.author


def setup(bot):
	bot.add_cog(Characters(bot))
