# Importing modules
import pygame
import sys
import random
import math

# Initialise pygame
pygame.init()

# Creating the game window, 32:9 aspect ratio
screen = pygame.display.set_mode()
width, height = screen.get_size()
screen = pygame.display.set_mode((width, height/2))

# Constants
BGCOL = (32,33,36)

# Setting the caption on startup
pygame.display.set_caption("Blob Dodge - Main Menu")

# Fonts
fonts = {
    "Header":pygame.font.Font("assets/fonts/Gotham Black.ttf", 100),
    "Smaller":pygame.font.Font("assets/fonts/Gotham Black.ttf", 50),
    "Tiny":pygame.font.Font("assets/fonts/Gotham Black.ttf", 20)
}
            
def gameLoop() -> None:
    # Load and store images for running animation
    run1 = pygame.image.load("assets/run/run1.png").convert_alpha()
    run2 = pygame.image.load("assets/run/run2.png").convert_alpha()
    frames = [run1, run2]

    # Get time in ms
    timer = pygame.time.get_ticks()

    # Interval between frame switches and the frame index
    interval = 100
    frameIndex = 0

    # For the scrolling background
    scroll = 0

    # Blob speed and randomly spawning blob variables
    moveBlobSpeed = 0
    randomHeightIndex = random.randint(0,2)

    # Obstacle speed
    moveObstacleSpeed = 0

    # Loop for the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fills the screen grey and makes the floor
        screen.fill(BGCOL)

        # Background stuff #
        # As there are going to be multiple images, I am storing them in a dict
        imgOne = pygame.image.load("assets/background/stars.png").convert_alpha()

        # Scaling the image and putting it on screen
        scaledImage = pygame.transform.scale(imgOne, (330, 330))

        # See how many images I am going to need
        imageWidth = scaledImage.get_width()
        howMany = (math.ceil((int(width)/int(imageWidth)))) + 1

        # Scroll background speed
        scroll -= 10

        # Reset scroll
        # Checks if image is off screen, scroll is a negative value so use absolute
        if abs(scroll) > imageWidth:
            scroll = 0

        for i in range (0, howMany):
            # x coordinate can't always be 0, needs offsetting by width of image, hence imageWidth
            screen.blit(scaledImage, (i * imageWidth + scroll, 0))
        
        # Blob stuff #
        blob = pygame.image.load("assets/blob/blob.png")

        # Using 331 as that is where the floor starts
        heights = [331 - blob.get_height(), 331 - blob.get_height()*2, 331 - blob.get_height()*3.5]

        # Positioning the blob
        moveBlobSpeed -= 5
        blobX = width + moveBlobSpeed
        blobY = heights[randomHeightIndex]

        # Check if blob's off screen
        if blobX + blob.get_width() < 0:
            # If it is off screen, reset it's position
            moveBlobSpeed = 0
            randomHeightIndex = random.randint(0, 2)
            blobY = heights[randomHeightIndex]

        # Drawing the blob to the screen
        screen.blit(blob, (blobX, blobY))

        # Obstacle stuff #
        obstacle1 = pygame.image.load("assets/obstacles/obstacle1.png")
        scaledObstale1 = pygame.transform.scale(obstacle1, (45, 60))

        moveObstacleSpeed -= 10
        obstacleX = width + moveObstacleSpeed
        obstacleY = 331 - scaledObstale1.get_height()

        if obstacleX + scaledObstale1.get_width() < 0:
            moveObstacleSpeed = 0
            obstacleY = 331 - scaledObstale1.get_height()

        screen.blit(scaledObstale1, (obstacleX, obstacleY))

        # Drawing the floor #
        floor()
        
        # Logic for running animation #
        currentTime = pygame.time.get_ticks()
        if currentTime - timer >= interval:
            frameIndex = (frameIndex + 1) % len(frames)
            timer = currentTime

        # Draws the frame to the screen
        screen.blit(frames[frameIndex], (400, 331 - frames[frameIndex].get_height()))

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

def mainMenu() -> None:
    # importing classes used in the main menu to avoid a circular import error
    from classes.button import Button

    # Popup flags
    settingsflag = False
    helpflag = False

    # Loading and store images for the idle aniamtion
    openEyes = pygame.image.load("assets/idle/idle1.png").convert_alpha()
    blink = pygame.image.load("assets/idle/idle2.png").convert_alpha()
    frames = [openEyes, blink]

    # Get time in ms
    timer = pygame.time.get_ticks()

    # Interval between blinks in ms
    interval = 0
    frameIndex = 0

    # All instances of main menu buttons, x pos is None because automatically centered on that axis
    playbutton = Button("PLAY", 155, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, True)
    settingsbutton = Button("SETTINGS", 240, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, True)
    helpbutton = Button("HELP", 375, (242, 225, 36), (255, 192, 20), fonts["Tiny"], 10, 5, True)

    # Loop for the main menu
    while True:
        for event in pygame.event.get():
            # If the mouse button is pressed, go to the game loop
            if event.type == pygame.MOUSEBUTTONDOWN and playbutton.isClicked():
                pygame.display.set_caption("Blob Dodge - Game Loop")
                gameLoop()

            # If the settings button is pressed, open the settings window
            if event.type == pygame.MOUSEBUTTONDOWN and settingsbutton.isClicked():
                settingsflag = True

            # If the help button is pressed, open the help window
            if event.type == pygame.MOUSEBUTTONDOWN and helpbutton.isClicked(): 
                helpflag = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fills the screen grey and makes the floor
        screen.fill(BGCOL)
        floor()
        
        # Idle animation code being written here as it needs to be inside a while loop to keep updating the animation
        # Gets the current time in ms
        currentTime = pygame.time.get_ticks()

        # Chekcs if characters eyes are open, and if enough time has passed since last blink, close eyes
        if frameIndex == 0 and currentTime - timer >= interval:
            # Switch to the next frame
            frameIndex = 1
            # Set the interval for the next blink, 1 to 10 secs
            interval = random.randint(1000, 10000)
            # Update the timer to the current time to calculate time for next blink
            timer = currentTime

        # Check if the time since the last update is greater than the interval for blunk eyes, open eyes after 150ms
        if frameIndex == 1 and currentTime - timer >= 150:
            # Then switches to the open eyes frame where it loops back to the first if statement
            frameIndex = 0

        # Draws the frame to the screen
        screen.blit(frames[frameIndex], (400, 331 - frames[frameIndex].get_height()))

        # Calling the drawing and hovering methods to the play, help and settings button
        playbutton.drawButton()
        playbutton.isHovered()

        settingsbutton.drawButton()
        settingsbutton.isHovered()

        helpbutton.drawButton()
        helpbutton.isHovered()

        # Puts the main menu text at the top of the screen
        MMtext = fonts["Header"].render("MAIN MENU", True, ("white"))
        main_menu_text_rect = MMtext.get_rect(center=(width // 2, height // 12))
        screen.blit(MMtext, (main_menu_text_rect))

        highScore(helpbutton)

        if settingsflag == True:
            from classes.popup import Popup
            # Create an instance of a popup window
            SettingsPopup = Popup()
            SettingsPopup.drawPopup()
            SettingsPopup.backButton()
            
            # Disable the play and settings button when the popup is open
            playbutton = Button("PLAY", 155, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, False)
            settingsbutton = Button("SETTINGS", 240, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, False)

        if helpflag == True:
            from classes.popup import Popup
            # Create an instance of a popup window
            HelpPopup = Popup()
            HelpPopup.drawPopup()
            HelpPopup.backButton()

            # Disable the play and settings button when the popup is open
            playbutton = Button("PLAY", 155, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, False)
            settingsbutton = Button("SETTINGS", 240, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 25, 10, False)

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

def highScore(helpbutton) -> None:
    # Opens and reads the highscore text file
    file = open("highscore.txt", "r")
    fileVal = file.read()

    # Gets the highscore text and the value of the file
    highScoreText = fonts["Tiny"].render(f"Highscore: {fileVal}", True, (89, 186, 255))
    
    # Get the position to draw the high score above the help button, 360 bc that's
    helpbuttonCenter = (width // 2, helpbutton.y)
    highscorePos = (helpbuttonCenter[0] - highScoreText.get_width() // 2, helpbuttonCenter[1] - highScoreText.get_height() - 10)

    # Draws the highscore text and value of the file to the screen
    screen.blit(highScoreText, highscorePos)

    # Closes the file once the operation has been completed
    file.close()

def floor(): 
    pygame.draw.line(screen, (172, 172, 172), (0,331), (width, 331), 2) 

if __name__ == "__main__":
    mainMenu()