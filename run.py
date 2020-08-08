#MapFeed beta1
#By Jplayz

#Collecting all the libraries
import os
import time
import json

from MapFeed import mapCheck

#These ones need to be installed using pip so we check for the user
try:
    from bs4 import BeautifulSoup
except:
    raise RuntimeError("bs4 required: pip install bs4")
    time.sleep(10)

try:
    import requests
    from discord_hooks import Webhook
    
except:
    raise RuntimeError("requests required: pip install requests")
    time.sleep(10)

#The feed to read from
URL = "https://osu.ppy.sh/beatmapsets/events?user=&types%5B%5D=nominate&types%5B%5D=qualify&types%5B%5D=rank&types%5B%5D=nomination_reset&types%5B%5D=disqualify"
OldMaps = [None,  None , None , None, None]
#-----------------------------Checking Config File---------------------------

#Checks if a config file has been created
if os.path.exists("config.txt"):
    print("Config file is present")

#If it doesn't, generate one
else:
    print("No config file found")
    NewKey = input("What is your osu!Api Key?:")
    NewWebhook = input("What is your Discord webhook?:")
    #Putting the information into an array
    data = []  
    data.append({  
        'Osu!Key': NewKey,
        'Webhook': NewWebhook
    })

    #Dumps informfation into a file
    with open('config.txt', 'w') as outfile:  
        json.dump(data, outfile)
        outfile.close()
#-------------------------------------------------------------------------------
while True:
    mapCheck(URL,OldMaps)
    time.sleep(45)
