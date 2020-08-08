import MapFeed

def getAll(mapID):
    mapInfo = MapFeed.getMapInfo(mapID)

    data = []  
    data.append({  
        'BPM': getBPM(mapInfo),
        'Length': getLength(mapInfo),
        'GMFormat': getGamemodes(mapInfo),
        'GMFormat2': getGameInfo(mapInfo)
    })

    return data

def getBPM(mapInfo):
    BPM = mapInfo[0]['bpm']

    return BPM

def getLength(mapInfo):
    TotalLength = int(mapInfo[0]['total_length']) 
    #Getting Map Length
    Minutes = str(int(TotalLength//60)) #Converts to a string for later use
    Seconds = str(int(TotalLength%60))

    #Prevents map from ending up looking like 2:2 if it is 2 minutes and 2 seconds long
    if len(Seconds) != 2:
        Seconds = "0"+Seconds

    #Creates string to be used in the message
    Length = Minutes+":"+Seconds

    return Length

def getGamemodes(mapInfo):
    gamemode = getMapsetType(mapInfo)

    #This takes it out of a list and turns it into a usable format without the square brackets
    GM = ", ".join(gamemode)
    #Sets up format for if there is 1 gamemode present
    GMFormat = "hybrid" #this helps reduce lines of code later on
    if len(gamemode) == 1:
        GMFormat = GM

        return GMFormat
    
    else:
        return GMFormat

def getMapsetType(mapInfo):
    #Getting the gamemodes avaliable to play              
    #Set all values to 0
    std = tko = ctb = man = 0

    #Getting all gamemodes avaliable
    for x in range(0,len(mapInfo)):
        Mode = mapInfo[x]['mode']

        if Mode == "0": #Standard
            std += 1

        if Mode == "1": #Taiko
            tko += 1

        if Mode =="2": #CTB
            ctb += 1

        if Mode == "3": #Mania
            man += 1

    #Create an array for the gamemodes
    gamemode = []
    gamemode = list(gamemode)

    #Adding each gamemode to the array if its present in mapset
    if man >= 1:
        gamemode.insert(0,"osu!mania")

    if ctb >= 1:
        gamemode.insert(0,"osu!catch")

    if tko >= 1:
        gamemode.insert(0,"osu!taiko")

    if std >= 1:
        gamemode.insert(0,"osu!standard")

    return gamemode

def getGameInfo(mapInfo):
    gamemode = getMapsetType(mapInfo)
    #Set all values to 0
    std = tko = ctb = man = 0
    
    #Getting all gamemodes avaliable
    for x in range(0,len(mapInfo)):
        Mode = mapInfo[x]['mode']

        if Mode == "0": #Standard
            std += 1

        if Mode == "1": #Taiko
            tko += 1

        if Mode =="2": #CTB
            ctb += 1

        if Mode == "3": #Mania
            man += 1

    GM = getGamemodes(mapInfo)
    
    if len(gamemode) == 1:
        GMFormat = GM

        if GM == "osu!standard":
            if std >= 1:
                GMFormat2 = "● {} {} difficulties".format(str(std), GM)
            else:
                GMFormat2 = "● {} {} difficulty".format(str(std), GM)
            
        elif GM == "osu!taiko":
            if tko >= 1:
                GMFormat2 = "● {} {} difficulties".format(str(tko), GM)
            else:
                GMFormat2 = "● {} {} difficulty".format(str(tko), GM)
        elif GM =="osu!catch":
            if ctb >= 1:
                GMFormat2 = "● {} {} difficulties".format(str(ctb), GM)
            else:
                GMFormat2 = "● {} {} difficulty".format(str(ctb), GM)
        elif GM =="osu!mania":
            if man >= 1:
                GMFormat2 = "● {} {} difficulties".format(str(man), GM)
            else:
                GMFormat2 = "● {} {} difficulty".format(str(man), GM)

    elif len(gamemode) == 2:
        GM1 = ""
        GM2 = ""
        if std >= 1:
            GM1 = "osu!standard"
            val1 = std

        if tko >= 1:
            if len(GM1) != 0:
                GM2 = "osu!taiko"
                val2 = tko
            else:
                GM1 = "osu!taiko"
                val1 = tko

        if ctb >= 1:
            if len(GM1) > 3:
                GM2 = "osu!catch"
                val2 = ctb
            else:
                GM1 = "osu!catch"
                val1 = ctb

        if man >= 1:
            GM2 = "osu!mania"
            val2 = man

        GMFormat2 = """● {} {}
● {} {}""".format(val1, GM1, val2, GM2)


    elif len(gamemode) == 3:
        GM1 = ""
        GM2 = ""
        GM3 = ""
        
        if std > 1:
            GM1 = "osu!standard"
            val1 = std

        if tko > 1:
            if len(GM1) > 3:
                GM2 = "osu!taiko"
                val2 = tko
            else:
                GM1 = "osu!taiko"
                val1 = tko

        if ctb > 1:
            if len(GM2) > 3:
                GM3 = "osu!catch"
                val3 = ctb
            else:
                GM2 = "osu!catch"
                val2 = ctb

        if man > 1:
            GM3 = "osu!mania"
            val3 = man

        GMFormat2 = """● {} {}
● {} {}
● {} {}""".format(val1, GM1, val2, GM2, val3, GM3)

    elif len(gamemode) == 4:
        GMFormat2 = """● {} osu!standard diffs
● {} osu!taiko diffs
● {} osu!catch diffs
● {} osu!mania diffs""".format(std,tko,ctb,man)

    return GMFormat2
