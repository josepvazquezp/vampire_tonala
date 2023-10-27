import pygame
from sys import exit
import math
from settings import *
from player import *
from projectile import *
'''
El bat tiene HP: 1, power: 5, speed: 1.4
El mantis tiene HP: 150, power: 20, speed: 0.8
El skulon tiene HP: 30, power: 10, speed: 1
El reeper tiene HP: 600, power: 60, speed: 5
'''

class Enemy(pygame.sprite.Sprite):
    ENEMIES = []

    def __init__(self, position, hp, speed, power, image, player):
        super().__init__(enemy_group, all_sprites)

        self.hp = hp  # Health points
        self.speed = speed  # Speed of the enemy
        self.power = power

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

    def get_vector_distance(self, player_vector, enemy_vector):
        return (player_vector - enemy_vector).magnitude()

    def update(self):
        self.chase_player()

    def take_damage(self, damage: int):
        ''''''
        self.hp -= damage
        if self.hp <= 0:
            Enemy.ENEMIES.remove(self)
            del self

class Pipeestrello(Enemy):
    def __init__(self, position, image, player):
        super().__init__(position, 1, 1.4, 5, image, player)

class Mantichana(Enemy):
    def __init__(self, position, image, player):
        super().__init__(position, 150, 0.8, 20, image, player)

class Reaper(Enemy):
    def __init__(self, position, image, player):
        super().__init__(position, 600, 5, 60, image, player)

class Skullone(Enemy):
    def __init__(self, position, image, player):
        super().__init__(position, 30, 1, 10, image, player)

enemy_group = pygame.sprite.Group()