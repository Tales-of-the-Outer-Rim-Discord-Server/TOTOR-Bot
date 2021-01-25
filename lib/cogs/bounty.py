from random import choice, randint
from typing import Optional
from ..db import db


from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown

CREDITS_SYMBOL = "<:Credits:801201215375015966>"
BOUNTY_BOARD_CHANNEL = 801213077353660436

class Bounty(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="set-bounty", aliases=["new-bounty", "bounty-n", "bounty-s"])
	async def New_Bounty(self, ctx, target: Member, alive: Optional[int]=1000, dead: Optional[int] ="Not to be brought in dead", *, OtherInfo: Optional[str]="No Other Info"):
		author = ctx.author
		if target:

			bounty_embed = Embed(title="New Bounty",
								colour=0xff0000)

			Fields = [("Contract Held By", author.mention, False),
					  ("Target", target.mention, False),
				      ("Price Alive", f"{alive:,} {CREDITS_SYMBOL}", False),
					  ("Price Dead", f"{dead:,} {CREDITS_SYMBOL}", False),
					  ("Other Information", f"```{OtherInfo}```", False)]

			for name, value, inline in Fields:
					bounty_embed.add_field(name=name, value=value, inline=inline)

			bounty_board = ctx.guild.get_channel(BOUNTY_BOARD_CHANNEL)


			db.execute("INSERT INTO BountyBoard (PlacedByID, TargetID, ValueAlive, ValueDead, OtherInfo) VALUES (?, ?, ?, ?, ?)", author.id, target.id, alive, dead, OtherInfo)
			db.commit()


			await bounty_board.send(embed=bounty_embed)
			await ctx.send(f"{author.mention}, your bounty has been posted in <#{BOUNTY_BOARD_CHANNEL}>")

		else:
			await ctx.send(f"{author.mention} you must mention a target for the bounty")








	@command(name="claim-bounty", aliases=["bounty-claim", "claim", "bounty-c"])
	async def Claim_Bounty(self, ctx, holder: Member, target: Member, dead: Optional[str]=False):
		"""Claim a bounty on completion of the task"""
		author = ctx.author
		pass








	@command(name="list-bounties", aliases=["bounties-list", "bounties-l"])
	async def List_Bounties(self, ctx, target: Optional[Member]):
		pass


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("Bounty")
			


def setup(bot):
	bot.add_cog(Bounty(bot))
