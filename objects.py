class Player:
  def __init__(self, name, health, money, level, xp, color, head, chest, legs, feet, bag):
    self.name = name
    self.health = health
    self.maxHealth = health
    self.money = money
    self.level = level
    self.xp = xp
    self.color = color
    
    self.head = head
    self.chest = chest
    self.legs = legs
    self.feet = feet
    self.bag = bag

class Armor:
  def __init__(self, quantity, armorName, referenceName, defense, agility, stamina, strength, health):
    self.quantity = quantity
    self.name = armorName
    self.reference_name = referenceName
    self.defense = defense
    self.agility = agility
    self.stamina = stamina
    self.strength = strength
    self.health = health

class Weapon:
  def __init__(self, quantity, weaponName, referenceName, damageType, damageValue, speed):
    self.quantity = quantity
    self.name = weaponName
    self.reference_name = referenceName
    self.damageType = damageType
    self.damageValue = damageValue
    self.speed = speed

class Item:
  def __init__(self, quantity, itemName, referenceName, itemType, itemValue, itemValue2, equip_region, isKeyItem):
    self.quantity = quantity
    self.name = itemName
    self.reference_name = referenceName
    self.itemType = itemType
    self.itemValue = itemValue
    self.itemValue2 = itemValue2
    self.equip_region = equip_region
    self.isKeyItem = isKeyItem

class Enemy:
  def __init__(self, enemyName, referenceName, enemyType, prefix, description, color, armor, speed, damage, critChance, health, isBoss, lootTable):
    self.name = enemyName
    self.reference_name = referenceName
    self.enemyType = enemyType
    self.prefix = prefix
    self.description = description
    self.color = color
    self.armor = armor
    self.speed = speed
    self.damage = damage
    self.critChance = critChance #persentage value, range 0-100
    self.health = health
    self.isBoss = isBoss
    self.lootTable = lootTable

itemData = {
  "empty":Item(1,"Empty","empty","empty",0,0,"none",False),
  
  #MISC:
  "rustyKey":Item(1,"Rusty Key","rustyKey","key",0,0,"none",True),

  #BACKPACKS:
  "pockets":Item(1,"Pockets","pockets","backpack",2,0,"bag",False),
  "wornPack":Item(1,"Worn Pack","wornPack","backpack",7,0,"bag",True),
  "cleanPack":Item(1,"Clean Pack","cleanPack","backpack",10,0,"bag",True),
  "backpack":Item(1,"Backpack","backpack","backpack",15,0,"bag",True),
  "largePack":Item(1,"Large Pack","largePack","backpack",25,0,"bag",True),
  "holdingBag":Item(1,"Bag of Holding","holdingBag","backpack",999999999999,0,"bag",True),
  
  #WEAPONS:
  "rustyPipe":Weapon(1,"Rusty Pipe","rustyPipe","melee",2,1),
  "pinataBat":Weapon(1,"Piñata Bat","pinataBat","melee",5,1),
}

#enemyName, referenceName, enemyType, prefix, color, armor, speed, damage, health, isBoss, lootTable
#loot table format: money (range [0,3]) and items -> [0,3,"baseballBat","wornPack"]
enemyData = {
  "greenSlime":Enemy("Green Slime","greenSlime","slime","a","A variant of slime with a green coloring. More akin to plant than creature, some believe they have adapted to capture energy from the sun. Because of this, they are fairly weak.","\033[m",0,1,1,25,5,False,[0,4,[]]),
}