from __future__ import annotations
from abc import ABC, abstractmethod
import math
import pygame
from enemy import Enemy

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
        super().__init__(5, 12, MagicWand.IMAGE, "magic_wand")
    
    def create_projectile(self, x:float, y:float, direction:int, space, player) -> Projectile:
        return MagicWandProjectile(x, y, direction, space)
    
class FireWand(Weapon):
    IMAGE = pygame.image.load('Assets/Weapons/Sprite-Fire_Wand.png')

    def __init__(self) -> None:
        super().__init__(5, 30, FireWand.IMAGE, "fire_wand")
    
    def create_projectile(self, x:float, y:float, direction:int, space, player) -> Projectile:
        angle = 0

        if(len(Enemy.ENEMIES) > 0):
            enemy_vector = pygame.math.Vector2(Enemy.ENEMIES[0].get_enemy_hitbox_rect().center)
            player_vector = pygame.math.Vector2(player.center)

            mul = (enemy_vector.y - player_vector.y)
            div = (enemy_vector.x - player_vector.x)
            
            if(div != 0):
                angle = math.degrees(math.atan(mul / div))
                
        return [FireWandProjectile(x, y, angle - 20, space, player), FireWandProjectile(x, y, angle, space, player), FireWandProjectile(x, y, angle + 20, space, player)]