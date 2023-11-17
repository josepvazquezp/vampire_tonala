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
    """
    A class representing an enemy in a game.

    Attributes:
        ENEMIES (list): A class variable that stores all instances of Enemy.
        hp (int): The health points of the enemy.
        speed (float): The movement speed of the enemy.
        power (int): The power of the enemy, possibly representing attack strength.
        cooldown (int): The cooldown time for the enemy's actions.
        attackCooldown (int): The cooldown for the enemy's attacks.
        image (pygame.Surface): The image representing the enemy.
        rect (pygame.Rect): The rectangle representing the enemy's position and size.
        position (pygame.math.Vector2): The position of the enemy.
        direction (pygame.math.Vector2): The direction of the enemy's movement.
        velocity (pygame.math.Vector2): The velocity of the enemy.
        player (Player): A reference to the player object.
        body (pymunk.Body): The physical body for the enemy in the physics space.
        shape (pymunk.Shape): The shape of the enemy for collision handling.
        space (pymunk.Space): The space to which the enemy's body and shape are added.

    Args:
        position (tuple): The (x, y) position of the enemy.
        hp (int): The health points of the enemy.
        speed (float): The speed of the enemy.
        power (int): The power of the enemy.
        image (pygame.Surface): The image for the enemy sprite.
        player (Player): The player object to interact with.
        space (pymunk.Space): The pymunk space where the enemy will exist.
        size (int): The size of the enemy's collision shape.
    """
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
        """
        Makes the enemy chase the player.

        The method calculates the direction and velocity for the enemy to move towards the player.
        """
        player_vector = pygame.math.Vector2(
            self.player.get_player_hitbox_rect().center)
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
        """
        Checks if the enemy is dead.

        Returns:
            bool: True if the enemy's health points are less than or equal to zero, False otherwise.
        """
        return self.hp <= 0

    def get_vector_distance(self, player_vector, enemy_vector):
        """
        Calculates the distance between the enemy and the player.

        Args:
            player_vector (pygame.math.Vector2): The vector representing the player's position.
            enemy_vector (pygame.math.Vector2): The vector representing the enemy's position.

        Returns:
            float: The distance between the enemy and the player.
        """
        return (player_vector - enemy_vector).magnitude()

    def update(self):
        """
        Updates the enemy's state.

        This method should be called every frame to update the enemy's behavior.
        """
        self.chase_player()

    def take_damage(self, damage: int):
        """
        Applies damage to the enemy.

        Args:
            damage (int): The amount of damage to apply to the enemy.
        """
        self.hp -= damage
        if self.hp <= 0:
            self.drop_item()
            self.space.remove(self.body, self.shape)
            Enemy.ENEMIES.remove(self)
            self.kill()

    def drop_item(self):
        """
        Determines and creates a random item drop upon enemy death.
        """

        choice = random.randint(0, 100)

        if choice < 50:
            return
        elif choice >= 50 and choice <= 76:
            self.item = ExperienceGem(
                (self.position.x, self.position.y), self.space, Enemy.GEM_IMAGE)

        elif choice >= 77 and choice <= 86:
            self.item = FloorChicken(
                (self.position.x, self.position.y), self.space, Enemy.CHICKEN_IMAGE)

        elif choice >= 87 and choice <= 97:
            self.item = GoldCoin(
                (self.position.x, self.position.y), self.space, Enemy.COIN_IMAGE)
        elif choice >= 98 and choice <= 100:
            self.chest = Chest((self.position.x, self.position.y),
                               self.space, Enemy.CHEST_IMAGE)
            chest_group.add(self.chest)
            all_sprites.add(self.chest)
            return

        items_group.add(self.item)
        all_sprites.add(self.item)

    def restoreCooldown(self):
        """
        Resets the enemy's attack cooldown.
        """
        self.attackCooldown = self.cooldown

    def get_enemy_hitbox_rect(self):
        """
        Returns the enemy's hitbox.

        Returns:
            pygame.Rect: The rectangle representing the enemy's hitbox.
        """
        return self.rect

# 1.- Interface para enemies


class SpecificEnemy(ABC):
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
