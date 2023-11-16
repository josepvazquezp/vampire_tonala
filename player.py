from __future__ import annotations
import pygame
import math
from Camera import *
from equipment import Equipment
from settings import *
from projectile import *
import pymunk
from weapon import * 

def convert_coordinates(point):
        return int(point[0]), (int(point[1]))

class Player(pygame.sprite.Sprite):
    Weapons = []
    Equipment = []
    MAX_CAPACITTY = 2

    def __init__(self, hp, speed, space):
        super().__init__()
        self.pos = pygame.math.Vector2(WIDTH/2, HEIGHT/2)
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/Characters/Antonio/Sprite-Antonio.jpg').convert_alpha(),0,.5)
        self.speed = speed
        
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.current_direction = 0

        self.hp = hp
        self.max_hp = self.hp
        self.armor = 0
        self.move_speed = 1
        self.attack = 1
        
        self.level: int = 0
        self.curren_xp: int = 0
        self.next_level_xp = 100
        self.gold = 0
        

        self.body = pymunk.Body(1, 100)
        self.body.position = convert_coordinates(self.pos)
        self.shape = pymunk.Circle(self.body, 25)
        self.shape.collision_type = 1

        self.space = space
        space.add(self.body, self.shape)

        Player.Weapons.append(Knife())

    def take_damage(self, damage: int):
        ''' '''
        self.hp -= damage

    def is_dead(self):
        if self.hp > 0:
            return False
        return True


    def player_rotate(self):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_a]):
            self.image = pygame.transform.flip(self.base_player_image,True,False)
        elif(keys[pygame.K_d]):
            self.image = self.base_player_image
        
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
    
    def get_player_hitbox_rect(self):
        return self.hitbox_rect
    
    def user_input(self):

        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
            self.current_direction = 180
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
            self.current_direction = 0
        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
            self.current_direction = 270
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
            self.current_direction = 90

        if self.velocity_x != 0 and self.velocity_y != 0: # Diagonal movement
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

    def using_weapon(self):
        for weapon in Player.Weapons:
            if weapon.actual_cooldown == 0:
                weapon.actual_cooldown = weapon.cooldown
                spawn_projectile = self.pos

                projectile = weapon.create_projectile(spawn_projectile[0], spawn_projectile[1], self.current_direction, self.space)
                projectile_group.add(projectile)
                all_sprites.add(projectile)

    def add_item(self, item):
        if issubclass(type(item), Equipment):
            print("Es equipamiento")
            if item in Player.Equipment:
                index = Player.Equipment.index(item)
                if Player.Equipment[index].upgrade_equipment():
                    stat, modifier = item.get_effect()
                    self.apply_stat(stat, modifier)
            else:
                Player.Equipment.append(item)
                stat, modifier = item.get_effect()
                self.apply_stat(stat, modifier)

        elif issubclass(type(item), Weapon):
            print("Es arma")
        else:
            stat, modifier = item.get_effect()
            self.apply_stat(stat, modifier)

        

    
    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x,self.velocity_y)

        self.hitbox_rect.center = self.pos
        self.body.position = convert_coordinates(self.pos)

    def apply_stat(self, stat: int, modif: float):
        ''' Recibe un stat a modificar y la cantidad que se le va a aplicar '''
        if(stat == 1):
            self.gain_xp(modif)
        elif(stat == 2):
            self.heal(modif)
        elif(stat == 3):
            self.earn_gold(modif)
        elif(stat == 4): #Armor
            self.armor += modif
        elif(stat == 5): #Max Healt
            self.max_hp += self.max_hp * modif
        elif(stat == 6): #Attack
            self.attack += modif
        elif(stat == 7): #Wings
            self.move_speed += modif
        


    def gain_xp(self, xp: int):
        ''' Recibe una cantidad de experiencia como entero y la aplica al jugador.
            Si la experiencia actual (current_xp) iguala o supera a la experiencia
            para el siguiente nivel (nex_level_xp) sube de nivel'''
        self.curren_xp += xp
        


    def able_to_level_up(self):
        '''  '''
        if(self.curren_xp >= self.next_level_xp):
            return True
        return False
        

    def level_up(self):
        ''' Sube de nivel al jugador y establece la nueva meta para el siguiente nivel '''
        self.level += 1
        self.next_level_xp += 150 
        print("LEVEL UP")


    def heal(self, heal: int):
        '''  '''
        if self.hp + heal > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp += heal

    def earn_gold(self, gold: int):
        ''''''
        self.gold += gold



    def update(self):
        self.user_input()
        self.move()
        self.player_rotate()


        for weapon in Player.Weapons:
            if weapon.actual_cooldown > 0:
                weapon.actual_cooldown -= 1

