import pygame
from sys import exit
import math
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self,x,y,angle):
        super().__init__()
        self.image = pygame.image.load('Assets/Projectiles/Icon-KnifeBG.jpg').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,.25)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        self.angle = angle  
        self.speed = 10
        self.x_vel = self.speed * math.cos(math.radians(self.angle))
        self.y_vel = self.speed * math.sin(math.radians(self.angle))
        self.projectile_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()
    
    def projectile_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x = (self.x)
        self.rect.y = (self.y)

        if pygame.time.get_ticks() -self.spawn_time > self.projectile_lifetime:
            self.kill()
    
    
    def update(self):
        self.projectile_movement()
projectile_group = pygame.sprite.Group()