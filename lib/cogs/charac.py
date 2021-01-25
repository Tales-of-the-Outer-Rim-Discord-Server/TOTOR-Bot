from asyncio.windows_events import NULL
from operator import not_, truediv
from random import choice, randint
import sqlite3
from typing import Optional

from discord.ext.commands.core import has_permissions
from ..db import db
from ..bot import CREDITS_SYMBOL

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument, MissingPermissions
from discord.ext.commands import command, cooldown
from sqlite3 import IntegrityError

START_VALUE = 0
COMPLETED_JOBS = 0
START_GUILD = "No guild"

class Characters(Cog):
    def __init__(self, bot):
        self.bot = bot




    @command(name="bounty-hunter", aliases=["register-hunter"])
    async def Register_Hunter(self, ctx, name: Optional[str]):
        """Register a Bounty Hunter"""

        author = ctx.author
        discordID = author.id

        CheckExists = db.field("SELECT DiscordID FROM BountyHunter WHERE DiscordID=?", discordID)

        # print(f"---------------------------------------------------------\n -->> DiscordID: {CheckExists}\n---------------------------------------------------------")
        
        
        if CheckExists:
            await ctx.send(f"{author.mention} you already have a Bounty Hunter registered.")
        else:
            if name:
                hunterName = name

                db.execute("INSERT INTO BountyHunter (DiscordID, HunterName) VALUES (?, ?)", discordID, hunterName)
                db.commit()

                bh_embed = Embed(title="New Registration",
                                        colour = author.colour)

                Fields = [("Owner", author.mention, False),
                          ("Bounty Hunter Name", name, False),
                          ("Completed Contracts", COMPLETED_JOBS, True),
                          ("Total Value of Jobs", f"{START_VALUE} {CREDITS_SYMBOL}", True),
                          ("Bounty Hunters Guild", START_GUILD, False)]
                
                for name, value, inline in Fields:
                    bh_embed.add_field(name=name, value=value, inline=inline)
            
                await ctx.send(embed=bh_embed)

            else:
                Name = author.display_name
                hunterName = Name

                db.execute("INSERT INTO BountyHunter (DiscordID, HunterName) VALUES (?, ?)", discordID, hunterName)
                db.commit()

                bh_embed = Embed(title="New Registration",
                                        colour = author.colour)
                Fields = [("Owner", author.mention, False),
                          ("Bounty Hunter Name", hunterName, False),
                          ("Completed Contracts", COMPLETED_JOBS, True),
                          ("Total Value of Jobs", f"{START_VALUE} {CREDITS_SYMBOL}", True),
                          ("Bounty Hunters Guild", START_GUILD, False)]
                
                for name, value, inline in Fields:
                    bh_embed.add_field(name=name, value=value, inline=inline)

                await ctx.send(embed=bh_embed)
      
    @Register_Hunter.error
    async def hunter_register_error(self, ctx, exc):
        if isinstance(exc, IntegrityError):
            await ctx.send("An error occured. It appears that you already have a bounty hunter registered.")




    @command(name="assassin", aliases=["register-assassin"])
    async def Register_Assassin(self, ctx, name: Optional[str]):
        """Register an Assassin Character"""
        author = ctx.author
        discordID = author.id

        CheckExists = db.field("SELECT DiscordID FROM Assassins WHERE DiscordID=?", discordID)
        if CheckExists:
            await ctx.send(f"{author.mention} you already have a Bounty Hunter registered.")

        else:
            if name:
                AssassinName = name

                db.execute("INSERT INTO Assassins (DiscordID, AssassinName) VALUES (?, ?)", discordID, AssassinName)
                db.commit()

                # EMBED
                a_embed = Embed(title="New Registration",
                                        colour = author.colour)

                Fields = [("Owner", author.mention, False),
                          ("Assassin Name", name, False),
                          ("Completed Contracts", COMPLETED_JOBS, True),
                          ("Total Value of Jobs", f"{START_VALUE} {CREDITS_SYMBOL}", True)]
                
                for name, value, inline in Fields:
                    a_embed.add_field(name=name, value=value, inline=inline)
            
                await ctx.send(embed=a_embed)

            else:
                name = author.display_name
                AssassinName = name

                db.execute("INSERT INTO Assassins (DiscordID, AssassinName) VALUES (?, ?)", discordID, AssassinName)
                db.commit()

                # EMBED
                a_embed = Embed(title="New Registration",
                                        colour = author.colour)

                Fields = [("Owner", author.mention, False),
                          ("Assassin Name", name, False),
                          ("Completed Contracts", COMPLETED_JOBS, True),
                          ("Total Value of Jobs", f"{START_VALUE} {CREDITS_SYMBOL}", True)]
                
                for name, value, inline in Fields:
                    a_embed.add_field(name=name, value=value, inline=inline)
            
                await ctx.send(embed=a_embed)

    @Register_Assassin.error
    async def Register_Assassin_Error(self, ctx, exc):
        if isinstance(exc, IntegrityError):
            await ctx.send("An error occured. It appears that you already have an assassin registered.")









    @command(name="list-hunters", aliases=["list-bounty-hunters", "hunters"])
    async def List_Hunters(self, ctx):
        """ Get a list of all bounty hunters in the server """
        pass

    @command(name="list-assassins", aliases=["assassins"])
    async def List_Assassins(self, ctx):
        """ Get a list of all assassins in the server """
        pass








    @command(name="hunter-search", aliases=["hunter-stats", "hunter-s"])
    async def Search_Hunters(self, ctx, target: Optional[Member]):
        """Get the stats of a bounty hunter (default is yourself)"""
        author = ctx.author
        
        if not target:
            target = author
            CheckExists = db.field("SELECT DiscordID FROM BountyHunter WHERE DiscordID=?", target.id)
            if CheckExists:
                print(f"---------------------------------------\n -->> {target.display_name} : {target.id}\n--------------------------------------------------")
                    
                bh_embed = Embed(title="Bounty Hunter Search",
                                description=f"Searched for {target.mention}",
                                colour=author.colour)

                DiscordID = db.field("SELECT DiscordID FROM BountyHunter WHERE DiscordID=?", target.id)
                HunterName = db.field("SELECT HunterName FROM BountyHunter WHERE DiscordID=?", target.id)
                CompletedBounties = db.field("SELECT Completed FROM BountyHunter WHERE DiscordID=?", target.id)
                BountyValue = db.field("SELECT Total_Jobs_Value FROM BountyHunter WHERE DiscordID=?", target.id)
                Guild = db.field("SELECT Guild FROM BountyHunter WHERE DiscordID=?", target.id)

                Fields = [("Owner", f"<@{DiscordID}>", False),
                        ("Bounty Hunter Name", HunterName, False),
                        ("Completed Jobs", CompletedBounties, True),
                        ("Total Job Value", f"{BountyValue} {CREDITS_SYMBOL}", True),
                        ("Guild", Guild, False)]

                for name, value, inline in Fields:
                    bh_embed.add_field(name=name, value=value, inline=inline)

                await ctx.send(embed=bh_embed)
            else:
                await ctx.send(f"{author.mention}, when I searched for {target.mention} I found no results. They must not have a bounty hunter registered.")

        else:
            Target = target
            CheckExists = db.field("SELECT DiscordID FROM BountyHunter WHERE DiscordID=?", target.id)

            if CheckExists:
                print(f"---------------------------------------\n -->> {Target.display_name} : {Target.id}\n--------------------------------------------------")

                bh_embed = Embed(title="Bounty Hunter Search",
                                 description=f"Searched for {target.mention}",
                                 colour=author.colour)

                DiscordID = db.field("SELECT DiscordID FROM BountyHunter WHERE DiscordID=?", target.id)
                HunterName = db.field("SELECT HunterName FROM BountyHunter WHERE DiscordID=?", target.id)
                CompletedBounties = db.field("SELECT Bounties_Completed FROM BountyHunter WHERE DiscordID=?", target.id)
                BountyValue = db.field("SELECT Total_Jobs_Value FROM BountyHunter WHERE DiscordID=?", target.id)
                Guild = db.field("SELECT Guild FROM BountyHunter WHERE DiscordID=?", target.id)

                Fields = [("Owner", f"<@{DiscordID}>", False),
                        ("Bounty Hunter Name", HunterName, False),
                        ("Completed Jobs", CompletedBounties, True),
                        ("Total Job Value", f"{BountyValue} {CREDITS_SYMBOL}", True),
                        ("Guild", Guild, False)]

                for name, value, inline in Fields:
                    bh_embed.add_field(name=name, value=value, inline=inline)

                await ctx.send(embed=bh_embed)
            else:
                await ctx.send(f"{author.mention}, when I searched for {target.mention} I found no results. They must not have a bounty hunter registered.")


    @command(name="assassin-search", aliases=["assassin-s", "assassin-stats"])
    async def Search_Assassins(self, ctx, target: Optional[Member]):
        """Get the stats of an Assassin (default is yourself)"""
        author = ctx.author
        if not target:
            target = author
            CheckExists = db.field("SELECT DiscordID FROM Assassins WHERE DiscordID=?", target.id)
            if CheckExists:
                print(f"---------------------------------------\n -->> {target.display_name} : {target.id}\n--------------------------------------------------")
                    
                a_embed = Embed(title="Bounty Hunter Search",
                                description=f"Searched for {target.mention}",
                                colour=author.colour)

                DiscordID = db.field("SELECT DiscordID FROM Assassins WHERE DiscordID=?", target.id)
                HunterName = db.field("SELECT AssassinName FROM Assassins WHERE DiscordID=?", target.id)
                CompletedBounties = db.field("SELECT Completed FROM Assassins WHERE DiscordID=?", target.id)
                BountyValue = db.field("SELECT Total_Jobs_Value FROM Assassins WHERE DiscordID=?", target.id)

                Fields = [("Owner", f"<@{DiscordID}>", False),
                        ("Assassin Name", HunterName, False),
                        ("Completed Jobs", CompletedBounties, True),
                        ("Total Job Value", f"{BountyValue} {CREDITS_SYMBOL}", True)]

                for name, value, inline in Fields:
                    a_embed.add_field(name=name, value=value, inline=inline)

                await ctx.send(embed=a_embed)
            else:
                await ctx.send(f"{author.mention}, when I searched for {target.mention} I found no results. They must not have a bounty hunter registered.")

        else:
            Target = target
            CheckExists = db.field("SELECT DiscordID FROM Assassins WHERE DiscordID=?", target.id)

            if CheckExists:
                print(f"---------------------------------------\n -->> {Target.display_name} : {Target.id}\n--------------------------------------------------")

                a_embed = Embed(title="Bounty Hunter Search",
                                 description=f"Searched for {target.mention}",
                                 colour=author.colour)

                DiscordID = db.field("SELECT DiscordID FROM Assassins WHERE DiscordID=?", target.id)
                HunterName = db.field("SELECT AssassinName FROM Assassins WHERE DiscordID=?", target.id)
                CompletedBounties = db.field("SELECT Completed FROM Assassins WHERE DiscordID=?", target.id)
                BountyValue = db.field("SELECT Total_Jobs_Value FROM Assassins WHERE DiscordID=?", target.id)

                Fields = [("Owner", f"<@{DiscordID}>", False),
                        ("Assassin Name", HunterName, False),
                        ("Completed Jobs", CompletedBounties, True),
                        ("Total Job Value", f"{BountyValue} {CREDITS_SYMBOL}", True)]

                for name, value, inline in Fields:
                    a_embed.add_field(name=name, value=value, inline=inline)

                await ctx.send(embed=a_embed)
            else:
                await ctx.send(f"{author.mention}, when I searched for {target.mention} I found no results. They must not have a bounty hunter registered.")



    async def Add_To_Guild(self, ctx, target, guild):
        CheckExists = db.field("SELECT DiscordID FROM BountyHunter WHERE DiscordID=?", target.id)

        if CheckExists:

            await ctx.send("Updating Database...")

            db.execute("UPDATE BountyHunter SET Guild=? WHERE DiscordID=?", guild, target.id)
            db.commit()

        else:
            await ctx.send("That person has not registered a bounty hunter on the server.")
        




    @command(name="assign-guild", aliases=["assign"])
    @has_permissions(manage_roles=True)
    async def Add_Guild(self, ctx, target: Member, guildID: int):
        # House Tresario  - 1
        # House Paramexor - 2
        # House Salaktori - 3

        if guildID == 0:
            guild = "No Guild"

            await self.Add_To_Guild(ctx, target, guild)

            bh_embed = Embed(title="Bounty Hunter Updated",
                              description=f"Records updated for {target.mention}",
                              colour=0xff0000)

            DiscordID = db.field("SELECT DiscordID FROM BountyHunter WHERE DiscordID=?", target.id)
            HunterName = db.field("SELECT HunterName FROM BountyHunter WHERE DiscordID=?", target.id)
            CompletedBounties = db.field("SELECT Completed FROM BountyHunter WHERE DiscordID=?", target.id)
            BountyValue = db.field("SELECT Total_Jobs_Value FROM BountyHunter WHERE DiscordID=?", target.id)
            NewGuild = db.field("SELECT Guild FROM BountyHunter WHERE DiscordID=?", target.id)

            Fields = [("Owner", f"<@{DiscordID}>", False),
                      ("Bounty Hunter Name", HunterName, False),
                      ("Completed Jobs", CompletedBounties, True),
                      ("Total Job Value", f"{BountyValue} {CREDITS_SYMBOL}", True),
                      ("Guild", NewGuild, False)]

            for name, value, inline in Fields:
                bh_embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=bh_embed) 
            # assign House Salaktori
    
        elif guildID == 1:
            guild = "House Tresario"

            await self.Add_To_Guild(ctx, target, guild)

            bh_embed = Embed(title="Bounty Hunter Updated",
                              description=f"Records updated for {target.mention}",
                              colour=0xff0000)

            DiscordID = db.field("SELECT DiscordID FROM BountyHunter WHERE DiscordID=?", target.id)
            HunterName = db.field("SELECT HunterName FROM BountyHunter WHERE DiscordID=?", target.id)
            CompletedBounties = db.field("SELECT Completed FROM BountyHunter WHERE DiscordID=?", target.id)
            BountyValue = db.field("SELECT Total_Jobs_Value FROM BountyHunter WHERE DiscordID=?", target.id)
            NewGuild = db.field("SELECT Guild FROM BountyHunter WHERE DiscordID=?", target.id)

            Fields = [("Owner", f"<@{DiscordID}>", False),
                      ("Bounty Hunter Name", HunterName, False),
                      ("Completed Jobs", CompletedBounties, True),
                      ("Total Job Value", f"{BountyValue} {CREDITS_SYMBOL}", True),
                      ("Guild", NewGuild, False)]

            for name, value, inline in Fields:
                bh_embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=bh_embed) 
            # assign House Tresario
        elif guildID == 2:
            guild = "House Paramexor"

            await self.Add_To_Guild(ctx, target, guild)

            bh_embed = Embed(title="Bounty Hunter Updated",
                              description=f"Records updated for {target.mention}",
                              colour=0xff0000)

            DiscordID = db.field("SELECT DiscordID FROM BountyHunter WHERE DiscordID=?", target.id)
            HunterName = db.field("SELECT HunterName FROM BountyHunter WHERE DiscordID=?", target.id)
            CompletedBounties = db.field("SELECT Completed FROM BountyHunter WHERE DiscordID=?", target.id)
            BountyValue = db.field("SELECT Total_Jobs_Value FROM BountyHunter WHERE DiscordID=?", target.id)
            NewGuild = db.field("SELECT Guild FROM BountyHunter WHERE DiscordID=?", target.id)

            Fields = [("Owner", f"<@{DiscordID}>", False),
                      ("Bounty Hunter Name", HunterName, False),
                      ("Completed Jobs", CompletedBounties, True),
                      ("Total Job Value", f"{BountyValue} {CREDITS_SYMBOL}", True),
                      ("Guild", NewGuild, False)]

            for name, value, inline in Fields:
                bh_embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=bh_embed) 
            # assign house Paramexor
            
        elif guildID == 3:
            guild = "House Salaktori"

            await self.Add_To_Guild(ctx, target, guild)

            bh_embed = Embed(title="Bounty Hunter Updated",
                              description=f"Records updated for {target.mention}",
                              colour=0xff0000)

            DiscordID = db.field("SELECT DiscordID FROM BountyHunter WHERE DiscordID=?", target.id)
            HunterName = db.field("SELECT HunterName FROM BountyHunter WHERE DiscordID=?", target.id)
            CompletedBounties = db.field("SELECT Completed FROM BountyHunter WHERE DiscordID=?", target.id)
            BountyValue = db.field("SELECT Total_Jobs_Value FROM BountyHunter WHERE DiscordID=?", target.id)
            NewGuild = db.field("SELECT Guild FROM BountyHunter WHERE DiscordID=?", target.id)

            Fields = [("Owner", f"<@{DiscordID}>", False),
                      ("Bounty Hunter Name", HunterName, False),
                      ("Completed Jobs", CompletedBounties, True),
                      ("Total Job Value", f"{BountyValue} {CREDITS_SYMBOL}", True),
                      ("Guild", NewGuild, False)]

            for name, value, inline in Fields:
                bh_embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=bh_embed) 
            # assign House Salaktori
            
        else:
            guilds_embed = Embed(title="Unique IDs for the 3 guilds",
                                 description="Each house has been assigned a unique ID for use with that command. \nPlease try again using the correct id shown below.",
                                 colour = ctx.author.colour)
            Fields = [("No Guild",        "Unique ID: 0", False),
                      ("House Tresario",  "Unique ID: 1", False),
                      ("House Paramexor", "Unique ID: 2", False),
                      ("House Salaktori", "Unique ID: 3", False)]

            for name, value, inline in Fields:
                guilds_embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=guilds_embed) 

  

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Characters")



def setup(bot):
	bot.add_cog(Characters(bot))
