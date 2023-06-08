import discord
import os
import google.generativeai as palm
from keep_alive import keep_alive
from discord import app_commands

keep_alive()
palm.configure('<PaLM API KEY>') # Put your PaLM 2 API key here
bot_token = '<Discord Bot Token>' # Put your Discord bot token here
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
  await tree.sync()
  await client.change_presence(activity=discord.Activity(
    name="with PaLM 2!!", type=discord.ActivityType.playing, details="PaLM 2")) # Sets the bot's status
  print(f'Connected to Discord!')


conversation_history = {}


@client.event
async def on_message(message):
  if message.content.startswith("<@Bot ID>"): # Replace this with your bot ID (for example "<@1234567890>"
    user_id = message.author.id
    if not os.path.exists(f"{user_id}_history.txt"):
      with open(f"{user_id}_history.txt", "w") as f:
        f.write("")

    with open(f"{user_id}_history.txt") as f:
      history = f.read()

    message_content = message.content.replace("<Bot ID>", "") # Same as above. Replace with your bot ID

    context = "Act like a helpful assistant named Andres" # Replace this with how you want your bot to behave.
    examples = [("Hello there", "Hi, how can I help you?"),
                ("Who are you?", "I am Andres, your helpful assitant!")] # Replace these with examples of how your bot should respond to the user input

    if len(history.splitlines()) > 50: # Set this number to the max conversation history. The longer it is, the more likely you will run into errors.
      with open(f"{user_id}_history.txt", "r+") as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines(lines[2:])

    prompt = f"{history}\nUser: {message_content}\Me: "

    response = palm.chat(
      messages=[prompt],
      context=context,
      examples=examples,
      temperature=0.9, # Set this to the temperature (described in the readme)
    )

    if response is None:
      return

    last_response = response.last.replace("\n", " - ")
    
    with open(f"{user_id}_history.txt", "a") as f:
      for line in last_response.splitlines():
        f.write(line + "\n")

    parts = [] # This splits the message into multiple parts if it is too long to avoid Discord character limit.
    while response.last is not None and len(response.last) > 2000: 
      first_half = response.last[:2000]
      second_half = response.last[2000:]
      parts.append(first_half)
      last_response = second_half
    if len(response.last) > 0:
      parts.append(response.last)
    for part in parts:
       await message.channel.send(part, reference=message)

client.run(bot_token)
