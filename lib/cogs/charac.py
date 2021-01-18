from asyncio.windows_events import NULL
from operator import not_, truediv
from random import choice, randint
from typing import Optional

from discord.ext.commands.core import has_permissions
from ..db import db

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown


class Characters(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def hunter_register(self, author, Name):
        Check1 = db.record("SELECT * FROM BountyHunter WHERE DiscordID=?", author.id)
        if not Name: 
            if not Check1:
                db.execute("INSERT INTO BountyHunter (DiscordID) VALUES (?)", author.id)
                db.execute("UPDATE BountyHunter SET HunterName=? WHERE DiscordID =?", Name, author.id)

    @command(name="bounty-hunter", aliases=["register-hunter"])
    async def Register_Hunter(self, ctx, name: Optional[str]):
        """Register a Bounty Hunter"""
        author = ctx.author
        if name:
                Name = name
                self.hunter_register(author, Name)
                # await ctx.send(f"Hunter Registered \n Owner: {ctx.author.mention} \n Character Name: {name} \n Guild: None \n Completed Bounties: 0 \n Completed Bounty Value: 0")
        else:
            Name = author.display_name
            self.hunter_register(author, Name)
            # await ctx.send(f"Hunter Registered \n Owner: {author.mention} \n Character Name: {name} \n Guild: None \n Completed Bounties: 0 \n Completed Bounty Value: 0")

    @command(name="assassin", aliases=["register-assassin"])
    async def Register_Assassin(self, ctx, name: Optional[str]):
        """Register an Assassin Character"""
        author = ctx.author
        if name:
            await ctx.send(f"Assassin Registered \n Owner: {ctx.author.mention} \n Character Name: {name} \n Completed Jobs: 0 \n Completed Jobs Value: 0")
        else:
            name = author.display_name
            await ctx.send(f"Assassin Registered \n Owner: {author.mention} \n Character Name: {name} \n Completed Jobs: 0 \n Completed Jobs Value: 0")

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
        author = ctx.author
        if not name:
            name = author.display_name
            await ctx.send(f"Searched for {name} in the Galactic Archives.")
        else:
            await ctx.send(f"Searched for {name} in the Galactic Archives")

    @command(name="assassin-search", aliases=["assassin-s"])
    async def Search_Assassins(self, ctx, name: Optional[str]):
        """Get the stats of an Assassin (default is yourself)"""
        author = ctx.author
        if not name:
            name = author.display_name
            await ctx.send(f"Searched for {name} in the Galactic Archives.")
        else:
            await ctx.send(f"Searched for {name} in the Galactic Archives")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Bounty")



def setup(bot):
	bot.add_cog(Characters(bot))
