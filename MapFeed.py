import requests
import json
import time
from bs4 import BeautifulSoup
from MapFeedClasses import *

#Open the config
def openConfig():
    with open('config.txt','r') as config_file:
        config = json.load(config_file)
    config_file.close()
    #openConfig()[0]["Osu!Key"] to get osu api key
    #openConfig()[0]["Webhook"] to get webhook
    return config


#Checks for an update 
def mapCheck(url, OldMaps):
        r = connectionCheck(url)
        #Seeing if a new beatmap has been ranked, using the URLs as identifiers
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            soup2 = soup.find("script", {"id":"json-events"})   #Gets information from the first ranked beatmap on the page
            SoupSplit = list(soup2)                             #Splits it so we can get the URL of the beatmap
            GetInfo = json.loads(SoupSplit[0])                  #This cleans up the data and turns it into a json file to work with

        except:
            return None
        #Setups up an array to identify new maps
        NewMaps = [None]
        
        #This takes the first 5 items from the GetInfo array
        for i in range(0,5):
            NewMaps.insert(0,GetInfo[i])                    #This adds the value being searched to the NewMaps array
            for j in range(0,len(OldMaps)):
                #if its found in OldMaps
                if GetInfo[i]['id'] == OldMaps[j]:
                    NewMaps.remove(GetInfo[i])              #It gets deleted


        #if new maps are found
        if NewMaps != [None]:
            #Adds all NewMaps to the OldMaps array
            for i in range(len(NewMaps)-1):
                MapID = NewMaps[i]['beatmapset']['id']          #Gets the ID of the map
                EventID = NewMaps[i]['id']
                OldMaps.insert(0 , EventID)
                OldMaps.pop(5)                             #This keeps the length of the array low and stops it going on forever

                MapEvent = NewMaps[i]['type']

                if MapEvent == "nominate":
                    if i < (len(NewMaps)-2) :                       #This makes sure the next map isn't out of range
                        if NewMaps[i+1]['type'] == "qualify":
                            MapEvent = Qualified(MapID, EventID)      #Maps qualified have an eventID of +1 of the 2nd nomination 
                            MapEvent.sendHook()

                        else:
                            MapEvent = Nomination(MapID, EventID)
                            MapEvent.sendHook()

                
                    else:
                        MapEvent = Nomination(MapID, EventID)
                        MapEvent.sendHook()
                        
                #Qualify stays as an event so errors can still be caught if beatmaps/events changes in anyway
                elif MapEvent == "qualify":
                    next

                elif MapEvent == "rank":
                    MapID = NewMaps[i]['beatmapset']['id'] 
                    MapEvent = Ranked(MapID, EventID)
                    MapEvent.sendHook()

                elif MapEvent == "disqualify":
                    MapEvent = Disqualified(MapID, EventID)       #Maps qualified have an eventID of +1 of the 2nd nomination 
                    MapEvent.sendHook()

                #Nomination reset
                elif MapEvent == "nomination_reset":
                    MapEvent = Problem(MapID, EventID)        #Maps qualified have an eventID of +1 of the 2nd nomination 
                    MapEvent.sendHook()

                else:
                    print("error")


        else:
            time.sleep(20)
    
#Check Modding Discussions
def checkModDisc(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup2 = soup.find("script", {"id":"json-beatmapset-discussion"}).text
    soupJson = json.loads(soup2)
    cleanSoup = soupJson['beatmapset']['events']

    return cleanSoup

#Get the information from the beatsmap
def getMapInfo(mapID):
    APIKey = openConfig()[0]["Osu!Key"]
    MapURL = "http://osu.ppy.sh/api/get_beatmaps?k={}&s={}".format(APIKey, mapID)
    r = requests.get(MapURL)
    mapInfo = list(r.json())
    return mapInfo

def getUserInfo(userID):
    APIKey = openConfig()[0]["Osu!Key"]
    NomURL = "http://osu.ppy.sh/api/get_user?k={}&u={}".format(APIKey, userID)
    r = requests.get(NomURL)
    userInfo = list(r.json())
    return userInfo

def getDiscussion(mapID, EventID):
        #Checking the modding disscussion
        URL = "https://osu.ppy.sh/beatmapsets/{}/discussion".format(mapID)

        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        soup2 = soup.find("script", {"id":"json-beatmapset-discussion"}).text

        #Turns it into a json to work with
        setJson = json.loads(soup2)

        js = setJson['beatmapset']['events']
        for j in range(len(js)):
            if js[j]['id'] == EventID:
                dqPostID = js[j]['comment']['beatmap_discussion_post_id']

        return dqPostID
        
def connectionCheck(url):
    try:
        r = requests.get(url)
        return r

    except:
        print("No Connection")
        
    
