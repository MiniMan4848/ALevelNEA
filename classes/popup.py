import pygame
from main import *

class Popup():
    # Constructor
    def __init__(self):
        pass

    def drawPopup(self):
        # Defining the popup's width, height, x and y value
        popupWidth, popupHeight = 455, 410
        popupX = ((width - popupWidth)//2) + 5
        popupY = (height - popupHeight)//22

        # Drawing the shadow
        shadowOffset = 10
        pygame.draw.rect(screen, (0, 0, 0), (popupX + shadowOffset, popupY + shadowOffset, popupWidth, popupHeight), 0, 10)

        # Main popup
        pygame.draw.rect(screen, (BGCOL), (popupX, popupY , popupWidth, popupHeight), 0, 10)

        # The stroke around the popup
        pygame.draw.rect(screen, ("black"), (popupX, popupY , popupWidth, popupHeight), 1, 10)

    def backButton(self):
        # Importing the back button class from the button.py 
        from classes.button import BackButton

        # Defining the popup's width, height, x and y value
        popupWidth, popupHeight = 455, 410
        popupX = ((width - popupWidth)//2) + 5
        popupY = (height - popupHeight)//22
        
        # drawing the back button, +n is padding
        back = BackButton("BACK", popupX + 10, popupY + 10, (207, 17, 4), (235, 64, 52), fonts["Tiny"], 10, 5, True)
        back.drawButton()
        back.isHovered()

        # Go back to the main menu if the back button is pressed
        if back.isClicked():
            mainMenu()