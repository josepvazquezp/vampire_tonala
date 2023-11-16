from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import math
import pygame
from enemy import Enemy

from projectile import FireWandProjectile, KnifeProjectile, MagicWandProjectile, Projectile

class Weapon(ABC):
    def __init__(self, max_tier:int, cooldown:float, image:str, name:str, type) -> None:
        self.tier:int = 1
        self.max_tier:int = max_tier
        self.cooldown:float = cooldown
        self.actual_cooldown:float = 0
        self.image = image
        self.name = name
        self.type = type

    def upgrade_weapon(self) -> None:
        if(self.tier != self.max_tier):
            self.tier += 1

# 1.- Interface para weapons
class SpecificWeapon(ABC):
    def create(self) -> Weapon:
        ''' Crea una weapon en especifico y retorna ese objeto'''
        pass
    
    def create_projectile(self, x:float, y:float, direction:int, space, player, tier:int) -> Projectile:
        pass

class Knife(SpecificWeapon):
    IMAGE = pygame.image.load('Assets/Projectiles/Icon-Knife.jpg')

    def create(self) -> Weapon:
        return Weapon(5, 10, Knife.IMAGE, "knife", FactoryWeapon.WeaponCatalog.KNIFE)
    
    def create_projectile(self, x:float, y:float, direction:int, space, player, tier:int) -> Projectile:
        return KnifeProjectile(x, y, direction, space, tier)

class MagicWand(SpecificWeapon):
    IMAGE = pygame.image.load('Assets/Weapons/Sprite-Magic_Wand.png')

    def create(self) -> Weapon:
        return Weapon(5, 20, MagicWand.IMAGE, "magic_wand", FactoryWeapon.WeaponCatalog.MAGIC_WAND)
    
    def create_projectile(self, x:float, y:float, direction:int, space, player, tier:int) -> Projectile:
        return MagicWandProjectile(x, y, direction, space, tier)
    
class FireWand(SpecificWeapon):
    IMAGE = pygame.image.load('Assets/Weapons/Sprite-Fire_Wand.png')

    def create(self) -> Weapon:
        return Weapon(5, 30, FireWand.IMAGE, "fire_wand", FactoryWeapon.WeaponCatalog.FIRE_WAND)
    
    def create_projectile(self, x:float, y:float, direction:int, space, player, tier:int) -> Projectile:
        angle = 0

        if(len(Enemy.ENEMIES) > 0):
            enemy_vector = pygame.math.Vector2(Enemy.ENEMIES[0].get_enemy_hitbox_rect().center)
            player_vector = pygame.math.Vector2(player.center)

            mul = (enemy_vector.y - player_vector.y)
            div = (enemy_vector.x - player_vector.x)
            
            if(div != 0):
                angle = math.degrees(math.atan(mul / div))
                
        return [FireWandProjectile(x, y, angle - 20, space, player, tier), FireWandProjectile(x, y, angle, space, player, tier), FireWandProjectile(x, y, angle + 20, space, player, tier)]
    
class FactoryWeapon():
    class WeaponCatalog(Enum):
             KNIFE = Knife()
             MAGIC_WAND = MagicWand()
             FIRE_WAND = FireWand()
     
    def create_weapon(self, type) -> Weapon:
        return type.value.create()