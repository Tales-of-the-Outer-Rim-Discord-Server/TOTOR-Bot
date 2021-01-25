from datetime import datetime
from os import name
from typing import Optional

from discord import Embed
from discord.utils import get, time_snowflake
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog
from discord.ext.commands import command

from ..bot import PREFIX, OWNER_ID

class Ping(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="Ping", aliases=["p", "info", "bot-info"])
    async def ping(self, ctx):
        """ Gets the bot's ping to the server. """                                                                      # COMMAND DESCRIPTION
        ping = round(self.bot.latency * 1000)                                                                           # GENERATES PING VALUE
        
        PingEmbed = Embed(title=f"{ctx.guild.me.name}'s PING",colour= ctx.author.colour,timestamp=datetime.utcnow())    # SET TITLE, COLOUR, TIMESTAMP
        PingEmbed.set_author(name=ctx.author.display_name, icon_url = ctx.author.avatar_url)                            # SET AUTHOR
        PingEmbed.set_thumbnail(url=ctx.guild.me.avatar_url)                                                            # SET THUMBNAIL
        PingEmbed.add_field(name=f"Ping:", value= f"{ping} ms", inline=True)                                           ## ADD FIELD: PING
        PingEmbed.add_field(name="Prefix:", value=PREFIX, inline=True)                                                 ## ADD FIELD: PREFIX
        PingEmbed.add_field(name="Creator", value=f"<@{OWNER_ID}>", inline=True)                                       ## ADD FIELD: CREATOR
        PingEmbed.add_field(name="Currently In:", value=f"{ctx.guild.name}", inline=False)                             ## ADD FIELD: CURRENT SERVER
        PingEmbed.add_field(name="Need Help", value=f"Run the `{PREFIX}help` command in the bot commands channel")     ## ADD FIELD: HELP POINTER
        
        await ctx.send(embed=PingEmbed)                                                                                 # SEND EMBED

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("ping")


def setup(bot):
	bot.add_cog(Ping(bot))