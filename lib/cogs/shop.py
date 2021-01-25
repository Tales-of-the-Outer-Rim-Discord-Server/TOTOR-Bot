from asyncio.windows_events import NULL
from random import choice, randint
from typing import Optional

from aiohttp import request
from attr import __description__
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown
from datetime import datetime
from discord.ext.menus import MenuPages, ListPageSource

OTHER_ITEMS_PER_PAGE = 5
SHIPS_PER_PAGE = 5
ARMS_PER_PAGE = 3      # 3 shows all per class


# gives a paginated shop list for the server and the price of the items
# # Arms Dealers shop (weapons, armor)
# # Ship Dealer shop (Ship hulls)
# # Other dealer (spice coaxium etc... )


class Arms_dealer_shop_pages(ListPageSource):
	def __init__(self, ctx, data):
			self.ctx = ctx

			super().__init__(data , per_page=ARMS_PER_PAGE)

	async def write_page(self, menu, weapons=[]):
		offset = (menu.current_page*self.per_page) + 1
		len_data = len(weapons)

		embed_items = Embed(title= "Arms Dealer Shop",
						    description = f"These are the items you can aquire from an arms dealer. \n ```Posessing anything RESTRICTED allows you to be captured and turned in to the Empire for a reward.``````RESTRICTED items can only be bought from player controlled Arms Dealers```",
						    colour = self.ctx.author.colour)
		embed_items.set_author(name= self.ctx.author.display_name, icon_url=self.ctx.author.avatar_url )
		embed_items.set_footer(text=f" {offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} items.")

		for name, value in weapons:
			embed_items.add_field(name=name, value=value, inline=False)
		
		return embed_items


	async def format_page(self, menu, weapons=[]):		
		 return await self.write_page(menu, weapons)

class Ship_dealer_shop_pages(ListPageSource):
	def __init__(self, ctx, data):
		self.ctx = ctx

		super().__init__(data , per_page=SHIPS_PER_PAGE)

	async def write_page(self, menu, ship_classes=[]):
		offset = (menu.current_page*self.per_page) + 1
		len_data = len(ship_classes)

		embed_ships = Embed(title= "Ship Dealer Shop",
						description = f"These are the items you can aquire from an ship dealer. \n ```Posessing anything RESTRICTED allows you to be captured and turned in to the Empire for a reward.``````RESTRICTED items can only be bought from player controlled Ship Dealers```",
						colour = self.ctx.author.colour)
		embed_ships.set_author(name= self.ctx.author.display_name, icon_url=self.ctx.author.avatar_url )
		embed_ships.set_footer(text=f" {offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} hulls.")

		for name, value in ship_classes:
			embed_ships.add_field(name=name, value=value, inline=False)
		
		return embed_ships


	async def format_page(self, menu, ship_classes=[]):		
		 return await self.write_page(menu, ship_classes)

class Other_dealer_shop_pages(ListPageSource):
	def __init__(self, ctx, data):
		self.ctx = ctx

		super().__init__(data , per_page=OTHER_ITEMS_PER_PAGE)

	async def write_page(self, menu, other_items=[]):
		offset = (menu.current_page*self.per_page) + 1
		len_data = len(other_items)

		embed_other = Embed(title= "Regular Dealer Shop",
						description = f"These are the items you can aquire from a regular dealer. \n ```Posessing anything RESTRICTED allows you to be captured and turned in to the Empire for a reward.``````RESTRICTED items can only be bought from player controlled Regular Dealers```",
						colour = self.ctx.author.colour)
		embed_other.set_author(name= self.ctx.author.display_name, icon_url=self.ctx.author.avatar_url )
		embed_other.set_footer(text=f" {offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} hulls.")

		for name, value in other_items:
			embed_other.add_field(name=name, value=value, inline=False)
		
		return embed_other


	async def format_page(self, menu, other_items=[]):		
		 return await self.write_page(menu, other_items)


class Shop(Cog):
	def __init__(self, bot):
		self.bot = bot
	weapons = [ # Blaster Pistol
				    ("Blaster Pistol (Common)", 			200),
					("Blaster Pistol (Rare)", 				600),
					("Blaster Pistol (Restricted)",			1500),
					# Blaster Carbine
					("Blaster Carbine (Common)", 			300),
					("Blaster Carbine (Rare)", 				900),
					("Blaster Carbine (Restricted)", 		3000),
					# Blaster Rifle
					("Blaster Rifle (Common)",				400),
					("Blaster Rifle (Rare)",		 		1200),
					("Blaster Rifle (Restricted)", 			2000),
					# Sniper Rifle
					("Sniper Rifle (Common)", 				600),
					("Sniper Rifle (Rare)", 				1800),
					("Sniper Rifle (Restricted)", 			6000),
					# Other Weapon
					("Other Weapon (Common)", 				800),
					("Other Weapon (Rare)", 				2400),
					("Other Weapon (Restricted)",	 		10000),
					# Armor
					("Armor (Common)", 						200),
					("Armor (Rare)", 						500),
					("Armor (Restricted)", 					800),
					# Grenade
					("Grenade (Common)", 					30),
					("Grenade (Rare)", 						90),
					("Grenade (Restricted)", 				150),
					# Rocket Launcher
					("Rocket Launcher (Restricted)",		12000)
					]

	ship_classes = [("Fighter | Bomber | Interceptor   (Common)",        5000),
	                ("Fighter | Bomber | Interceptor   (Rare)",		    15000),
					("Fighter | Bomber | Interceptor   (Restricted)",   50000),
					("Freighter   (Common)",                             7000),
					("Freighter   (Rare)",                              21000),
					("Patrol Craft   (Common)",                         14000),
					("Corvette   (Common)",                             28000),
					("Frigate   (Rare)",                                60000),
					("Cruiser   (Rare)",                               120000),
					("Light Carrier   (Rare)",                         240000),
					("Heavy Cruiser   (Resctricted)",                  720000),
					("Star Destroyer   (Rescricted)",                 1440000),
					("Battlecruiser   (Restricted)",                  1600000)]

	other_items = [("Other Item (Common)",               10),
	               ("Other Item (Rare)",                 30),
				   ("Other Item (Restricted)",          100),
				   ("Carbonite Spray *(Common)",         50),
				   ("Death Sticks (Restricted)",         60),
				   ("Spice (Restricted)",               300),
				   ("Refined Coaxium (Restricted)",    1500),
				   ("Raw Coaxium (Restricted)",        2500),
				   ("Raw Tabana Gas (Restricted)",     2000),
				   ("Refined Tabana Gas (Restricted)", 1000),
				   ("Rhydonium (Restricted)",          2000)]


	@command(name="arms-dealer", aliases=["weapons-shop", "armor", "armor-shop", "grenades", "grenades-shop", "weapons"])
	async def arms_dealer_shop(self, ctx):	
			""" DISPLAY A LIST OF ARMS DEALER ITEMS """
			item_menu = MenuPages(source=Arms_dealer_shop_pages(ctx, list(self.weapons)),
							delete_message_after = True,
							timeout = 180.0)

			await item_menu.start(ctx)
			
	@command(name="ship-dealer", aliases=["ships", "ship", "ship-shop"])
	async def ship_dealer_shop(self, ctx):
		""" DISPLAY A LIST OF SHIP DEALER ITEMS """
		ship_menu = MenuPages(source=Ship_dealer_shop_pages(ctx, list(self.ship_classes)),
							delete_message_after = True,
							timeout = 180.0)

		await ship_menu.start(ctx)

	@command(name="other-dealer", aliases=["other-shop", "other"])
	async def other_dealer_shop(self, ctx):
		""" DISPLAY A LIST OF OTHER ITEMS YOU CAN OWN IN THE SERVER """
		other_menu = MenuPages(source=Other_dealer_shop_pages(ctx, list(self.other_items)),
							delete_message_after = True,
							timeout = 180.0)

		await other_menu.start(ctx)

	@command(name="item-level", aliases=["info-restricted", "info-rare", "info-common", "item-levels"])
	async def item_level_info(self, ctx):
		""" DEFINITION OF COMMON, RARE & RESTRICTED ITEMS """
		Author = ctx.author
		item_info_embed = Embed(title="Item Level System",
		                        description="This embed shows you what the different levels of items/gear mean",
								colour=Author.colour)
		item_info_embed.set_author(name=Author.display_name, icon_url=Author.avatar_url)
		
		item_levels = [("Common", "```Common items are those that were mass produced and barely policed by the Empire in 3ABY```", False),
		               ("Rare", "```Rare items are those which are from no earlier than the Clone Wars. These are slightly policed by the empire but are not considdered illigal```", False),
					   ("Restricted", "```Restricted items are those that are from before the clone wars or are deemed too powerful for a regular to control. These items are heavilly policed by the Empire and are classified as illegal```", False)]
		
		for name, value, inline in item_levels:
    			item_info_embed.add_field(name=name, value=value, inline=inline)

		
		await ctx.send(embed=item_info_embed)
	

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("shop")


def setup(bot):
	bot.add_cog(Shop(bot))