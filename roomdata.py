#FORMAT:    roomName, roomDesc, roomExits, roomMetaData
#ROOMEXIT FORMAT:  NORTH SOUTH EAST WEST (1111)
roomData = {
  #"(?, ?)":["This is a room name","This is a room description.","1111","default"],
  "(0, 0)":["\033[96mFlodded Passageway\033[0m","A pile of rubble blocks the exit to the SOUTH. The stone brick floor is cracked and shattered and the room is partially flooded. The only source of light is from a sewer grate above, and there is a passageway to the NORTH.","1200","tutorialRoom"],
  "(0, 1)":["Sewer Junction","placeholderdesc01","1101","tutorialRoom"],
  "(0, 2)":["placeholdername02","placeholderdesc02","0101","tutorialRoom"],
  "(-1, 2)":["placeholdername-12","placeholderdesc-12","0010","tutorialRoom"],
  "(-1, 1)":["placeholdername-11","placeholderdesc-11","0011","tutorialRoom"],
  "(-2, 1)":["placeholdername-21","placeholderdesc-21","1011","tutorialRoom"],
  "(-2, 2)":["placeholdername-22","placeholderdesc-22","0100","tutorialRoom"],
  "(-3, 1)":["placeholdername-31","placeholderdesc-31","0010","tutorialRoom"]
}