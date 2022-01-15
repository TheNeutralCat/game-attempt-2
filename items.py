class Armor:
  def __init__(self, quantity, armorName, referenceName, defense, agility, stamina, strength, health):
    self.quantity = quantity
    self.name = armorName
    self.referenceName = referenceName
    self.defense = defense
    self.agility = agility
    self.stamina = stamina
    self.strength = strength
    self.health = health

class Weapon:
  def __init__(self, quantity, weaponName, referenceName, damageType, damageValue, speed):
    self.quantity = quantity
    self.name = weaponName
    self.referenceName = referenceName
    self.damageType = damageType
    self.damageValue = damageValue
    self.speed = speed

class Item:
  def __init__(self, quantity, itemName, referenceName, itemType):
    self.quantity = quantity
    self.name = itemName
    self.referenceName = referenceName
    self.itemType = itemType

from json import JSONEncoder
class myClass(JSONEncoder):
  def default(self, o):
    return o.__dict__

itemData = {
  "baseballBat":Weapon(1, "Baseball Bat", "baseballBat", "melee", 5, 1),
  "pinataBat":Weapon(1, "Piñata Bat", "pinataBat", "melee", 5, 1),
}

