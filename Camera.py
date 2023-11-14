from enum import Enum
from random import choice
import pygame
from sys import exit
import math

import pymunk
from settings import *
# import button

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class CameraGroup(pygame.sprite.Group):

    # RESUME_BUTTON = button.Button(WIDTH / 2 - pygame.image.load("Assets/buttons/button_resume.png").convert_alpha().get_width() / 2, 400, pygame.image.load("Assets/buttons/button_resume.png").convert_alpha(), 1)
    # QUIT_BUTTON = button.Button(WIDTH / 2 - pygame.image.load("Assets/buttons/button_quit.png").convert_alpha().get_width() / 2, 550, pygame.image.load("Assets/buttons/button_quit.png").convert_alpha(), 1)
    # OPEN_BUTTON = button.Button(WIDTH / 2 - pygame.image.load("Assets/buttons/button_open.png").convert_alpha().get_width()/2, 500, pygame.image.load("Assets/buttons/button_open.png").convert_alpha(), 1)

    # SURFACE = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # TREASURE_B = pygame.image.load("Assets/screens/treasure_background.png").convert_alpha()

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

    # def draw_time(self, min, seconds):
    #     font = pygame.font.Font(None, 50)
    #     hp_text = font.render(f'Time: {min}:{seconds}', True, (255, 255, 255))
    #     self.display_surface.blit(hp_text, (WIDTH / 2 - 50, 10))
    
    # def draw_pause(self, game, stop_event):
    #     font = pygame.font.Font(None, 48)

    #     pygame.draw.rect(CameraGroup.SURFACE, (0, 0, 0, 150), [0,0, WIDTH, HEIGHT])
    
    #     self.display_surface.blit(CameraGroup.SURFACE, (0,0))
    #     pause_text = font.render(f'GAME PAUSED', True, (255, 255, 255))
    #     self.display_surface.blit(pause_text, (WIDTH / 2 - 100, 100))

    #     if CameraGroup.RESUME_BUTTON.draw(screen):
    #         game.current_state.change_to_play()
    #         game.change_paused()

    #     if CameraGroup.QUIT_BUTTON.draw(screen):
    #         stop_event.set()
    #         pygame.quit()
    #         exit()
    
    # def draw_chest(self, game):
    #     self.display_surface.blit(CameraGroup.SURFACE, (0,0))
    #     self.display_surface.blit(CameraGroup.TREASURE_B, (WIDTH/2 - 175,20))

    #     if CameraGroup.OPEN_BUTTON.draw(screen):
    #         game.current_state.change_to_play()
    #         game.change_paused()


all_sprites = CameraGroup()