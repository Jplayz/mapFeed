import MapFeed
import RankedMap
from discord_hooks import Webhook

class Event:
    def __init__(self, beatMap, eventID):
        self.beatMap = beatMap
        self.eventID = eventID
        self.event = None
        self.color = None
        self.icon = None

    def getNominator(self):
        NomID = None
        URL = "https://osu.ppy.sh/beatmapsets/{}/discussion".format(self.beatMap)
        soupJson = MapFeed.checkModDisc(URL)
        for i in range(len(soupJson)):
            if soupJson[i]['id'] == self.eventID:
                NomID = soupJson[i]['user_id']

            else:
                next

        return NomID
        
    def sendHook(self):
        MapID = self.beatMap
        mapInfo = MapFeed.getMapInfo(self.beatMap)
        NomID = str(self.getNominator())
        NomName = MapFeed.getUserInfo(NomID)[0]['username']
        
        #Getting all the mapper information here
        MapperID = mapInfo[0]['creator_id']
        Mapper = mapInfo[0]['creator']
        Title = mapInfo[0]['title']
        Artist = mapInfo[0]['artist']
        EmbedTitle = "{} - {}".format(Artist, Title)
        Banner = "https://assets.ppy.sh/beatmaps/{}/covers/list.jpg".format(MapID)
        MapLink = "https://osu.ppy.sh/beatmapsets/{}".format(MapID)

        self.post(MapLink, EmbedTitle, Banner, Mapper, NomName, NomID, MapperID)

    def post(self, MapLink, EmbedTitle, Banner, Mapper, NomName, NomID, MapperID):
        webhook = MapFeed.openConfig()[0]["Webhook"]
    
        #Setting up a message
        embed = Webhook(webhook, color=self.color)
        embed.set_author(name='{}'.format(self.event), icon=self.icon)
        embed.set_title(title='**__{}__**'.format(EmbedTitle),url=MapLink)
        embed.set_thumbnail(Banner)
        embed.set_desc("Mapped by {}".format(Mapper))
        embed.set_footer(text='{}'.format(NomName), ts=True,icon='https://a.ppy.sh/{}'.format(NomID))
        embed.post()

class Nomination(Event):
    def __init__(self, beatMap, eventID):
        super().__init__(beatMap, eventID)
        self.event = "Nominated!"
        self.color = 0x0000FF
        self.icon = 'https://old.ppy.sh/forum/images/icons/misc/thinking.gif'
    
               
class Qualified(Event):
    def __init__(self, beatMap, eventID):
        super().__init__(beatMap, eventID)
        self.event = "Qualified!"
        self.color = 0xFFB6C1
        self.icon = 'https://osu.ppy.sh/forum/images/icons/misc/heart.gif'
    
class Disqualified(Event):
    def __init__(self, beatMap, eventID):
        super().__init__(beatMap, eventID)
        self.event = "Disqualified!"
        self.color = 0xFF0000
        self.icon = 'https://osu.ppy.sh/forum/images/icons/misc/bubblepop.png'

    def sendHook(self):
        MapID = self.beatMap
        mapInfo = MapFeed.getMapInfo(self.beatMap)
        NomID = str(self.getNominator())
        NomName = MapFeed.getUserInfo(NomID)[0]['username']

        dqPostID = MapFeed.getDiscussion(self.beatMap, self.eventID)
        
        #Getting all the mapper information here
        MapperID = mapInfo[0]['creator_id']
        Mapper = mapInfo[0]['creator']
        Title = mapInfo[0]['title']
        Artist = mapInfo[0]['artist']
        EmbedTitle = "{} - {}".format(Artist, Title)
        Banner = "https://assets.ppy.sh/beatmaps/{}/covers/list.jpg".format(MapID)
        MapLink = "https://osu.ppy.sh/beatmapsets/{}/discussion#/{}".format(MapID,dqPostID)

        self.post(MapLink, EmbedTitle, Banner, Mapper, NomName, NomID, MapperID)
    

class Problem(Disqualified):
    def __init__(self, beatMap, eventID):
        super().__init__(beatMap, eventID)
        self.event = "Nomination Reset!"
        self.color = 0xFF0000
        self.icon = 'https://osu.ppy.sh/forum/images/icons/misc/bubblepop.png'


class Ranked(Nomination):
    def __init__(self, beatMap, eventID):
        super().__init__(beatMap, eventID)

    def post(self, MapLink, EmbedTitle, Banner, Mapper, NomName, NomID, MapperID):
        webhook = MapFeed.openConfig()[0]["Webhook"]

        mapInfo = RankedMap.getAll(self.beatMap)

        embed = Webhook(webhook, color=0xFFB6C1)
        embed.set_author(name='New {} map by {}'.format(mapInfo[0]['GMFormat'], Mapper), icon='https://a.ppy.sh/{}'.format(MapperID), url='https://osu.ppy.sh/users/{}'.format(MapperID))
        embed.set_title(title='**__{}__**'.format(EmbedTitle),url=MapLink)
        embed.set_thumbnail(Banner)

        embed.set_desc("""**BPM:** {}
**Song Length:** {}
**Containing:**
{}""".format(mapInfo[0]['BPM'], mapInfo[0]['Length'], mapInfo[0]['GMFormat2']))

        embed.set_footer(text='Ranked!',ts=True,icon='https://hypercyte.s-ul.eu/W4GBjy0M')
        embed.post()

