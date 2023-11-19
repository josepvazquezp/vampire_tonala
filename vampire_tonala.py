from __future__ import annotations
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

class Game(object):
    _instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.current_state: state.State = state.PlayState(self)
        self.paused = False
        self.selected_item_display = []
        self.level_item_display = [FactoryWeapon.WeaponCatalog.KNIFE, FactoryWeapon.WeaponCatalog.FIRE_WAND,
                                   FactoryWeapon.WeaponCatalog.MAGIC_WAND, equipment.FactoryEquipment.EquipmentCatalog.ARMOR,
                                   equipment.FactoryEquipment.EquipmentCatalog.HOLLOWHEART, equipment.FactoryEquipment.EquipmentCatalog.SPINACH,
                                   equipment.FactoryEquipment.EquipmentCatalog.WINGS]
        self.cleaned_weapons: bool = False
        self.cleaned_equipment: bool = False
        self.chest = None
        self.chest_open = False
        self.chest_item = None

        self.initialized_global_variables()

        #run main game
        self.mainGame()

    def initialized_global_variables(self) -> None:
        # Initialize pygame
        pygame.init()

        self.space = pymunk.Space()
        self.space.gravity = (0, 0)

        #===============================================
        # Create the screen
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.background = pygame.transform.scale(pygame.image.load(
            'Background/background.jpg').convert(), (WIDTH, HEIGHT))
        
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        #===============================================
        # Create player
        self.player = Player(100, 5, self.space)
        self.player.equip_weapon(FactoryWeapon.WeaponCatalog.KNIFE)

        all_sprites.add(self.player)

        #===============================================
        # Enemy
        self.enemyCooldown = []
        # Spawn variables
        self.max_enemies = 12
        self.angle_increment = 360 / self.max_enemies
        self.current_angle = 0  # To keep track of the last spawn angle
        self.SPAWN_RADIUS = 600  # radius around the player within which enemies will spawn
        self.spawned_enemies = []  # List to keep track of spawned enemies
        self.fact_enemy = FactoryEnemy()
        self.enemy_spawn_probabilities = {
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

        #===============================================
        # Thread for timer and variables timer
        self.gameSeconds = 0
        self.gameMin = 0
        self.playing = True
        self.stop_event = Event()

        self.hilo = threading.Thread(target = self.timer, args=(10,))
        self.hilo.start()
        
        #===============================================
        # Hitboxes handlers pymunk
        self.handler = self.space.add_collision_handler(1, 2)
        self.handler.pre_solve = self.enemy_hit_player

        self.item_hanlder = self.space.add_collision_handler(1, 3)
        self.item_hanlder.begin = self.player_pick_item


        self.chest_handler = self.space.add_collision_handler(1, 4)
        self.chest_handler.begin = self.player_pick_chest

        self.handler2 = self.space.add_collision_handler(3, 2)
        self.handler2.begin = self.projectile_hit_enemigo
        
        #===============================================
        # Images and buttons
        self.resume_img = pygame.image.load(
            "Assets/buttons/button_resume.png").convert_alpha()
        self.resume_button = button.Button(
            WIDTH/2 - self.resume_img.get_width()/2, 400, self.resume_img, 1)

        self.open_img = pygame.image.load("Assets/buttons/button_open.png").convert_alpha()
        self.open_button = button.Button(
            WIDTH/2 - self.resume_img.get_width()/2, 500, self.open_img, 1)

        self.quit_img = pygame.image.load("Assets/buttons/button_quit.png").convert_alpha()
        self.quit_button = button.Button(
            WIDTH/2 - self.resume_img.get_width()/2, 550, self.quit_img, 1)

        self.treasure_background_img = pygame.image.load(
            "Assets/screens/treasure_background.png").convert_alpha()
        self.level_up_background_img = pygame.image.load(
            "Assets/screens/level_up_background.png").convert_alpha()
        self.item_select_img = pygame.image.load(
            "Assets/screens/item_select.png").convert_alpha()
        self.item_button_1 = button.Button(WIDTH / 2 - 240, 170, self.item_select_img, 1)
        self.item_button_2 = button.Button(WIDTH / 2 - 240, 350, self.item_select_img, 1)

        self.title_font = pygame.font.Font(None, 48)
        self.items_font = pygame.font.Font(None, 40)

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

    def spawn_enemy(self, player, angle, enemy_type):
        ppx = player.body.position[0]
        ppy = player.body.position[1]
        x = ppx + self.SPAWN_RADIUS * math.cos(math.radians(angle))
        y = ppy + self.SPAWN_RADIUS * math.sin(math.radians(angle))
        if enemy_type == 1:
            enemy = self.fact_enemy.create_enemy(
                (x, y), player, self.space, FactoryEnemy.EnemyCatalog.PIPEESTRELLO)
        elif enemy_type == 2:
            enemy = self.fact_enemy.create_enemy(
                (x, y), player, self.space, FactoryEnemy.EnemyCatalog.SKULLONE)
        elif enemy_type == 3:
            enemy = self.fact_enemy.create_enemy(
                (x, y), player, self.space, FactoryEnemy.EnemyCatalog.MANTICHANA)
        elif enemy_type == 4:
            enemy = self.fact_enemy.create_enemy(
                (x, y), player, self.space, FactoryEnemy.EnemyCatalog.REAPER)
            
        self.spawned_enemies.append(enemy)


    def updateSpawn(self):
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
        
        if len(self.spawned_enemies) < self.max_enemies:
            # Calculate probabilities for the current minute
            minute_probabilities = [(enemy_type, prob) for (
                min, enemy_type), prob in self.enemy_spawn_probabilities.items() if min == self.gameMin]

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
                    self.spawn_enemy(self.player, self.current_angle, enemy_type)
                    break

            # Increment the angle for the next spawn
            self.current_angle += self.angle_increment + random.uniform(-10, 10)
            if self.current_angle >= 360:
                self.current_angle = 0

    def timer(self, segundos):
        """
        A timer function that controls various game mechanics based on time elapsed.

        This function is intended to be run in a separate thread and updates game seconds, 
        manages enemy spawn rates, and handles other time-based game events.

        Args:
            segundos (int): The initial time in seconds to start the timer from.

        Globals:
            gameSeconds (int): The game's current seconds counter.
            gameMin (int): The game's current minute counter.
            playing (bool): Flag indicating if the game is currently being played.
            current_enemy_types (list): A list of current enemy types in the game.
            max_enemies (int): The maximum number of enemies that can be spawned.
        """
        milis = 0
        maxenemy_spawn_control = 0
        while self.playing:
            if self.stop_event.is_set():
                self.playing = False
            if not self.paused:
                milis += 1
            if (milis == 10):
                milis = 0

                # incremento el numero de enemigos de manera speudoaleatoria
                maxenemy_spawn_control += choice([1, 2])
                self.gameSeconds += 1

                if maxenemy_spawn_control >= 10:
                    self.max_enemies += 2
                    maxenemy_spawn_control = 0

                if self.gameSeconds == 60:
                    self.gameMin += 1
                    self.gameSeconds = 0

                    # randomizo el numero de enemigos que se reduce cada vez que cambien las condiciones de spawn
                    if (self.gameMin == 1):
                        self.max_enemies -= choice([1, 2, 3])
                    elif (self.gameMin == 2):
                        self.max_enemies -= choice([2, 4, 6])
                    elif (self.gameMin == 3):
                        self.max_enemies -= choice([4, 6, 8])
                    elif (self.gameMin == 4):
                        self.max_enemies -= choice([6, 8, 10])
                    elif (self.gameMin == 5):
                        flag = False
                        for i in self.spawned_enemies:
                            if flag == True:
                                i.take_damage(1000)
                            else:
                                flag = True
                        self.max_enemies = 1

                for ene in self.enemyCooldown:
                    ene.attackCooldown -= 1

                    if (ene.attackCooldown == 0):
                        self.enemyCooldown.remove(ene)

            self.player.using_weapon()

            time.sleep(0.1)
    
    
    # Manejadores de Colisiones
    # =========================================================================================================

    def enemy_hit_player(self, arbiter, space, garbage):
        """
        Handles collision between enemy and player.

        This function is triggered when there is a collision between the player and an enemy. 
        It checks for specific conditions and applies damage to the player if necessary.

        Args:
            arbiter: The arbiter for the collision.
            space (pymunk.Space): The space where the collision is taking place.

        Returns:
            bool: True if the collision is handled, False otherwise.
        """
        for ene in Enemy.ENEMIES:
            if pygame.Rect.colliderect(self.player.rect, ene.rect) and ene.attackCooldown == 0:
                self.player.take_damage(ene.power)

                if self.player.is_dead():
                    self.current_state.change_to_game_over()
                    self.change_paused()

                ene.restoreCooldown()
                self.enemyCooldown.append(ene)
                return True

        return False


    def player_pick_item(self, arbiter, space, garbage):
        """
        Handles the player picking up an item.

        This function is called when there is a collision between the player and an item. 
        It applies the item's effects to the player and removes the item from the game.

        Args:
            arbiter: The arbiter for the collision.
            space (pymunk.Space): The space where the collision is taking place.

        Returns:
            bool: True if the item is picked up, False otherwise.
        """
        for it in Item.ITEMS:
            if pygame.Rect.colliderect(self.player.rect, it.rect):
                stat, mod = it.pick_up()
                self.player.apply_stat(stat, mod)

                if self.player.able_to_level_up():
                    self.prepare_level_up()

                it.destroy()
                return True

        return False


    def player_pick_chest(self, arbiter, space, garbage):
        """
        Handles the player interacting with a chest.

        This function is triggered when the player collides with a chest. It changes the game state to allow the player
        to interact with the chest.

        Args:
            arbiter: The arbiter for the collision.
            space (pymunk.Space): The space where the collision is taking place.

        Returns:
            bool: True if the chest is interacted with, False otherwise.
        """
        for che in Chest.CHESTS:
            if pygame.Rect.colliderect(self.player.rect, che.rect):
                self.chest = che
                self.prepare_chest()
                return True
        return False


    def projectile_hit_enemigo(self, arbiter, space, garbage):
        """
        Handles collision between a projectile and an enemy.

        This function is called when a projectile collides with an enemy. 
        It applies damage to the enemy and handles the destruction of the projectile.

        Args:
            arbiter: The arbiter for the collision.
            space (pymunk.Space): The space where the collision is taking place.

        Returns:
            bool: True if the collision is handled, False otherwise.
        """
        for proj in Projectile.PROJECTILES:
            for ene in Enemy.ENEMIES:
                if pygame.Rect.colliderect(proj.rect, ene.rect):
                    temp = proj.damage
                    proj.destroy_projectile()
                    ene.take_damage(temp)
                    return True

        return False
    
    # =========================================================================================================


    # Pantallas
    # =========================================================================================================
    def prepare_level_up(self):
        """
        Prepares the game for the level-up phase.

        This function is triggered when the player is eligible for a level-up. It pauses the game, changes the game state to level-up, 
        and prepares the display items for the level-up screen based on the player's current inventory and equipment status.
        """
        self.player.level_up()
        self.change_paused()
        self.current_state.change_to_level_up()

        self.selected_item_display = []
        
        for i in self.player.Weapons:
            if i.tier == i.max_tier:
                if i.type in self.level_item_display:
                    self.level_item_display.remove(i.type)

        for i in self.player.Equipment:
            if i.tier == i.max_tier:
                if i.type in self.level_item_display:
                    self.level_item_display.remove(i.type)

        if len(self.level_item_display) == 0:
            self.selected_item_display.append(
                GoldCoin((self.player.pos.x + 100, self.player.pos.y + 100), self.space, Enemy.COIN_IMAGE))
            self.selected_item_display.append(FloorChicken(
                (self.player.pos.x + 100, self.player.pos.y + 100), self.space, Enemy.CHICKEN_IMAGE))
        elif len(self.level_item_display) == 1:
            self.selected_item_display.append(self.level_item_display[0])
        else:
            temp_poll = self.level_item_display.copy()
            for i in range(0, 2):
                self.selected_item_display.append(random.choice(temp_poll))
                temp_poll.remove(self.selected_item_display[i])


    def prepare_chest(self):
        """
        Prepares the game for the chest interaction phase.

        This function is called when the player interacts with a chest. It pauses the game and changes the game state to allow 
        chest interaction.
        """
        self.change_paused()
        self.current_state.change_to_chest()


    def get_chest_item(self):
        """
        Determines and handles the item obtained from the chest.

        This function selects an item from the chest based on certain game conditions and player's current inventory. 
        It then updates the game state to reflect the item obtained.
        """
        items_to_chest = []
        for i in self.player.Weapons:
            items_to_chest.append(i)
        for i in self.player.Equipment:
            items_to_chest.append(i)

        selected_items = []

        for i in items_to_chest:
            if i.tier != i.max_tier:
                selected_items.append(i)

        temp = []
        for i in selected_items:
            temp.append(i.type)
        selected_items = temp

        if selected_items == []:
            selected_items = [GoldCoin((self.player.pos.x + 100, self.player.pos.y + 100), self.space, Enemy.COIN_IMAGE),
                            FloorChicken((self.player.pos.x + 100, self.player.pos.y + 100), self.space, Enemy.CHICKEN_IMAGE)]

        self.chest_item = self.chest.open_chest(selected_items)
        self.chest.destroy()
        self.chest_open = True


    def add_chest_item(self):
        """
        Adds the obtained chest item to the player's inventory.

        This function is triggered after the player interacts with the chest and an item is selected. It adds the selected item 
        to the player's inventory and updates the game state.
        """
        self.player.add_item(self.chest_item)
        self.chest_open = False

    def draw_pause_screen(self):
        """
        Draws the pause screen of the game.

        This function is called when the game is paused. It displays the pause menu, including game statistics and options to resume or quit the game.
        """

        pygame.draw.rect(self.surface, (0, 0, 0, 150), [0, 0, WIDTH, HEIGHT])

        screen.blit(self.surface, (0, 0))
        pause_text = self.title_font.render(f'GAME PAUSED', True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH / 2 - 100, 100))
        pause_text = self.title_font.render(
            f'Max HP: {self.player.max_hp}', True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH / 2 - 100, 200))
        pause_text = self.title_font.render(
            f'Armor: {self.player.armor}', True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH / 2 - 100, 250))
        pause_text = self.title_font.render(
            f'Attack: {self.player.attack}', True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH / 2 - 100, 300))
        pause_text = self.title_font.render(
            f'Move Speed: {self.player.move_speed}', True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH / 2 - 100, 350))

        if self.resume_button.draw(screen):
            self.current_state.change_to_play()
            self.change_paused()

        if self.quit_button.draw(screen):
            self.stop_event.set()
            pygame.quit()
            exit()


    def draw_chest_screen(self):
        """
        Draws the chest interaction screen.

        This function is responsible for rendering the screen when the player interacts with a chest. It shows the chest and the item obtained (if any).
        """

        screen.blit(self.surface, (0, 0))
        screen.blit(self.treasure_background_img, (WIDTH/2 - 175, 20))

        if not self.chest_open:
            if self.open_button.draw(screen):
                self.get_chest_item()

        if self.chest_open:

            if not isinstance(self.chest_item, FactoryEquipment.EquipmentCatalog) and not isinstance(self.chest_item, FactoryWeapon.WeaponCatalog):
                screen.blit(self.chest_item.image, (WIDTH / 2 -
                            self.chest_item.image.get_width() / 2, 250))
            else:
                screen.blit(self.chest_item.value.IMAGE, (WIDTH / 2 -
                            self.chest_item.value.IMAGE.get_width() / 2, 250))
            if self.resume_button.draw(screen):
                self.add_chest_item()
                self.current_state.change_to_play()
                self.change_paused()


    def draw_level_up_screen(self):
        """
        Draws the level-up screen.

        This function renders the level-up screen, showing available items or upgrades for the player to choose from when leveling up.
        """

        screen.blit(self.surface, (0, 0))
        screen.blit(self.level_up_background_img, (WIDTH/2 - 300, 20))

        if len(self.selected_item_display) > 0:
            if self.item_button_1 .draw(screen):
                self.player.add_item(self.selected_item_display[0])
                self.current_state.change_to_play()
                self.change_paused()
            if len(self.level_item_display) == 0:
                item_text_1 = self.items_font.render(
                    f'{self.selected_item_display[0].name}', True, (255, 255, 255))
                screen.blit(
                    self.selected_item_display[0].image, (WIDTH / 2 - 160, 200))
                screen.blit(item_text_1, (WIDTH / 2 - 20, 245))
            else:
                item_text_1 = self.items_font.render(
                    f'{self.selected_item_display[0].name}', True, (255, 255, 255))
                screen.blit(
                    self.selected_item_display[0].value.IMAGE, (WIDTH / 2 - 160, 200))
                screen.blit(item_text_1, (WIDTH / 2 - 20, 245))

        if len(self.selected_item_display) > 1:
            if self.item_button_2.draw(screen):
                self.player.add_item(self.selected_item_display[1])
                self.current_state.change_to_play()
                self.change_paused()
            if len(self.level_item_display) == 0:
                item_text_2 = self.items_font.render(
                    f'{self.selected_item_display[1].name}', True, (255, 255, 255))
                screen.blit(
                    self.selected_item_display[1].image, (WIDTH / 2 - 160, 400))
                screen.blit(item_text_2, (WIDTH / 2 - 20, 400))
            else:
                item_text_2 = self.items_font.render(
                    f'{self.selected_item_display[1].name}', True, (255, 255, 255))
                screen.blit(
                    self.selected_item_display[1].value.IMAGE, (WIDTH / 2 - 160, 400))
                screen.blit(item_text_2, (WIDTH / 2 - 20, 410))


    def draw_game_over_screen(self):
        """
        Draws the game over screen.

        This function is called when the player loses all health points. It displays the game over message and options to quit the game.
        """
        pygame.draw.rect(self.surface, (255, 0, 0, 150), [0, 0, WIDTH, HEIGHT])
        screen.blit(self.surface, (0, 0))

        game_over_text = self.title_font.render(f'GAME OVER', True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH / 2 - 100, 100))

        if self.quit_button.draw(screen):
            self.stop_event.set()
            pygame.quit()
            exit()


    def select_screen(self, screen_name):
        """
        Selects and draws the appropriate game screen based on the given screen name.

        This function is responsible for managing the transitions between different game screens like pause, level-up, 
        chest interaction, and game over screens.

        Args:
            screen_name (str): The name of the screen to be drawn.
        """
        if screen_name == "Pause":
            self.draw_pause_screen()
        elif screen_name == "Level":
            self.draw_level_up_screen()
        elif screen_name == "Chest":
            self.draw_chest_screen()
        elif screen_name == "Over":
            self.draw_game_over_screen()
    # =========================================================================================================
    
    # Music
    def music(self):
        """ Método para mandar llamar a la música """
        pygame.mixer.music.load('./Assets/music/bloody_tears.mp3')
        pygame.mixer.music.play(-1)


    # Main Game
    def mainGame(self):
        self.music()

        while True:
            self.updateSpawn()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_event.set()
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.paused and self.current_state.name == "Pause":
                            self.current_state.change_to_play()
                            self.change_paused()

                        elif not self.paused and self.current_state.name == "Play":
                            self.current_state.change_to_pause()
                            self.change_paused()

            for enemy in self.spawned_enemies:
                if enemy.is_dead():
                    self.spawned_enemies.remove(enemy)
                    self.updateSpawn()

            if not self.paused:
                all_sprites.update()

            all_sprites.custom_draw(self.player)

            self.select_screen(self.current_state.name)

            # Toda esta madre sirve para hacer un display bien sencillo del HP del cabron
            font = pygame.font.Font(None, 36)
            hp_text = font.render(f'HP: {self.player.hp}', True, (255, 255, 255))
            screen.blit(hp_text, (10, 10))

            font = pygame.font.Font(None, 36)
            hp_text = font.render(f'Lvl: {self.player.level}', True, (255, 255, 255))
            screen.blit(hp_text, (10, 40))

            font = pygame.font.Font(None, 36)
            hp_text = font.render(f'XP: {self.player.curren_xp}', True, (255, 255, 255))
            screen.blit(hp_text, (10, 70))

            font = pygame.font.Font(None, 36)
            hp_text = font.render(
                f'Next: {self.player.next_level_xp}', True, (255, 255, 255))
            screen.blit(hp_text, (10, 100))

            font = pygame.font.Font(None, 80)
            hp_text = font.render(
                f'Time: {self.gameMin}:{self.gameSeconds}', True, (255, 255, 255))
            screen.blit(hp_text, (WIDTH / 2 - 100, 10))

            font = pygame.font.Font(None, 36)
            hp_text = font.render(f'Feria: {self.player.gold}', True, (255, 255, 255))
            screen.blit(hp_text, (1000, 10))

            # max enemies display
            font = pygame.font.Font(None, 36)
            hp_text = font.render(f'Max Enemies: {self.max_enemies}', True, (255, 255, 255))
            screen.blit(hp_text, (1000, 40))

            pygame.display.update()
            self.clock.tick(FPS)
            self.space.step(1 / FPS)

Game()