# Importing modules#git push NEA main --force# Forces push.
import pygame
import sys
import random
import math
import time

# Computer vision modules
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from keras.models import load_model

# Initialise pygame
pygame.init()

# Initialise mediapipe #
# Peforms hand recognition algorithm, object stored in hands
mpHands = mp.solutions.hands
# .Hands configures model, paramaters are self explanatory
handsConfiguration = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
# Draws detected key points so don't have to do it manually
mpDraw = mp.solutions.drawing_utils

# Initialise tensorflow and webcam #
# Load tensorflow pretrained model
model = load_model("HandTrack")
# Initialize webcam
cap = cv2.VideoCapture(0)

# Load gesture names
f = open("HandTrack/gesture.names" , "r")
gestureNames = f.read().split('\n')
f.close()
print(gestureNames)

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

# Variables used in multiple functions
arrowKeyControls = False
handGestureControls = True

coinCollisionCount = 0

def gameLoop() -> None: 
    global coinCollisionCount
    global handGestureControls
    global arrowKeyControls

    # Loading and storing images for running animation, crouching animation and death
    run1 = pygame.image.load("assets/run/run1.png").convert_alpha()
    run2 = pygame.image.load("assets/run/run2.png").convert_alpha()

    crouchedRun1 = pygame.image.load("assets/run/crouchedRun1.png").convert_alpha()
    crouchedRun2 = pygame.image.load("assets/run/crouchedRun2.png").convert_alpha()

    deathImage = pygame.image.load("assets/idle/dead.png").convert_alpha()

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

    shieldTimer = time.time()

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
    
    # Variables used for jumping and crouching
    characterX = 400
    characterY = 331 - run2.get_height()
    jumpCount = 10
    jumping = False
    crouching = False

    # Variables for scoring
    score = 0
    scoringTimer = time.time()

    # Creating rects and variables for collisions (coin, blob and obstacle rects are in their logic)
    runningRect = pygame.Rect(characterX, characterY, run1.get_width(), run1.get_height())
    
    # Variables for collisions and powerups
    fatalCollisionFlag = False
    coinCollisionFlag = False
    
    coinRespawnInterval = 3
    coinCollisionCount = 4
    
    shieldActive = False

    # Hand gesture variables
    gestureName = ""

    # Loop for the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if handGestureControls == True:
            # vision #
            # Read each frame
            res, frame = cap.read()
            x, y, z = frame.shape 
            
            # vertically flips the frame
            frame = cv2.flip(frame, 1)

            # change frame to RGB
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get hand landmark prediction, returns result class
            result = handsConfiguration.process(frameRGB)

            # If a hand is detected
            if result.multi_hand_landmarks:
                landmarks = []
                # Loop through detection and store coordinate in list
                for handslms in result.multi_hand_landmarks:
                    for xyz in handslms.landmark:
                        landmarkX = int(xyz.x * x)
                        landmarkY = int(xyz.y * y)

                        landmarks.append([landmarkX, landmarkY])

                    # Draw landmarks on frames
                    mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                    # Predict the gesture
                    prediction = model.predict([landmarks])
                    gestureID = np.argmax(prediction)
                    gestureName = gestureNames[gestureID]

                    # print the current gesture to console
                    print ("Current gesture: " + str(gestureName))

            # Resize and reposition the frame
            frame = cv2.resize(frame, (160, 90))

            # Show the final output
            cv2.imshow("Window", frame)

            # Move the window
            cv2.moveWindow("Window", 0, 305)

        # Logic for crouching with hand gestures #
        if arrowKeyControls == False:
            if gestureName == "crouch" and handGestureControls == True:
                crouching = True
            else:
                crouching = False

            # Logic for jumping with hand gestures #
            if fatalCollisionFlag == False and arrowKeyControls == False:
                # Checking if the character is not already jumping
                if not (jumping):
                    # Check for input and start jumping process if there is input
                    if gestureName == "jump":
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

                        # Moves hitbox with jump
                        runningRect = pygame.Rect(characterX, characterY, run1.get_width(), run1.get_height())

                        # Freezing the character
                        runningFrames = [run1, run1]

                        # Decrement jumpcount so the y value slowly does not change by anything once jumpCount has reached 0
                        jumpCount -= 1
                    else:
                        # Jump has finished, resets jumping and jumpCount and starts the running animation again
                        jumping = False
                        jumpCount = 10
                        runningFrames = [run1, run2]
        
        if handGestureControls == False:
            keys = pygame.key.get_pressed()

            # Logic for crouching with arrow keys #
            # Check for down arrow key input 
            if keys[pygame.K_DOWN] and arrowKeyControls == True:
                crouching = True
            else:
                crouching = False

            # Logic for jumping with arrow keys #
            # Only be able to jump if the character is alive
            if fatalCollisionFlag == False:
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

                        # Moves hitbox with jump
                        runningRect = pygame.Rect(characterX, characterY, run1.get_width(), run1.get_height())

                        # Freezing the character
                        runningFrames = [run1, run1]

                        # Decrement jumpcount so the y value slowly does not change by anything once jumpCount has reached 0
                        jumpCount -= 1
                    else:
                        # Jump has finished, resets jumping and jumpCount and starts the running animation again
                        jumping = False
                        jumpCount = 10
                        runningFrames = [run1, run2]
        
        if crouching == True:
            # Switch to crouching frames and move hitbox
            runningFrames = [crouchedRun1, crouchedRun2]
            runningRect = pygame.Rect(characterX, characterY+13, crouchedRun1.get_width(), crouchedRun1.get_height())

        if crouching == False:
            # Switch back to normal frames and hitbox
            runningFrames = [run1, run2]
            runningRect = pygame.Rect(characterX, characterY, run1.get_width(), run1.get_height())


        # Fills the screen grey
        screen.fill(BGCOL)

        # Background stuff #
        # As there are going to be multiple images, I am storing them in a dict
        background = pygame.image.load("assets/background/stars.png").convert_alpha()

        # Scaling the image and putting it on screen
        scaledImage = pygame.transform.scale(background, (330, 330))

        # See how many images I am going to need
        imageWidth = scaledImage.get_width()
        howMany = (math.ceil((int(width)/int(imageWidth)))) + 1

        # Scroll background speed
        actualBgSpeed = 10
        moveBgSpeed -= actualBgSpeed

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
        actualBlobSpeed = 25
        moveBlobSpeed -= actualBlobSpeed

        # Storing the height's that a blob can spawn at
        heights = [331 - blob.get_height(), 331 - blob.get_height()*2, 331 - blob.get_height()*3.5]

        # Positioning the blob
        blobX = width + moveBlobSpeed
        blobY = heights[randomHeightIndex]
        blobRect = pygame.Rect(blobX, blobY, blob.get_width(), blob.get_height())

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

        scaledObstacle1 = pygame.transform.scale(obstacle1, (45, 60))

        # Moving the obstacle
        actualObstacleSpeed = 11
        moveObstacleSpeed -= actualObstacleSpeed

        # Positioning the obstacle
        obstacleX = width + moveObstacleSpeed
        obstacleY = 331 - scaledObstacle1.get_height()
        obstacleRect = pygame.Rect(obstacleX, obstacleY, scaledObstacle1.get_width(), scaledObstacle1.get_height())

        # Spawns a obstacle
        if timeElapsedForSpawningObstacle >= obstacleSpawnInterval and obstacleX + scaledObstacle1.get_width() < 0:

            # Puts obstacle at the beginning and chooses new random spawn interval
            moveObstacleSpeed = 0
            obstacleY = 331 - scaledObstacle1.get_height()
            obstacleSpawnInterval = random.randint(2, 10)

            # Reset the timer
            obstacleTimerForSpawning = currentObstacleSpawning

        screen.blit(scaledObstacle1, (obstacleX, obstacleY))
        
        # Coin stuff #
        currentCoinTimeForAnimation = time.time()
        currentCoinTimeForSpawning = time.time()

        TimeElapsedForAnimation = currentCoinTimeForAnimation - coinTimerForAnimation
        timeElapsedForSpawning = currentCoinTimeForSpawning - coinTimerForSpawning
        
        # Moving and positioning the coin
        moveCoinSpeed -= 15
        coinX = width + moveCoinSpeed
        
        # Move coin's hitbox off screen after a collision
        if coinCollisionFlag == False:
            coinRect = pygame.Rect(coinX, randomHeight, coinFrames[0].get_width(), coinFrames[0].get_height())
        else:
            coinRect = pygame.Rect(10000, 10000, coinFrames[0].get_width(), coinFrames[0].get_height())

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
            coinSpawnInterval = random.randint(3, 10)

            # Reset the timer
            coinTimerForSpawning = currentCoinTimeForSpawning

        # Only draw a coin if it has not been collided with
        if coinCollisionFlag == False:
            # Draw the coin
            screen.blit(coinFrames[coinFrameIndex], (coinX, randomHeight))

        # Drawing the floor #
        floor()
        
        # Only be able to crouch if the character is alive
        if fatalCollisionFlag == False:
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
            
        scoreText = fonts["Medium"].render(str(score), True, (68, 230, 50))

        # Drawing the highscore
        # Opens and reads the highscore text file
        file = open("highscore.txt", "r")
        fileVal = file.read()

        # Gets the highscore text and the value of the file
        highScoreText = fonts["Medium"].render(f"HI: {fileVal}", True, (68, 230, 50))

        # Highscore aspect of the scoring system
        if score > int(fileVal):
            file = open("highscore.txt", "w")
            file.write(str(score))

        # # Only be able to imacrement score if the character is alive
        if fatalCollisionFlag == False:
            score = math.ceil(timeElapsedForScoring * 10)

            # drawing to screen
            screen.blit(highScoreText, (width/72, ((height/2)/10) - 40))
            # Got x and y by getting a pixel value i like then dividing it by the width/height(/2).
            # On my screen width is 1440 and height/2 is 410, want height at 20 so do 1440/20 which
            # is 72 and so width/72 == 20. Same principle for the height.
            screen.blit(scoreText, (width/72, ((height/2)/10)))

        # Draw Hitboxes
        pygame.draw.rect(screen, (255, 0, 0), coinRect, 2)
        pygame.draw.rect(screen, (255, 0, 0), runningRect, 2)
        pygame.draw.rect(screen, (255, 0, 0), obstacleRect, 2)
        pygame.draw.rect(screen, (255, 0, 0), blobRect, 2)

        # Logic for collisions #
        
        # If character collides with a coin
        if runningRect.colliderect(coinRect) and not shieldActive:
            coinCollisionFlag = True
            coinCollisionCount += 1

        # If character collides with a blob
        if runningRect.colliderect(blobRect) and not shieldActive:
            fatalCollisionFlag = True

        # If character collides with an obstacle
        if runningRect.colliderect(obstacleRect) and not shieldActive:
            fatalCollisionFlag = True
            
        if fatalCollisionFlag == True:
            from classes.button import Button
            
            runningFrames = [deathImage, deathImage]
            screen.blit(runningFrames[runningFrameIndex], (characterX, characterY))
            
            # Making coin and running animations freeze
            runningInterval = 999
            coinInterval = 999

            # Making everything moving onscreen freeze
            moveCoinSpeed += 15
            moveObstacleSpeed += actualObstacleSpeed
            moveBlobSpeed += actualBlobSpeed
            moveBgSpeed += actualBgSpeed

            # Creating game over text
            gameOverText = fonts["Header"].render(str("GAME OVER"), True, (184, 12, 0))
            gameOverTextX = (width - gameOverText.get_width()) //2
            screen.blit(gameOverText, (gameOverTextX, 20))

            # Showing users score
            deathScoreText = fonts["Medium"].render(str("YOUR SCORE: " + str(score)), True, (255, 60, 46))
            deathScoreTextX = (width - deathScoreText.get_width()) //2
            screen.blit(deathScoreText, (deathScoreTextX, 135))

            # Creates button to go back to main menu
            deathButton = Button("MAIN MENU", 185, (255, 60, 46), (255, 84, 71), fonts["Medium"], 25, 10, True)
            deathButton.drawButton()
            deathButton.isHovered()
            
            if deathButton.isClicked():
                mainMenu()

        if coinCollisionFlag == True:
            # Check if the time elapsed for spawning is >= than coin respawn interval
            if timeElapsedForSpawning >= coinRespawnInterval:
                # If so, reset all variables used in the coin operation which allows coins to spawn again
                # and increment the coin collision counter by 1
                coinCollisionFlag = False

        # Coin counter bar stuff #
        if fatalCollisionFlag == False:
            emptyBarRect = pygame.Rect(21, 93, 200, 35)

            # The x value is based off of the width of the other rectangles
            rects = [pygame.Rect(219-(40+(i*40))+2, 93, 40, 35) for i in range(5)]

            # Drawing the rectangles
            if coinCollisionCount >= 5:
                colour = (255, 230, 0)
            else:
                colour = (255, 200, 0)

            for i in range(coinCollisionCount):
                pygame.draw.rect(screen, colour, rects[4 - i])

            pygame.draw.rect(screen, ('black'), emptyBarRect, 2)

            # shield stuff #

            # Start the current timer at the start
            currentShieldTimer = time.time()

            # Make shield active, reset the timer and coin count when hitting 5 coins
            if coinCollisionCount >= 5:
                shieldActive = True
                shieldTimer = currentShieldTimer
                coinCollisionCount = 0

            # Make the time elapsed variable
            timeElapsedForShield = currentShieldTimer - shieldTimer
            
            # If the time surpasses 30 seconds, make the time elapsed for shield false
            if timeElapsedForShield >= 30:
                shieldActive = False
            
            # If the shield is active, spawn the shield and make the bar yellow
            if shieldActive:
                rotateSpeed = -5
                colour = (255, 230, 0)

                # load and rotate image
                shieldImage = pygame.image.load("assets/powerups/shield.png").convert_alpha()
                # image, angle, ticks constantly change so good to use in this context
                rotatedShield = pygame.transform.rotate(shieldImage, pygame.time.get_ticks() // rotateSpeed)

                # positioning
                shieldRect = rotatedShield.get_rect()
                shieldRect.center = (characterX+40, characterY+25)

                # Drawing, if not topleft it bounces
                screen.blit(rotatedShield, shieldRect.topleft)

                # in range 5 because there are 5 divisions of the bar
                for i in range(5):
                    pygame.draw.rect(screen, colour, rects[4 - i])

            # If character collides with an obstacle with shield
            if (runningRect.colliderect(obstacleRect) or runningRect.colliderect(blobRect)) and shieldActive:
                #number here is (the time the shield is active for in total)-(the time of invulnerability)
                shieldTimer = currentShieldTimer-29.9

        # Makes the game run at 60 FPS
        # 60 for arrow, higher for hands, each frame for hands takes longer so need higher fps
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
    global hands

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
            # Run the hand gesture recognition code
            if handGestureControls == True and arrowKeyControls == False:
                arrows = BackButton("ARROWS", (width-455)//2+218, (height-410)//22+300, (0, 0, 0), (50, 156, 78), fonts["Medium"], 10, 10, True)
                hands = BackButton("HANDS", (width-455)//2+80, (height-410)//22+300, (42, 189, 81), (30, 212, 78), fonts["Medium"], 10, 10, True)

            # Calling methods to draw buttons
            hands.drawButton()
            hands.isHovered()
            arrows.drawButton()
            arrows.isHovered()

        if handGestureControls == True:
            # vision #
            # Read each frame
            res, frame = cap.read()
            x, y, z = frame.shape 
            
            # vertically flips the frame
            frame = cv2.flip(frame, 1)

            # change frame to RGB
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get hand landmark prediction, returns result class
            result = handsConfiguration.process(frameRGB)

            # If a hand is detected
            if result.multi_hand_landmarks:
                # Loop through detection and store coordinate in list
                for handslms in result.multi_hand_landmarks:
                    # Draw landmarks on frames
                    mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Resize and reposition the frame
            frame = cv2.resize(frame, (160, 90))

            # Show the final output
            cv2.imshow("Window", frame)

            # Move the window
            cv2.moveWindow("Window", 0, 305)

        if arrowKeyControls == True:
            cv2.destroyAllWindows()

        # If the help button is pressed
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
    highScoreText = fonts["Tiny"].render(f"Highscore: {fileVal}", True, (68, 230, 50))
    
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