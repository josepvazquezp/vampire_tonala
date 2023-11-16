import pygame
from sys import exit
import math
from enemy import Enemy
from settings import *
import pymunk
from abc import ABC, abstractmethod

class Projectile(pygame.sprite.Sprite, ABC):
    PROJECTILES = []

    def __init__(self,x:float, y:float, angle:int, speed:int, damage:int,space, image):
        super().__init__()
        self.image = image

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        self.angle = angle  
        self.speed = speed
        self.x_vel = self.speed * math.cos(math.radians(self.angle))
        self.y_vel = self.speed * math.sin(math.radians(self.angle))
        self.projectile_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()
        self.damage = damage

        #Todo esto se puede ajustar
        self.body = pymunk.Body(1, 100)
        self.body.position = self.x, self.y
        self.shape = pymunk.Circle(self.body, 10) #El segundo valor es el radio del cuerpo
        self.shape.collision_type = 3
        self.space = space
        space.add(self.body, self.shape)
        
        Projectile.PROJECTILES.append(self)
        
    @abstractmethod
    def projectile_movement(self):
        pass


    def destroy_projectile(self):
        self.space.remove(self.body, self.shape)
        Projectile.PROJECTILES.remove(self)
        self.kill()
    
    
    def update(self):
        self.projectile_movement()

    def get_vector_distance(self, enemy_vector, projectile_vector):
        return (enemy_vector - projectile_vector).magnitude()

class KnifeProjectile(Projectile):
    IMAGE = pygame.transform.rotozoom(pygame.image.load('Assets/Projectiles/navaja.png'), 0, .25)

    def __init__(self, x:float, y:float, angle:int, space) -> None:
        image = KnifeProjectile.IMAGE

        if(angle != 0):
            image = pygame.transform.rotate(image, angle)
            if(angle == 270 or angle == 90):
                image = pygame.transform.flip(image, False, True)

        super().__init__(x, y, angle, 10, 10, space, image)

    def projectile_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x = (self.x)
        self.rect.y = (self.y)
        self.body.position = self.x, self.y
        if pygame.time.get_ticks() - self.spawn_time > self.projectile_lifetime:
            self.destroy_projectile()

class MagicWandProjectile(Projectile):
    IMAGE = pygame.image.load('Assets/Projectiles/magic_wand_projectile.png')

    def __init__(self, x:float, y:float, angle:int, space) -> None:
        super().__init__(x, y, angle, 10, 10, space, MagicWandProjectile.IMAGE)
    
    def projectile_movement(self):
        enemy_vector = pygame.math.Vector2(Enemy.ENEMIES[0].get_enemy_hitbox_rect().center)
        projectile_vector = pygame.math.Vector2(self.rect.center)

        distance = self.get_vector_distance(enemy_vector, projectile_vector)

        if distance > 0:
            self.angle = (enemy_vector - projectile_vector).normalize()
        else:
            self.angle = pygame.math.Vector2(0, 0)

        projectile_vector += self.angle * self.speed

        self.rect.centerx = projectile_vector.x
        self.rect.centery = projectile_vector.y
        self.body.position = projectile_vector.x, projectile_vector.y

class FireWandProjectile(Projectile):
    IMAGE = pygame.image.load('Assets/Projectiles/fire_wand_projectile.png')

    def __init__(self, x:float, y:float, angle:int, space, player) -> None:
        super().__init__(x, y, angle, 10, 10, space, FireWandProjectile.IMAGE)
        self.player = player
        

    def projectile_movement(self):
        enemy_vector = pygame.math.Vector2(Enemy.ENEMIES[0].get_enemy_hitbox_rect().center)
        player_vector = pygame.math.Vector2(self.player.center)
        
        if(enemy_vector - player_vector != 0):
            self.angle = (enemy_vector - player_vector).normalize()
        else:
            self.angle = pygame.math.Vector2(0, 0)

        projectile_vector = pygame.math.Vector2(self.rect.center)
        
        projectile_vector += self.angle * self.speed

        self.rect.centerx = projectile_vector.x
        self.rect.centery = projectile_vector.y
        self.body.position = projectile_vector.x, projectile_vector.y

projectile_group = pygame.sprite.Group()