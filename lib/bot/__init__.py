from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "="
OWNER_IDS = [197748134485426177]


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

		def run(self, version):
			self.VERSION = version
			self.TOKEN = "Nzk1NDQzODU1MTQ3MTM5MTEz.X_Jc0Q.szTUo6gPDB2El-7hn4zGwib1Bv8"
			# with open("./lib/bot/token", "r", encoding="UTF-8") as tf:
			# 	self.TOKEN = tf.read()

			print("Running Bot...")
			super().run(self.TOKEN, reconnect=True)

		async def connect(self):
			print("Bot Connected!")

		async def disconnect(self):
			print("Bot Disconnected!")

		async def on_ready(self):
			if not self.ready:
				self.ready = True
				self.guild = self.get_guild(778645541671403551)
				print("Bot Ready!")

			else:
				print("Bot Reconnected!")

		async def on_message(self, message):
			pass


bot = Bot()