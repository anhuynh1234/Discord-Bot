"""
Inspired from freecodecamp's https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

motivatonal quotes taken from api https://type.fit/api/quotes
"""
from replit import db
import discord
# import os
import json
import requests
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
starter_encouragements = [
  "Cheer up!", "Hang in there.", "You are a great person!"
]

if 'responding' not in db.keys():
  db['responding'] = 'on'

def quote():

  quotes = dict()
  rq = requests.get("https://type.fit/api/quotes")
  
  json_data = json.loads(rq.text)
  
  for i in json_data:
    if i['text'] not in list(quotes.keys()):
      quotes[i['text']] = i['author']
  
  quote_random = random.choice(list(quotes.keys()))
  
  return('"' + quote_random + '" - '  + quotes[quote_random])

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
    
  if message.content.startswith('$hello') and db['responding'] == 'on':
    await message.channel.send('Hello!')
    
  if any(y in ['inspire', 'motivate'] for y in list(message.content[1:].lower().split())) and db['responding'] == 'on':
    await message.channel.send(quote())
    
  msg = message.content[1:].lower()

  options = starter_encouragements
  
  if any([x in sad_words for x in list(msg.split())]) and db['responding'] == 'on':
    await message.channel.send((random.choice(options)))
      
  if "encouragements" in db.keys():
    options = options + list(db["encouragements"])
    
  if message.content.startswith("$new"):
    encouraging_message = message.content.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if message.content.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(message.content.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if message.content.startswith('$response'):
    if message.content.split()[1] == 'on':
      db['responding'] = 'on'
      await message.channel.send("Response is now on.")
    elif message.content.split()[1] == 'off':
      db['responding'] = 'off'
      await message.channel.send("Response is off.")

client.run(
  'MTA2MzE2OTYyOTQ0ODU4MTIwMQ.GgPhgk.HzKbiraUGHhI4gr3eOwVSpEWZRfIbT84N3wIBs')
