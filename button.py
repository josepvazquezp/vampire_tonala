import pygame

# button class


class Button():
    def __init__(self, x, y, image, scale):
        """
Initialize a new Button object.

Args:
x (int): The x-coordinate of the top left corner of the button.
y (int): The y-coordinate of the top left corner of the button.
image (pygame.Surface): The image to be used for the button.
scale (float): The factor by which to scale the button's image.

Attributes:
image (pygame.Surface): The scaled image of the button.
rect (pygame.Rect): The rectangle representing the button's position and size.
clicked (bool): A flag indicating whether the button has been clicked.
"""
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        """
Draw the button on a given surface and handle button click events.

Args:
surface (pygame.Surface): The surface on which the button is to be drawn.

Returns:
bool: True if the button is clicked, otherwise False.

This method checks for mouseover and mouse click events. If the button is clicked, it returns True, otherwise it returns False. It also handles the visual representation of the button on the given surface.
"""

        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
