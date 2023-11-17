from enum import Enum
from random import choice
import pygame
from sys import exit
import math
import random
import copy

import pymunk
from Camera import *
from chest import Chest
from item import Item

from settings import *
from player import *
from projectile import *
from enemy import *
import state
import button
import equipment


import time
import threading
from threading import Event


# Initialize pygame
pygame.init()

space = pymunk.Space()
space.gravity = (0, 0)

# Create the screen

pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load('Background/background.jpg').convert(), (WIDTH, HEIGHT))
# Create player
player = Player(100, 5, space)
#reaper = Reaper((800,620), reaperImage, player, space)
#Spawn variables


player.equip_weapon(FactoryWeapon.WeaponCatalog.KNIFE)

#Spawn variables
max_enemies = 12
angle_increment = 360 / max_enemies
current_angle = 0  # To keep track of the last spawn angle
SPAWN_RADIUS = 600  # radius around the player within which enemies will spawn
spawned_enemies = []  # List to keep track of spawned enemies
#ENEMY_TYPES = [1,2,3]  # Add more enemy types as needed
#ENEMY_SPAWN_RATE = [20, 40, 60]  # The game time (in seconds) at which new enemy types are introduced
#current_enemy_types = [1]  # List to keep track of current enemy types


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
        self.selected_item_display = []
        self.level_item_display = [ FactoryWeapon.WeaponCatalog.KNIFE, FactoryWeapon.WeaponCatalog.FIRE_WAND, 
                                   FactoryWeapon.WeaponCatalog.MAGIC_WAND, equipment.FactoryEquipment.EquipmentCatalog.ARMOR,
                                   equipment.FactoryEquipment.EquipmentCatalog.HOLLOWHEART, equipment.FactoryEquipment.EquipmentCatalog.SPINACH,
                                   equipment.FactoryEquipment.EquipmentCatalog.WINGS]
        self.cleaned_weapons : bool = False
        self.cleaned_equipment : bool = False

        #self.equipment_available = [equipment.Armor(), equipment.HollowHeart(), equipment.Spinach(), equipment.Wings()]

        self.chest = None
        self.chest_open = False
        self.chest_item = None

    def change_state(self, new_state: state.State):
        ''' Método que cambia el estado '''
        self.current_state = new_state


    def change_paused(self):
        ''' Metodo que cambia entre pausa y jugar '''
        self.paused = not self.paused

    def clean_weapons(self):
        self.cleaned_weapons = True

    def clean_equipment(self):
        self.cleaned_equipment = True


this_game = Game()
fact_enemy = FactoryEnemy()

enemy_spawn_probabilities = {
    # (minute, enemy_type): probability
    # The sum of probabilities for each minute should be 1
    (0, 1): 1,
    (0, 2): 0,  
    (0, 3): 0,
    (0, 4): 0,
    # The sum of probabilities for each minute should be 2
    (1, 1): 0.7,  
    (1, 2): 0.28,  
    (1, 3): 0.02,
    (1, 4): 0,
    # The sum of probabilities for each minute should be 3
    (2, 1): 0.3,  
    (2, 2): 0.65,  
    (2, 3): 0.05, 
    (2, 4): 0,
    # The sum of probabilities for each minute should be 4
    (3, 1): 0.05,  
    (3, 2): 0.45,  
    (3, 3): 0.5,
    (3, 4): 0,
    # The sum of probabilities for each minute should be 5
    (4, 1): 0,  
    (4, 2): 0.25,  
    (4, 3): 0.75, 
    (4, 4): 0,
    # The sum of probabilities for each minute should be 6
    (5, 1): 0,  
    (5, 2): 0,  
    (5, 3): 0,
    (5, 4): 1, 

}

def spawn_enemy(player, angle, enemy_type):
    ppx=player.body.position[0]
    ppy=player.body.position[1]
    x = ppx + SPAWN_RADIUS * math.cos(math.radians(angle))
    y = ppy + SPAWN_RADIUS * math.sin(math.radians(angle))
    if enemy_type == 1:
        enemy = fact_enemy.create_enemy((x, y), player, space, FactoryEnemy.EnemyCatalog.PIPEESTRELLO) 
    elif enemy_type == 2:
        enemy = fact_enemy.create_enemy((x, y), player, space, FactoryEnemy.EnemyCatalog.SKULLONE) 
    elif enemy_type == 3:
        enemy = fact_enemy.create_enemy((x, y), player, space, FactoryEnemy.EnemyCatalog.MANTICHANA)
    elif enemy_type == 4:
        enemy = fact_enemy.create_enemy((x, y), player, space, FactoryEnemy.EnemyCatalog.REAPER)
    spawned_enemies.append(enemy)


def updateSpawn():
    """
    Update and manage the spawning of enemies based on time-based probabilities.

    This function checks if the current number of spawned enemies is less than the maximum allowed.
    If so, it calculates which type of enemy to spawn based on the probabilities defined for
    the current game minute. It then spawns an enemy of the selected type at the current angle
    and increments the angle for the next spawn.

    Global Variables:
        - current_angle: The current angle (in degrees) at which the next enemy will be spawned.
        - gameMin: The current minute in the game used to determine enemy spawn probabilities.
        - max_enemies: The maximum number of enemies that can be spawned at any given time.
        - spawned_enemies: A list of currently spawned enemies.

    Probability Handling:
        - enemy_spawn_probabilities: A dictionary mapping (minute, enemy_type) to spawn probabilities.
        - accumulated_probability: The accumulated probability used to select the enemy type.
        - random_threshold: A random threshold used to select the enemy type based on probabilities.

    Enemy Spawning:
        - The function calculates the total probability for the current minute and generates a
          random number within this range.
        - It iterates through the enemy types and their respective probabilities for the current
          minute, accumulating the probability until it exceeds the random threshold.
        - Once the threshold is exceeded, the corresponding enemy type is spawned.
    """
    global current_angle
    if len(spawned_enemies) < max_enemies:
        # Calculate probabilities for the current minute
        minute_probabilities = [(enemy_type, prob) for (min, enemy_type), prob in enemy_spawn_probabilities.items() if min == gameMin]

        # If there are no probabilities defined for this minute, exit the function
        if not minute_probabilities:
            return

        # Calculate the total probability and generate a random threshold
        total_probability = sum(prob for _, prob in minute_probabilities)
        random_threshold = random.uniform(0, total_probability)

        # Iterate through probabilities to select an enemy type
        accumulated_probability = 0
        for enemy_type, probability in minute_probabilities:
            accumulated_probability += probability
            if accumulated_probability >= random_threshold:
                spawn_enemy(player, current_angle, enemy_type)
                break

        # Increment the angle for the next spawn
        current_angle += angle_increment + random.uniform(-10, 10)
        if current_angle >= 360:
            current_angle = 0
            
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
            maxenemy_spawn_control += choice([1,2])
            gameSeconds += 1
            
            if maxenemy_spawn_control >= 10:
                max_enemies += 2
                maxenemy_spawn_control = 0
                
            if gameSeconds == 60:
                gameMin += 1
                gameSeconds = 0

                #randomizo el numero de enemigos que se reduce cada vez que cambien las condiciones de spawn
                if(gameMin == 1):
                    max_enemies -= choice([1,2,3])
                elif(gameMin == 2):
                    max_enemies -= choice([2,4,6])
                elif(gameMin == 3):
                    max_enemies -= choice([4,6,8])
                elif(gameMin == 4):
                    max_enemies -= choice([6,8,10])
                elif(gameMin == 5):
                    flag=False
                    for i in spawned_enemies:
                        if flag==True:
                            i.take_damage(1000)
                        else:
                            flag=True
                    max_enemies =1
                    
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
                this_game.current_state.change_to_game_over()
                this_game.change_paused()
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
                prepare_level_up()

            it.destroy()
            return True
    
    return False

def player_pick_chest(self, arbiter, space):
    for che in Chest.CHESTS:
        if pygame.Rect.colliderect(player.rect, che.rect):
            this_game.chest = che
            prepare_chest()
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
item_button_1 = button.Button(WIDTH / 2 - 240, 170, item_select_img, 1)
item_button_2 = button.Button(WIDTH / 2 - 240, 350, item_select_img, 1)


title_font = pygame.font.Font(None, 48)
items_font = pygame.font.Font(None, 40)


#Este arreglo debe estar cargado con todos los items y armas disponibles
#Cuando se maxee algo, se quita de la lista
#Cuando se llegue a 2 o 3 armas, todas las demás armas se borran de la lista


#Este arreglo toma dos items random para desplegar en la pantalla de Level Up



def prepare_level_up():
    player.level_up()
    this_game.change_paused()
    this_game.current_state.change_to_level_up()

    this_game.selected_item_display = []

    for i in player.Weapons:
        print(f"Arma: {i.name} Tier: {i.tier}")
        if i.tier == i.max_tier:
            print("Arma Maxeada")
            if i.type in this_game.level_item_display:
                this_game.level_item_display.remove(i.type)

    for i in player.Equipment:
        print(f"Equipamiento: {i.name} Tier: {i.tier}")
        if i.tier == i.max_tier:
            print("Equipamiento Maxeado")
            if i.type in this_game.level_item_display:
                this_game.level_item_display.remove(i.type)

    # if len(player.Weapons) == player.MAX_CAPACITTY and not this_game.cleaned_weapons:
    #     print("Se llenó armas")
    #     this_game.clean_weapons()
    #     temp = []
    #     for i in range(0, len(this_game.level_item_display)):
    #         if issubclass(type(this_game.level_item_display[i]), Weapon):
    #             if this_game.level_item_display[i]  in player.Weapons:
    #                 temp.append(this_game.level_item_display[i])
    #         else:
    #             temp.append(this_game.level_item_display[i])
    #     this_game.level_item_display = temp

    # if len(player.Equipment) == player.MAX_CAPACITTY and not this_game.cleaned_equipment:
    #     print("Se llenó el equipamiento")
    #     this_game.clean_equipment()
    #     temp = []
    #     for i in range(0, len(this_game.level_item_display)):
    #         if issubclass(type(this_game.level_item_display[i]), Equipment):
    #             if this_game.level_item_display[i]  in player.Equipment:
    #                 temp.append(this_game.level_item_display[i])
    #         else:
    #             temp.append(this_game.level_item_display[i])
    #     this_game.level_item_display = temp

    print("====================================")
    print("ITEMS PARA DISPLAY")
    for i in range(0, len(this_game.level_item_display)):
        print(this_game.level_item_display[i].name)
    print("====================================")


    if len(this_game.level_item_display) == 0:
        this_game.selected_item_display.append(GoldCoin((player.pos.x + 100, player.pos.y + 100), space, Enemy.COIN_IMAGE))
        this_game.selected_item_display.append(FloorChicken((player.pos.x + 100, player.pos.y + 100), space, Enemy.CHICKEN_IMAGE))
        print("====================================")
        print("Items")
        for i in range(0, len(this_game.selected_item_display)):
            print(this_game.selected_item_display[i])
        print(f"Cantidad: {len(this_game.selected_item_display)}")
        print("====================================")
    
    elif len(this_game.level_item_display) == 1:
        this_game.selected_item_display.append(this_game.level_item_display[0])
    else:
        temp_poll = this_game.level_item_display.copy()
        for i in range(0, 2):
            this_game.selected_item_display.append(random.choice(temp_poll))
            temp_poll.remove(this_game.selected_item_display[i])
        

def prepare_chest():
    this_game.change_paused()
    this_game.current_state.change_to_chest()
    
def get_chest_item():
    items_to_chest = []
    for i in player.Weapons:
        items_to_chest.append(i)
    for i in player.Equipment:
        items_to_chest.append(i)

    selected_items = []

    for i in items_to_chest:
        print(f"Objeto: {i.name} Tier: {i.tier}")
        if i.tier != i.max_tier:
            selected_items.append(i)

    temp = []
    for i in selected_items:
        temp.append(i.type)
    selected_items = temp


    if selected_items == []:
        selected_items = [GoldCoin((player.pos.x + 100, player.pos.y + 100), space, Enemy.COIN_IMAGE), FloorChicken((player.pos.x + 100, player.pos.y + 100), space, Enemy.CHICKEN_IMAGE)]
    

    print("Selected")
    print(selected_items)

    this_game.chest_item = this_game.chest.open_chest(selected_items)
    this_game.chest.destroy()
    this_game.chest_open = True


def add_chest_item():
    player.add_item(this_game.chest_item)
    this_game.chest_open = False


def draw_play_screen():

    pass

def draw_pause_screen():
 
    pygame.draw.rect(surface, (0, 0, 0, 150), [0,0, WIDTH, HEIGHT])
    
    screen.blit(surface, (0,0))
    pause_text = title_font.render(f'GAME PAUSED', True, (255, 255, 255))
    screen.blit(pause_text, (WIDTH / 2 - 100, 100))
    pause_text = title_font.render(f'Max HP: {player.max_hp}', True, (255, 255, 255))
    screen.blit(pause_text, (WIDTH / 2 - 100, 200))
    pause_text = title_font.render(f'Armor: {player.armor}', True, (255, 255, 255))
    screen.blit(pause_text, (WIDTH / 2 - 100, 250))
    pause_text = title_font.render(f'Attack: {player.attack}', True, (255, 255, 255))
    screen.blit(pause_text, (WIDTH / 2 - 100, 300))
    pause_text = title_font.render(f'Move Speed: {player.move_speed}', True, (255, 255, 255))
    screen.blit(pause_text, (WIDTH / 2 - 100, 350))
    


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

    if not this_game.chest_open:
        if open_button.draw(screen):
            get_chest_item()

    if this_game.chest_open:

        if not isinstance(this_game.chest_item, FactoryEquipment.EquipmentCatalog) and not isinstance(this_game.chest_item, FactoryWeapon.WeaponCatalog):
            screen.blit(this_game.chest_item.image, (WIDTH / 2 - this_game.chest_item.image.get_width()/ 2, 250))
        else:
            screen.blit(this_game.chest_item.value.IMAGE, (WIDTH / 2 - this_game.chest_item.value.IMAGE.get_width()/ 2, 250))
        if resume_button.draw(screen):
            add_chest_item()
            this_game.current_state.change_to_play()
            this_game.change_paused()


def draw_level_up_screen():
    
    screen.blit(surface, (0,0))
    screen.blit(level_up_background_img, (WIDTH/2 - 300,20))

    if len(this_game.selected_item_display) > 0:
        if item_button_1.draw(screen):
            player.add_item(this_game.selected_item_display[0])
            this_game.current_state.change_to_play()
            this_game.change_paused()
        if len(this_game.level_item_display) == 0:
            item_text_1 = items_font.render(f'{this_game.selected_item_display[0].name}', True, (255, 255, 255))
            screen.blit(this_game.selected_item_display[0].image, (WIDTH / 2 - 160, 200))
            screen.blit(item_text_1, (WIDTH / 2 - 20, 245))
        else:
            item_text_1 = items_font.render(f'{this_game.selected_item_display[0].name}', True, (255, 255, 255))
            screen.blit(this_game.selected_item_display[0].value.IMAGE, (WIDTH / 2 - 160, 200))
            screen.blit(item_text_1, (WIDTH / 2 - 20, 245))


    if len(this_game.selected_item_display) > 1:
        if item_button_2.draw(screen):
            player.add_item(this_game.selected_item_display[1])
            this_game.current_state.change_to_play()
            this_game.change_paused()
        if len(this_game.level_item_display) == 0:
            item_text_2 = items_font.render(f'{this_game.selected_item_display[1].name}', True, (255, 255, 255))
            screen.blit(this_game.selected_item_display[1].image, (WIDTH / 2 - 160, 400))
            screen.blit(item_text_2, (WIDTH / 2 - 20, 400))
        else:
            item_text_2 = items_font.render(f'{this_game.selected_item_display[1].name}', True, (255, 255, 255))
            screen.blit(this_game.selected_item_display[1].value.IMAGE, (WIDTH / 2 - 160, 400))
            screen.blit(item_text_2, (WIDTH / 2 - 20, 410))



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
                    this_game.change_paused()
                    
                elif not this_game.paused and this_game.current_state.name == "Play":
                    this_game.current_state.change_to_pause()
                    this_game.change_paused()
                


    # screen.blit(background, (0, 0))
    # all_sprites.draw(screen)

    for enemy in spawned_enemies:
        if enemy.is_dead():
           
            spawned_enemies.remove(enemy)
            updateSpawn()

    if not this_game.paused:
        all_sprites.update()

    all_sprites.custom_draw(player)

    select_screen(this_game.current_state.name)

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

    pygame.display.update()
    clock.tick(FPS)
    space.step(1 / FPS)