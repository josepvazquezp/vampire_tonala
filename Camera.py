from enum import Enum
from random import choice
import pygame
from sys import exit
import math

import pymunk
from settings import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class CameraGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #camera offset
        self.offset = pygame.math.Vector2()

        #background
        self.background = pygame.transform.scale(pygame.image.load('Background/background.jpg').convert_alpha(), (10000, 10000))
        self.background_rect = self.background.get_rect(center=(WIDTH//2, HEIGHT//2))  

    def center_target_camera(self, target):
        self.offset.x= WIDTH/2 - target.body.position[0]
        self.offset.y= HEIGHT/2 - target.body.position[1]


    def custom_draw(self, player):
        self.center_target_camera(player)

        # Calcular el offset del fondo
        background_width, background_height = self.background.get_size()
        top_left_x = (self.background_rect.left + self.offset.x) % background_width
        top_left_y = (self.background_rect.top + self.offset.y) % background_height

        # Dibujar el fondo repetido
        for x in range(-background_width, WIDTH + background_width, background_width):
            for y in range(-background_height, HEIGHT + background_height, background_height):
                self.display_surface.blit(self.background, (x + top_left_x, y + top_left_y))

        # Dibujar sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_position)

all_sprites = CameraGroup()