import pygame
from sys import exit
import math
from chest import *
from item import *
from settings import *
from player import *
from projectile import *
import random

import pymunk
'''
El bat tiene HP: 1, power: 5, speed: 1.4
El mantis tiene HP: 150, power: 20, speed: 0.8
El skulon tiene HP: 30, power: 10, speed: 1
El reeper tiene HP: 600, power: 60, speed: 5
'''

class Enemy(pygame.sprite.Sprite):
    ENEMIES = []

    def __init__(self, position, hp, speed, power, image, player, space, size, items):
        super().__init__(enemy_group, all_sprites)

        self.hp = hp  # Health points
        self.speed = speed  # Speed of the enemy
        self.power = power
        self.cooldown = 2
        self.attackCooldown = 0

        # Image and hitbox
        self.image = image.convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, .4)
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

        self.items = items

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

        if choice >= 0 and choice <= 10:
            self.chest = Chest((self.position.x, self.position.y), self.space, self.items[3])
            chest_group.add(self.chest)
            all_sprites.add(self.chest)
            return
        elif choice >= 11 and choice <= 40:
            self.item = ExperienceGem((self.position.x, self.position.y), self.space, self.items[0])

        elif choice >= 41 and choice <= 70:
            self.item = FloorChicken((self.position.x, self.position.y), self.space, self.items[1])

        elif choice >= 71 and choice <= 100:
            self.item = GoldCoin((self.position.x, self.position.y), self.space, self.items[2])
        items_group.add(self.item)
        all_sprites.add(self.item)

    def restoreCooldown(self):
        self.attackCooldown = self.cooldown

class Pipeestrello(Enemy):
    def __init__(self, position, image, player, space, items):
        super().__init__(position, 1, 1.4, 5, image, player, space, 15, items)

class Mantichana(Enemy):
    def __init__(self, position, image, player, space, items):
        super().__init__(position, 150, 0.8, 20, image, player, space, 40, items)

class Reaper(Enemy):
    def __init__(self, position, image, player, space, items):
        super().__init__(position, 600, 5, 60, image, player, space, 40, items)

class Skullone(Enemy):
    def __init__(self, position, image, player, space, items):
        super().__init__(position, 30, 1, 10, image, player, space, 25, items)

enemy_group = pygame.sprite.Group()