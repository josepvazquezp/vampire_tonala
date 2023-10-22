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


# Create player
player=Player()
bat=Enemy((800,600), player)
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


