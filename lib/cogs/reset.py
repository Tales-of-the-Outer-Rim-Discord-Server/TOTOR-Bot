from lib.bot import OWNER_ID

from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.converter import Greedy
from discord.ext.commands.core import bot_has_permissions, has_permissions

from ..db import db


class Reset(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="reset", aliases=["rs", "reset_user"])
	@bot_has_permissions(manage_roles=True)
	async def reset_user(self, ctx):
		""" RESET YOUR ROLES """
		Author = ctx.author

		if ctx.guild.me.top_role.position > Author.top_role.position:
			if not self.characterless_id in Author.roles:
				if self.staff_role in Author.roles:
					if Author.id == OWNER_ID:
						await Author.edit(roles=[self.characterless_id,self.Alliegance_seperator,self.Business_seperator,self.other_seperator, self.neutral_role,
												self.staff_role, self.staff_seperator,self.head_role])
						await ctx.send(f"{Author.mention} | Your roles have been reset. \nUnfortunately I am unable to reset your nickname for you.")
					elif self.head_role in Author.roles:
						await Author.edit(roles=[self.characterless_id,self.Alliegance_seperator,self.Business_seperator,self.other_seperator, self.neutral_role,
													self.staff_role, self.staff_seperator,self.head_role])
						await Author.edit(nick=None)
						await ctx.send(f"{Author.mention} | Your roles have been reset.")
					elif self.admin_role in Author.roles:
						await Author.edit(roles=[self.characterless_id,self.Alliegance_seperator,self.Business_seperator,self.other_seperator, self.neutral_role,
													self.staff_role, self.staff_seperator,self.admin_role])
						await Author.edit(nick=None)
						await ctx.send(f"{Author.mention} | Your roles have been reset.")
					elif self.mod_role in Author.roles:
						await Author.edit(roles=[self.characterless_id,self.Alliegance_seperator,self.Business_seperator,self.other_seperator, self.neutral_role,
													self.staff_role, self.staff_seperator,self.admin_role])
						await Author.edit(nick=None)
						await ctx.send(f"{Author.mention} | Your roles have been reset.")	
				else:
					await Author.edit(roles=[self.characterless_id, self.Alliegance_seperator, self.Business_seperator, self.other_seperator, self.neutral_role])
					await Author.edit(nick=None)
					await ctx.send(f"{Author.mention} | Your roles have been reset.")
			else: 
				await ctx.send(f"{Author.mention} already has the characterless role.")
		else:
    			ctx.send(f"I do not have the required permissions to perform this task. Try moving my role above {Author.top_role}")


	@command(name="multi_reset", aliases=["m_reset", "Multi", "Multi_Reset"])
	@bot_has_permissions(manage_roles = True)
	@has_permissions(manage_roles = True, manage_guild = True)
	async def Multi_Reset(self, ctx, targets: Greedy[Member]):
		"""RESET MULTIPLE USER'S ROLES (staff only)"""
		Author = ctx.author

		if len(targets):
			for target in targets:
				if ctx.guild.me.top_role.position > target.top_role.position:
					if not self.characterless_id in target.roles:
						if self.staff_role in target.roles:
							if target.id == OWNER_ID:
									await target.edit(roles=[self.characterless_id,self.Alliegance_seperator,self.Business_seperator,self.other_seperator, self.neutral_role,
															self.staff_role, self.staff_seperator,self.head_role])
									await ctx.send(f"{Author.mention} | {target.mention}'s roles have been reset.\n Unfortunately I am unable to reset thier nickname.")	
							elif self.head_role in target.roles:
								await target.edit(roles=[self.characterless_id,self.Alliegance_seperator,self.Business_seperator,self.other_seperator, self.neutral_role,
														self.staff_role, self.staff_seperator,self.head_role])
								await target.edit(nick=None)
								await ctx.send(f"{Author.mention} | {target.name}'s nickname & roles have been reset.")

							elif self.admin_role in target.roles:
								await target.edit(roles=[self.characterless_id,self.Alliegance_seperator,self.Business_seperator,self.other_seperator, self.neutral_role,
														self.staff_role, self.staff_seperator,self.admin_role])
								await target.edit(nick=None)
								await ctx.send(f"{Author.mention} | {target.name}'s nickname & roles have been reset.")

							elif self.mod_role in target.roles:
								await target.edit(roles=[self.characterless_id,self.Alliegance_seperator,self.Business_seperator,self.other_seperator, self.neutral_role,
															self.staff_role, self.staff_seperator,self.admin_role])
								await target.edit(nick=None)
								await ctx.send(f"{Author.mention} | {target.name}'s nickname & roles have been reset.")
						else:
							await target.edit(roles=[self.characterless_id,self.Alliegance_seperator,self.Business_seperator,self.other_seperator, self.neutral_role])
							await target.edit(nick=None)
							await ctx.send(f"{Author.mention} | {target.name}'s nickname & roles have been reset.")
					else:
							await ctx.send(f"{target.display_name} already has the characterless role.")
				else:
						ctx.send(f"I do not have the required permissions to perform this task. Try moving my role above {target.top_role}")
		else:
    			await ctx.send(f"{Author.mention} | Please mention a user whos roles you wish to reset.")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.characterless_id = self.bot.guild.get_role(788359199595823115)

			self.Alliegance_seperator = self.bot.guild.get_role(788348547199664188)

			self.Business_seperator = self.bot.guild.get_role(788348363321507840)

			self.other_seperator = self.bot.guild.get_role(788348677038800937)

			self.staff_role = self.bot.guild.get_role(787378188502040576)

			self.staff_seperator = self.bot.guild.get_role(788347977059663883)

			self.mod_role = self.bot.guild.get_role(787464237592477706)

			self.admin_role = self.bot.guild.get_role(787463482953170954)

			self.head_role = self.bot.guild.get_role(787464152880513045)

			self.neutral_role = self.bot.guild.get_role(788349338094927882)
			
			self.bot.cogs_ready.ready_up("reset")


def setup(bot):
	bot.add_cog(Reset(bot))