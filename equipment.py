from __future__ import annotations
import pygame
import math
import pymunk
from abc import ABC, abstractmethod

class Equipment(ABC):
    '''  '''

    def __init__(self,nombre: str, max_tier: int, associated_stat: int, modifier: float, image) -> None:
        self.name: str = nombre
        self.tier: int = 1
        self.max_tier: int  = max_tier
        self.associated_stat : int  = associated_stat
        self.modifier: float = modifier
        self.image = pygame.transform.scale(image, (image.get_width() * 0.5, image.get_height() * 0.5))

    def upgrade_equipment(self) -> bool:
        '''  '''
        if(self.tier != self.max_tier):
            self.tier += 1
            return True
        return False

    def get_effect(self):
        return self.associated_stat, self.modifier
    

class Armor(Equipment):
    IMAGE = pygame.image.load('Assets/Equipment/Sprite-Armor.jpg').convert_alpha()

    def __init__(self) -> None:
        super().__init__("armor", 5, 4, 1, Armor.IMAGE)

class HollowHeart(Equipment):
    IMAGE = pygame.image.load('Assets/Equipment/Sprite-Hollow_Heart.jpg').convert_alpha()

    def __init__(self) -> None:
        super().__init__("hollow heart", 5, 5, 0.1, HollowHeart.IMAGE)

class Spinach(Equipment):
    IMAGE = pygame.image.load('Assets/Equipment/Sprite-Spinach.jpg').convert_alpha()

    def __init__(self) -> None:
        super().__init__("spinach", 5, 6, 0.1, Spinach.IMAGE)

class Wings(Equipment):
    IMAGE = pygame.image.load('Assets/Equipment/Sprite-Wings.jpg').convert_alpha()

    def __init__(self) -> None:
        super().__init__("wings", 5, 7, 0.1, Wings.IMAGE)