from __future__ import annotations
from enum import Enum
import pygame
import math
import pymunk
from abc import ABC, abstractmethod


class Equipment():
    """
    Represents a piece of equipment with various attributes and functionalities.

    Attributes:
        tier (int): The current tier of the equipment.
        max_tier (int): The maximum tier the equipment can reach.
        associated_stat (int): The stat associated with the equipment.
        modifier (float): The modifier value that affects the equipment's performance.
        name (str): The name of the equipment.
        type (Enum): The type of the equipment.

    Args:
        max_tier (int): The maximum tier of the equipment.
        associated_stat (int): The stat associated with the equipment.
        modifier (float): The modifier for the equipment's effect.
        name (str): The name of the equipment.
        type (Enum): The type of the equipment.
    """

    def __init__(self, max_tier: int, associated_stat: int, modifier: float, name: str, type) -> None:
        self.tier: int = 1
        self.max_tier: int = max_tier
        self.associated_stat: int = associated_stat
        self.modifier: float = modifier
        self.name = name
        self.type = type
        # self.image = pygame.transform.scale(image, (image.get_width() * 0.5, image.get_height() * 0.5))

    def upgrade_equipment(self) -> bool:
        """
        Upgrades the equipment to the next tier if it hasn't reached its maximum tier.

        Returns:
            bool: True if the equipment was upgraded, False otherwise.
        """
        if (self.tier != self.max_tier):
            self.tier += 1
            return True
        return False

    def get_effect(self):
        """
        Gets the effect of the equipment based on its associated stat and modifier.

        Returns:
            tuple: A tuple containing the associated stat and the modifier.
        """
        return self.associated_stat, self.modifier


class SpecificEquipment(ABC):
    """
    Abstract base class for creating specific equipment.

    This class provides an interface for creating specific types of equipment.
    """

    def create(self):
        """
        Abstract method to create a specific equipment.

        This method should be implemented by subclasses to create and return an instance of Equipment.
        """
        pass


class Armor(SpecificEquipment):
    """
    Concrete class representing Armor equipment.

    Inherits from SpecificEquipment.
    """
    IMAGE = pygame.transform.rotozoom(pygame.image.load(
        'Assets/Equipment/Sprite-Armor.jpg'), 0, .5)
    NAME = "armor"
    STAT = 4
    MOFIFIER = 1

    def create(self) -> None:
        """
        Creates an instance of Armor equipment.

        Returns:
            Equipment: An instance of Armor equipment with predefined attributes.
        """
        return Equipment(5, 4, 1, "armor", FactoryEquipment.EquipmentCatalog.ARMOR)


class HollowHeart(SpecificEquipment):
    """
    Concrete class representing Armor equipment.

    Inherits from SpecificEquipment.
    """
    IMAGE = pygame.transform.rotozoom(pygame.image.load(
        'Assets/Equipment/Sprite-Hollow_Heart.jpg'), 0, .5)
    NAME = "hollow_heart"
    STAT = 5
    MOFIFIER = 0.1

    def create(self) -> Equipment:
        """
        Creates an instance of Armor equipment.

        Returns:
            Equipment: An instance of Armor equipment with predefined attributes.
        """
        return Equipment(5, 5, 0.1, "hollow_heart", FactoryEquipment.EquipmentCatalog.HOLLOWHEART)


class Spinach(SpecificEquipment):
    """
    Concrete class representing Armor equipment.

    Inherits from SpecificEquipment.
    """
    IMAGE = pygame.transform.rotozoom(pygame.image.load(
        'Assets/Equipment/Sprite-Spinach.jpg'), 0, .5)
    NAME = "spinach"
    STAT = 6
    MOFIFIER = 0.1

    def create(self) -> Equipment:
        """
        Creates an instance of Armor equipment.

        Returns:
            Equipment: An instance of Armor equipment with predefined attributes.
        """
        return Equipment(5, 6, 0.1, "spinach", FactoryEquipment.EquipmentCatalog.SPINACH)


class Wings(SpecificEquipment):
    IMAGE = pygame.transform.rotozoom(pygame.image.load(
        'Assets/Equipment/Sprite-Wings.jpg'), 0, .5)
    NAME = "wings"
    STAT = 7
    MOFIFIER = 0.1

    def create(self) -> Equipment:
        return Equipment(5, 7, 0.1, "wings", FactoryEquipment.EquipmentCatalog.WINGS)


class FactoryEquipment():
    """
    Factory class to create specific equipment.

    This class uses the Factory pattern to create instances of specific equipment based on a given type.
    """
    class EquipmentCatalog(Enum):
        """
        Enum for cataloging different types of equipment.

        Each enum value corresponds to a specific type of equipment.
        """
        ARMOR = Armor()
        HOLLOWHEART = HollowHeart()
        SPINACH = Spinach()
        WINGS = Wings()

    def create_equipment(self, type):
        """
        Creates an equipment instance based on the specified type.

        Args:
            type (Enum): The type of equipment to be created.

        Returns:
            Equipment: An instance of the specified equipment type.
        """
        return type.value.create()
