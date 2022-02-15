import time, random, json, sys
from objects import *
from lists import *
from functions import *
from roomdata import roomData
from sequences import introSequence, inFight

Cursor.show()

gameName = "game-attempt-2.py"
gameVersion = "0.1"
debugMode = False
doIntroSequence = False

with open("roomobjectdata.json", "w") as json_file:
  json.dump({"(0, 0)": [["wornPack"]],"(0, 1)":[["rustyPipe"]],"(666, 666)": [["holdingBag"]]}, json_file)
  #THE DEFAULT DROPPED ITEMS FOR ROOMS. IF YOU WANT TO ADD A ROOM WITH A KEY ITEM IN IT, YOU NEED TO CHANGE THIS DICTIONARY

playerX = 0
playerY = 0
playerInventory = []
playerName = "Player" #default (if one is not set from previous save file or introSequence)

if doIntroSequence == True:
  introSequence(gameVersion, debugMode, gameName)
  playerName = introSequence.playerName
#health maxhealth money level xp color
player = Player(playerName, 25, 0, 1, 0, rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)), itemData["empty"], itemData["empty"], itemData["empty"], itemData["empty"], itemData["pockets"])

firstTimeEnteringRoom = True

while True:
  playerCoords = (playerX,playerY)
  getRoomExits(playerCoords, roomData)

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


  elif playerInput.lower() == "cls":
    clearConsole()
    firstTimeEnteringRoom = True


  
  elif playerInput.lower() == "rgb":
    currentItem = 0
    while True:
      Cursor.hide()
      print(f"\033[2K\r\033[38;2;{255-currentItem};{currentItem};{255-currentItem}m16 million colors! [{currentItem}]\033[0m",end="")
      time.sleep(0.01)
      if currentItem == 255: forwards = False
      if currentItem == 0: forwards = True
      if forwards == True: currentItem += 1
      else: currentItem -= 1
    Cursor.show()
  


  elif playerInput.lower().startswith("beep ") == True:
    try: playerInput = int(playerInput[5:])
    except ValueError: pass
    time.sleep(0.5)
    if int(playerInput) > 1000:
      print("\033[31mhttps://www.cdc.gov/nceh/hearing_loss/how_does_loud_noise_cause_hearing_loss.html\033[0m")
    elif int(playerInput) > 100:
      print("\033[31mToo loud!\033[0m")
    elif int(playerInput) > 0:
      beep(playerInput)

  
  elif playerInput.lower().startswith("xp") == True:
    try: playerInput = int(playerInput[3:])
    except ValueError: print("\033[31mInvalid number!\033[0m")

    player = addPlayerXp(player, playerInput)
    print(f"\033[92mGiven player {placeValue(playerInput)} xp points!\033[0m")
    

  
  elif playerInput.lower() == "fight":
    inFight(playerCoords, playerInventory, player, enemyData["greenSlime"])
    player = inFight.player
    firstTimeEnteringRoom = True


  elif playerInput.lower().startswith("debug") == True:
    if debugMode == True:
      print("\033[93mDebug mode: \033[31moff\033[0m")
      debugMode = False
    elif debugMode == False:
      print("\033[93mDebug mode: \033[92mon \033[2m(this will print a lot of text when calling functions)\033[0m")
      debugMode = True



  elif playerInput.lower() == "roomitems":
    print(f"currentRoomItems: {currentRoomItems}")


  
  elif playerInput.lower() == "name":
    print("What would you like to be called?")
    while True:
      playerInput = input("> ")
      
      if len(playerInput) > 20:
        print("\033[31mName is too long!\033[0m")
      elif len(playerInput) <= 2:
        pint("\033[31mName is too short!\033[0m")
      else:
        player.name = properNoun(playerInput)
        print(f"Ok, I will call you {player.color}{player.name}.\033[0m")
        break



  elif playerInput.lower() in inventory:
    tempList = []
    tempString = ", "
    for x in playerInventory:
      tempList.append(x.name)
    tempList = tempString.join(tempList)
          
    filledRatio = len(playerInventory)/int(player.bag.itemValue)*100
    #CALCULATES THE PERCENTAGE OF HOW FULL THE BAG IS
    
    color = percentageToColor(filledRatio, True)
    
    print(f"\033[95m--------- {player.bag.name} ---------\033[0m")
    print(f"\033[95mITEMS: \033[0m{tempList}")
    print(f"\033[95mCAPACITY: \033[0m({color}{len(playerInventory)}/{player.bag.itemValue}\033[0m)")
    print(f"\033[95mWALLET: \033[93;4m${placeValue(player.money)}\033[0m")
    print(f"\033[95m--------- {player.bag.name} ---------\033[0m")
  



  elif playerInput.lower().startswith("stat") == True:
    levelUpPersentage = player.xp/xpToLevelUp(player.level)*100

    print(f"\033[95m--------- {player.name} ---------\033[0m")
    print(f"\033[95mLEVEL: {placeValue(player.level)}")
    print(statusBar(levelUpPersentage, 20+len(player.name), "\033[92m", "\033[90m"))
    print(f"\033[95mXP: {player.xp}/{xpToLevelUp(player.level)}")
    print(f"\033[95m--------- {player.name} ---------\033[0m")




  elif playerInput.lower() in helpList:
    for x in helpText:
      print(x)
      time.sleep(0.05)



  elif playerInput.lower() in mapList:
    print("playerX =",playerX)
    print("playerY =",playerY)
    print("playerCoords =",playerCoords)
  



  elif playerInput.lower() == "date":
    time.sleep(0.05)
    print(f"\033[0mThe time is \033[93m{getTime('US/Pacific')} \033[2m(US/Pacific)\033[0m ")




  elif playerInput.lower().startswith("get") == True:
    try: bagCapacity = player.bag.itemValue
    except AttributeError:
      print("\033[31mDEBUG: Cannot retrieve value for player's bag slot (AttributeError).\033[0m")
      bagCapacity = 2
      #checks to see if you can pick up an item or not

    if len(playerInput) <= 4:
      print("\033[31mUsage: get [item name] (non-case sensitive): pick up a specific item from the room.\033[0m")
    else:
      if playerInput[4:5] == "$":
        getMoney(playerInput, playerCoords, playerInventory, currentRoomItems, player.money, debugMode)

        if getMoney.functionSuccess == True:
          player.money = getMoney.playerMoney
          currentRoomItems = getMoney.currentRoomItems
      else:
        if len(playerInventory) < bagCapacity:
          getItem(playerInput, playerCoords, playerInventory, currentRoomItems, player.bag, player.money, itemData, debugMode)
          
          if getItem.functionSuccess == True:
            playerInventory = getItem.playerInventory
            currentRoomItems = getItem.currentRoomItems
            player.bag = getItem.playerBag
        else:
          print(f"\033[31mYou can't carry any more! ({len(playerInventory)}/{bagCapacity})\033[0m")
      
      



  elif playerInput.lower().startswith("drop") == True:
    if len(playerInput) <= 5:
      print("\033[31mUsage: drop [item name] (non-case sensitive): drop one of your items in the current room.\033[0m")
    else:
      if playerInput[5:6] == "$":
        dropMoney(playerInput, playerCoords, playerInventory, currentRoomItems, player.money, debugMode)

        if dropMoney.functionSuccess == True:
          player.money = dropMoney.playerMoney
          currentRoomItems = dropMoney.currentRoomItems
      else:
        #checks if inventory size is less than bag capacity
        dropItem(playerInput, playerCoords, playerInventory, itemData, currentRoomItems, player.money, debugMode)
          
        if dropItem.functionSuccess == True:
          playerInventory = dropItem.playerInventory
          currentRoomItems = dropItem.currentRoomItems
        





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
            player.bag.append(currentEquip)

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
    
    saveProgress(saveInput, playerX, playerY, player.money, playerInventory)
    



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
          player.money = int(loadProgress.playerMoney)
          playerInventory = loadProgress.playerInventory
          firstTimeEnteringRoom = True
          print("\033[92mLoaded successfully!\033[0m")
      except:
        print("\033[31mCould not update player variables to loaded values.\033[0m")

  


  
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
    if getRoomExits.north == True:
      playerY = playerY + 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the NORTH.\033[0m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])
  
  elif playerInput.lower() in south:
    if getRoomExits.south == True:
      playerY = playerY - 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the SOUTH.\033[0m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])
  
  elif playerInput.lower() in east:
    if getRoomExits.east == True:
      playerX = playerX + 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the EAST.\033[0m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])
  
  elif playerInput.lower() in west:
    if getRoomExits.west == True:
      playerX = playerX - 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the WEST.\033[0m")
    else:
      try:
        print(bumpList[random.randint(0,6)])
      except:
        print(bumpList[0])