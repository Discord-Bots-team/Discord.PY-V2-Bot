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
		print(f'{cog} Cog ready!')

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
			print(f"{cog} cog loaded")

		print("Setup Complete")


	def run(self, version):
		self.VERSION = version

		print("Running setup...")
		self.setup()
		
		with open('./lib/bot/token.0', 'r', encoding='UTF-8') as tf:
			self.TOKEN = tf.read()

		print('Running bot...')
		super().run(self.TOKEN, reconnect=True)

	async def print_message(self):
		await self.stdout.send("I am a timed notification!")


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
			self.scheduler.add_job(self.print_message, CronTrigger(minute=0, second=0))

			# Standard message to specific channel
			await self.stdout.send('Now Online')

			# # Sending an Embed
			# embed = Embed(
			# 	title= "Now Online",
			# 	description= "Bot is now online",
			# 	color=0xFF0000, #Bright red hexadecimal
			# 	timestamp=datetime.utcnow()
			# 	)

			# # Setting the Author
			# embed.set_author(name="UrbanHaaks", icon_url="https://cdn.discordapp.com/avatars/795443855147139113/bf47e9aa8ffc93a643a16bbbdd5400e9.webp?size=256")

			# # Setting the footer
			# embed.set_footer(text="This is a footer!")

			# # Setting the thumbnail
			# embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/795443855147139113/bf47e9aa8ffc93a643a16bbbdd5400e9.webp?size=256")

			# # Setting the image
			# embed.set_image(url="https://cdn.discordapp.com/avatars/795443855147139113/bf47e9aa8ffc93a643a16bbbdd5400e9.webp?size=256")

			# # Formatting additional Fields using tupples
			# fields = [("Name", "V2", True),
			# 		  ("Another Field", "This field is next to the other one", True),
			# 		  ("Non Inline Field", "This field will appear on its own row", False),
			# 		  ("Final Inline Field", "This should be at the bottom", True),
			# 		  ("Test", "Test", True)]
			
			# for name, value, inline in fields:

			# 	embed.add_field(name=name, value=value, inline=inline)

			# await channel.send(embed=embed)

			# Sending a file to discord
			# await channel.send(file=File("./data/images/Galactic_Empire.png"))
			
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