import pygame
from main import *

class Button:
    # Constructor
    def __init__(self, text:str, x:int, y:int, colour:tuple, hovercol:tuple, enabled:bool):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.hovercol = hovercol
        self.enabled = enabled

    def drawButton(self) -> bool:
        # text, anti alisasing, colour
        buttonText = GothamBlackSmaller.render(self.text, True, self.colour)

        # x and y coordinate, width and height for button. Fits text. +n is padding
        buttonRect = pygame.rect.Rect((self.x, self.y), (buttonText.get_width() + 25, buttonText.get_height() + 10))

        # make text center of the rect
        textx = self.x + (buttonRect.width - buttonText.get_width()) // 2
        texty = self.y + (buttonRect.height - buttonText.get_height()) // 2

        # surface, colour, rectangle to draw, width (0 fills, >0 line thickness), curve edge radius
        # Hollow button style, border same colour as text
        pygame.draw.rect(screen, self.colour, buttonRect, 2, 0)

        screen.blit(buttonText, (textx, texty))

    def isHovered(self) -> bool:
        mx, my = pygame.mouse.get_pos()

        buttonText = GothamBlackSmaller.render(self.text, True, self.colour)
        buttonRect = pygame.rect.Rect((self.x, self.y), (buttonText.get_width() + 25, buttonText.get_height() + 10))
        buttonTextHover = GothamBlackSmaller.render(self.text, True, self.hovercol)

        textx = self.x + (buttonRect.width - buttonText.get_width()) // 2
        texty = self.y + (buttonRect.height - buttonText.get_height()) // 2

        # checking if the mouse is over the button/rect
        if buttonRect.collidepoint(mx, my) and self.enabled == True:
            pygame.draw.rect(screen, self.hovercol, buttonRect, 2, 0)
            screen.blit(buttonTextHover, (textx, texty))
            return True
        else:
            return False

    def isClicked(self) -> bool:
        mx, my = pygame.mouse.get_pos()
        # checking for left click
        leftClick = pygame.mouse.get_pressed()[0]

        buttonText = GothamBlackSmaller.render(self.text, True, self.colour)
        buttonRect = pygame.rect.Rect((self.x, self.y), (buttonText.get_width() + 25, buttonText.get_height() + 10))

        if leftClick and buttonRect.collidepoint(mx,my) and self.enabled == True:
            return True
        else:
            return False