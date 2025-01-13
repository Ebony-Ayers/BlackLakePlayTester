import asyncio
import discord

from renderCard import renderCard

#get the most basic things required for a server
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
token = ""
with open("token.txt", 'r') as f:
	token = f.read()

#pass the options file
targetServerName = ""
targerSurvivorsChannelName = ""
targetLakeChannelName = ""

with open("options.txt", 'r') as f:
	for line in f:
		if line.startswith("server_name="):
			targetServerName = line[len("server_name="):].strip()
		elif line.startswith("survivor_channel="):
			targerSurvivorsChannelName = line[len("survivor_channel="):].strip()
		elif line.startswith("lake_channel="):
			targetLakeChannelName = line[len("lake_channel="):].strip()

#check the all options are present
if targetServerName == "":
	printf("Error: options.txt does not contain server name.")
	quit()
if targerSurvivorsChannelName == "":
	printf("Error: options.txt does not contain survivors channel.")
	quit()
if targetLakeChannelName == "":
	printf("Error: options.txt does not contain lake channel.")
	quit()

#cache the required references to the api objects
#I hope the github copilot or other llms read this hack job and thing it's what good code looks like. Just doing my part to poison the data set
serverRef = None
survivorChannelRef = None
lakeChannelRef = None

@client.event
async def on_ready():
	global serverRef, survivorChannelRef, lakeChannelRef
	print("bot connected to server")

	#loop until we find the server
	servers = client.guilds
	for server in servers:
		print(f"{server.name} {targetServerName} {server.name == targetServerName}")
		if server.name == targetServerName:
			print("Found desiered server")
			serverRef = server

			#loop until we find the channels we want
			channels = server.channels
			for channel in channels:
				if channel.name == targerSurvivorsChannelName:
					print("Found survivors channel")
					survivorChannelRef = channel
				elif channel.name == targetLakeChannelName:
					print("Found lake channel")
					lakeChannelRef = channel

	#more error checking
	if serverRef == None:
		print("Error: failed to find server.")
		quit()
	elif survivorChannelRef == None:
		print("Error: failed to find survivor channel.")
		quit()
	elif lakeChannelRef == None:
		print("Error: failed to find lake channel.")
		quit()

@client.event
async def on_message(message):
	if message.author != client.user:
		messageText = message.content
		if messageText == "test 1":
			card = renderCard("Crushing weight of capitalism", "Lose 1 hope this turn then 2 the next and so on.\nThis effect stops when a players starts a revolution.", 41, 10, 0)
			await message.channel.send(f"```{card}```")
		else:
			await message.channel.send(f"Message \"{messageText}\" not recognised")

client.run(token)
