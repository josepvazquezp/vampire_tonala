import pygame
from sys import exit
import math
from settings import *
from player import *
'''
El bat tiene HP: 1, power: 5, speed: 1.4
El mantis tiene HP: 150, power: 20, speed: 0.8
El skulon tiene HP: 30, power: 10, speed: 1
El reeper tiene HP: 600, power: 60, speed: 5
'''

class Enemy(pygame.sprite.Sprite):
    ENEMIES = []


    def __init__(self, position, player, type):
        super().__init__(enemy_group, all_sprites)

        self.hp = 10  # Health points
        self.speed = 1  # Speed of the enemy
        self.damage = 5

        # Image and hitbox
        self.image = pygame.image.load('Assets/Enemies/Sprite-BAT1.jpg').convert_alpha()
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

        # self.body = pymunk.Body(1, 100)
        # self.body.position = position
        # self.shape = pymunk.Circle(self.body, 10)
        # self.shape.collision_type = type


    def take_damage(self, damage: int):
         ''''''
         self.hp -= damage
         if self.hp <= 0:
              Enemy.ENEMIES.remove(self)
              del self

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
        # self.body.position = self.position.x, self.position.y

    def get_vector_distance(self, player_vector, enemy_vector):
        return (player_vector - enemy_vector).magnitude()

    def update(self):
         
        self.chase_player()

enemy_group = pygame.sprite.Group()