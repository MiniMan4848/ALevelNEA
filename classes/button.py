import pygame
from main import *

class Button:
    # Constructor
    def __init__(self, text:str, y:int, colour:tuple, hoverCol:tuple, font:str, paddingX:int, paddingY:int, enabled:bool):
        self.text = text
        self.y = y
        self.colour = colour
        self.hoverCol = hoverCol
        self.font = font
        self.paddingX = paddingX # Original padding: 25, 10
        self.paddingY = paddingY
        self.enabled = enabled

    def drawButton(self) -> bool:
        # text, anti alisasing, colour
        buttonText = self.font.render(self.text, True, self.colour)

        # x and y coordinate, width and height for button. Fits text.
        buttonRect = pygame.rect.Rect((0, self.y), (buttonText.get_width() + self.paddingX, buttonText.get_height() + self.paddingY))

        # Calculate x pos to center the button horizontally
        buttonX = (screen.get_width() - buttonRect.width) // 2

        # Set the x position of the buttonRect
        buttonRect.x = buttonX

        # make text center of the rect
        textx = buttonX + (buttonRect.width - buttonText.get_width()) // 2
        texty = self.y + (buttonRect.height - buttonText.get_height()) // 2

        # surface, colour, rectangle to draw, width (0 fills, >0 line thickness), curve edge radius
        # Hollow button style, border same colour as text
        pygame.draw.rect(screen, self.colour, buttonRect, 2, 0)

        # Drawing the button to the screen
        screen.blit(buttonText, (textx, texty))

    def isHovered(self) -> bool:
        # Getting the mouse position in the form of a tuple
        mx, my = pygame.mouse.get_pos()

        # Drawing the button's text and rectangle
        buttonText = self.font.render(self.text, True, self.colour)
        buttonRect = pygame.rect.Rect((0, self.y), (buttonText.get_width() + self.paddingX, buttonText.get_height() + self.paddingY))
        buttonX = (screen.get_width() - buttonRect.width) // 2
        buttonRect.x = buttonX

        # how the text will look when it's been hovered over
        buttonTextHover = self.font.render(self.text, True, self.hoverCol)

        # Setting the text's x and y position
        textx = buttonX + (buttonRect.width - buttonText.get_width()) // 2
        texty = self.y + (buttonRect.height - buttonText.get_height()) // 2

        # checking if the mouse is over the button/rect
        if buttonRect.collidepoint(mx, my) and self.enabled == True:
            # And if it is, changing the colour of the text and rectangle
            pygame.draw.rect(screen, self.hoverCol, buttonRect, 2, 0)
            screen.blit(buttonTextHover, (textx, texty))
            return True
        else:
            return False

    def isClicked(self) -> bool:
        # Getting the mouse position in the form of a tuple
        mx, my = pygame.mouse.get_pos()

        # Checking for left click
        leftClick = pygame.mouse.get_pressed()[0]

        # The button's text and rectangle
        buttonText = self.font.render(self.text, True, self.colour)
        buttonRect = pygame.rect.Rect((0, self.y), (buttonText.get_width() + self.paddingX, buttonText.get_height() + self.paddingY))
        
        # Button's x values
        buttonX = (screen.get_width() - buttonRect.width) // 2
        buttonRect.x = buttonX

        # If the button is clicked, return true
        if leftClick and buttonRect.collidepoint(mx,my) and self.enabled == True:
            return True
        else:
            return False

# Creating almost identical back button class because don't want to center the back button
class BackButton:
    # Constructor
    def __init__(self, text:str, x:int, y:int, colour:tuple, hoverCol:tuple, font:str, paddingX:int, paddingY:int, enabled:bool):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.hoverCol = hoverCol
        self.font = font
        self.paddingX = paddingX # Original padding: 25, 10
        self.paddingY = paddingY
        self.enabled = enabled

    def drawButton(self) -> bool:
        # text, anti alisasing, colour
        buttonText = self.font.render(self.text, True, self.colour)

        # x and y coordinate, width and height for button. Fits text. +n is padding
        buttonRect = pygame.rect.Rect((self.x, self.y), (buttonText.get_width() + self.paddingX, buttonText.get_height() + self.paddingY))

        # make text center of the rect
        textx = self.x + (buttonRect.width - buttonText.get_width()) // 2
        texty = self.y + (buttonRect.height - buttonText.get_height()) // 2

        # surface, colour, rectangle to draw, width (0 fills, >0 line thickness), curve edge radius
        # Hollow button style, border same colour as text
        pygame.draw.rect(screen, self.colour, buttonRect, 2, 0)

        screen.blit(buttonText, (textx, texty))

    def isHovered(self) -> bool:
        mx, my = pygame.mouse.get_pos()

        buttonText = self.font.render(self.text, True, self.colour)
        buttonRect = pygame.rect.Rect((self.x, self.y), (buttonText.get_width() + self.paddingX, buttonText.get_height() + self.paddingY))
        buttonTextHover = self.font.render(self.text, True, self.hoverCol)

        textx = self.x + (buttonRect.width - buttonText.get_width()) // 2
        texty = self.y + (buttonRect.height - buttonText.get_height()) // 2

        # checking if the mouse is over the button/rect
        if buttonRect.collidepoint(mx, my) and self.enabled == True:
            pygame.draw.rect(screen, self.hoverCol, buttonRect, 2, 0)
            screen.blit(buttonTextHover, (textx, texty))
            return True
        else:
            return False

    def isClicked(self) -> str:
        mx, my = pygame.mouse.get_pos()
        # checking for left click
        leftClick = pygame.mouse.get_pressed()[0]

        buttonText = self.font.render(self.text, True, self.colour)
        buttonRect = pygame.rect.Rect((self.x, self.y), (buttonText.get_width() + self.paddingX, buttonText.get_height() + self.paddingY))

        if leftClick and buttonRect.collidepoint(mx,my) and self.enabled == True:
            return True
        else:
            return False