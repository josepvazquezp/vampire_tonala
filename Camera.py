from enum import Enum
from random import choice
import pygame
from sys import exit
import math

import pymunk
from settings import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class CameraGroup(pygame.sprite.Group):
    """
    Un grupo de sprites personalizado que representa una cámara en un entorno de juego.

    Gestiona la visualización de sprites en relación a una cámara que sigue a un objetivo
    y dibuja un fondo que se ajusta a la posición de la cámara.

    Atributos:
        display_surface (Surface): Superficie de visualización de Pygame.
        offset (Vector2): Desplazamiento de la cámara en relación al objetivo.
        background (Surface): Superficie de Pygame para el fondo del juego.
        background_rect (Rect): Rectángulo que define la posición y el tamaño del fondo.

    Métodos:
        center_target_camera: Centra la cámara en un objetivo específico.
        custom_draw: Dibuja el fondo y los sprites en la superficie de visualización en función del desplazamiento de la cámara.
    """
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #camera offset
        self.offset = pygame.math.Vector2()

        #background
        self.background = pygame.transform.scale(pygame.image.load('Background/background.jpg').convert_alpha(), (10000, 10000))
        self.background_rect = self.background.get_rect(center=(WIDTH//2, HEIGHT//2))  

    def center_target_camera(self, target):
        """
        Centra la cámara en el objetivo dado.

        Args:
            target: El objetivo (generalmente un sprite) que la cámara debe seguir.
        """
        # ...
        self.offset.x= WIDTH/2 - target.body.position[0]
        self.offset.y= HEIGHT/2 - target.body.position[1]


    def custom_draw(self, player):
        """
        Dibuja el fondo y los sprites en la superficie de visualización.

        Ajusta la posición de los sprites y el fondo en función de la posición del jugador
        y el desplazamiento de la cámara. Ordena los sprites basándose en su posición y 
        los dibuja en la superficie de visualización.

        Args:
            player: El jugador u objeto que la cámara está siguiendo.
        """
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