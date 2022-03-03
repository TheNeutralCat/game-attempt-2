import time, random, json, sys
from objects import *
from lists import *
from functions import *
from roomdata import roomDict
from sequences import menuSequence, inFight

Cursor.show()
ClearScreen.screen()

gameName = "game-attempt-2.py"
gameVersion = "0.1"

################## ROOMOBJECTDATA.JSON ##################
with open("roomobjectdata.json", "w") as json_file:
  json.dump({"(0, 0)": [["wornPack"]],"(0, 1)":[["rustyPipe"]],"(666, 666)": [["holdingBag"]]}, json_file)
  #ROOMDATA.JSON IS CREATED HERE AUTOMATICALLY. IF YOU WANT
  #TO MODIFY THE FILE, CHANGE THIS LINE
################## ROOMOBJECTDATA.JSON ##################


  
#################### SETTINGS LOADER ####################
from objects import Settings
gameSettings = Settings()
with open("options.json", "r") as json_file:
  loadOptions = json.load(json_file)
  
for x in gameSettings.varList:
  vars(gameSettings)[x] = loadOptions[x]

gameSettings.screenWidth = int(gameSettings.screenWidth)
gameSettings.doIntroSequence = toBool(gameSettings.doIntroSequence)
gameSettings.debugMode = toBool(gameSettings.debugMode)
rgbList = gameSettings.highlightColor.split(",")
gameSettings.highlightColor = f"\033[48;2;{rgbList[0]};{rgbList[1]};{rgbList[2]}m"
#use "toBool()" and not "bool()" here because bool() returns nonempty strings as True and empty strings as False (the string "False" would return True)
#################### SETTINGS LOADER ####################


playerX = 0
playerY = 0
playerName = "PlayerNameeeeee" #default
playerInventory = []

if gameSettings.doIntroSequence == True:
  menuSequence(gameVersion, gameName, gameSettings, playerName)
  playerName = menuSequence.playerName
#name health money level xp color
player = Player(playerName, 25, 0, 1, 0, "\033[92m", 0, 0, 0, 0, itemData["pockets"])




def drawMiniMap(f=False):
  Cursor.savePos()
  Cursor.moveTo()

  leftMargin = (gameSettings.screenWidth-4)//2-2
  rightMargin = math.ceil((gameSettings.screenWidth-4)/2)-2
  #cuts off the 2 border chars on each side, splits it in half,
  #and cuts off the 2 remaining border chars
  
  if (gameSettings.screenWidth % 2) == 0: #checks for even number
    healthBarLength = rightMargin-10
  else:
    healthBarLength = rightMargin-9
  #adjusts split for odd/even screen sizes

  healthPerc = (player.health/player.maxHealth)*100
  healthColor = percentageToColor(healthPerc)
  healthBar = statusBar(persentage=healthPerc,size=healthBarLength,color="\033[31m",char="❤ ")
  
  nameLength = len(player.name)
  moneyLength = len(str(player.money))+1
  if nameLength+moneyLength > 

  sys.stdout.write(f"\033[2K\r{printBorder(gameSettings.screenWidth,split=True)}\n")
  
  
  sys.stdout.write(f"\033[2K\r| {player.color}{player.name}\033[0m{space(gameSettings.screenWidth//2-4)[:-len(player.name)-len(str(player.money))-1]}\033[93m${player.money}\033[0m || ")
  #|-----------------------||
  #| PlayerName       $224 ||
  #|-----------------------||
  
  
  sys.stdout.write(f"{healthBar}     {healthColor}{player.health}/{player.maxHealth}\033[0m |\n")
  #||-----------------------|
  #|| ❤❤❤❤❤❤      25/25 |
  #||-----------------------|
  
  sys.stdout.write(f"\033[2K\r{printBorder(gameSettings.screenWidth,split=True)}\n")
  Cursor.loadPos()
  if f == True: sys.stdout.flush()



def updateRoomDisplay(f=True):
  Cursor.moveTo(4)
  
  roomName = getRoomName(playerCoords,roomDict)
  roomDesc = getRoomDesc(playerCoords,roomDict)
  roomExits = printRoomExits(playerCoords,roomDict)
  #roomItems = getRoomItems(playerCoords,itemData)
  margin = space(gameSettings.screenWidth-4)
    
  sys.stdout.write(f"| {roomName[:gameSettings.screenWidth-4]}{margin[:-len(removeAnsi(roomName))]} |\n")
  sys.stdout.write(f"| {roomDesc[:gameSettings.screenWidth-4]}{margin[:-len(removeAnsi(roomDesc))]} |\n")
  sys.stdout.write(f"| {roomExits[:gameSettings.screenWidth-4]}{margin[:-len(removeAnsi(roomExits))]} |\n")
  sys.stdout.write(f"{printBorder(gameSettings.screenWidth,split=True)}\n")
  if f == True: sys.stdout.flush()




firstTimeEnteringRoom = True
Cursor.moveTo(4)
while True:
  ################## UPDATED EVERY FRAME ##################
  playerCoords = (playerX,playerY)
  getRoomExits(playerCoords, roomDict)
  drawMiniMap()
  ################## UPDATED EVERY FRAME ##################

  
  if firstTimeEnteringRoom == True:
    updateRoomDisplay()
    ClearScreen.toEnd()
    firstTimeEnteringRoom = False


  
  ClearLine.toEnd()
  #useful but not sacred
  
  
  ################################
  playerInput = input(f"\r>> ") ##
  ################################
  #        the sacred line


  
  
   #################################### COMMANDS ####################################
  if playerInput.lower() in look:
    print(getRoomName(playerCoords, roomDict))
    print(getRoomDesc(playerCoords, roomDict))
    print(printRoomExits(playerCoords, roomDict))
    getRoomItems(playerCoords, itemData)


  elif playerInput.lower() == "cls":
    Cursor.moveTo(0,0)
    ClearScreen.screen()
    drawMiniMap(f=True)
    firstTimeEnteringRoom = True


  elif playerInput.lower() == "a":
    player.health -= 1


  
  elif playerInput.lower() == "Rgb": #disabled intentionally
    currentItem = 0
    while True:
      Cursor.hide()
      print(f"\033[2K\r\033[38;2;{255-currentItem};{currentItem};{255-currentItem}m16 million colors! [{currentItem}]\033[0m")
      time.sleep(0.01)
      if currentItem == 255: forwards = False
      if currentItem == 0: forwards = True
      if forwards == True: currentItem += 1
      else: currentItem -= 1
    Cursor.show()
  

  
  elif playerInput.lower().startswith("xp") == True:
    try: playerInput = int(playerInput[3:])
    except ValueError: print("\033[31mInvalid number!\033[0m")

    player = addPlayerXp(player, playerInput)
    print(f"\033[92mGiven player {placeValue(playerInput)} xp points!\033[0m")
    

  
  elif playerInput.lower() == "fight":
    inFight(playerCoords, playerInventory, gameSettings, player, enemyData["greenSlime"])
    player = inFight.player
    firstTimeEnteringRoom = True


  elif playerInput.lower().startswith("debug") == True:
    if gameSettings.debugMode == True:
      print("\033[93mDebug mode: \033[31moff\033[0m")
      gameSettings.debugMode = False
    elif gameSettings.debugMode == False:
      print("\033[93mDebug mode: \033[92mon \033[2m(this will print a lot of text when calling functions)\033[0m")
      gameSettings.debugMode = True



  elif playerInput.lower() == "roomitems":
    print(f"currentRoomItems: {currentRoomItems}")


  
  elif playerInput.lower() == "name":
    print("What would you like to be called?")
    while True:
      playerInput = input("> ")
      
      if len(playerInput) > 20:
        print("\033[31mName is too long!\033[0m")
      elif len(playerInput) <= 2:
        print("\033[31mName is too short!\033[0m")
      else:
        if playerInput.lower() == "arjun":
          ClearScreen.screen(); Cursor.moveTo(0,0)
          print("get fucked")
          quit()
        elif playerInput.lower() in ["dan","daniel"]:
          print("This name has been taken by a genius individual")
        elif playerInput.lower() == "collin":
          print("This name has been reserved for a genius coder")
          #my friend put this here I swear I'm not a narcissist
        elif playerInput.lower() == "ellis":
          print("This name has been taken by someone who thinks apcr is better than heat")
        elif playerInput.lower() in ["wil","willow"]:
          print("This name has been taken by someone with a horrible sense of humor")
        elif playerInput.lower() in ["name","player"]:
          print("Wow, real original.")
          break
        else:
          player.name = properNoun(playerInput)
          print(f"Ok, I will call you {player.color}{player.name}.\033[0m")
          break

  

  elif playerInput.lower() == "color":
    def colorCorrection(color):
      try: color = int(color)
      except: color = 255
      if color > 255: color = 255
      return color
    
    print("rgb values (0-255):")
    red = input("r> ")
    red = colorCorrection(red)
    green = input("g> ")
    green = colorCorrection(green)
    blue = input("b> ")
    blue = colorCorrection(blue)

    player.color = f"\033[38;2;{red};{blue};{green}m"
    print(f"Your color is now {player.color}({red},{green},{blue})\033[0m")


  
  elif playerInput.lower() in inventory:
    tempList = []
    tempString = ", "
    for x in playerInventory:
      tempList.append(x.name)
    tempList = tempString.join(tempList)
          
    filledRatio = len(playerInventory)/int(player.bag.itemValue)*100
    #CALCULATES THE PERCENTAGE OF HOW FULL THE BAG IS
    # why is this comment in all caps I don't remember writing this
    
    color = percentageToColor(filledRatio, True)
    
    sys.stdout.write(f"\033[95m-{printBorder(math.ceil(gameSettings.screenWidth/4))[1:]} {player.bag.name} {printBorder(math.floor(gameSettings.screenWidth/4))[:-1]}-\033[0m\n")
    print(f"\033[95mITEMS: \033[0m{tempList}")
    print(f"\033[95mCAPACITY: \033[0m({color}{len(playerInventory)}/{player.bag.itemValue}\033[0m)")
    print(f"\033[95mWALLET: \033[93;4m${placeValue(player.money)}\033[0m")
    print(f"\033[95m--------- {player.bag.name} ---------\033[0m")
  



  elif playerInput.lower().startswith("stat") == True:
    statBorder = f"\033[95m{printBorder(math.ceil(gameSettings.screenWidth/2)-math.ceil(len(player.name)/2))[:-1]}- {player.name} -{printBorder(math.floor(gameSettings.screenWidth/2)-math.floor(len(player.name)/2))[1:]}\033[0m\n"
    statLevel = placeValue(player.level)
    statXpRequired = xpToLevelUp(player.level)

    
    sys.stdout.write(statBorder)
    sys.stdout.write(f"\033[95m| LEVEL: {statLevel}{space(gameSettings.screenWidth-len(statLevel)-9)} |\033[0m\n")
    sys.stdout.write(f"\033[95m| "+str(statusBar((player.xp/statXpRequired*100), gameSettings.screenWidth-2, '\033[92m', '\033[90m'))+" \033[95m|\033[0m\n")
    sys.stdout.write(f"\033[95m| XP: {player.xp}/{statXpRequired}{space(gameSettings.screenWidth-len(str(player.xp))-len(str(statXpRequired))-7)} |\033[0m\n")
    sys.stdout.write(statBorder)
    sys.stdout.flush()




  elif playerInput.lower() in helpList:
    for x in helpText:
      print(x)
      time.sleep(0.04)



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
        getMoney(playerInput, playerCoords, playerInventory, currentRoomItems, player.money, gameSettings.debugMode)

        if getMoney.functionSuccess == True:
          player.money = getMoney.playerMoney
          currentRoomItems = getMoney.currentRoomItems
      else:
        if len(playerInventory) < bagCapacity:
          getItem(playerInput, playerCoords, playerInventory, currentRoomItems, player.bag, player.money, itemData, gameSettings.debugMode)
          
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
        dropMoney(playerInput, playerCoords, playerInventory, currentRoomItems, player.money, gameSettings.debugMode)

        if dropMoney.functionSuccess == True:
          player.money = dropMoney.playerMoney
          currentRoomItems = dropMoney.currentRoomItems
      else:
        #checks if inventory size is less than bag capacity
        dropItem(playerInput, playerCoords, playerInventory, itemData, currentRoomItems, player.money, gameSettings.debugMode)
          
        if dropItem.functionSuccess == True:
          playerInventory = dropItem.playerInventory
          currentRoomItems = dropItem.currentRoomItems


  

  elif playerInput.lower() == "reeses puffs reeses puffs":
    quit("Eat 'em up eat 'em up eat 'em up'")
        



  elif playerInput.lower().startswith("equip") == True:
    pass




  elif playerInput.lower() == "move":
    print("\033[92mUse N,S,E,W to move north, south, east, or west.\033[0m")



  
  elif playerInput.lower().startswith(("menu","quit","exit")) == True:
    print("Exit to main menu? (y/n)")
    areYouSure = input(">> ")

    if areYouSure.lower() == "y":
      ClearScreen.screen()
      menuSequence(gameVersion, gameName, gameSettings, playerName)
  

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
      loadProgress(loadInput, gameSettings.debugMode)
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
        if areYouSure.lower() == "y":
          clearSlot(deleteSlotInput)
        else:
          print("\033[92mClear cancelled.\033[0m")




  
  elif playerInput.lower() in ["north","n","up"]:
    if getRoomExits.north == True:
      playerY = playerY + 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the NORTH.\033[0m")
    else:
      bump = random.randint(0,len(bumpList)-1)
      print(f"\033[31m{bumpList[bump]}\033[0m")
      if bump == 2: player.health -= 1
  
  elif playerInput.lower() in ["south","s","down"]:
    if getRoomExits.south == True:
      playerY = playerY - 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the SOUTH.\033[0m")
    else:
      bump = random.randint(0,len(bumpList)-1)
      print(f"\033[31m{bumpList[bump]}\033[0m")
      if bump == 2: player.health -= 1
  
  elif playerInput.lower() in ["east","e","right"]:
    if getRoomExits.east == True:
      playerX = playerX + 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the EAST.\033[0m")
    else:
      bump = random.randint(0,len(bumpList)-1)
      print(f"\033[31m{bumpList[bump]}\033[0m")
      if bump == 2: player.health -= 1
  
  elif playerInput.lower() in ["west","w","left"]:
    if getRoomExits.west == True:
      playerX = playerX - 1
      firstTimeEnteringRoom = True
      print("\033[93mYou walk to the WEST.\033[0m")
    else:
      bump = random.randint(0,len(bumpList)-1)
      print(f"\033[31m{bumpList[bump]}\033[0m")
      if bump == 2: player.health -= 1


  
  
  if playerInput.lower() == "pun":
    print("why ask me? ask willow if you want any decent puns.")
    playerInput = input(">> ")
    if playerInput.lower() in ["why","why?"]:
      print("because fuck you, that's why")
  
  if playerInput.lower() == "humor":
    print("so a russian, a ukranian and a swiss walk into a bar...")

  if playerInput.lower() == "fuck":
    print(FUCK[random.randint(0,len(FUCK)-1)])

  if playerInput.lower() == "quack":
    print("quack quack")
    
  if player.health <= 0:
    ClearScreen.screen(); Cursor.moveTo(0,0)
    print(f"\033[38;2;0;255;0m\033[48;2;175;50;175m{deathList[random.randint(0,len(deathList)-1)]}\033[0m")
    quit()
  if player.health > player.maxHealth:
    player.health = player.maxHealth