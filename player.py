import pygame
import math
from settings import *
from projectile import *

class Player(pygame.sprite.Sprite):
    def __init__(self, hp, speed):
        super().__init__()
        self.pos = pygame.math.Vector2(WIDTH/2, HEIGHT/2)
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/Characters/Antonio/Sprite-Antonio.jpg').convert_alpha(),0,.5)
        self.speed = speed
        self.hp = hp
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.use_weapon=False
        self.weapon_cooldown=0
        self.current_direction = 0

    def take_damage(self, damage: int):
        ''' '''
        self.hp -= damage

    def player_rotate(self):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_a]):
            self.image = pygame.transform.flip(self.base_player_image,True,False)
        elif(keys[pygame.K_d]):
            self.image = self.base_player_image
        
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
    
    def get_player_hitbox_rect(self):
        return self.hitbox_rect
    
    def user_input(self):

        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed

        if self.velocity_x != 0 and self.velocity_y != 0: # Diagonal movement
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if keys[pygame.K_SPACE]:
            self.use_weapon=True
            self.using_weapon()
        else:
            self.use_weapon=False

    def using_weapon(self):
        keys = pygame.key.get_pressed()
        if self.weapon_cooldown == 0:
            self.weapon_cooldown = 10
            spawn_projectile = self.pos
            
            if keys[pygame.K_d]:
                self.current_direction = 0
            elif keys[pygame.K_a]:
                self.current_direction = 180
            elif keys[pygame.K_w]:
                self.current_direction = 270
            elif keys[pygame.K_s]:
                self.current_direction = 90

            self.projectile = Projectile(spawn_projectile[0],spawn_projectile[1],self.current_direction)
            projectile_group.add(self.projectile)
            all_sprites.add(self.projectile)

    
    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x,self.velocity_y)
        self.hitbox_rect.center = self.pos

    def update(self):
        self.user_input()
        self.move()
        self.player_rotate()

        if self.weapon_cooldown > 0:
            self.weapon_cooldown -= 1
all_sprites = pygame.sprite.Group()
