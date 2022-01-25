def inFight(playerCoords, playerInventory):
  from objects import itemData, enemyData
  
  foe = enemyData["greenSlime"]
  print(f"\033[31m{foe.prefix.upper()} {foe.color}[{foe.name}]\033[31m enters the room!\033[0m")

  while True:
    
    #############################
    playerInput = input(">> ") ##
    #############################
    #      the sacred line      