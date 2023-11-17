from __future__ import annotations
from enum import Enum
import pygame
import math
import pymunk
from abc import ABC, abstractmethod

class Equipment():
    '''  '''

    def __init__(self, max_tier: int, associated_stat: int, modifier: float, name: str, type) -> None:
        self.tier: int = 1
        self.max_tier: int  = max_tier
        self.associated_stat : int  = associated_stat
        self.modifier: float = modifier
        self.name = name
        self.type = type
        #self.image = pygame.transform.scale(image, (image.get_width() * 0.5, image.get_height() * 0.5))

    def upgrade_equipment(self) -> bool:
        '''  '''
        if(self.tier != self.max_tier):
            self.tier += 1
            return True
        return False

    def get_effect(self):
        return self.associated_stat, self.modifier
    

class SpecificEquipment(ABC):
    def create(self):
        pass


class Armor(SpecificEquipment):
    IMAGE = pygame.image.load('Assets/Equipment/Sprite-Armor.jpg').convert_alpha()
    NAME = "armor"
    STAT = 4
    MOFIFIER = 1

    def create(self) -> None:
        return Equipment(5, 4, 1, "armor", FactoryEquipment.EquipmentCatalog.ARMOR)

class HollowHeart(SpecificEquipment):
    IMAGE = pygame.image.load('Assets/Equipment/Sprite-Hollow_Heart.jpg').convert_alpha()
    NAME = "hollow_heart"
    STAT = 5
    MOFIFIER = 0.1

    def create(self) -> Equipment:
        return Equipment( 5, 5, 0.1, "hollow_heart", FactoryEquipment.EquipmentCatalog.HOLLOWHEART)

class Spinach(SpecificEquipment):
    IMAGE = pygame.image.load('Assets/Equipment/Sprite-Spinach.jpg').convert_alpha()
    NAME = "spinach"
    STAT = 6
    MOFIFIER = 0.1

    def create(self)-> Equipment:
        return Equipment(5, 6, 0.1, "spinach", FactoryEquipment.EquipmentCatalog.SPINACH)

class Wings(SpecificEquipment):
    IMAGE = pygame.image.load('Assets/Equipment/Sprite-Wings.jpg').convert_alpha()
    NAME = "wings"
    STAT = 7
    MOFIFIER = 0.1

    def create(self) -> Equipment:
        return Equipment( 5, 7, 0.1, "wings", FactoryEquipment.EquipmentCatalog.WINGS)


class FactoryEquipment():
    class EquipmentCatalog(Enum):
        ARMOR = Armor()
        HOLLOWHEART = HollowHeart()
        SPINACH = Spinach()
        WINGS = Wings()

    def create_equipment(self, type):
        return type.value.create()