import time, sys, math, random

def introSequence(gameVersion, debugMode, gameName):
  from functions import Cursor, getSaveSlotData, printSaveSlotList, loadProgress, clearConsole, properNoun, fancyPrint
  introSequence.playerName = "Player" #default
  introSequence.newGame = False
  Cursor.hide()

  print(gameName)
  print(f"v{gameVersion}")
  time.sleep(1)

  Cursor.show()
  getSaveSlotData()
  if getSaveSlotData.allEmpty != True:
    fancyPrint("\nExisting saves found.\nWould you like to load an existing save?\n")
    printSaveSlotList()
    fancyPrint('Choose the slot you want to load (ex. \033[93m"slot 1", "slot 2"\033[0m), or type \033[93m"new"\033[0m for a new game.\n')
    
    loadGate = False
    while True:
      playerInput = input(">> ")

      if playerInput.startswith(tuple(["slot","save"])) == True:
        if playerInput[4:5] == " ":
          playerInput = playerInput[0:4]+playerInput[5:6]
        playerInput = playerInput[4:5]
        loadGate = True
      
      elif playerInput.startswith(tuple(["1","2","3"])) == True:
        playerInput = playerInput[0:1]
        loadGate = True
      
      elif playerInput == "n" or playerInput == "new":
        clearConsole()
        break #this will move on to the next "while True:" in introSequence
      
      else:
        print('\033[31mType the slot you want to load, or type "n" or "new" to start a new game.\033[0m')
      
      if loadGate == True:
        loadProgress(playerInput, debugMode)


  print("\nWhat would you like to be called? (max 20 chars)\n")
  
  while True:
    playerInput = input(">> ")

    if len(playerInput) <= 20 and len(playerInput) >= 2:
      Cursor.hide()
      playerName = str(properNoun(playerInput))
      print(f"\nWelcome to the realm, {playerName}.")
      
      introSequence.playerName = playerName
      introSequence.newGame = True
      
      time.sleep(2); clearConsole(); time.sleep(1); Cursor.hide()
      break
    elif len(playerInput) <= 2:
      print("\033[31mName is too short!")
    else:
      print("\033[31mName is too long!\033[0m")








def inFight(playerCoords, playerInventory, player, foe):
  from objects import itemData, enemyData
  from functions import Cursor, ClearScreen, ClearLine, statusBar, space, percentageToColor, printFormattedLines, removeAnsi
  from getkey import getkey, keys
  
  inFight.inFight = True
  foe.maxHealth = foe.health

  border = "|---------------------------------|---------------------------------|"
  borderSmall = "|---------------------------------|"
  
  def exitFight():
    Cursor.moveTo(0,0)
    ClearScreen.screen()
    Cursor.show()
    inFight.player = player
    inFight.inFight = False
    return

  def optionBarUpdater(noneSelected=False):
    Cursor.moveTo(6)
    options = ["ATTACK","INVENTORY","EQUIP","CHECK","RUN"]
    if noneSelected == False:
      options.insert(currentItem, "\033[48;2;255;0;255m") #magenta
      options.insert(currentItem+2, "\033[0m")
    string = ""
    for x in options:
      string += x + "  "

    sys.stdout.write(f"{border}\n| {space(43)[0:-math.ceil((len(string)/2))]}{string}{space(43)[0:-math.floor((len(string)/2))]} |\n{border}")
    sys.stdout.flush()
    
    optionBarUpdater.options = options
    return


  Cursor.hide()
  ClearScreen.screen()
  Cursor.moveTo(0,0)

  sys.stdout.write(f"\n  {player.color}{player.name[0:30]+space(30)[:-len(player.name)]}\033[0m     {foe.color}{foe.name[0:30]+space(30)[:-len(foe.name)]}\033[0m  \n")
  sys.stdout.write(f"\n\n\n{border}\n")
  sys.stdout.flush() #prints the names of the fighters and the lines the health bars will sit at, but doesn't print the bars themselves yet because they are already printed there each frame in the updater so it would be redundant


  while True:  
    #-----HEALTH BAR UPDATER-----#
    if player.maxHealth <= 0: playerHpPerc = 0
    else: playerHpPerc = player.health/player.maxHealth*100
    if foe.maxHealth <= 0: foeHpPerc = 0
    else: foeHpPerc = foe.health/foe.maxHealth*100
    #to avoid division by zero
    
    Cursor.moveTo(3)

    sys.stdout.write("  "+statusBar(playerHpPerc, 30, percentageToColor(playerHpPerc), "\033[2m"+str(player.color))+"     "+statusBar(foeHpPerc, 30, percentageToColor(foeHpPerc), "\033[31;2m")+"  ")
    #updates the status bar

    sys.stdout.write(f"\n  {percentageToColor(playerHpPerc)}{str(player.health)[0:15]}/{str(player.maxHealth)[0:15]+space(30)[0:-len(str(player.health)+str(player.maxHealth))]}\033[0m    {percentageToColor(foeHpPerc)}{str(foe.health)[0:15]}/{str(foe.maxHealth)[0:15]+space(30)[0:-len(str(foe.health)+str(foe.maxHealth))]}\033[0m ")
    sys.stdout.flush()
    
    Cursor.moveTo(6)
    #-----HEALTH BAR UPDATER-----#



    if player.health <= 0 or foe.health <= 0:
      Cursor.moveTo(9)
      ClearScreen.toEnd()

    if player.health <= 0 and foe.health <= 0:
      printFormattedLines([f"\033[31m{foe.name} has died!\033[0m",f"\033[31m{player.name} has died!\033]0m","You recieved no xp from this fight."],65,flush=True)
      
      while True:
        playerInput = getkey()
        if playerInput != keys.ENTER: break
        #only proceeds if you press something other than enter
      
      exitFight()
      return
      #activates if both the player and the enemy die at the same time ("draw" condition)
    

    
    elif foe.health <= 0:
      moneyGained = random.randint(foe.lootTable[0],foe.lootTable[1])
      #gives you some money generated somewhere in between the min and max values on the loot table for the monster you killed

      printFormattedLines([f"\033[31m{foe.name} has died!\033[0m"],65)
      if moneyGained > 0:
         printFormattedLines([f"\033[93mYou found ${moneyGained}!\033[0m"],65)
         player.money += moneyGained
      sys.stdout.write(border)
      sys.stdout.flush()
      
      while True:
        playerInput = getkey()
        if playerInput != keys.ENTER: break
        #only proceeds if you press something other than enter
      
      exitFight()
      return
    

    
    elif player.health <= 0:
      printFormattedLines(["\033[93m{player.name} has died!\033[0m","Press any key to continue."])
      sys.stdout.write(border)
      sys.stdout.flush()
      
      while True:
        playerInput = getkey()
        if playerInput != keys.ENTER: break
        #only proceeds if you press something other than enter
      
      exitFight()
      return



    currentItem = 0
    isPlayerTurn = True
    ############################## THE PLAYER'S TURN ##############################
    while isPlayerTurn == True:
      optionBarUpdater()
        
      actionSelect = getkey()
      
      #-----option selector-----#
      if actionSelect == keys.LEFT:
        currentItem -= 1
      elif actionSelect == keys.RIGHT:
        currentItem += 1
      
      if currentItem < 0:
        currentItem = 0
      elif currentItem > len(optionBarUpdater.options) - 3:
        currentItem = len(optionBarUpdater.options) - 3
        #this is 3 instead of 1 because of the 2 highlighting variables inserted into the list after it is created
      #-----option selector-----#


      if actionSelect == keys.ENTER:
        if currentItem == 0: #attack
          Cursor.moveTo(9)
          ClearScreen.toEnd()
          printFormattedLines([f"\033[31m{player.name} does 1 damage to the {foe.name}!\033[0m"],65)
          sys.stdout.write(border); sys.stdout.flush()

          foe.health -= 1
          isPlayerTurn = False
        
        
        
        elif currentItem == 1: #inventory
          Cursor.moveTo(9)
          ClearScreen.toEnd()
          
          if len(playerInventory) > 0:
            for x in playerInventory:
              sys.stdout.write(f"| {x.name}{space(65)[0:-len(removeAnsi(x.name))]} |")
          else:
            printFormattedLines(["\033[31mYour inventory is empty!\033[0m"],65)
          sys.stdout.write(border); sys.stdout.flush()
        
        
        
        elif currentItem == 2: #equip
          Cursor.moveTo(9)
          ClearScreen.toEnd()
          
          if len(playerInventory) > 0:
            for x in playerInventory:
              sys.stdout.write(f"| {x.name}{space(65)[0:-len(removeAnsi(x.name))]} |")
          else:
            printFormattedLines(["\033[31mNothing to equip!\033[0m"],65)
          sys.stdout.write(border); sys.stdout.flush()
        
        
        
        elif currentItem == 3: #check
          Cursor.moveTo(9)
          ClearScreen.toEnd()

          ############### adjusts spacing and space(30) char count ###############
          if len(str(foe.maxHealth)) > 5:
            sys.stdout.write(f"| HEALTH: {str(foe.maxHealth)[0:5]}…{space(5)[:-len(str(foe.maxHealth))]}")
          else:
            sys.stdout.write(f"| HEALTH: {foe.maxHealth}{space(6)[:-len(str(foe.maxHealth))]}")

          if len(str(foe.armor)) > 7:
            sys.stdout.write(f" DEFENSE: {str(foe.armor)[0:6]}…{space(9)[:-len(str(foe.armor))]}")
          else:
            sys.stdout.write(f" DEFENSE: {foe.armor}{space(9)[:-len(str(foe.armor))]}")
          sys.stdout.write(f"{space(33)}|\n")

          if len(str(foe.damage)) > 5:
            sys.stdout.write(f"| ATTACK: {str(foe.damage)[0:5]}… {space(30)[:-len(str(foe.damage))-26]}")
          else:
            sys.stdout.write(f"| ATTACK: {foe.damage}  {space(30)[:-len(str(foe.damage))-26]}")
          
          if len(str(foe.speed)) > 9:
            sys.stdout.write(f" SPEED: {str(foe.speed)[0:8]}…  ")
          else:
            sys.stdout.write(f" SPEED: {foe.speed}{space(30)[:-len(str(foe.speed))-19]}")
          sys.stdout.write(f"{space(33)}|\n{border}\n")
          ############### adjusts spacing and space(30) char count ###############



          descriptionLineCount = math.ceil(len(foe.description)/65) #rounds up
          for x in range(0,descriptionLineCount):
            if foe.description[0+65*x:65+65*x][0] == " ":
              sys.stdout.write(f"| {foe.description[1+65*x:65+65*x]} {space(65)[0:-len(foe.description[0+65*x:65+65*x])]} |\n")
              #removes a space if it is the first character of a line
            else:
              sys.stdout.write(f"| {foe.description[0+65*x:65+65*x]}{space(65)[0:-len(foe.description[0+65*x:65+65*x])]} |\n")
              #figures out how many lines of the description there are to print
          sys.stdout.write(border); sys.stdout.flush()
      
        elif currentItem == 4: #run
          exitFight()
          return
      #-----option selector-----#
    ############################## THE PLAYER'S TURN ##############################



    #the next while loop will control the enemy's response to the player's actions
    isFoeTurn = True



    ############################### THE FOE'S TURN ################################
    while isFoeTurn == True:
      time.sleep(1)
      Cursor.moveTo(10)
      ClearLine.line()

      isFoeTurn = False
    ############################### THE FOE'S TURN ################################