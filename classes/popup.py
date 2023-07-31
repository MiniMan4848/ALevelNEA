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
        pygame.draw.rect(screen, (0, 0, 0), (popupx + shadowOffset, popupy + shadowOffset, popupwidth, popupheight), 0)

        # Main popup
        pygame.draw.rect(screen, (BGCOL), (popupx, popupy , popupwidth, popupheight), 0)
        # The stroke around the popup
        pygame.draw.rect(screen, ("black"), (popupx, popupy , popupwidth, popupheight), 1)

    def backButton(self):
        # Importing the button class to be used as a back button
        from classes.button import Button

        back = Button("BACK", 510, 35, (207, 17, 4), (235, 64, 52), fonts["Tiny"], 10, 5, True)
        back.drawButton()
        back.isHovered()
        # Go back to the main menu if the back button is pressed
        if back.isClicked():
            mainMenu()
