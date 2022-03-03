import time, sys, math, random

def menuSequence(gameVersion, gameName, gameSettings, playerName):
  from functions import Cursor, getSaveSlotData, loadProgress, ClearScreen, ClearLine, space, removeAnsi, printBorder, clearSlot, properNoun
  from getkey import getkey, keys
  
  menuSequence.playerName = "Player" #default
  
  Cursor.hide()
  print(gameName)
  print(f"v{gameVersion}")
  
  currentItem = 0
  while True:  
    ######################  MAIN MENU UPDATER  ######################
    def drawMainMenu(f=True,h=True):
      drawMainMenu.menuOptionsList = ["NEW GAME","LOAD GAME","OPTIONS","QUIT"]
      if h == True:
        drawMainMenu.menuOptionsList.insert(currentItem, gameSettings.highlightColor)
        drawMainMenu.menuOptionsList.insert(currentItem+2, "\033[0m")
      else:
        drawMainMenu.menuOptionsList.insert(currentItem, "\033[48;2;100;100;100m")
        drawMainMenu.menuOptionsList.insert(currentItem+2, "\033[0m")
        
      string = ""
      for x in drawMainMenu.menuOptionsList:
        string += x
        for y in range(gameSettings.screenWidth // 25):
          string += " "
          #padding for larger screens
  
      Cursor.moveTo(4)
      ClearScreen.toEnd()
      sys.stdout.write(f"{printBorder(gameSettings.screenWidth,split=True)}\n")
      sys.stdout.write(f"| {space(math.ceil(gameSettings.screenWidth/2)-2)[0:-math.ceil((len(removeAnsi(string))/2))]}{string}{space(math.floor(gameSettings.screenWidth/2)-2)[0:-math.floor((len(removeAnsi(string))/2))]} |")
      sys.stdout.write(f"\n{printBorder(gameSettings.screenWidth,split=True)}")
      
      if f == True:
        sys.stdout.flush()
      return
    ######################  MAIN MENU UPDATER  ######################


    drawMainMenu()
    playerInput = getkey()
    #the less sacred but still pretty damn sacred line


      
    ###################### OPTION SELECTOR ######################
    if playerInput == keys.LEFT or playerInput == keys.A: currentItem -= 1
    elif playerInput == keys.RIGHT or playerInput == keys.D: currentItem += 1
      
    if currentItem < 0:
      currentItem = 0
    elif currentItem > len(drawMainMenu.menuOptionsList) - 3:
      currentItem = len(drawMainMenu.menuOptionsList) - 3
      #this is 3 instead of 1 because of the 2 highlighting variables inserted into the list after it is created
    ###################### OPTION SELECTOR ######################


      
    if playerInput == keys.ENTER or playerInput == keys.DOWN:
      if currentItem in [0,1,2,3]:
        drawMainMenu(h=False)
      
      if currentItem == 0: #new
        exitLoop = False
        Cursor.moveTo(8)
        sys.stdout.write(printBorder(gameSettings.screenWidth,split=True))
        Cursor.moveTo(7)
        
        choice = 0
        while True:
          confirmChoice = ["YES","NO"]
          confirmChoice.insert(choice, gameSettings.highlightColor)
          confirmChoice.insert(choice+2, "\033[0m")

          export = ""
          for x in confirmChoice:
            export += x + " "

          ClearLine.toEnd()
          string = f"Start a new game?   {export}"
          sys.stdout.write(f"\r| {string}{space(gameSettings.screenWidth-len(removeAnsi(string))-4)} |")

          sys.stdout.flush()
          choiceInput = getkey()

          if choiceInput == keys.LEFT or choiceInput == keys.A: choice -= 1
          elif choiceInput == keys.RIGHT or choiceInput == keys.D: choice += 1
          elif choiceInput == keys.UP:
            Cursor.moveTo(7)
            ClearScreen.toEnd()
            break
          elif choiceInput == keys.ENTER or choiceInput == keys.E or choiceInput == keys.DOWN:
            if choice == 0: #yes
              Cursor.moveTo(4); ClearScreen.toEnd()
              sys.stdout.write("What do you want to be called?")
              Cursor.show()

              while True:
                Cursor.moveTo(5); ClearLine.toEnd()
                sys.stdout.flush()
                playerInput = input("\r>> ")

                if len(playerInput) > 25:
                  Cursor.moveTo(6)
                  sys.stdout.write("\033[31mName is too long! (max 25 characters)\033[0m")
                  ClearScreen.toEnd()
                elif len(playerInput) < 2:
                  Cursor.moveTo(6)
                  sys.stdout.write("\033[31mName is too short! (min 2 characters)\033[0m")
                  ClearScreen.toEnd()
                elif playerInput.lower().startswith(("cancel","quit","menu","exit")) == True:
                  exitLoop = True
                  break
                else:
                  ClearScreen.screen(); Cursor.hide()
                  menuSequence.playerName = properNoun(playerInput[0:25])
                  print(f"Welcome, {menuSequence.playerName}!")
                  time.sleep(1.5)
                  ClearScreen.screen(); Cursor.show()
                  return
            elif choice == 1: #no
              Cursor.moveTo(7)
              ClearScreen.toEnd()
              break
          if exitLoop == True:
            break

          if choice > 1: choice = 1
          if choice < 0: choice = 0
          
        
      
      
      
      
      
      elif currentItem == 1: #load
        getSaveSlotData()
        line = 7
        while True:
          slot1 = getSaveSlotData.slot1[0]
          slot2 = getSaveSlotData.slot2[0]
          slot3 = getSaveSlotData.slot3[0]
          
          Cursor.moveTo(7)
          sys.stdout.write(f"| {slot1[0:gameSettings.screenWidth-4]}{space(gameSettings.screenWidth-4)[:-len(removeAnsi(slot1))]} |\n")
          sys.stdout.write(f"| {slot2[0:gameSettings.screenWidth-4]}{space(gameSettings.screenWidth-4)[:-len(removeAnsi(slot2))]} |\n")
          sys.stdout.write(f"| {slot3[0:gameSettings.screenWidth-4]}{space(gameSettings.screenWidth-4)[:-len(removeAnsi(slot3))]} |\n")
          sys.stdout.write(printBorder(gameSettings.screenWidth,split=True))
          Cursor.moveTo(line)

          currentSlot = locals()[f'slot{line-6}']
          sys.stdout.write(f"| {gameSettings.highlightColor}{removeAnsi(currentSlot[0:gameSettings.screenWidth-4])}\033[0m{space(gameSettings.screenWidth)[:-len(removeAnsi(currentSlot))-4]}")
          
          sys.stdout.flush()
          verticalInput = getkey()
  
          if verticalInput == keys.UP or verticalInput == keys.W: line -= 1
          elif verticalInput == keys.DOWN or verticalInput == keys.S: line += 1
          
          elif verticalInput == keys.ENTER or verticalInput == keys.E:
            sys.stdout.write(f"\r| \033[48;2;100;100;100m{currentSlot[0:gameSettings.screenWidth-4]}\033[0m{space(gameSettings.screenWidth)[:-len(removeAnsi(currentSlot))-4]}")
            Cursor.moveTo(11)
            sys.stdout.write(f"\n{printBorder(gameSettings.screenWidth,split=True)}")
            
            currentItem = 0
            slotSelected = True
            while slotSelected:
              saveSlotMenuItems = ["LOAD","CLEAR","CANCEL"]
              saveSlotMenuItems.insert(currentItem, gameSettings.highlightColor)
              saveSlotMenuItems.insert(currentItem+2, "\033[0m")
  
              string = ""
              for x in saveSlotMenuItems:
                string += x
                for y in range(gameSettings.screenWidth // 25):
                  string += " "
                  #padding for larger screens

              Cursor.moveTo(11)
              sys.stdout.write(f"| {space(math.ceil(gameSettings.screenWidth/2)-2)[0:-math.ceil((len(removeAnsi(string))/2))]}{string}{space(math.floor(gameSettings.screenWidth/2)-2)[0:-math.floor((len(removeAnsi(string))/2))]} |")
              
              sys.stdout.flush()
              loadSlotInput = getkey()

              if loadSlotInput == keys.LEFT or loadSlotInput == keys.A: currentItem -= 1
              elif loadSlotInput == keys.RIGHT or loadSlotInput == keys.D: currentItem += 1
              elif loadSlotInput == keys.UP:
                Cursor.moveTo(11)
                ClearScreen.toEnd()
                break
              
              elif loadSlotInput == keys.ENTER or loadSlotInput == keys.E:
                if currentItem == 0: #load
                  while True:
                    string = f"\033[93mLoad slot {line-6}?\033[0m"
                    choice = 0
                    while True:
                      confirmChoice = ["YES","NO"]
                      confirmChoice.insert(choice, gameSettings.highlightColor)
                      confirmChoice.insert(choice+2, "\033[0m")

                      export = ""
                      for x in confirmChoice:
                        export += x + " "

                      Cursor.moveTo(11)
                      ClearLine.toEnd()
                      sys.stdout.write(f"\r| {string[0:gameSettings.screenWidth-4]}{space(3)}{export[0:gameSettings.screenWidth-4-len(removeAnsi(export))]}{space(gameSettings.screenWidth-4)[:-len(removeAnsi(string))-len(removeAnsi(export))-3]} |")
                      
                      sys.stdout.flush()
                      confirmChoiceInput = getkey()

                      if confirmChoiceInput == keys.LEFT or confirmChoiceInput == keys.A: choice -= 1
                      elif confirmChoiceInput == keys.RIGHT or confirmChoiceInput == keys.D: choice += 1
                      elif confirmChoiceInput == keys.ENTER or loadSlotInput == keys.E:
                        if choice == 0:
                          Cursor.moveTo(11)
                          ClearScreen.toEnd()
                          slotSelected = False
                          break
                        elif choice == 1:
                          break

                      if choice < 0: choice = 0
                      if choice > 1: choice = 1
                    break
                elif currentItem == 1:
                  while True:
                    string = f"\033[31mClear slot {line-6}?\033[0m"
                    choice = 0
                    while True:
                      confirmChoice = ["YES","NO"]
                      confirmChoice.insert(choice, gameSettings.highlightColor)
                      confirmChoice.insert(choice+2, "\033[0m")

                      export = ""
                      for x in confirmChoice:
                        export += x + " "

                      Cursor.moveTo(11)
                      ClearLine.toEnd()
                      sys.stdout.write(f"\r| {string[0:gameSettings.screenWidth-4]}{space(3)}{export[0:gameSettings.screenWidth-4-len(removeAnsi(export))]}{space(gameSettings.screenWidth-4)[:-len(removeAnsi(string))-len(removeAnsi(export))-3]} |")
                      
                      sys.stdout.flush()
                      confirmChoiceInput = getkey()

                      if confirmChoiceInput == keys.LEFT or confirmChoiceInput == keys.A: choice -= 1
                      elif confirmChoiceInput == keys.RIGHT or confirmChoiceInput == keys.D: choice += 1
                      elif confirmChoiceInput == keys.ENTER or loadSlotInput == keys.E:
                        if choice == 0:
                          clearSlot(line-6)
                          Cursor.moveTo(11)
                          ClearLine.toEnd()
                          string = "\033[92mSlot cleared!\033[0m"
                          sys.stdout.write(f"\r| {string[0:gameSettings.screenWidth-4]}{space(gameSettings.screenWidth-4)[:-len(removeAnsi(string))]} |")
                          getSaveSlotData()
                          slotSelected = False
                          break
                        elif choice == 1:
                          break

                      if choice < 0: choice = 0
                      if choice > 1: choice = 1
                    break
                elif currentItem == 2:
                  Cursor.moveTo(11)
                  ClearScreen.toEnd()
                  break

              if currentItem < 0: currentItem = 0
              if currentItem > 2: currentItem = 2
  
          if line < 7:
            Cursor.moveTo(7)
            ClearScreen.toEnd()
            break
          elif line > 9: line = 9
          else: Cursor.moveTo(line)
          #puts a cap on vertical cursor movement
      
      




      
      
      
      elif currentItem == 2: #options
        screenWidth = gameSettings.screenWidth
        border = printBorder(screenWidth,split=True)
        margin = space(screenWidth-4)
        
        Cursor.moveTo(7); line = 7
        ClearScreen.toEnd()

        def drawOptionsBar(border,h=True,f=False):
          drawOptionsBar.optionControlsList = ["SAVE AS DEFAULT","RESET"]
          if h == True:
            drawOptionsBar.optionControlsList.insert(currentItem, gameSettings.highlightColor)
            drawOptionsBar.optionControlsList.insert(currentItem+2, "\033[0m")
            
          string = ""
          for x in drawOptionsBar.optionControlsList:
            string += x
            for y in range(gameSettings.screenWidth // 25):
              string += " "
              #padding for larger screens
      
          Cursor.moveTo(len(gameSettings.varList)+7)
          sys.stdout.write(f"{border}\n")
          sys.stdout.write(f"| {space(math.ceil(gameSettings.screenWidth/2)-2)[:-math.floor(len(removeAnsi(string))/2)]}{string}{space(math.floor(gameSettings.screenWidth/2)-2)[-math.ceil(len(removeAnsi(string))/2)]} |")
          sys.stdout.write(f"\n{border}")

        drawOptionsBar(border,h=False)
        
        while True:
          rgbValues = repr(vars(gameSettings)["highlightColor"])[11:-2]
          rgbValues = rgbValues.split(";")
          for x in range(0,len(rgbValues)): #so it starts at index 0
            rgbValues[x] = int(rgbValues[x])
          #this decodes the highlight escape sequence to display as rgb values
          
          Cursor.moveTo(7)
          optionItem = 0
          for x in gameSettings.varList:
            optionItem += 1
            
            if optionItem == 4:
              string = f"{x} = {rgbValues[0]},{rgbValues[1]},{rgbValues[2]}"
            else: string = f"{x} = {vars(gameSettings)[x]}"

            ClearLine.toEnd()
            sys.stdout.write(f"\033[0m| {string}\033[0m{margin[:-len(removeAnsi(string))]} |\n")
          #this prints all the vars from gameSettings specified in optionList

          
          Cursor.moveTo(line)
          try:
            if line == 10:
              string = f"{gameSettings.highlightColor}{gameSettings.varList[line-7]}\033[0m = {rgbValues[0]},{rgbValues[1]},{rgbValues[2]}"
            else:
              string = f"{gameSettings.highlightColor}{gameSettings.varList[line-7]}\033[0m = {vars(gameSettings)[gameSettings.varList[line-7]]}"
            sys.stdout.write(f"\033[0m| {string}\033[0m{margin[:-len(removeAnsi(string))]} |")
          except IndexError: pass
          #this highlights the option corresponding to the "line" var

          sys.stdout.flush()
          verticalInput = getkey()
            
          if verticalInput == keys.UP or verticalInput == keys.W: line -= 1
          elif verticalInput == keys.DOWN or verticalInput == keys.S: line += 1
          elif verticalInput == keys.ENTER or verticalInput == keys.E:
            exitLoop = False
            while True:
              ClearLine.line()
              string = f"{gameSettings.varList[line-7]} = <{gameSettings.highlightColor}{vars(gameSettings)[gameSettings.varList[line-7]]}\033[0m>"
              if line == 7:
                string += " (in characters)"
              elif line == 10:
                rgbItem = 0
                tempHighlight = gameSettings.highlightColor
                while True:
                  rgbList = [str(rgbValues[0]),str(rgbValues[1]),str(rgbValues[2])]
                  rgbList.insert(rgbItem, tempHighlight)
                  rgbList.insert(rgbItem+2, "\033[0m")
        
                  export = ""
                  for x in rgbList:
                    export += x + " "
        
                  Cursor.moveTo(line)
                  ClearLine.toEnd()
                  string = f"{gameSettings.varList[line-7]} = {export}"
                  sys.stdout.write(f"\r| {string}{space(gameSettings.screenWidth-len(removeAnsi(string))-4)} |")
        
                  sys.stdout.flush()
                  rgbInput = getkey()
        
                  if rgbInput == keys.LEFT or rgbInput == keys.A: rgbItem -= 1
                  elif rgbInput == keys.RIGHT or rgbInput == keys.D: rgbItem += 1
                  if rgbInput == keys.UP or rgbInput == keys.W:
                    rgbValues[rgbItem] += 1
                  elif rgbInput == keys.DOWN or rgbInput == keys.S:
                    rgbValues[rgbItem] -= 1
                  elif rgbInput == keys.ENTER or rgbInput == keys.E:
                    gameSettings.highlightColor = f"\033[48;2;{rgbValues[0]};{rgbValues[1]};{rgbValues[2]}m"
                    exitLoop = True
                    break

                  if rgbItem > 2: rgbItem = 2
                  if rgbItem < 0: rgbItem = 0
                  if rgbValues[rgbItem] > 255: rgbValues[rgbItem] = 255
                  if rgbValues[rgbItem] < 0: rgbValues[rgbItem] = 0

                  tempHighlight = f"\033[48;2;{rgbValues[0]};{rgbValues[1]};{rgbValues[2]}m"
              if exitLoop == True: break
                  
              
              sys.stdout.write(f"\r\033[0m| {string}\033[0m{margin[:-len(removeAnsi(string))]} |")
              sys.stdout.flush()
              horizontalInput = getkey()
              
              if horizontalInput == keys.LEFT or horizontalInput == keys.A:
                if type(vars(gameSettings)[gameSettings.varList[line-7]]) == bool:
                  vars(gameSettings)[gameSettings.varList[line-7]] = not vars(gameSettings)[gameSettings.varList[line-7]]
                if type(vars(gameSettings)[gameSettings.varList[line-7]]) == int:
                  if line == 7 and vars(gameSettings)[gameSettings.varList[line-7]] <= 50:
                    pass
                  else:
                    vars(gameSettings)[gameSettings.varList[line-7]] = vars(gameSettings)[gameSettings.varList[line-7]] - 1
            
              elif horizontalInput == keys.RIGHT or horizontalInput == keys.D:
                if type(vars(gameSettings)[gameSettings.varList[line-7]]) == bool:
                  vars(gameSettings)[gameSettings.varList[line-7]] = not vars(gameSettings)[gameSettings.varList[line-7]]
                if type(vars(gameSettings)[gameSettings.varList[line-7]]) == int:
                  if line == 7 and vars(gameSettings)[gameSettings.varList[line-7]] >= 150:
                    pass
                  else:
                    vars(gameSettings)[gameSettings.varList[line-7]] = vars(gameSettings)[gameSettings.varList[line-7]] + 1

              elif horizontalInput == keys.ENTER or horizontalInput == keys.E:
                break
          
          

            
          if line < 7:
            Cursor.moveTo(7)
            ClearScreen.toEnd()
            break
          
          elif line-6 > len(vars(gameSettings))-1:
            #line = len(vars(gameSettings))+5
            line -= 1
            string = f"{gameSettings.varList[line-7]} = {vars(gameSettings)[gameSettings.varList[line-7]]}"
            sys.stdout.write(f"\r| {string}{margin[:-len(removeAnsi(string))]} |")
            sys.stdout.flush()
            
            while True:
              pass
          
          else: Cursor.moveTo(line)
          #puts a cap on vertical cursor movement

            
            
            
            
        
      elif currentItem == 3: #quit
        Cursor.moveTo(7)
        string = "Are you sure you want to quit?"
        choice = 0
        while True:
          confirmChoice = ["NO","YES"]
          confirmChoice.insert(choice, gameSettings.highlightColor)
          confirmChoice.insert(choice+2, "\033[0m")

          export = ""
          for x in confirmChoice:
            export += x + " "

          Cursor.moveTo(7)
          ClearLine.toEnd()
          sys.stdout.write(f"\r| {string[:gameSettings.screenWidth-4]}{space(3)}{export[:gameSettings.screenWidth-4-len(removeAnsi(export))]}{space(gameSettings.screenWidth-4)[:-len(removeAnsi(string))-len(removeAnsi(export))-3]} |\n")
          sys.stdout.write(printBorder(gameSettings.screenWidth,split=True))

          sys.stdout.flush()
          choiceInput = getkey()

          if choiceInput == keys.LEFT or choiceInput == keys.A: choice -= 1
          elif choiceInput == keys.RIGHT or choiceInput == keys.D: choice += 1
          elif choiceInput == keys.UP:
            Cursor.moveTo(7)
            ClearScreen.toEnd()
            break
          elif choiceInput == keys.ENTER or choiceInput == keys.E or choiceInput == keys.DOWN:
            if choice == 0: #no
              Cursor.moveTo(7)
              ClearScreen.toEnd()
              break
            elif choice == 1: #yes
              ClearScreen.screen()
              quit()

          if choice > 1: choice = 1
          if choice < 0: choice = 0






def inFight(playerCoords, playerInventory, gameSettings, player, foe):
  from objects import itemData, enemyData
  from functions import Cursor, ClearScreen, ClearLine, statusBar, space, percentageToColor, printFormattedLines, removeAnsi, printBorder
  from getkey import getkey, keys
  
  inFight.inFight = True
  foe.maxHealth = foe.health

  border = printBorder(gameSettings.screenWidth,split=True)
  padding = space(gameSettings.screenWidth)
  
  def exitFight():
    ClearScreen.screen()
    Cursor.show()
    inFight.player = player
    inFight.inFight = False
    return

  
  def optionBarUpdater(noneSelected=False,flush=False):
    Cursor.moveTo(6)
    options = ["ATTACK","INVENTORY","EQUIP","CHECK","RUN"]
    if noneSelected == False:
      options.insert(currentItem, gameSettings.highlightColor)
      options.insert(currentItem+2, "\033[0m")
    
    string = ""
    for x in options:
      string += x
      for y in range(gameSettings.screenWidth // 25):
        string += " "

    sys.stdout.write(f"{border}\n")
    if noneSelected == False:
      sys.stdout.write(f"| {space(math.ceil(gameSettings.screenWidth/2))[:-len(removeAnsi(string))]}{string}{space(math.ceil(gameSettings.screenWidth/2))[:-len(removeAnsi(string))]} |\n")
    else:
      sys.stdout.write(f"| {space(math.ceil(gameSettings.screenWidth/2))[:-len(removeAnsi(string))]}{string}{space(math.ceil(gameSettings.screenWidth/2))[:-len(removeAnsi(string))]} |\n")
    
    if flush == True:
      sys.stdout.flush()
    optionBarUpdater.options = options
    return

  
  def healthBarUpdater(flush=False):
    if player.maxHealth <= 0: playerHpPerc = 0
    else: playerHpPerc = player.health/player.maxHealth*100
    if foe.maxHealth <= 0: foeHpPerc = 0
    else: foeHpPerc = foe.health/foe.maxHealth*100
    #to avoid division by zero

    
    Cursor.moveTo(3)
    sys.stdout.write("  "+statusBar(playerHpPerc, 30, percentageToColor(playerHpPerc), "\033[2m"+str(player.color))+"     "+statusBar(foeHpPerc, 30, percentageToColor(foeHpPerc), "\033[31;2m")+"  ")
    #updates the status bar

    sys.stdout.write(f"\n  {percentageToColor(playerHpPerc)}{str(player.health)[0:15]}/{str(player.maxHealth)[0:15]+space(30)[0:-len(str(player.health)+str(player.maxHealth))]}\033[0m    {percentageToColor(foeHpPerc)}{str(foe.health)[0:15]}/{str(foe.maxHealth)[0:15]+space(30)[0:-len(str(foe.health)+str(foe.maxHealth))]}\033[0m ")
    if flush == True:
      sys.stdout.flush()
    return

  def nameUpdater(flush=False):
    Cursor.moveTo(2,0)
    sys.stdout.write(f"  {player.color}{player.name[0:30]+space(30)[:-len(player.name)]}\033[0m     {foe.color}{foe.name[0:30]+space(30)[:-len(foe.name)]}\033[0m")
    if flush == True:
      sys.stdout.flush()

  Cursor.hide()
  ClearScreen.screen()
  #sets the screen up for the fight sequence




  
  while True:
    nameUpdater()
    healthBarUpdater(flush=True)
    Cursor.moveTo(6)

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
          healthBarUpdater(flush=True)
        
        
        
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
              sys.stdout.write(f"| {x.name}{padding[0:-len(removeAnsi(x.name))]} |")
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



          for x in range(math.ceil(len(foe.description)/gameSettings.screenWidth)):
            if foe.description[gameSettings.screenWidth*x:gameSettings.screenWidth+gameSettings.screenWidth*x][0] == " ":
              sys.stdout.write(f"| {foe.description[gameSettings.screenWidth*x:gameSettings.screenWidth+gameSettings.screenWidth*x]} {padding[0:-len(foe.description[gameSettings.screenWidth*x:gameSettings.screenWidth+gameSettings.screenWidth*x])]} |\n")
              #removes a space if it is the first character of a line
            else:
              sys.stdout.write(f"| {foe.description[gameSettings.screenWidth*x:gameSettings.screenWidth+gameSettings.screenWidth*x]}{padding[0:-len(foe.description[gameSettings.screenWidth*x:gameSettings.screenWidth+gameSettings.screenWidth*x])]} |\n")
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
      optionBarUpdater(noneSelected=True)
      time.sleep(1)
      Cursor.moveTo(9)
      ClearLine.line()
      printFormattedLines([f"\033[31mThe {foe.name} hits you for {foe.damage} damage!\033[0m"],65,True)

      player.health -= 1

      isFoeTurn = False
    ############################### THE FOE'S TURN ################################