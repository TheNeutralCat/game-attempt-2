import time
import random
import json
from objects import *
from lists import *
from functions import *
from roomdata import roomData
from sequences import inFight

gameVersion = "v0.1"
debugMode = False

with open("roomitemdata.json", "w") as json_file:
  json.dump({"(0, 0)": [["wornPack","baseballBat","largePack","holdingBag"],100],"(0, 1)":[[],10],"(666, 666)": [["holdingBag"]]}, json_file)
  #THE DEFAULT DROPPED ITEMS FOR ROOMS. IF YOU WANT TO ADD A ROOM WITH A KEY ITEM IN IT, YOU NEED TO CHANGE THIS DICTIONARY

playerX = 0
playerY = 0
playerMoney = 3
playerHealth = 100
playerInventory = []
playerEquipped = {"head":"EMPTY","chest":"EMPTY","legs":"EMPTY","feet":"EMPTY"}
playerBag = itemData["pockets"]

firstTimeEnteringRoom = True




print('\033[95mMESSAGE OF THE DAY\n\033[0mUse "cls" to clear the screen and reduce clutter\033[0m\n\n')




while True:
  playerCoords = (playerX,playerY)

  if firstTimeEnteringRoom == True:
    print(getRoomName(playerCoords, roomData))
    print(getRoomDesc(playerCoords, roomData))
    print(printRoomExits(playerCoords, roomData))
    getRoomItems(playerCoords, itemData)
    currentRoomItems = getRoomItems.currentRoomItems
    firstTimeEnteringRoom = False


  #############################
  playerInput = input(">> ") ##
  #############################
  #      the sacred line      



  if playerInput.lower() in look:
    print(getRoomName(playerCoords, roomData))
    print(getRoomDesc(playerCoords, roomData))
    print(printRoomExits(playerCoords, roomData))
    getRoomItems(playerCoords, itemData)


  if playerInput.lower() in clear:
    clearConsole()
    firstTimeEnteringRoom = True

  
  if playerInput.lower() == "fight":
    inFight(playerCoords, playerInventory)


  elif playerInput.lower().startswith("debug") == True:
    if playerInput[6:].lower() == "on" or playerInput[6:].lower() == "enable":
      if debugMode == True:
        print("\033[31mDebug is already enabled!\033[0m")
      else:
        print("\033[93mDebug mode: \033[92mon \033[2m(this will print a lot of text when calling functions)\033[0m")
        debugMode = True
    elif playerInput[6:].lower() == "off" or playerInput[6:].lower() == "disable":
      if debugMode == False:
        print("\033[31mDebug is already disabled!\033[0m")
      else:
        print("\033[93mDebug mode: \033[31moff\033[0m")
        debugMode = False
    elif debugMode == True:
      print("\033[93mDebug mode: \033[31moff\033[0m")
      debugMode = False
    elif debugMode == False:
      print("\033[93mDebug mode: \033[92mon \033[2m(this will print a lot of text when calling functions)\033[0m")
      debugMode = True




  elif playerInput.lower() in inventory:
    print(f"\033[95m--------- {playerBag.name} ---------\033[0m")
    currentItem = 0
    tempList = []
    tempString = ", "
    while True:
      try:
        tempList.append(playerInventory[currentItem].name)
        currentItem += 1
        time.sleep(0.05)
      except IndexError:
        currentItem = 0
        tempList = tempString.join(tempList)
        print("\033[95mITEMS:\033[0m",tempList)
          
        filledRatio = int(len(playerInventory))/int(playerBag.itemValue)*100
        #CALCULATES THE PERCENTAGE OF HOW FULL THE BAG IS

        color = ""
        if filledRatio >= 80:
          color = "\033[31m" #red
        elif filledRatio >= 60:
          color = "\033[93m" #yellow
        elif filledRatio <= 60:
          color = "\033[92m" #green
            
        print(f"\033[95mCAPACITY: \033[0m({color}{len(playerInventory)}/{playerBag.itemValue}\033[0m)")
        print(f"\033[95mWALLET: \033[93;4m${playerMoney}\033[0m")
        print(f"\033[95m--------- {playerBag.name} ---------\033[0m")
        break
  



  elif playerInput.lower() in helpList:
    maxLength = len(helpText)
    currentItemCount = 0
    while True:
      try:
        print(helpText[currentItemCount])
        time.sleep(0.05)
        currentItemCount += 1
      except:
       break
  



  elif playerInput.lower() in mapList:
    print("playerX =",playerX)
    print("playerY =",playerY)
    print("playerCoords =",playerCoords)
  



  elif playerInput.lower() == "date":
    time.sleep(0.05)
    print(f"\033[0mThe time is \033[93m{getTime('US/Pacific')} \033[2m(US/Pacific)\033[0m ")




  elif playerInput.lower().startswith("get") == True:
    try: bagCapacity = playerBag.itemValue
    except AttributeError:
      print("\033[31mDEBUG: Cannot retrieve value for player's bag slot (AttributeError).\033[0m")
      bagCapacity = 2
      #checks to see if you can pick up an item or not

    if len(playerInput) <= 4:
      print("\033[31mUsage: get [item name] (non-case sensitive): pick up a specific item from the room.\033[0m")
    else:
      if playerInput[4:5] == "$":
        getMoney(playerInput, playerCoords, playerInventory, currentRoomItems, playerMoney, debugMode)

        if getMoney.functionSuccess == True:
          playerMoney = getMoney.playerMoney
          currentRoomItems = getMoney.currentRoomItems
      else:
        if len(playerInventory) < bagCapacity:
          getItem(playerInput, playerCoords, playerInventory, currentRoomItems, playerBag, playerMoney, debugMode)
          
          if getItem.functionSuccess == True:
            playerInventory = getItem.playerInventory
            currentRoomItems = getItem.currentRoomItems
            playerBag = getItem.playerBag
        else:
          print(f"\033[31mYou can't carry any more! ({len(playerInventory)}/{bagCapacity})\033[0m")
      
      



  elif playerInput.lower().startswith("drop") == True:
    if len(playerInput) <= 5:
      print("\033[31mUsage: drop [item name] (non-case sensitive): drop one of your items in the current room.\033[0m")
    else:
      dropItem(playerInput, playerCoords, playerInventory, itemData, currentRoomItems, playerMoney)
      if dropItem.functionSuccess == True:
        playerInventory = dropItem.playerInventory
        currentRoomItems = dropItem.currentRoomItems
        playerMoney = dropItem.playerMoney
        





  elif playerInput.lower().startswith("equip") == True:
    if len(playerInput) <= 6:
      print("\033[31mUsage: equip [item name] (non-case sensitive): equip an item from your inventory (removes it from your inventory).\033[0m")
    else:
      playerInput = playerInput[6:]
      currentItem = 0
      loop = False
      while True:
        try:
          if playerInput == playerInventory[currentItem].name.lower():
            loop = True
            break
          else:
            currentItem += 1
        except IndexError:
          break
      #this function determines whether the player has the item they requested to equip in their inventory
      if loop == True:
        currentEquip = playerInventory.pop(currentItem)
        currentItem = 0
        try:
          equip_region = currentEquip.equip_region
          print(equip_region)
        except AttributeError:
          print("\033[31mDEBUG: Item cannot be equipped, no equip region value given.\033[0m")
          playerInventory.append(currentEquip)
          equip_region = "empty"
        
        if len(playerEquipped[equip_region]) != 0:
          equip_region = "none"

          if equip_region.lower() == "head":
            playerHead.append(currentEquip)
          elif equip_region.lower() == "chest":
            playerChest.append(currentEquip)
          elif equip_region.lower() == "legs":
            playerLegs.append(currentEquip)
          elif equip_region.lower() == "feet":
            playerFeet.append(currentEquip)
          elif equip_region.lower() == "bag":
            playerBag.append(currentEquip)

        else:
          print("\033[31mYou already have something equipped there!\033[0m")
          playerInventory.append(currentEquip)
      
      else:
        print("\033[31mYou don't have",str(playerInput)+"\033[0m")

  elif playerInput.lower() == "move":
    print("\033[92mUse N,S,E,W to move north, south, east, or west.\033[0m")

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




  elif playerInput.lower().startswith("save") == True:
    printSaveSlotList()
    saveInput = input("\033[92mChoose a slot to save to: (1-3)\n>> ")
    print("\033[0m",end="\r")
    
    saveProgress(saveInput, playerX, playerY, playerMoney, playerInventory)
    



  elif playerInput.lower().startswith("load") == True:
    printSaveSlotList()
    if printSaveSlotList.allEmpty == True:
      print("\033[31mNo saves to load!\033[0m")
    else:
      loadInput = input("\033[93mChoose a file to load: (1-3)\n>> ")
      print("\033[0m",end="\r")
      loadProgress(loadInput, debugMode)
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

  
  elif playerInput.lower().startswith("clear") == True:
    printSaveSlotList()
    
    if printSaveSlotList.allEmpty == False:
      deleteSlotInput = input("\033[31mChoose a slot to clear: (1-3)\n>> ")

      if isSlotValid(deleteSlotInput) == True:
        areYouSure = input("\033[93mAre you sure you want to clear this slot?: (y/n)\n>> ")
        if areYouSure == "y":
          clearSlot(deleteSlotInput)
        else:
          print("\033[92mClear cancelled.\033[0m")





  elif playerInput.lower() in north:
    if getRoomExits(playerCoords, "north", roomData) == True:
      playerY = playerY + 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the NORTH.\033[00m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])
  
  elif playerInput.lower() in south:
    if getRoomExits(playerCoords, "south", roomData) == True:
      playerY = playerY - 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the SOUTH.\033[00m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])
  
  elif playerInput.lower() in east:
    if getRoomExits(playerCoords, "east", roomData) == True:
      playerX = playerX + 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the EAST.\033[00m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])
  
  elif playerInput.lower() in west:
    if getRoomExits(playerCoords, "west", roomData) == True:
      playerX = playerX - 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the WEST.\033[00m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])