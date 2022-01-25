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
  def __init__(self, enemyName, referenceName, enemyType, prefix, color, armor, speed, damage, health):
    self.name = enemyName
    self.reference_name = referenceName
    self.enemyType = enemyType
    self.prefix = prefix
    self.color = color
    self.armor = armor
    self.speed = speed
    self.damage = damage
    self.health = health

itemData = {
  "pockets":Item(1,"Pockets","pockets","backpack",2,0,"bag",False),
  
  "wornPack":Item(1,"Worn Pack","wornPack","backpack",7,0,"bag",True),
  "cleanPack":Item(1,"Clean Pack","cleanPack","backpack",10,0,"bag",True),
  "backpack":Item(1,"Backpack","backpack","backpack",15,0,"bag",True),
  "largePack":Item(1,"Large Pack","largePack","backpack",25,0,"bag",True),
  "holdingBag":Item(1,"Bag of Holding","holdingBag","backpack",999999999999,0,"bag",True),
  
  "baseballBat":Weapon(1,"Baseball Bat","baseballBat","melee",5,1),
  "pinataBat":Weapon(1,"Piñata Bat","pinataBat","melee",5,1),
}

enemyData = {
  "greenSlime":Enemy("Green Slime","greenSlime","slime","a","\033[92m",0,1,1,5)
}