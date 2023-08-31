# Importing modules #git push NEA main --force# Forces push.
import pygame
import sys
import random
import math
import time

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
    "Medium":pygame.font.Font("assets/fonts/Gotham Black.ttf", 35),
    "Tiny":pygame.font.Font("assets/fonts/Gotham Black.ttf", 20)
}

# Variables used in the game loop and main menu
arrowKeyControls = True
handGestureControls = False
            
def gameLoop() -> None:

    # Loading and storing images for running and crouching animation
    run1 = pygame.image.load("assets/run/run1.png").convert_alpha()
    run2 = pygame.image.load("assets/run/run2.png").convert_alpha()

    crouchedRun1 = pygame.image.load("assets/run/crouchedRun1.png").convert_alpha()
    crouchedRun2 = pygame.image.load("assets/run/crouchedRun2.png").convert_alpha()

    runningFrames = [run1, run2]

    # Loading blob and obstacle images
    blob = pygame.image.load("assets/blob/blob.png").convert_alpha()
    obstacle1 = pygame.image.load("assets/obstacles/obstacle1.png").convert_alpha()

    # Getting initial times
    runningTimer = time.time()

    coinTimerForAnimation = time.time()
    coinTimerForSpawning = time.time()

    blobTimerForSpawning = time.time()

    obstacleTimerForSpawning = time.time()

    # Interval's between frame switches and frame indexes
    runningInterval = 0.1
    runningFrameIndex = 0

    coinInterval = 0.1
    coinFrameIndex = 0

    randomHeightIndex = random.randint(0,2)

    coinSpawnInterval = random.randint(5, 15)
    blobSpawnInterval = random.randint(5, 20)
    obstacleSpawnInterval = random.randint(2, 10)
    
    # Speed for the scrolling background
    moveBgSpeed = 0

    # Initial moving speeds
    moveBlobSpeed = 0
    moveObstacleSpeed = 0
    moveCoinSpeed = 0
    
    # Loading and scaling the coin frames by first creating an emptly list of the coin framaes
    coinFrames = []

    # Load the images using a for loop with values of i from 1 to 4 as the images are named from 1 to 4 and append to the coinFrames list
    # with the scaling operation
    for i in range (1, 5):
        coinFrames.append(pygame.transform.scale(pygame.image.load(f"assets/coin/coin{str(i)}.png").convert_alpha(), (50, 50)))

    randomHeight = random.randint(0, 331 - coinFrames[0].get_height())
    
    # Variables used for jumping
    characterX = 400
    characterY = 331 - run2.get_height()
    jumpCount = 10
    jumping = False

    # Variables for scoring
    score = 0
    scoringTimer = time.time()

    # Loop for the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Logic for jumping #
        keys = pygame.key.get_pressed()

        # Logic for crouching #
        # Check for down arrow key input 
        if keys[pygame.K_DOWN] and arrowKeyControls == True:
            # If there is down arrow key input, switch to the crouching frames
            runningFrames = [crouchedRun1, crouchedRun2]
        # If not, use the normal running frames
        else:
            runningFrames = [run1, run2]

        # Checking if the character is not already jumping
        if not (jumping):
            # Check for input and start jumping process if there is input
            if keys[pygame.K_UP] and arrowKeyControls == True:
                jumping = True
        else:
            if jumpCount >= - 10:
                # Does not move the chatacter as multiplying by 1
                neg = 1

                # If jumpCount is a negative number which occurs on 'jumpCount -=1', this moves character down
                if jumpCount < 0:
                    neg = -1

                # Model's the jump on a quadratic, change character's y pos by this value. 0.5 could represent the jump height. The lower
                # the value, the smaller the jump, 0.5 is the right amount. Neg moves character downwards as it is a negative value and it
                # represents c in the quadratic formula which is the y intercept
                characterY -= (jumpCount **2) * 0.5 * neg

                # Freezing the character
                runningFrames = [run1, run1]

                # Decrement jumpcount so the y value slowly does not change by anything once jumpCount has reached 0
                jumpCount -= 1
            else:
                # Jump has finished, resets jumping and jumpCount and starts the running animation again
                jumping = False
                jumpCount = 10
                runningFrames = [run1, run2]

        # Fills the screen grey
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
        moveBgSpeed -= 10

        # Reset moveBgSpeed
        # Checks if image is off screen, moveBgSpeed is a negative value so use absolute
        if abs(moveBgSpeed) > imageWidth:
            moveBgSpeed = 0

        for i in range (0, howMany):
            # x coordinate can't always be 0, needs offsetting by width of image, hence imageWidth
            screen.blit(scaledImage, (i * imageWidth + moveBgSpeed, 0))
        
        # Blob stuff #
        currentBlobSpawning = time.time()
        timeElapsedForSpawningBlob = currentBlobSpawning - blobTimerForSpawning

        # Moving the blob
        moveBlobSpeed -= 25

        # Storing the height's that a blob can spawn at
        heights = [331 - blob.get_height(), 331 - blob.get_height()*2, 331 - blob.get_height()*3.5]

        # Positioning the blob
        blobX = width + moveBlobSpeed
        blobY = heights[randomHeightIndex]
        
        # Spawns a blob
        if timeElapsedForSpawningBlob >= blobSpawnInterval and blobX + blob.get_width() < 0:

            # Puts the blob at the beginning and chooses new random height
            moveBlobSpeed = 0
            randomHeightIndex = random.randint(0, 2)
            blobY = heights[randomHeightIndex]

            # Create's a new spawn interval
            blobSpawnInterval = random.randint(5, 20)

            # Resets the timer
            blobTimerForSpawning = currentBlobSpawning

        # Drawing the blob to the screen
        screen.blit(blob, (blobX, blobY))

        # Obstacle stuff #
        currentObstacleSpawning = time.time()
        timeElapsedForSpawningObstacle = currentObstacleSpawning - obstacleTimerForSpawning

        scaledObstale1 = pygame.transform.scale(obstacle1, (45, 60))

        # Moving the obstacle
        moveObstacleSpeed -= 11

        # Positioning the obstacle
        obstacleX = width + moveObstacleSpeed
        obstacleY = 331 - scaledObstale1.get_height()

        # Spawns a obstacle
        if timeElapsedForSpawningObstacle >= obstacleSpawnInterval and obstacleX + scaledObstale1.get_width() < 0:

            # Puts obstacle at the beginning and chooses new random spawn interval
            moveObstacleSpeed = 0
            obstacleY = 331 - scaledObstale1.get_height()
            obstacleSpawnInterval = random.randint(2, 10)

            # Reset the timer
            obstacleTimerForSpawning = currentObstacleSpawning

        screen.blit(scaledObstale1, (obstacleX, obstacleY))

        # Coin stuff #
        currentCoinTimeForAnimation = time.time()
        currentCoinTimeForSpawning = time.time()

        TimeElapsedForAnimation = currentCoinTimeForAnimation - coinTimerForAnimation
        timeElapsedForSpawning = currentCoinTimeForSpawning - coinTimerForSpawning
        
        # Moving and positioning the coin
        moveCoinSpeed -= 15
        coinX = width + moveCoinSpeed

        # For the coin's animation
        if TimeElapsedForAnimation >= coinInterval:
            coinFrameIndex = (coinFrameIndex + 1) % (len(coinFrames))
            coinTimerForAnimation = currentCoinTimeForAnimation

        # For the coin's spawning behaviour/spawns a coin
        if timeElapsedForSpawning >= coinSpawnInterval:
    
            # Puts the coin at the beginning and makes a random height
            moveCoinSpeed = 0
            randomHeight = random.randint(0, 331 - coinFrames[0].get_height())

            # Create a new spawn interval
            coinSpawnInterval = random.randint(5, 15)

            # Reset the timer
            coinTimerForSpawning = currentCoinTimeForSpawning

        # Draw the coin
        screen.blit(coinFrames[coinFrameIndex], (coinX, randomHeight))

        # Drawing the floor #
        floor()
        
        # Logic for running animation #
        currentTime = time.time()
        if currentTime - runningTimer >= runningInterval:
            runningFrameIndex = (runningFrameIndex + 1) % len(runningFrames)
            runningTimer = currentTime

        # Draws the running frame to the screen
        if runningFrames == [run1, run2]:
            screen.blit(runningFrames[runningFrameIndex], (characterX, characterY))

        # Moves the character down by 13px if crouched
        elif runningFrames == [crouchedRun1, crouchedRun2]:
            screen.blit(runningFrames[runningFrameIndex], (characterX, characterY+13))

        # This else statement is for when the player is not running or crouching e.g, jumping
        else:
            screen.blit(runningFrames[runningFrameIndex], (characterX, characterY))

        # Scoring stuff #

        # Generating and drawing the current score
        currentScoringTimer = time.time()
        timeElapsedForScoring = currentScoringTimer - scoringTimer
        score = math.ceil(timeElapsedForScoring * 10)

        scoreText = fonts["Medium"].render(str(score), True, (68, 230, 50))
        # Got x and y by getting a pixel value i like then dividing it by the width/height(/2).
        # On my screen width is 1440 and height/2 is 410, want height at 20 so do 1440/20 which
        # is 72 and so width/72 == 20. Same principle for the height.
        screen.blit(scoreText, (width/72, ((height/2)/10)))

        # Drawing the highscore
        # Opens and reads the highscore text file
        file = open("highscore.txt", "r")
        fileVal = file.read()

        # Gets the highscore text and the value of the file
        highScoreText = fonts["Medium"].render(f"HI: {fileVal}", True, (68, 230, 50))

        # drawing to screen
        screen.blit(highScoreText, (width/72, ((height/2)/10) - 40))

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

def mainMenu() -> None:
    # importing classes used in the main menu to avoid a circular import error
    from classes.button import Button

    # Popup flags
    settingsFlag = False
    helpFlag = False

    # Making the variables globally accessible
    global arrowKeyControls
    global handGestureControls

    # Loading and storing images for the idle aniamtion
    openEyes = pygame.image.load("assets/idle/idle1.png").convert_alpha()
    blink = pygame.image.load("assets/idle/idle2.png").convert_alpha()
    frames = [openEyes, blink]

    # Get time in ms
    timer = time.time()

    # Interval between blinks in ms
    interval = 0
    blinkingFrameIndex = 0

    # All instances of main menu buttons, x pos is None because automatically centered on that axis
    playButton = Button("PLAY", 155, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 20, 5, True)
    settingsButton = Button("SETTINGS", 240, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 20, 5, True)
    helpButton = Button("HELP", 375, (242, 225, 36), (255, 192, 20), fonts["Tiny"], 10, 5, True)

    # Loop for the main menu
    while True:
        for event in pygame.event.get():
            # If the mouse button is pressed, go to the game loop
            if event.type == pygame.MOUSEBUTTONDOWN and playButton.isClicked():
                pygame.display.set_caption("Blob Dodge - Game Loop")
                gameLoop()

            # If the settings button is pressed, open the settings window
            if event.type == pygame.MOUSEBUTTONDOWN and settingsButton.isClicked():
                settingsFlag = True

            # If the help button is pressed, open the help window
            if event.type == pygame.MOUSEBUTTONDOWN and helpButton.isClicked(): 
                helpFlag = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fills the screen grey and makes the floor
        screen.fill(BGCOL)
        floor()
        
        # Idle animation code being written here as it needs to be inside a while loop to keep updating the animation
        # Gets the current time in ms
        currentTime = time.time()

        # Chekcs if characters eyes are open, and if enough time has passed since last blink, close eyes
        if blinkingFrameIndex == 0 and currentTime - timer >= interval:
            # Switch to the next frame
            blinkingFrameIndex = 1
            # Set the interval for the next blink, 1 to 10 secs
            interval = random.randint(1, 10)
            # Update the timer to the current time to calculate time for next blink
            timer = currentTime

        # Check if the time since the last update is greater than the interval for blunk eyes, open eyes after 0.15s
        if blinkingFrameIndex == 1 and currentTime - timer >= 0.15:
            # Then switches to the open eyes frame where it loops back to the first if statement
            blinkingFrameIndex = 0

        # Draws the frame to the screen
        screen.blit(frames[blinkingFrameIndex], (400, 331 - frames[blinkingFrameIndex].get_height()))

        # Calling the drawing and hovering methods to the play, help and settings button
        playButton.drawButton()
        playButton.isHovered()

        settingsButton.drawButton()
        settingsButton.isHovered()

        helpButton.drawButton()
        helpButton.isHovered()

        # Puts the main menu text at the top of the screen
        mainMenuText = fonts["Header"].render("MAIN MENU", True, ("white"))
        mainMenuTextRect = mainMenuText.get_rect(center=(width // 2, height // 12))
        screen.blit(mainMenuText, (mainMenuTextRect))

        highScore(helpButton)

        if settingsFlag == True:
            from classes.popup import Popup
            from classes.button import BackButton
            # Create an instance of a popup window
            SettingsPopup = Popup()
            SettingsPopup.drawPopup()
            SettingsPopup.backButton()

            # Disable the play and settings button when the popup is open
            playButton = Button("PLAY", 155, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 20, 5, False)
            settingsButton = Button("SETTINGS", 240, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 20, 5, False)

            # Instantiating buttons for the character controls and creating the text
            chooseControlsText = fonts["Tiny"].render("CHOOSE CONTROLS", True, (85, 85, 85))
            chooseControlsTextRect = chooseControlsText.get_rect(center=(width//2, height//3))
            screen.blit(chooseControlsText, (chooseControlsTextRect))

            hands = BackButton("HANDS", (width-455)//2+80, (height-410)//22+300, (0, 0, 0), (50, 156, 78), fonts["Medium"], 10, 10, True)
            arrows = BackButton("ARROWS", (width-455)//2+218, (height-410)//22+300, (0, 0, 0), (50, 156, 78), fonts["Medium"], 10, 10, True)

            # If the arrow key option is selected, make the arrow key flag true and the hand gesture flag false
            if arrows.isClicked():
                arrowKeyControls = True
                handGestureControls = False

            # If the hand gesture option is selected, make the hand gesture flag true and the arrow key flag false
            if hands.isClicked():
                handGestureControls = True
                arrowKeyControls = False

            # Carries on from the first if statement, this changes the colour of the 'arrows' button
            if arrowKeyControls == True and handGestureControls == False:
                arrows = BackButton("ARROWS", (width-455)//2+218, (height-410)//22+300, (42, 189, 81), (30, 212, 78), fonts["Medium"], 10, 10, True)
                hands = BackButton("HANDS", (width-455)//2+80, (height-410)//22+300, (0, 0, 0), (50, 156, 78), fonts["Medium"], 10, 10, True)

            # Carries on from the second if statement, this changes the colour of the 'hands' button
            if handGestureControls == True and arrowKeyControls == False:
                arrows = BackButton("ARROWS", (width-455)//2+218, (height-410)//22+300, (0, 0, 0), (50, 156, 78), fonts["Medium"], 10, 10, True)
                hands = BackButton("HANDS", (width-455)//2+80, (height-410)//22+300, (42, 189, 81), (30, 212, 78), fonts["Medium"], 10, 10, True)

            # Calling methods to draw buttons
            hands.drawButton()
            hands.isHovered()
            arrows.drawButton()
            arrows.isHovered()

        if helpFlag == True:
            from classes.popup import Popup
            # Create an instance of a popup window
            HelpPopup = Popup()
            HelpPopup.drawPopup()
            HelpPopup.backButton()

            # Disable the play and settings button when the popup is open
            playButton = Button("PLAY", 155, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 20, 5, False)
            settingsButton = Button("SETTINGS", 240, (242, 225, 36), (255, 192, 20), fonts["Smaller"], 20, 5, False)

        # Makes the game run at 60 FPS
        pygame.time.Clock().tick(60)
        pygame.display.update()

def highScore(helpButton) -> None:
    # Opens and reads the highscore text file
    file = open("highscore.txt", "r")
    fileVal = file.read()

    # Gets the highscore text and the value of the file
    highScoreText = fonts["Tiny"].render(f"Highscore: {fileVal}", True, (89, 186, 255))
    
    # Get the position to draw the high score above the help button
    helpButtonCenter = (width // 2, helpButton.y)
    highScorePos = (helpButtonCenter[0] - highScoreText.get_width() // 2, helpButtonCenter[1] - highScoreText.get_height() - 10)

    # Draws the highscore text and value of the file to the screen
    screen.blit(highScoreText, highScorePos)

    # Closes the file once the operation has been completed
    file.close()

def floor(): 
    pygame.draw.line(screen, (172, 172, 172), (0,331), (width, 331), 2) 

if __name__ == "__main__":
    mainMenu()