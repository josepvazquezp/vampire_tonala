import pygame
from sys import exit
import math
from settings import *
import pymunk

class Projectile(pygame.sprite.Sprite):
    PROJECTILES = []

    def __init__(self,x,y,angle, space, image):
        super().__init__()
        self.image = image
        if(angle != 0):
            self.image = pygame.transform.rotate(self.image, angle)
            if(angle == 270 or angle == 90):
                self.image = pygame.transform.flip(self.image,False,True)
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
        self.damage = 10

        #Todo esto se puede ajustar
        self.body = pymunk.Body(1, 100)
        self.body.position = self.x, self.y
        self.shape = pymunk.Circle(self.body, 10) #El segundo valor es el radio del cuerpo
        self.shape.collision_type = 3
        self.space = space
        space.add(self.body, self.shape)
        
        Projectile.PROJECTILES.append(self)
        

    def projectile_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x = (self.x)
        self.rect.y = (self.y)
        self.body.position = self.x, self.y
        if pygame.time.get_ticks() - self.spawn_time > self.projectile_lifetime:
            self.destroy_projectile()


    def destroy_projectile(self):
        self.space.remove(self.body, self.shape)
        Projectile.PROJECTILES.remove(self)
        self.kill()
    
    
    def update(self):
        self.projectile_movement()
projectile_group = pygame.sprite.Group()