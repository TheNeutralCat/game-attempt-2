import time
import random
import json
from items import itemData
from items import *
from commands import *
from functions import *

with open("roomitemdata_default.json", 'r') as f:
  roomitemdefaults = json.load(f)
with open("roomitemdata.json", "w") as f:
  json.dump(roomitemdefaults, f)

playerX = 0
playerY = 0
playerMoney = 0
playerInventory = []

firstTimeEnteringRoom = True

while True:
  playerCoords = (playerX,playerY)
  currentRoomItems = getRoomItems(playerCoords, True, itemData)

  if firstTimeEnteringRoom == True:
    print(getRoomName(playerCoords))
    print(getRoomDesc(playerCoords))
    print(printRoomExits(playerCoords))
    getRoomItems(playerCoords, False, itemData)
    firstTimeEnteringRoom = False
  
  ##########################
  playerInput = input(">> ")
  ##########################
  #    the sacred line     #

  if playerInput.lower() in look:
    print(getRoomName(playerCoords))
    print(getRoomDesc(playerCoords))
    print(printRoomExits(playerCoords))
    getRoomItems(playerCoords, False, itemData)
  
  elif playerInput.lower() in inventory:
    print(playerInventory)
  
  elif playerInput.lower() in helpList:
    hLoop = True
    maxLength = len(helpText)
    currentItemCount = 0
    while hLoop == True:
      try:
        print(helpText[currentItemCount])
        time.sleep(0.05)
        currentItemCount += 1
      except:
        hLoop = False
    #this code sets up a loop to print every item in the list for helpText. it's nice because you can add as much as you want to the helpText list and you don't have to worry about changing this.
  
  elif playerInput.lower() in mapList:
    print("playerX =",playerX)
    print("playerY =",playerY)
    print("playerCoords =",playerCoords)
  
  elif playerInput.lower() == "date":
    time.sleep(0.05)
    print("\033[2mThe time (US/Pacific) is \033[0m"+str(getTime('US/Pacific')))
  



  elif playerInput.lower().startswith("get ") == True:
    playerInput = playerInput[4:]
    currentItem = 0
    loop = True
    while loop == True:
      try:
        if playerInput == str(currentRoomItems[currentItem].name.lower()):
          pickedUpItem = currentRoomItems.pop(currentItem)
          print("\033[96mPicked up "+pickedUpItem.name+"!\033[0m") #picks up the player's requested object and removes it from the "currentRoomItems" list (in preperation for saving)
          currentItem += 1
          loop = False
      except IndexError:
        loop = False
        print("\033[31mYou don't see that here!\033[0m")
    loop = True
    currentItem = 0
    updatedRoomItems = []
    while loop == True:
      try:
        updatedRoomItems.append(currentRoomItems[currentItem].referenceName)
        currentItem += 1
      except IndexError:
        updatedDict = {str(playerCoords):list(updatedRoomItems)}
        loop = False
        with open("roomitemdata.json") as json_file:
          jsondata = json.load(json_file)
          newjsondata = jsondata
        try:
          with open("roomitemdata.json", "w") as json_file:
            newjsondata.update(updatedDict)
            json.dump(newjsondata, json_file)
            playerInventory.append(pickedUpItem)
            #loads the coordinate-to-room item dict, updates it by removing the item from the list, and saves it.
        except:
          with open("roomitemdata.json", "w") as json_file:
            json.dump(jsondata, json_file)
          print("\033[31mDEBUG: Fatal error updating roomitemdata.json! Changes have not been applied to prevent file corruption.\033[0m")
  
  elif playerInput.lower().startswith("drop ") == True:
    playerInput = playerInput[5:]
    currentItem = 0
    loop = True
    while loop == True:
      if playerInput == str(playerInventory[currentItem].name.lower()):
        droppedItem = playerInventory.pop(currentItem)
        print("dropped",droppedItem.name)
      else:
        currentItem += 1
      loop = False


    

  elif playerInput.lower() == "get":
    print("\033[31mUsage: get [item name] (non-case sensitive): pick up a specific item from the room.\033[0m")
  
  elif playerInput.lower() == "drop":
    print("\033[31mUsage: drop [item name] (non-case sensitive): drop one of your items in the current room.\033[0m")

  elif playerInput.lower() == "colorpallete":
    printColor("red", "red")
    printColor("ltred", "ltred")
    printColor("yellow", "yellow")
    printColor("drkyellow", "drkyellow")
    printColor("green", "green")
    printColor("drkgreen", "drkgreen")
    printColor("blue", "blue")
    printColor("ltblue", "ltblue")
    printColor("cyan", "cyan")
    printColor("drkcyan","drkcyan")
    printColor("magenta", "magenta")
    printColor("drkmagenta", "drkmagenta")
    printColor("black", "black")
  
  elif playerInput.lower() == "cl":
    pass

  elif playerInput.lower() == "save":
    printSaveSlotList()
    
    saveInput = input("\033[92mChoose a slot to save to: (1-3)\n>> ")
    print("\033[0m",end="\r")
    saveProgress(saveInput, playerX, playerY, playerMoney, playerInventory)
    
  elif playerInput.lower() == "load":
    printSaveSlotList()
    if printSaveSlotList.allEmpty == True:
      print("\033[31mNo saves to load!\033[0m")
    else:
      loadInput = input("\033[93mChoose a file to load: (1-3)\n>> ")
      print("\033[0m",end="\r")
      loadProgress(loadInput)
      try:
        if loadProgress.loadSuccess == True:
          playerX = int(loadProgress.playerX)
          playerY = int(loadProgress.playerY)
          playerMoney = int(loadProgress.playerMoney)
          firstTimeEnteringRoom = True
        
          print("\033[92mLoaded successfully!\033[0m")
      except:
        print("\033[31mCould not update player variables to loaded values.\033[0m")
      try:
        from items import itemData
        playerInventory.append(itemData[loadProgress.playerInventory[0]])
      except IndexError:
        pass
      except AttributeError:
        pass

  
  elif playerInput.lower() == "clear":
    printSaveSlotList()
    
    deleteSlotInput = input("\033[31mChoose a slot to clear: (1-3)\n>> ")
    print("\033[0m",end="\r")
    
    deleteSlotIsValid = isValidSlot(deleteSlotInput)
    if deleteSlotIsValid == True:
      deleteSlotIsValid = False
      areYouSure = input("\033[93mAre you sure you want to clear this slot?: (y/n)\n>> ")
      print("\033[0m",end="\r")
      if areYouSure == "y":
        clearSlot(deleteSlotInput)
      else:
        print("\033[92mClear cancelled.\033[0m")





  elif playerInput.lower() in north:
    if getRoomExits(playerCoords, "north") == True:
      playerY = playerY + 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the NORTH.\033[00m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])
  
  elif playerInput.lower() in south:
    if getRoomExits(playerCoords, "south") == True:
      playerY = playerY - 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the SOUTH.\033[00m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])
  
  elif playerInput.lower() in east:
    if getRoomExits(playerCoords, "east") == True:
      playerX = playerX + 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the EAST.\033[00m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])
  
  elif playerInput.lower() in west:
    if getRoomExits(playerCoords, "west") == True:
      playerX = playerX - 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the WEST.\033[00m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])