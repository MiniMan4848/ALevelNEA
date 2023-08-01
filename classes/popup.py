import pygame
from main import *

class Popup():
    # Constructor
    def __init__(self):
        pass

    def drawPopup(self):
        popupwidth, popupheight = 455, 410
        popupx = ((width - popupwidth)//2) + 5
        popupy = (height - popupheight)//22

        # Drawing the shadow
        shadowOffset = 10
        pygame.draw.rect(screen, (0, 0, 0), (popupx + shadowOffset, popupy + shadowOffset, popupwidth, popupheight), 0, 10)

        # Main popup
        pygame.draw.rect(screen, (BGCOL), (popupx, popupy , popupwidth, popupheight), 0, 10)
        # The stroke around the popup
        pygame.draw.rect(screen, ("black"), (popupx, popupy , popupwidth, popupheight), 1, 10)

    def backButton(self):
        # Importing the button class to be used as a back button
        from classes.button import BackButton

        popupwidth, popupheight = 455, 410
        popupx = ((width - popupwidth)//2) + 5
        popupy = (height - popupheight)//22
        
        # +n is padding
        back = BackButton("BACK", popupx + 10, popupy + 10, (207, 17, 4), (235, 64, 52), fonts["Tiny"], 10, 5, True)
        back.drawButton()
        back.isHovered()
        # Go back to the main menu if the back button is pressed
        if back.isClicked():
            mainMenu()
