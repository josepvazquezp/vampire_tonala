import pygame
from sys import exit
import math
from settings import *
from player import *
from projectile import *
from enemy import *




# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Load images
background = pygame.transform.scale(pygame.image.load('Background/background.jpg').convert(), (WIDTH, HEIGHT))

class Enemy(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__(enemy_group,all_sprites)

        self.hp=None # Health points
        self.speed=None # Speed of the enemy

        #Image and hitbox
        self.image = pygame.image.load('Assets/Enemies/Sprite-BAT1.jpg').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,.4)
        self.rect = self.image.get_rect()

        #Position and movement
        self.rect.center = position
        self.position=pygame.math.Vector2(position)
        self.direction=pygame.math.Vector2(0,0)
        self.velocity=pygame.math.Vector2(0,0)

        

        
    #Enemy movement
    def chase_player(self):
        player_vector= pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector= pygame.math.Vector2(self.rect.center)

        distance=self.get_vector_distance(player_vector,enemy_vector)

        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2(0,0)

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def get_vector_distance(self,player_vector,enemy_vector):
        return (player_vector - enemy_vector).magnitude()
    def update(self):
        self.chase_player()




enemy_group = pygame.sprite.Group()
# Create player
player=Player()
bat=Enemy((800,600))
all_sprites.add(player)

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    all_sprites.update()

    pygame.display.update()
    clock.tick(FPS)


