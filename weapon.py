from __future__ import annotations
from abc import ABC, abstractmethod
import pygame

from projectile import FireWandProjectile, KnifeProjectile, MagicWandProjectile, Projectile

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
    def create_projectile(self, x:float, y:float, direction:int, space, player):
        pass

class Knife(Weapon):
    IMAGE = pygame.image.load('Assets/Projectiles/Icon-Knife.jpg')

    def __init__(self) -> None:
        super().__init__(5, 10, Knife.IMAGE, "knife")
    
    def create_projectile(self, x:float, y:float, direction:int, space, player) -> Projectile:
        return KnifeProjectile(x, y, direction, space)

class MagicWand(Weapon):
    IMAGE = pygame.image.load('Assets/Weapons/Sprite-Magic_Wand.png')

    def __init__(self) -> None:
        super().__init__(5, 10, MagicWand.IMAGE, "magic_wand")
    
    def create_projectile(self, x:float, y:float, direction:int, space, player) -> Projectile:
        return MagicWandProjectile(x, y, direction, space)
    
class FireWand(Weapon):
    IMAGE = pygame.image.load('Assets/Weapons/Sprite-Fire_Wand.png')

    def __init__(self) -> None:
        super().__init__(5, 20, FireWand.IMAGE, "fire_wand")
    
    def create_projectile(self, x:float, y:float, direction:int, space, player) -> Projectile:
        return FireWandProjectile(x, y, direction, space, player)