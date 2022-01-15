yes = {"yes","y"}
no = {"no","n"}

look = {"look","l", "look around"} #get information about the room you're in
inventory = {"inventory","inv","i"}
check = {"check","c","ch"} #get enemy information, used in combat
search = {"search","src"} #find enemies, items, and secrets
helpList = {"help","h","/help","/h","?help","?h","!h","!help"}
attack = {"attack","a","fight"}
mapList = {"map","m"}

slot1List = {"slot 1","1","slot1"}
slot2List = {"slot 2","2","slot2"}
slot3List = {"slot 3","3","slot3"}

bumpList = ["\033[31mYou've bumped into a wall.\033[0m","\033[31mThere's no door on this wall.\033[0m","\033[31mYou have taken [0] damage from smacking your face on this wall!\033[0m","\033[31mYou can't go that way.\033[0m","\033[31mThere's something in the way.\033[0m","\033[31mYou walk into a wall.\033[0m","\033[31mYou smack your head on the wall, in hopes an exit will appear.\033[0m"]

north = {"north","n","up"}
south = {"south","s","down"}
east = {"east","e","right"}
west = {"west","w","left"}

apst = "'"
helpText = [
  '\033[95m--------------------- LIST OF COMMANDS -----------------------\033[0m',
  '\033[93m"look"\033[0m (alias \033[93m"l"\033[0m) Get information about the room you'+apst+'re in',
  '\033[93m"map"\033[0m (no alias) Make sure you'+apst+'re going the right way',
  '',
  '\033[92m"save"\033[0m, \033[93m"load"\033[0m, \033[31m"clear"\033[0m (no aliases) Make sure to save often!',
  #'',
  '',
  '\033[92mMovement\033[0m',
  'To move, type a direction! (\033[93m"north"\033[0m, \033[93m"south"\033[0m, \033[93m"east"\033[0m, \033[93m"west"\033[0m)',
  '(alieses are \033[93m"n"\033[0m, \033[93m"s"\033[0m, \033[93m"e"\033[0m, \033[93m"w"\033[0m)',
  #'',
  '\033[95m-------------------------------------------------------------\033[0m',
  #'',
  #'',
  #'',
  #'\033[2m\033[93m"search"\033[0m\033[2m (alias \033[93m"src"\033[0m\033[2m) Look for anything from enemies to items\033[0m','\033[2m\033[93m"inventory"\033[0m\033[2m (aliases \033[93m"inv"\033[0m\033[2m, \033[93m"i"\033[0m\033[2m) Look through your stuff','\033[2m\033[93m"attack"\033[0m\033[2m (alias \033[93m"a"\033[0m\033[2m) Defend yourself from the bad guys!\033[0m','\033[93m\033[2m"get"\033[0m\033[2m (alias \033[93m"g"\033[0m\033[2m) Pick stuff up, works on money and items\033[0m',
]

errormsg1 = "If you're seeing this, the code is in what I thought was an unreachable state.\n\nI could give you advice for what do do, but honestly, why should you trust me? I clearly screwed this up. I'm writing a message that should n ever appear, yet I know it will probably appear someday.\n\nOn a deep level, I know I'm not up to this task. I'm so sorry."
errormsg2 = "ERROR: We've reached an unreachable state. Anything is possible. The limits were in our heads all along. Follow your dreams."
#https://xkcd.com/2200/