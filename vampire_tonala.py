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
bat2=Enemy((800,300), player)

enemies = [bat, bat2]
all_sprites.add(player)


#La función llama a una función que detecta la colisión entre dos objetos, pero sería mejor que detecte siempre que es una instancia de player con una instancia de enemy
#En otras palabras, se debe obtener el objeto que colisiona con Player y ver si es enemigo y hacer este desmadre
def detectar_colision(p : Player, e: Enemy):
    if pygame.Rect.colliderect(p.rect, e.rect):
        p.hp -= 1

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


    #Esto es lo más cercano que he logrado hacer para que detecte colision con enemigos
    if enemies:
        for enemy in enemies:
            detectar_colision(player, enemy)

    

    pygame.display.update()
    clock.tick(FPS)


