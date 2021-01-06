from asyncio.tasks import sleep
from datetime import datetime
from glob import glob

from discord import Intents, Embed, File
from discord.errors import Forbidden, HTTPException

from discord.ext.commands import Bot as BotBase, cog
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands.errors import CommandOnCooldown

from ..db import db


PREFIX = '='
OWNER_IDS = [197748134485426177]
COGS = [path.split("\\")[-1][:-3] for path in glob('./lib/cogs/*.py')]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


class ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)
	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f' - {cog} cog is ready!')
	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
	def __init__(self):
		self.PREFIX=PREFIX
		self.ready = False
		self.cogs_ready = ready()

		self.scheduler = AsyncIOScheduler()
		self.scheduler.start() 

		db.autosave(self.scheduler)
		super().__init__(
			command_prefix=PREFIX,
			owner_ids=OWNER_IDS,
			intents=Intents.all(),
			)

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f" - {cog} cog loaded")

		print("Setup Complete")

	def run(self, version):
		self.VERSION = version

		print("Running setup...")
		self.setup()
		
		with open('./lib/bot/token.0', 'r', encoding='UTF-8') as tf:
			self.TOKEN = tf.read()

		print('Running bot...')
		super().run(self.TOKEN, reconnect=True)

	async def on_connect(self):
		print('Bot connected!')
	async def  on_disconnect(self):
		print('Bot disconnected!')

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send('Something went wrong.')

		raise err
	async def on_command_error(self, ctx, exc):
		if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
			pass

		elif isinstance(exc, BadArgument):
			pass

		elif isinstance(exc, MissingRequiredArgument):
			await ctx.send("One or more arguments are missing.") 

		elif isinstance(exc, CommandOnCooldown):
    			await ctx.send(f'That command is on {str(exc.cooldown.type).split(".")[-1]} cooldown. Please try again in {exc.retry_after:,.2f} secs.')
		
		elif isinstance(exc.original, HTTPException):
			await ctx.send("Unable to send message")

		elif isinstance(exc.original, Forbidden):
			await ctx.send("I do not have permission to do that.")

		else:
			raise exc.original

	async def on_ready(self):
		if not self.ready:
			self.stdout = self.get_channel(795489592413257748)

			while not self.cogs_ready.all_ready():
				await sleep(0.5)
			
			self.ready = True
			print('Bot ready!')

		else:
			print('Bot reconnected!')

	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)

bot = Bot()