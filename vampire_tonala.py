import pygame
from sys import exit
import math
from settings import *
from player import *
from projectile import *
from enemy import *
import pymunk



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
bat=Enemy((800,300), player, 2)
bat2=Enemy((800,300), player, 2)

def draw_entity(screen, entity):
    for shape in entity.body.shapes:
        if isinstance(shape, pymunk.Circle):
            pos_x, pos_y = map(int, shape.body.position)
            pygame.draw.circle(screen, (255, 0, 0), (pos_x, pos_y), int(shape.radius))


all_sprites.add(player)



def detectar_colision(p : Player, e: Enemy):
    if pygame.Rect.colliderect(p.rect, e.rect):
        p.take_damage(e.damage)

while True:


    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    
    #Toda esta madre sirve para hacer un display bien sencillo del HP del cabron
    font = pygame.font.Font(None, 36)
    hp_text = font.render(f'HP: {player.hp}', True, (255, 255, 255))
    screen.blit(hp_text, (10, 10))


    # #Esto es lo más cercano que he logrado hacer para que detecte colision con enemigos
    if Enemy.ENEMIES:
        for enemy_ in Enemy.ENEMIES:
            detectar_colision(player, enemy_)

    

    pygame.display.update()
    clock.tick(FPS)