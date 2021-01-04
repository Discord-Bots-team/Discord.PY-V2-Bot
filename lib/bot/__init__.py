from datetime import datetime

from discord import Intents, Embed, File

from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ..db import db


PREFIX = '='
OWNER_IDS = [197748134485426177]

class Bot(BotBase):
	def __init__(self):
		self.PREFIX=PREFIX
		self.ready = False
		self.scheduler = AsyncIOScheduler()
		self.scheduler.start() 

		db.autosave(self.scheduler)
		super().__init__(
			command_prefix=PREFIX,
			owner_ids=OWNER_IDS,
			intents=Intents.all(),
			)



	def run(self, version):
		self.VERSION = version
		with open('./lib/bot/token.0', 'r', encoding='UTF-8') as tf:
			self.TOKEN = tf.read()

		print('Running bot...')
		super().run(self.TOKEN, reconnect=True)

	async def print_message(self):
		channel = self.get_channel(795489592413257748)
		await channel.send("I am a timed notification!")


	async def on_connect(self):
		print('Bot connected!')



	async def  on_disconnect(self):
		print('Bot disconnected!')


	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send('Something went wrong.')

		raise 


	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			pass

		elif hasattr(exc, "Original"):
			raise exc.original

		else:
			raise exc


	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.scheduler.add_job(self.print_message, CronTrigger(second="0,15,30,45"))

			# Standard message to specific channel
			channel = self.get_channel(795489592413257748)
			await channel.send('Now Online')

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

			print('Bot ready!')

		else:
			print('Bot reconnected!')



	async def on_message(self, message):
		pass

bot = Bot()