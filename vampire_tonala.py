import pygame
from sys import exit
import math

import pymunk

from settings import *
from player import *
from projectile import *
from enemy import *

import time
import threading
from threading import Event


# Initialize pygame
pygame.init()

space = pymunk.Space()
space.gravity = (0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Load images
background = pygame.transform.scale(pygame.image.load('Background/background.jpg').convert(), (WIDTH, HEIGHT))

mantisImage = pygame.image.load('Assets/Enemies/Sprite-XLMANTIS.jpg')
batImage = pygame.image.load('Assets/Enemies/Sprite-BAT1.jpg')
skulloneImage = pygame.image.load('Assets/Enemies/Sprite-SKULLNOAURA.jpg')
reaperImage = pygame.image.load('Assets/Enemies/Sprite-BOSS_XLDEATH.jpg')


# Create player
player=Player(100, 5, space)
bat = Pipeestrello((800,700), batImage, player, space)
mantis = Mantichana((400,600), mantisImage, player, space)
skullone = Skullone((200,200), skulloneImage, player, space)
reaper = Reaper((800,620), reaperImage, player, space)

all_sprites.add(player)

flagC = True
gameSeconds = 0
gameMin = 0
playing = True

stop_event = Event()

def draw_entity(screen, entity):
    for shape in entity.body.shapes:
        if isinstance(shape, pymunk.Circle):
            pos_x, pos_y = map(int, shape.body.position)
            pygame.draw.circle(screen, (255, 0, 0), (pos_x, pos_y), int(shape.radius))

def detectar_colision(p : Player, e: Enemy, flag: bool) -> bool:
    global flagC

    if pygame.Rect.colliderect(p.rect, e.rect) and flag:
        p.take_damage(e.power)
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



def draw_entity(screen, entity):
    for shape in entity.body.shapes:
        if isinstance(shape, pymunk.Circle):
            pos_x, pos_y = map(int, shape.body.position)
            pygame.draw.circle(screen, (255, 0, 0), (pos_x, pos_y), int(shape.radius))


def enemy_hit_player(self, arbiter, space):
    for ene in Enemy.ENEMIES:
        if pygame.Rect.colliderect(player.rect, ene.rect):
            player.take_damage(ene.power)
    return True


def projectile_hit_enemigo(self, arbiter, space):
    for proj in Projectile.PROJECTILES:
        for ene in Enemy.ENEMIES:
            if pygame.Rect.colliderect(proj.rect, ene.rect):
                ene.take_damage(proj.damage)
    return True

handler = space.add_collision_handler(1, 2)
handler.pre_solve =  enemy_hit_player

handler2 = space.add_collision_handler(3, 2)
handler2.begin =  projectile_hit_enemigo



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

    pygame.display.update()
    clock.tick(FPS)
    space.step(1 / FPS)
