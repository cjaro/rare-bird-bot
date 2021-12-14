import discord
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
 
  if message.content.startswith(".rba"):    
    # would like to grab this from the email that goes out
    # everything in between *** and ------------ etc

    regex = r'(?<=\*\*\* )[\s\S]*.*(?=---------------------------------------------)'

    rba = (
      """
      *** Species Summary:
	    Ring-necked Pheasant (Ring-necked) (1 St. Louis)
	    Mourning Dove (2 Roseau)
	    Northern Goshawk (1 Dakota)
	    Townsend's Solitaire (1 Hennepin, 1 Stearns)
	    Dark-eyed Junco (Oregon) (2 Dakota)
	    Savannah Sparrow (5 St. Louis)
	    Yellow-rumped Warbler (1 Chisago)
	    ---------------------------------------------
      """)

    matches = re.finditer(regex, rba, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
      print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

      await message.channel.send("[eBird Alert] Minnesota Rare Bird Alert <daily>\n" + f"{match.group()}") 

  if "--detail" in message.content:
    # ideally this would just match the species name in the main body of the email
    await message.channel.send("""
    Ring-necked Pheasant (Ring-necked) (Phasianus colchicus [colchicus Group]) (6)
- Reported Dec 10, 2021 08:00 by Ian Galeski
- Phoenix Dragon Farm, St. Louis, Minnesota
- Map: http://maps.google.com/?ie=UTF8&t=p&z=13&q=47.035888,-92.765103&ll=47.035888,-92.765103
- Checklist: https://ebird.org/checklist/S98744891
- Comments: "Walking in woods near our barn"
""")

client.run(os.getenv('TOKEN'))
