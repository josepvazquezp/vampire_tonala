from __future__ import annotations
import random
import pygame
import math
import pymunk


class Chest(pygame.sprite.Sprite):
    ''' Clase de Chest/Cofre
        Le otorga al jugador mejoras al
        armamento y equipamiento que
        posee en su inventario '''

    CHESTS  = []

    def __init__(self, position, space, image) -> None:
        super().__init__()
        self.image = image
        self.image = pygame.transform.rotozoom(self.image, 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.position = pygame.math.Vector2(position)


        self.body = pymunk.Body(1, 100)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 13)
        self.shape.collision_type = 4

        self.space = space
        space.add(self.body, self.shape)
        
        Chest.CHESTS.append(self)


    def open_chest(self, items):
        ''' Esta madre deberia de soltar del loot '''
        selected_item = random.choice(items)
        print(selected_item)
        return selected_item


        

    def destroy(self):
        Chest.CHESTS.remove(self)
        self.space.remove(self.body, self.shape)
        self.kill()

    def update(self):
        self.body.position = self.position.x, self.position.y

chest_group = pygame.sprite.Group()