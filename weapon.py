from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import math
import pygame
from enemy import Enemy

from projectile import FireWandProjectile, KnifeProjectile, MagicWandProjectile, Projectile

class Weapon(ABC):
    """
    Representa una arma abstracta en el juego con propiedades básicas.

    Atributos:
        tier (int): Nivel actual del arma.
        max_tier (int): Nivel máximo al que puede ascender el arma.
        cooldown (float): Tiempo de enfriamiento entre usos del arma.
        actual_cooldown (float): Tiempo actual de enfriamiento.
        image (str): Ruta de la imagen del arma.
        name (str): Nombre del arma.
        type: Tipo de arma, definido por una enumeración o similar.

    Métodos:
        upgrade_weapon: Aumenta el nivel del arma si no ha alcanzado su máximo.
    """
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

            if(self.tier % 2 == 0):
                self.type.value.damage += 0.1
            else:
                self.type.value.speed += 0.1

# 1.- Interface para weapons
class SpecificWeapon(ABC):
    """
    Interfaz para la creación de armas específicas y sus proyectiles asociados.

    Métodos abstractos:
        create: Crea y retorna un objeto de tipo Weapon.
        create_projectile: Crea y retorna un objeto de tipo Projectile.
    """
    def create(self) -> Weapon:
        ''' Crea una weapon en especifico y retorna ese objeto'''
        pass
    
    def create_projectile(self, x:float, y:float, direction:int, space, player, damage, speed) -> Projectile:
        pass

class Knife(SpecificWeapon):
    """
    Implementa la interfaz SpecificWeapon para crear un arma tipo 'Knife' y sus proyectiles.

    Atributos estáticos:
        IMAGE: Imagen asociada al arma 'Knife'.

    Métodos:
        create: Crea y retorna una instancia de Weapon configurada como un 'Knife'.
        create_projectile: Crea y retorna una instancia de KnifeProjectile.
    """
    IMAGE = pygame.transform.rotozoom(pygame.image.load('Assets/Projectiles/Icon-Knife.jpg'), 0, .5)
    name = "knife"
    damage = 6.5
    speed = 10

    def create(self) -> Weapon:
        return Weapon(8, 10, Knife.IMAGE, "knife", FactoryWeapon.WeaponCatalog.KNIFE)
    
    def create_projectile(self, x:float, y:float, direction:int, space, player, damage, speed) -> Projectile:
        return KnifeProjectile(x, y, direction, space, damage * player.attack, speed)

class MagicWand(SpecificWeapon):
    """
    Implementa la interfaz SpecificWeapon para crear un arma tipo 'Magic Wand' y sus proyectiles.

    Atributos estáticos:
        IMAGE: Imagen asociada al arma 'Magic Wand'.

    Métodos:
        create: Crea y retorna una instancia de Weapon configurada como un 'Magic Wand'.
        create_projectile: Crea y retorna una instancia de MagicWandProjectile.
    """
    IMAGE = pygame.transform.rotozoom(pygame.image.load('Assets/Weapons/Sprite-Magic_Wand.png'), 0, .5)
    
    name = "magicwand"
    damage = 10
    speed = 10

    def create(self) -> Weapon:
        return Weapon(8, 20, MagicWand.IMAGE, "magic_wand", FactoryWeapon.WeaponCatalog.MAGIC_WAND)
    
    def create_projectile(self, x:float, y:float, direction:int, space, player, damage, speed) -> Projectile:
        return MagicWandProjectile(x, y, direction, space, damage * player.attack, speed)
    
class FireWand(SpecificWeapon):
    """
    Implementa la interfaz SpecificWeapon para crear un arma tipo 'Fire Wand' y sus proyectiles.

    Atributos estáticos:
        IMAGE: Imagen asociada al arma 'Fire Wand'.

    Métodos:
        create: Crea y retorna una instancia de Weapon configurada como un 'Fire Wand'.
        create_projectile: Crea y retorna instancias de FireWandProjectile.
            Calcula el ángulo de disparo basándose en la posición del jugador y el enemigo más cercano.
    """
    IMAGE = pygame.transform.rotozoom(pygame.image.load('Assets/Weapons/Sprite-Fire_Wand.png'), 0, .5)
    name = "firewand"
    damage = 20
    speed = 7.5

    def create(self) -> Weapon:
        return Weapon(8, 30, FireWand.IMAGE, "fire_wand", FactoryWeapon.WeaponCatalog.FIRE_WAND)
    
    def create_projectile(self, x:float, y:float, direction:int, space, player, damage, speed) -> Projectile:
        angle = 0

        if(len(Enemy.ENEMIES) > 0):
            enemy_vector = pygame.math.Vector2(Enemy.ENEMIES[0].get_enemy_hitbox_rect().center)
            player_vector = pygame.math.Vector2(player.get_player_hitbox_rect().center)

            mul = (enemy_vector.y - player_vector.y)
            div = (enemy_vector.x - player_vector.x)
            
            if(div != 0):
                angle = math.degrees(math.atan(mul / div))
                
        return [FireWandProjectile(x, y, angle - 20, space, damage * player.attack, speed), FireWandProjectile(x, y, angle, space, damage * player.attack, speed), FireWandProjectile(x, y, angle + 20, space, damage * player.attack, speed)]
    
class FactoryWeapon():
    """
    Fábrica para la creación de armas basada en un catálogo de armas definido.

    Atributos estáticos:
        WeaponCatalog (Enum): Enumeración que define los tipos de armas disponibles.

    Métodos:
        create_weapon: Crea y retorna una instancia de Weapon basada en el tipo especificado.
    """
    class WeaponCatalog(Enum):
             KNIFE = Knife()
             MAGIC_WAND = MagicWand()
             FIRE_WAND = FireWand()
     
    def create_weapon(self, type) -> Weapon:
        return type.value.create()