# Importing modules
import pygame
import sys

# Importing classes
#from Classes.button import Button

# Initialise pygame
pygame.init()

# Creating the game window
screen = pygame.display.set_mode()
width, height = screen.get_size()
screen = pygame.display.set_mode((width, height/2))

# Setting the caption on startup
pygame.display.set_caption("Blob Dodge - Main Menu")

# Fonts
GothamBlackHeader = pygame.font.Font("Assets/Gotham Black.ttf", 100)
GothamBlackSmaller = pygame.font.Font("Assets/Gotham Black.ttf", 50)

class Button:
    # Constructor
    def __init__(self, text:str, x:int, y:int, width:int, height:int, colour:tuple, hovercol:tuple, enabled:bool):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.hovercol = hovercol
        self.enabled = enabled

    def drawButton(self) -> bool:
        # text, anti alisasing, colour
        buttonText = GothamBlackSmaller.render(self.text, True, self.colour)

        # x and y coordinate, width and height for button
        buttonRect = pygame.rect.Rect((self.x,self.y), (self.width,self.height))

        # surface, colour, rectangle to draw, width (0 fills, >0 line thickness), curve edge radius
        # Hollow button style, border same colour as text
        pygame.draw.rect(screen, self.colour, buttonRect, 2, 0)

        # added numbers are the padding?
        screen.blit(buttonText, (self.x+3, self.y))
        return False

    def isClicked(self) -> bool:
        mx, my = pygame.mouse.get_pos()
        # checking for left click
        leftClick = pygame.mouse.get_pressed()[0]
        buttonRect = pygame.rect.Rect((self.x,self.y), (self.width,self.height))
        if leftClick and buttonRect.collidepoint(mx,my) and self.enabled == True:
            return True
        else:
            return False
    
    def isHovered(self) -> bool:
        mx, my = pygame.mouse.get_pos()

        buttonRect = pygame.rect.Rect((self.x,self.y), (self.width,self.height))
        buttonText = GothamBlackSmaller.render(self.text, True, self.colour)
        buttonTextHover = GothamBlackSmaller.render(self.text, True, self.hovercol)

        # checking if the mouse is over the button/rect
        if buttonRect.collidepoint(mx, my) and self.enabled == True:
            pygame.draw.rect(screen, self.hovercol, buttonRect, 1, 0)
            screen.blit(buttonTextHover, (self.x+3, self.y))
            return True
        else:
            pass
            return False

def gameLoop():
    # Loop for the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fills the screen grey 
        screen.fill((40,43,48))

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

def mainMenu():

    # All instances of main menu buttons
    playbutton = Button("PLAY", 620, 155, 141, 55, (242, 225, 36), (255, 192, 20), True)

    # Loop for the main menu
    while True:
        for event in pygame.event.get():
            # If the mouse button is pressed, go to the game loop
            if event.type == pygame.MOUSEBUTTONDOWN and playbutton.isClicked():
                pygame.display.set_caption("Blob Dodge - Game Loop")
                gameLoop()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fills the screen grey 
        screen.fill((40,43,48))
        playbutton.drawButton()
        playbutton.isHovered()

        # Puts the main menu text at the top of the screen
        MMtext = GothamBlackHeader.render("MAIN MENU", True, "white")
        main_menu_text_rect = MMtext.get_rect(center=(width // 2, height // 12))
        screen.blit(MMtext, (main_menu_text_rect))

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

if __name__ == "__main__":
    mainMenu()