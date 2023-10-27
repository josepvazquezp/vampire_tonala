import pygame
from sys import exit
import math
from settings import *
from player import *
from projectile import *
from enemy import *

import time
import threading
from threading import Event


# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Load images
background = pygame.transform.scale(pygame.image.load('Background/background.jpg').convert(), (WIDTH, HEIGHT))

mantisImage = pygame.image.load('Assets/Enemies/Sprite-XLMANTIS.jpg')
batImage = pygame.image.load('Assets/Enemies/Sprite-BAT1.jpg')
# Create player
player=Player(100, 5)
bat=Enemy((800,600), 1, 1.4, 5, batImage, player)
mantis = Enemy((400,600), 150, 0.8, 20, mantisImage, player)

enemies = [bat, mantis]
all_sprites.add(player)

flagC = True
gameSeconds = 0
gameMin = 0
playing = True

stop_event = Event()

def detectar_colision(p : Player, e: Enemy, flag: bool) -> bool:
    global flagC

    if pygame.Rect.colliderect(p.rect, e.rect) and flag:
        p.hp -= e.power
        flagC = False

def timer(segundos):
    global flagC, gameSeconds, gameMin, playing
    while playing:
        if stop_event.isSet():
            playing = False

        if flagC == False:
            flagC = True

        gameSeconds += 1

        if gameSeconds == 60:
            gameMin += 1
            gameSeconds = 0

        time.sleep(1)

hilo = threading.Thread(target=timer, args=(10,))
hilo.start()

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_event.set()
            pygame.quit()
            exit()


    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    all_sprites.update()

    # Toda esta madre sirve para hacer un display bien sencillo del HP del cabron
    font = pygame.font.Font(None, 36)
    hp_text = font.render(f'HP: {player.hp}', True, (255, 255, 255))
    screen.blit(hp_text, (10, 10))

    font = pygame.font.Font(None, 80)
    hp_text = font.render(f'Time: {gameMin}:{gameSeconds}', True, (255, 255, 255))
    screen.blit(hp_text, (WIDTH / 2 - 100, 10))

    # Esto es lo más cercano que he logrado hacer para que detecte colision con enemigos
    if enemies:
        for enemy in enemies:
            detectar_colision(player, enemy, flagC)

    pygame.display.update()
    clock.tick(FPS)


