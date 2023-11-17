from __future__ import annotations
import pygame
import math
from Camera import *
from settings import *
from projectile import *
import pymunk
from weapon import * 
from enemy import Enemy

def convert_coordinates(point):
        return int(point[0]), (int(point[1]))

class Player(pygame.sprite.Sprite):
    """
    Clase que representa al jugador en el juego.

    Atributos:
        Weapons (list): Lista de armas que el jugador puede usar.
        FACT_WEAPON (FactoryWeapon): Fábrica para crear instancias de armas.
        pos (Vector2): Posición del jugador en el juego.
        image (Surface): Imagen que representa al jugador.
        speed (int): Velocidad de movimiento del jugador.
        hp (int): Puntos de salud actuales del jugador.
        max_hp (int): Máximo de puntos de salud del jugador.
        level (int): Nivel actual del jugador.
        curren_xp (int): Experiencia actual del jugador.
        next_level_xp (int): Experiencia necesaria para el siguiente nivel.
        gold (int): Cantidad de oro que posee el jugador.
        body (pymunk.Body): Cuerpo físico del jugador en el motor de física.
        shape (pymunk.Circle): Forma física asociada al cuerpo del jugador.
    """
    Weapons = []
    FACT_WEAPON = FactoryWeapon()

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

    def take_damage(self, damage: int):
        """
        Aplica daño al jugador reduciendo sus puntos de salud.

        Args:
            damage (int): Cantidad de daño a aplicar al jugador.
        """
        self.hp -= damage

    def is_dead(self):
        """
        Verifica si el jugador ha muerto.

        Returns:
            bool: True si los puntos de salud del jugador son 0 o menos, False en caso contrario.
        """
        if self.hp > 0:
            return False
        return True


    def player_rotate(self):
        """
        Rota la imagen del jugador basado en la entrada del usuario.
        Cambia la orientación del jugador a izquierda o derecha.
        """
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_a]):
            self.image = pygame.transform.flip(self.base_player_image,True,False)
        elif(keys[pygame.K_d]):
            self.image = self.base_player_image
        
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
    
    def get_player_hitbox_rect(self):
        """
        Retorna el rectángulo de colisión del jugador.

        Returns:
            Rect: Rectángulo de colisión de pygame del jugador.
        """
        return self.hitbox_rect
    
    def user_input(self):
        """
        Maneja la entrada del usuario para mover al jugador.
        Actualiza las velocidades x e y del jugador en función de las teclas presionadas.
        """

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
        """
        Utiliza las armas equipadas por el jugador.
        Crea y añade proyectiles al grupo de sprites en función del arma utilizada.
        """
        for weapon in Player.Weapons:
            if weapon.actual_cooldown == 0:
                weapon.actual_cooldown = weapon.cooldown
                spawn_projectile = self.pos
                
                projectile = weapon.type.value.create_projectile(spawn_projectile[0], spawn_projectile[1], self.current_direction, self.space, self.get_player_hitbox_rect(), weapon.tier)
                projectile_group.add(projectile)
                all_sprites.add(projectile)

    def equip_weapon(self, weapon):
        """
        Equipa una nueva arma o mejora una existente.

        Args:
            weapon (Weapon): Arma a equipar o mejorar.
        """
        flag = False

        for w in Player.Weapons:
            if(weapon == w.type):
                w.upgrade_weapon()
                flag = True
                print(w.tier)
                break

        if(weapon != None and not flag):
            Player.Weapons.append(Player.FACT_WEAPON.create_weapon(weapon))
    
    def move(self):
        """
        Actualiza la posición del jugador en función de su velocidad.
        Ajusta la posición y el cuerpo físico del jugador.
        """
        self.pos += pygame.math.Vector2(self.velocity_x,self.velocity_y)

        self.hitbox_rect.center = self.pos
        self.body.position = convert_coordinates(self.pos)

    def apply_stat(self, stat: int, modif: float):
        """
        Aplica un modificador a una estadística específica del jugador.

        Args:
            stat (int): El identificador de la estadística a modificar.
            modif (float): La cantidad a aplicar a la estadística.
        """
        if(stat == 1):
            self.gain_xp(modif)
        elif(stat == 2):
            self.heal(modif)
        elif(stat == 3):
            self.earn_gold(modif)


    def gain_xp(self, xp: int):
        ''' Recibe una cantidad de experiencia como entero y la aplica al jugador.
            Si la experiencia actual (current_xp) iguala o supera a la experiencia
            para el siguiente nivel (nex_level_xp) sube de nivel'''
        self.curren_xp += xp
        


    def able_to_level_up(self):
        """
        Verifica si el jugador puede subir de nivel.

        Returns:
            bool: True si el jugador tiene suficiente experiencia para subir de nivel, False en caso contrario.
        """
        if(self.curren_xp >= self.next_level_xp):
            return True
        return False
        

    def level_up(self):
        ''' Sube de nivel al jugador y establece la nueva meta para el siguiente nivel '''
        self.level += 1
        self.next_level_xp = int(self.next_level_xp * 1.5)
        print("LEVEL UP")


    def heal(self, heal: int):
        """
        Aumenta los puntos de salud del jugador.

        Args:
            heal (int): Cantidad de puntos de salud a añadir.
        """
        if self.hp + heal > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp += heal

    def earn_gold(self, gold: int):
        """
        Aumenta la cantidad de oro del jugador.

        Args:
            gold (int): Cantidad de oro a añadir.
        """
        self.gold += gold



    def update(self):
        """
        Actualiza el estado y la posición del jugador.
        Gestiona la entrada del usuario, movimiento, rotación y el uso de armas.
        """
        self.user_input()
        self.move()
        self.player_rotate()


        for weapon in Player.Weapons:
            if weapon.actual_cooldown > 0:
                weapon.actual_cooldown -= 1

