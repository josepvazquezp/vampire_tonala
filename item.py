from __future__ import annotations
import pygame
import math
import pymunk


class Item(pygame.sprite.Sprite):
    ''' Clase de Item
        Son los objetos que sueltan los enemigos
        y al recogerse otorgan aumentos al jugador '''

    ITEMS  = []

    def __init__(self,name, position, space, stat, modifier, image) -> None:
        super().__init__()

        self.stat : int  = stat
        self.modifier: float = modifier
        self.name = name

        self.image = image
        self.image = pygame.transform.rotozoom(self.image, 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.position = pygame.math.Vector2(position)

        self.body = pymunk.Body(1, 100)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.collision_type = 3

        self.space = space
        space.add(self.body, self.shape)
        Item.ITEMS.append(self)


    def pick_up(self):
        ''' Retorna el stat al que se hace la modificación
            y el valor de esta '''
        return self.stat, self.modifier

    def destroy(self):
        ''' Destruye el objeto y lo elimina del arreglo
            y del espacio de fisicas de pymunk '''
        Item.ITEMS.remove(self)
        self.space.remove(self.body, self.shape)
        self.kill()


    def update(self):
        self.body.position = self.position.x, self.position.y


class ExperienceGem(Item):
    def __init__(self, position, space, image) -> None:
        super().__init__( "exp",position, space, 1, 25, image)

class FloorChicken(Item):
    def __init__(self, position, space, image) -> None:
        super().__init__("chicken",position, space, 2, 30, image)

class GoldCoin(Item):
    def __init__(self, position, space, image) -> None:
        super().__init__("coin",position, space, 3, 1, image)

        
items_group = pygame.sprite.Group()