import pygame
from sys import exit
import math
from chest import *
from item import *
from settings import *
from player import *
from projectile import *
import random

from abc import ABC, abstractmethod
from enum import Enum

import pymunk
'''
El bat tiene HP: 1, power: 5, speed: 1.4
El mantis tiene HP: 150, power: 20, speed: 0.8
El skulon tiene HP: 30, power: 10, speed: 1
El reeper tiene HP: 600, power: 60, speed: 5
'''

class Enemy(pygame.sprite.Sprite):
    ENEMIES = []

    GEM_IMAGE = pygame.image.load('Assets/Items/Sprite-Experience_Gem.webp')
    CHICKEN_IMAGE = pygame.image.load('Assets/Items/Sprite-Floor_Chicken.webp')
    COIN_IMAGE = pygame.image.load('Assets/Items/Sprite-Gold_Coin.webp')
    CHEST_IMAGE = pygame.image.load('Assets/Items/Sprite-Treasure_Chest.webp')
    

    def __init__(self, position, hp, speed, power, image, player, space, size):
        super().__init__(enemy_group, all_sprites)

        self.hp = hp  # Health points
        self.speed = speed  # Speed of the enemy
        self.power = power
        self.cooldown = 2
        self.attackCooldown = 0

        # Image and hitbox
        self.image = pygame.transform.rotozoom(image.convert_alpha(), 0, .4)
        self.rect = self.image.get_rect()

        # Position and movement
        self.rect.center = position
        self.position = pygame.math.Vector2(position)
        self.direction = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)

        # Apuntador al player
        self.player = player
        Enemy.ENEMIES.append(self)

        self.body = pymunk.Body(1, 100)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, size)
        self.shape.collision_type = 2
        self.space = space
        space.add(self.body, self.shape)

    # Enemy movement
    def chase_player(self):
        player_vector = pygame.math.Vector2(self.player.get_player_hitbox_rect().center)
        enemy_vector = pygame.math.Vector2(self.rect.center)

        distance = self.get_vector_distance(player_vector, enemy_vector)

        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y
        self.body.position = self.position.x, self.position.y

    def is_dead(self):
        return self.hp <= 0
    
    def get_vector_distance(self, player_vector, enemy_vector):
        return (player_vector - enemy_vector).magnitude()

    def update(self):
        self.chase_player()

    def take_damage(self, damage: int):
        ''''''
        self.hp -= damage
        if self.hp <= 0:
            self.drop_item()
            self.space.remove(self.body, self.shape)
            Enemy.ENEMIES.remove(self)
            self.kill()

    def drop_item(self):
        ''''''
        

        choice = random.randint(0, 100)

        if choice < 50:
            return
        elif choice >= 50 and choice <= 76:
            self.item = ExperienceGem((self.position.x, self.position.y), self.space, Enemy.GEM_IMAGE)

        elif choice >= 77 and choice <= 86:
            self.item = FloorChicken((self.position.x, self.position.y), self.space, Enemy.CHICKEN_IMAGE)

        elif choice >= 87 and choice <= 97:
            self.item = GoldCoin((self.position.x, self.position.y), self.space, Enemy.COIN_IMAGE)
        elif choice >= 98 and choice <= 100:
            self.chest = Chest((self.position.x, self.position.y), self.space, Enemy.CHEST_IMAGE)
            chest_group.add(self.chest)
            all_sprites.add(self.chest)
            return

        items_group.add(self.item)
        all_sprites.add(self.item)

    def restoreCooldown(self):
        self.attackCooldown = self.cooldown

    def get_enemy_hitbox_rect(self):
        return self.rect

# 1.- Interface para enemies
class SpecificEnemy(ABC):

    @abstractmethod
    def create(self, position, player, space) -> Enemy:
        ''' Crea un enemigo especifico y retorna ese objeto'''
        pass


class Pipeestrello(SpecificEnemy):
    IMAGE = pygame.image.load('Assets/Enemies/Sprite-BAT1.jpg')

    def create(self, position, player, space) -> Enemy:
        return Enemy(position, 1, 1.4, 5, Pipeestrello.IMAGE, player, space, 15)

class Mantichana(SpecificEnemy):
    IMAGE = pygame.image.load('Assets/Enemies/Sprite-XLMANTIS.jpg')

    def create(self, position, player, space) -> Enemy:
        return Enemy(position, 150, 0.8, 20, Mantichana.IMAGE, player, space, 40)

class Reaper(SpecificEnemy):
    IMAGE = pygame.image.load('Assets/Enemies/Sprite-BOSS_XLDEATH.jpg')

    def create(self, position, player, space) -> Enemy:
        return Enemy(position, 600, 10, 9999, Reaper.IMAGE, player, space, 40)

class Skullone(SpecificEnemy):
    IMAGE = pygame.image.load('Assets/Enemies/Sprite-SKULLNOAURA.jpg')

    def create(self, position, player, space) -> Enemy:
        return Enemy(position, 30, 1, 10, Skullone.IMAGE, player, space, 25)

class FactoryEnemy():
    class EnemyCatalog(Enum):
             PIPEESTRELLO = Pipeestrello()
             SKULLONE = Skullone()
             MANTICHANA = Mantichana()
             REAPER = Reaper()
     
    def create_enemy(self, position, player, space, type) -> Enemy:
        return type.value.create(position, player, space)

enemy_group = pygame.sprite.Group()