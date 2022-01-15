def getRoomName(playerCoords):
  from roomdata import roomData
  try:
    roomName = roomData[str(playerCoords)]
    return roomName[0]
  except KeyError:
    return "\033[93mDEBUG: no room name exists for current room\033[0m"

def getRoomDesc(playerCoords):
  from roomdata import roomData
  try:
    roomDesc = roomData[str(playerCoords)]
    return roomDesc[1]
  except KeyError:
    return "\033[93mDEBUG: no room description exists for current room\033[0m"

def getRoomExits(playerCoords, desiredExitValue):
  from roomdata import roomData
  try:
    exits = roomData[str(playerCoords)]
    exits = exits[2]
  except KeyError:
    exits = "1111"

  exitList = []
  exitList[:0] = exits
  #breaks down "1011" into "north = true, south = false" etc

  canMoveNorth = canMoveSouth = canMoveEast = canMoveWest = False

  if exitList[0] == "1":
    canMoveNorth = True
  if exitList[1] == "1":
    canMoveSouth = True
  if exitList[2] == "1":
    canMoveEast = True
  if exitList[3] == "1":
    canMoveWest = True
  
  if desiredExitValue.lower() == "north":
    return canMoveNorth
  if desiredExitValue.lower() == "south":
    return canMoveSouth
  if desiredExitValue.lower() == "east":
    return canMoveEast
  if desiredExitValue.lower() == "west":
    return canMoveWest
  return False

def getRoomItems(playerCoords, convertItems):
  from items import itemData
  import json
  with open("roomitemdata.json") as json_file:
    try:
      loadedjsondata = json.load(json_file)
    except:
      print('\033[93mDEBUG: Failed to load file "roomitemdata.json"\033[0m')
      return
    
  try:
    roomItems = loadedjsondata[str(playerCoords)]
  except KeyError:
    return

  if convertItems == True:
    from items import itemData
    currentItem = 0
    export = []
    while currentItem <= len(roomItems):
      try:
        export.append(itemData[roomItems[currentItem]])
      except IndexError:
        return export
      currentItem += 1
      #CONVERTS THE LIST OF NAMES STORED IN THE ROOM TO A LIST OF OBJECTS AND RETURNS IT
  
  currentItem = 0
  loop = True
  while loop == True:
    try:
      globals()[f"item{currentItem}"] = itemData[str(roomItems[currentItem])]
    except IndexError:
      loop = False
    except KeyError:
      globals()[f"item{currentItem}"] = "???"
    currentItem += 1
    #I have no idea what this is or why it works but it dynamically creates variables (ex. "item1" "item2" "item3") chronologically

  currentItem = 0
  loop = True
  roomItemsText = []
  while loop == True:
    try:
      roomItemsText.append(globals()[f"item{currentItem}"].name)
    except KeyError:
      loop = False
    except AttributeError:
      print("\033[93mDEBUG: A room object failed to load as it does not have a definition within items.py.\033[0m")
    currentItem += 1
  
  itemString = "\033[35m, "
  totalListItems = len(roomItemsText)
  if totalListItems <= 0:
    return


  if totalListItems > 5:
    tempList = []
    currentItem = 0
    while currentItem <= 5:
      try:
        tempList.append(roomItemsText[currentItem])
      except IndexError:
        pass
      currentItem += 1
    roomItemsText = itemString.join(tempList)
    print("\033[95m"+"Items:\033[35m",str(roomItemsText)+"..."+"\033[0m")
  else:
    roomItemsText = itemString.join(roomItemsText)
    print("\033[95m"+"Items:\033[35m",str(roomItemsText)+"\033[0m")

def printRoomExits(playerCoords):
  from roomdata import roomData
  try:
    exits = roomData[str(playerCoords)]
    exits = exits[2]
  except:
    print("\033[93mDEBUG: no room exit data for current room\033[0m")
    exits = "1111"

  exitList = []
  exitList[:0] = exits
  #breaks down "1011" into "north = true, south = false" etc

  north = south = east = west = ""

  if exitList[0] == "1":
    north = "NORTH "
  if exitList[1] == "1":
    south = "SOUTH "
  if exitList[2] == "1":
    east = "EAST "
  if exitList[3] == "1":
    west = "WEST"
  
  return "\033[92mExits: "+north+south+east+west+"\033[0m"

def isValidSlot(slot):
  try:
    slot = int(slot)
  except:
    print("\033[31mInvalid slot!\033[0m")
    return False
  
  if slot > 3:
    print("\033[31mInvalid slot!\033[0m")
    return False
  return True

def saveProgress(slot, playerX, playerY, playerMoney, playerInventory):
  import json
  try:
    slot = int(slot)
  except:
    print("\033[31mInvalid slot!\033[0m")
    return
  if slot == 1 or slot == 2 or slot == 3: pass
  else:
    print("\033[31mCannot save to file outside of slot range.\033[0m")
    return
  slot = "slot"+str(slot)+".json"
  
  try:
    saveTime = getTime('US/Pacific')
  except:
    saveTime = "\033[31mUnknown save time.\033[0m"
  
  with open("roomitemdata.json") as json_file:
    try:
      roomitemdata = json.load(json_file)
    except:
      print('\033[93mDEBUG: Failed to load file "roomitemdata.json"\033[0m')
      return

  playerInventorySaveable = []
  tempvar = 0
  loop = True
  while loop == True:
    try:
      playerInventorySaveable.append(playerInventory[tempvar].referenceName)
      tempvar += 1
    except IndexError:
      loop = False

  saveData = [saveTime, playerX, playerY, playerMoney]
  saveDict = {"playerData":saveData,"playerInventory":playerInventorySaveable,"roomItemData":roomitemdata}

  print("\033[92m\033[2mSaving...\033[0m")
  with open(slot, 'w') as f:
    json.dump(saveDict, f)

def loadProgress(slot):
  loadProgress.loadSuccess = False
  loadFailedText = "\033[31mLoad failed.\033[0m"
  try:
    slot = int(slot)
  except:
    print("\033[31mInvalid slot!\033[0m")
    return

  if slot == 1 or slot == 2 or slot == 3:
    isSlotEmpty = getSaveSlotData(slot)
    if isSlotEmpty == "Empty":
      print("\033[31mSlot is empty!\033[0m")
      return
  else:
    print("\033[31mCannot load file outside of slot range.\033[0m")
    return
  
  slotFile = "slot"+str(slot)+".json"

  print("\033[93m\033[2mLoading...\033[0m")
  try:
    import json
    with open(slotFile) as json_file:
      loadedjsondata = json.load(json_file)
  except:
    print("\033[93mDEBUG: f.open() error.\033[0m")
    return

  try:
    loadedPlayerData = loadedjsondata["playerData"]
  except:
    print("\033[31mFailed to load generic save data.\033[0m")
    print(loadFailedText)
    return
  
  try:
    loadedInventoryData = loadedjsondata["playerInventory"]
  except:
    print("\033[31mFailed to load playerInventory.\033[0m")
    print(loadFailedText)
    return
  
  #try:
  loadedRoomItemData = loadedjsondata["roomItemData"]
  with open("roomitemdata.json", 'w') as f:
    json.dump(loadedRoomItemData, f)
  #except:
    #print("\033[31mFailed to load roomItemData.\033[0m")
    #print(loadFailedText)
    #return

  try:
    loadProgress.saveTime = loadedPlayerData[0]
    loadProgress.playerX = loadedPlayerData[1]
    loadProgress.playerY = loadedPlayerData[2]
    loadProgress.playerMoney = loadedPlayerData[3]
    loadProgress.playerInventory = loadedInventoryData
  except:
    print("\033[31mDEBUG: Save file misaligned, tried to load segment that doesn't exist.\033[0m")
    print(loadFailedText)
    return

  #keep this line at the end
  loadProgress.loadSuccess = True

def getSaveSlotData(slot):
  import json
  if slot == 1:
    slot = "slot"+str(slot)+".json"
  elif slot == 2:
    slot = "slot"+str(slot)+".json"
  elif slot == 3:
    slot = "slot"+str(slot)+".json"
  else:
    return "\033[31mFile not found.\033[0m"

  try:
    with open(slot) as json_file:
      loadedjsondata = json.load(json_file)
      loadedPlayerData = loadedjsondata["playerData"]
      return loadedPlayerData[0]
  except:
    return "Empty"

def clearSlot(slot):
  try:
    slot = int(slot)
  except:
    print("\033[31mInvalid slot!\033[0m")
    return

  if slot > 3:
    print("\033[31mInvalid slot!\033[0m")
    return

  slot = "slot"+str(slot)+".json"

  print("\033[2m\033[93mClearing slot...\033[0m")
  try:
    with open(slot, "w") as f:
      f.write("")
  except:
    print("\033[31mSlot is already empty!\033[0m")
    return
  print("\033[92mSlot cleared!\033[0m")

def printSaveSlotList():
  slot1 = "Slot 1 - "+getSaveSlotData(1)
  slot2 = "Slot 2 - "+getSaveSlotData(2)
  slot3 = "Slot 3 - "+getSaveSlotData(3)
  
  slot1Empty = slot2Empty = slot3Empty = False

  print()
  if slot1 != "Slot 1 - Empty":
    print(slot1)
  else:
    print("\033[2m"+slot1+"\033[0m")
    slot1Empty = True
    
  if slot2 != "Slot 2 - Empty":
    print(slot2)
  else:
    print("\033[2m"+slot2+"\033[0m")
    slot2Empty = True

  if slot3 != "Slot 3 - Empty":
    print(slot3)
  else:
    print("\033[2m"+slot3+"\033[0m")
    slot3Empty = True
  print()
  
  if slot1Empty == True and slot2Empty == True and slot3Empty == True:
    printSaveSlotList.allEmpty = True
    return
  printSaveSlotList.allEmpty = False

def commandValidity(playerCoords):
  from roomdata import roomMetaData, roomCommands
  zoneMetaData = roomMetaData[str(playerCoords)]
  cmdMetaData = roomCommands[zoneMetaData]
  print(cmdMetaData)

def getTime(timeZone):
  from datetime import date, datetime
  import pytz

  today = date.today()

  tz = pytz.timezone(timeZone)
  datetime_tz = datetime.now(tz)

  hour = int(datetime_tz.strftime("%H"))
  minute = int(datetime_tz.strftime("%M"))

  if hour > 12:
    hour -= 12
    meridiem = "PM"
  else:
    meridiem = "AM"
  
  if minute < 10:
    minute = "0"+str(minute)

  try:
    return str(hour)+":"+str(minute)+meridiem+", "+str(today)
  except:
    return "\033[31mFailed to retrieve date.\033[0m"

def printColor(string, color):
  if color.lower() == "red":
    print("\033[31m"+str(string)+"\033[0m") #red
  elif color.lower() == "ltred":
    print("\033[91m"+str(string)+"\033[0m") #light red
  elif color.lower() == "yellow":
    print("\033[93m"+str(string)+"\033[0m") #yellow
  elif color.lower() == "drkyellow":
    print("\033[33m"+str(string)+"\033[0m") #dark yellow
  elif color.lower() == "green":
    print("\033[92m"+str(string)+"\033[0m") #green
  elif color.lower() == "drkgreen":
    print("\033[32m"+str(string)+"\033[0m") #dark green
  elif color.lower() == "blue":
    print("\033[34m"+str(string)+"\033[0m") #blue
  elif color.lower() == "ltblue":
    print("\033[94m"+str(string)+"\033[0m") #light blue
  elif color.lower() == "cyan":
    print("\033[96m"+str(string)+"\033[0m") #cyan
  elif color.lower() == "drkcyan":
    print("\033[36m"+str(string)+"\033[0m") #dark cyan
  elif color.lower() == "magenta":
    print("\033[95m"+str(string)+"\033[0m") #magenta
  elif color.lower() == "drkmagenta":
    print("\033[35m"+str(string)+"\033[0m") #dark magenta
  elif color.lower() == "black":
    print("\033[90m"+str(string)+"\033[0m") #black