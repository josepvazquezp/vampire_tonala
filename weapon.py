from __future__ import annotations
from abc import ABC, abstractmethod
import pygame

from projectile import Projectile

class Weapon(ABC):
    def __init__(self, max_tier:int, cooldown:float, image:str, name:str) -> None:
        self.tier:int = 1
        self.max_tier:int = max_tier
        self.cooldown:float = cooldown
        self.actual_cooldown:float = 0
        self.image = image
        self.name = name

    def upgrade_weapon(self) -> None:
        if(self.tier != self.max_tier):
            self.tier += 1
    
    @abstractmethod
    def create_projectile(self, x:float, y:float, direction:int, space):
        pass

class Knife(Weapon):
    IMAGE = pygame.image.load('Assets/Projectiles/navaja.png')

    def __init__(self) -> None:
        super().__init__(3, 10, Knife.IMAGE, "knife")
    
    def create_projectile(self, x:float, y:float, direction:int, space) -> Projectile:
        return Projectile(x, y, direction, space, Knife.IMAGE)