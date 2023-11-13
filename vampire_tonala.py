from enum import Enum
from random import choice
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
import state
import button

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

# mantisImage = pygame.image.load('Assets/Enemies/Sprite-XLMANTIS.jpg')
# batImage = pygame.image.load('Assets/Enemies/Sprite-BAT1.jpg')
# skulloneImage = pygame.image.load('Assets/Enemies/Sprite-SKULLNOAURA.jpg')
# reaperImage = pygame.image.load('Assets/Enemies/Sprite-BOSS_XLDEATH.jpg')

# knifeImage = pygame.image.load('Assets/Projectiles/navaja.png').convert_alpha()

# gemImage = pygame.image.load('Assets/Items/Sprite-Experience_Gem.webp').convert_alpha()
# chickenImage = pygame.image.load('Assets/Items/Sprite-Floor_Chicken.webp').convert_alpha()
# coinImage = pygame.image.load('Assets/Items/Sprite-Gold_Coin.webp').convert_alpha()

# chestImage = pygame.image.load('Assets/Items/Sprite-Treasure_Chest.webp').convert_alpha()

# items = [gemImage, chickenImage, coinImage, chestImage]

# Create player
player = Player(100, 5, space)
#reaper = Reaper((800,620), reaperImage, player, space)

#Spawn variables

SPAWN_RADIUS = 600  # radius around the player within which enemies will spawn
spawned_enemies = []  # List to keep track of spawned enemies
ENEMY_TYPES = [1,2,3]  # Add more enemy types as needed
ENEMY_SPAWN_RATE = [20, 40, 60]  # The game time (in seconds) at which new enemy types are introduced
current_enemy_types = [1]  # List to keep track of current enemy types


all_sprites.add(player)

gameSeconds = 0
gameMin = 0
playing = True

stop_event = Event()
enemyCooldown = []

surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

class Game:
    def __init__(self) -> None:
        self.current_state : state.State = state.PlayState(self)
        self.paused = False


    def change_state(self, new_state: state.State):
        ''' Método que cambia el estado '''
        self.current_state = new_state
        print("Se cambió el estado")
        print(self.current_state.name)


    def change_paused(self):
        ''' Metodo que cambia entre pausa y jugar '''
        self.paused = not self.paused


this_game = Game()

def spawn_enemy(player, angle, enemy_type):
    playerposcoord= convert_coordinates(player.pos)
    ppx=playerposcoord[0]
    ppy=playerposcoord[1]
    x = ppx + SPAWN_RADIUS * math.cos(math.radians(angle))
    y = ppy + SPAWN_RADIUS * math.sin(math.radians(angle))
    if enemy_type == 1:
        enemy = Pipeestrello((x, y), player, space)
    elif enemy_type == 2:
        enemy = Skullone((x, y), player, space)
    elif enemy_type == 3:
        enemy = Mantichana((x, y), player, space)
    spawned_enemies.append(enemy)

#Spawn variables
max_enemies = 12
angle_increment = 360 / max_enemies
current_angle = 0  # To keep track of the last spawn angle

def updateSpawn():
    global current_angle
    if len(spawned_enemies) < max_enemies:
        enemy_type = random.choice(current_enemy_types)
        spawn_enemy(player, current_angle, enemy_type)
        current_angle += angle_increment
        if current_angle >= 360:
            current_angle = 0

def get_current_enemy_types(game_seconds):
    types = [1]
    for i, threshold in enumerate(ENEMY_SPAWN_RATE):
        if game_seconds >= threshold:
            if ENEMY_TYPES[i] not in types:
                types.append(ENEMY_TYPES[i])
    return types

def timer(segundos):
    global gameSeconds, gameMin, playing, current_enemy_types,max_enemies
    milis = 0
    maxenemy_spawn_control=0

    while playing:
        if stop_event.is_set():
            playing = False


        if not this_game.paused:
            milis += 1

        if(milis == 10):
            milis = 0
            #incremento el numero de enemigos de manera speudoaleatoria
            maxenemy_spawn_control += choice([1,2,3])

            gameSeconds += 1

            if maxenemy_spawn_control >= 10:
                max_enemies += 2
                maxenemy_spawn_control = 0

            if current_enemy_types != ENEMY_TYPES:
                current_enemy_types = get_current_enemy_types(gameSeconds)
            
            
            if gameSeconds == 60:
                gameMin += 1
                gameSeconds = 0
                #randomizo el numero de enemigos que se reduce cada vez que cambien las condiciones de spawn
                max_enemies -= choice([8,11,15])
                #garantizo que el minimo de spawn es 10
                max_enemies = max(10, max_enemies)

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

            if player.is_dead():
                #this_game.current_state.change_to_game_over()
                pass

            ene.restoreCooldown()
            enemyCooldown.append(ene)
            return True
        
    return False

def player_pick_item(self, arbiter, space):
    for it in Item.ITEMS:
        if pygame.Rect.colliderect(player.rect, it.rect):
            stat, mod = it.pick_up()
            player.apply_stat(stat, mod)

            if player.able_to_level_up():
                player.level_up()
                this_game.change_paused()
                this_game.current_state.change_to_level_up()

            it.destroy()
            return True
    
    return False

def player_pick_chest(self, arbiter, space):
    for che in Chest.CHESTS:
        if pygame.Rect.colliderect(player.rect, che.rect):
            che.open_chest()
            this_game.change_paused()
            this_game.current_state.change_to_chest()
            return True
    return False

def projectile_hit_enemigo(self, arbiter, space):
    for proj in Projectile.PROJECTILES:
        for ene in Enemy.ENEMIES:
            if pygame.Rect.colliderect(proj.rect, ene.rect):
                temp = proj.damage
                proj.destroy_projectile()
                ene.take_damage(temp)
                return True
    
    return False

handler = space.add_collision_handler(1, 2)
handler.pre_solve =  enemy_hit_player

item_hanlder = space.add_collision_handler(1, 3)
item_hanlder.begin = player_pick_item


chest_handler = space.add_collision_handler(1, 4)
chest_handler.begin =  player_pick_chest

handler2 = space.add_collision_handler(3, 2)
handler2.begin =  projectile_hit_enemigo
#=========================================================================================================



#Pantallas
#=========================================================================================================
resume_img = pygame.image.load("Assets/buttons/button_resume.png").convert_alpha()
resume_button = button.Button(WIDTH/2 - resume_img.get_width()/2, 400, resume_img, 1)

open_img = pygame.image.load("Assets/buttons/button_open.png").convert_alpha()
open_button = button.Button(WIDTH/2 - resume_img.get_width()/2, 500, open_img, 1)

quit_img = pygame.image.load("Assets/buttons/button_quit.png").convert_alpha()
quit_button = button.Button(WIDTH/2 - resume_img.get_width()/2, 550, quit_img, 1)

treasure_background_img = pygame.image.load("Assets/screens/treasure_background.png").convert_alpha()
level_up_background_img = pygame.image.load("Assets/screens/level_up_background.png").convert_alpha()
item_select_img = pygame.image.load("Assets/screens/item_select.png").convert_alpha()


title_font = pygame.font.Font(None, 48)

def draw_play_screen():
    pass

def draw_pause_screen():
 
    pygame.draw.rect(surface, (0, 0, 0, 150), [0,0, WIDTH, HEIGHT])
    
    screen.blit(surface, (0,0))
    pause_text = title_font.render(f'GAME PAUSED', True, (255, 255, 255))
    screen.blit(pause_text, (WIDTH / 2 - 100, 100))
    


    if resume_button.draw(screen):
        this_game.current_state.change_to_play()
        this_game.change_paused()

    if quit_button.draw(screen):
        stop_event.set()
        pygame.quit()
        exit()


def draw_chest_screen():
    
    screen.blit(surface, (0,0))
    screen.blit(treasure_background_img, (WIDTH/2 - 175,20))

    if open_button.draw(screen):
        this_game.current_state.change_to_play()
        this_game.change_paused()

def draw_level_up_screen():
    
    screen.blit(surface, (0,0))
    screen.blit(level_up_background_img, (WIDTH/2 - 300,20))
    i = 0
    for i in range(2):
        screen.blit(item_select_img, (WIDTH / 2 - 240, 165 * (i+1)))

    #Este botón se va a quitar cuando ya este lista la selección de items
    if resume_button.draw(screen):
        this_game.current_state.change_to_play()
        this_game.change_paused()

def draw_game_over_screen():
    pygame.draw.rect(surface, (255, 0, 0, 150), [0,0, WIDTH, HEIGHT])
    screen.blit(surface, (0,0))

    game_over_text = title_font.render(f'GAME OVER', True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH / 2 - 100, 100))

    if quit_button.draw(screen):
        stop_event.set()
        pygame.quit()
        exit()

def select_screen(screen_name):
    if screen_name == "Pause":
        draw_pause_screen()
    elif screen_name == "Level":
        draw_level_up_screen()
    elif screen_name == "Chest":
        draw_chest_screen()
    elif screen_name == "Over":
        draw_game_over_screen()
#=========================================================================================================



while True:
    updateSpawn()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_event.set()
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if this_game.paused and this_game.current_state.name == "Pause":
                    this_game.current_state.change_to_play()
                    
                elif not this_game.paused and this_game.current_state.name == "Play":
                    this_game.current_state.change_to_pause()
                this_game.change_paused()


    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    if not this_game.paused:
        all_sprites.update()
    
    select_screen(this_game.current_state.name)

    for enemy in spawned_enemies:
        if enemy.is_dead():
           
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

    #max enemies display
    font = pygame.font.Font(None, 36)
    hp_text = font.render(f'Max Enemies: {max_enemies}', True, (255, 255, 255))
    screen.blit(hp_text, (1000, 40))

    #current enemy types display
    font = pygame.font.Font(None, 12)
    hp_text = font.render(f'Current Enemy Types: {current_enemy_types}', True, (255, 255, 255))
    screen.blit(hp_text, (1000, 70))

    pygame.display.update()
    clock.tick(FPS)
    space.step(1 / FPS)