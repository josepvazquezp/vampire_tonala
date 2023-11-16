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


    def custom_draw(self,player):

        self.center_target_camera(player)

        #background
        ground_offset= self.background_rect.topleft + self.offset
        self.display_surface.blit(self.background, ground_offset)

        #Esto nos permite hacer draw a elementos unos sobre otro dependiendo de su posicion en y
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft+self.offset
            self.display_surface.blit(sprite.image, offset_position)

all_sprites = CameraGroup()