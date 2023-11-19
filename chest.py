from __future__ import annotations
import random
import pygame
import math
import pymunk


class Chest(pygame.sprite.Sprite):
    """
    A Chest class representing a treasure chest in a game.

    Attributes:
        CHESTS (list): A class variable that stores all instances of Chest.
        image (pygame.Surface): The image representing the chest.
        rect (pygame.Rect): The rectangle representing the chest's position and size.
        position (pygame.math.Vector2): The position of the chest.
        body (pymunk.Body): The physical body for the chest in the physics space.
        shape (pymunk.Circle): The shape of the chest for collision handling.
        space (pymunk.Space): The space to which the chest's body and shape are added.

    Args:
        position (tuple): The (x, y) position of the chest.
        space (pymunk.Space): The pymunk space where the chest will exist.
        image (pygame.Surface): The image for the chest sprite.
    """

    CHESTS = []

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
        """
        Simulates the action of opening a chest and obtaining a random item.

        Args:
            items (list): A list of items that can be obtained from the chest.

        Returns:
            Any: A randomly selected item from the provided list of items.
        """
        ''' Esta madre deberia de soltar del loot '''
        selected_item = random.choice(items)
        print(selected_item)
        return selected_item

    def destroy(self):
        """
        Removes the chest from the game.

        This method removes the chest from the list of chests, removes its body and shape from the pymunk space, and kills the sprite.
        """
        Chest.CHESTS.remove(self)
        self.space.remove(self.body, self.shape)
        self.kill()

    def update(self):
        """
        Updates the chest's position.

        This method synchronizes the chest's physical body position with its graphical position.
        """
        self.body.position = self.position.x, self.position.y


chest_group = pygame.sprite.Group()
