import pygame
from sys import exit
import math

import pymunk
from chest import Chest
from item import Item

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


#reaper = Reaper((800,620), reaperImage, player, space)

#Spawn variables
MAX_ENEMIES = 12
SPAWN_RADIUS = 300  # radius around the player within which enemies will spawn
spawned_enemies = []  # List to keep track of spawned enemies
ENEMY_TYPES = ['1', '2', '3']  # Add more enemy types as needed
ENEMY_SPAWN_RATE = [60, 120, 180]  # The game time (in seconds) at which new enemy types are introduced
current_enemy_types = ['1']  # List to keep track of current enemy types


all_sprites.add(player)


gameSeconds = 0
gameMin = 0
playing = True

stop_event = Event()
enemyCooldown = []

def spawn_enemy(player, angle, enemy_type):
    playerposcoord= convert_coordinates(player.pos)
    ppx=playerposcoord[0]
    ppy=playerposcoord[1]
    x = ppx + SPAWN_RADIUS * math.cos(math.radians(angle))
    y = ppy + SPAWN_RADIUS * math.sin(math.radians(angle))
    if enemy_type == '1':
        enemy = Pipeestrello((x, y), batImage, player, space)
    elif enemy_type == '2':
        enemy = Skullone((x, y), skulloneImage, player, space)
    elif enemy_type == '3':
        enemy = Mantichana((x, y), mantisImage, player, space)
    spawned_enemies.append(enemy)


angle_increment = 360 / MAX_ENEMIES
current_angle = 0  # To keep track of the last spawn angle

def updateSpawn():
    global current_angle
    if len(spawned_enemies) < MAX_ENEMIES:
        enemy_type = random.choice(current_enemy_types)
        spawn_enemy(player, current_angle, enemy_type)
        current_angle += angle_increment
        if current_angle >= 360:
            current_angle = 0


'''
def detectar_colision(p : Player, e: Enemy, flag: bool) -> bool:
    global flagC

    if pygame.Rect.colliderect(p.rect, e.rect) and flag:
        p.take_damage(e.power)
        flagC = False
'''

def timer(segundos):
    global gameSeconds, gameMin, playing, current_enemy_types
    milis = 0

    while playing:
        if stop_event.isSet():
            playing = False

        milis += 1

        if(milis == 10):
            milis = 0

            gameSeconds += 1

            # Update enemy types
            for i, time_threshold in enumerate(ENEMY_SPAWN_RATE):
                 if gameSeconds >= time_threshold:
                     if ENEMY_TYPES[i] not in current_enemy_types:
                         current_enemy_types.append(ENEMY_TYPES[i])

            if gameSeconds == 60:
                gameMin += 1
                gameSeconds = 0

            for ene in enemyCooldown:
                ene.attackCooldown -= 1

                if(ene.attackCooldown == 0):
                    enemyCooldown.remove(ene)

        player.using_weapon()

        time.sleep(0.1)

hilo = threading.Thread(target=timer, args=(10,))
hilo.start()

def draw_entity(screen, entity):
    for shape in entity.body.shapes:
        if isinstance(shape, pymunk.Circle):
            pos_x, pos_y = map(int, shape.body.position)
            pygame.draw.circle(screen, (255, 0, 0), (pos_x, pos_y), int(shape.radius))

#Manejadores de Colisiones
#=========================================================================================================

def enemy_hit_player(self, arbiter, space):
    for ene in Enemy.ENEMIES:
        if pygame.Rect.colliderect(player.rect, ene.rect) and ene.attackCooldown == 0:
            player.take_damage(ene.power)

            ene.restoreCooldown()
            enemyCooldown.append(ene)
    return True

def player_pick_item(self, arbiter, space):
    for it in Item.ITEMS:
        if pygame.Rect.colliderect(player.rect, it.rect):
            stat, mod = it.pick_up()
            player.apply_stat(stat, mod)
            it.destroy()
    return True

def player_pick_chest(self, arbiter, space):
    for che in Chest.CHESTS:
        if pygame.Rect.colliderect(player.rect, che.rect):
            che.open_chest()
            
    return True

def projectile_hit_enemigo(self, arbiter, space):
    for proj in Projectile.PROJECTILES:
        for ene in Enemy.ENEMIES:
            if pygame.Rect.colliderect(proj.rect, ene.rect):
                ene.take_damage(proj.damage)
    return True

handler = space.add_collision_handler(1, 2)
handler.pre_solve =  enemy_hit_player

item_hanlder = space.add_collision_handler(1, 3)
item_hanlder.begin = player_pick_item


chest_handler = space.add_collision_handler(1, 4)
chest_handler.begin =  player_pick_chest

handler2 = space.add_collision_handler(3, 2)
handler2.begin =  projectile_hit_enemigo
#=========================================================================================================


while True:
    updateSpawn()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_event.set()
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    all_sprites.update()

    for enemy in spawned_enemies:
        if enemy.is_dead():
            # Logic for removing enemy goes here...
            spawned_enemies.remove(enemy)
            
            # Spawn new enemy
            enemy_type = random.choice(current_enemy_types)
            spawn_enemy(player, current_angle, enemy_type)
            current_angle += angle_increment
            if current_angle >= 360:
                current_angle = 0

    # Toda esta madre sirve para hacer un display bien sencillo del HP del cabron
    font = pygame.font.Font(None, 36)
    hp_text = font.render(f'HP: {player.hp}', True, (255, 255, 255))
    screen.blit(hp_text, (10, 10))

    font = pygame.font.Font(None, 36)
    hp_text = font.render(f'Lvl: {player.level}', True, (255, 255, 255))
    screen.blit(hp_text, (10, 40))

    font = pygame.font.Font(None, 36)
    hp_text = font.render(f'XP: {player.curren_xp}', True, (255, 255, 255))
    screen.blit(hp_text, (10, 70))

    font = pygame.font.Font(None, 36)
    hp_text = font.render(f'Next: {player.next_level_xp}', True, (255, 255, 255))
    screen.blit(hp_text, (10, 100))

    font = pygame.font.Font(None, 80)
    hp_text = font.render(f'Time: {gameMin}:{gameSeconds}', True, (255, 255, 255))
    screen.blit(hp_text, (WIDTH / 2 - 100, 10))

    font = pygame.font.Font(None, 36)
    hp_text = font.render(f'Feria: {player.gold}', True, (255, 255, 255))
    screen.blit(hp_text, (1000, 10))

    pygame.display.update()
    clock.tick(FPS)
    space.step(1 / FPS)