# Coin stuff #
currentCoinTime = time.time()
timeSinceLastCoin = currentCoinTime - coinTimer
if currentCoinTime - coinTimer >= coinInterval:
    coinFrameIndex = (coinFrameIndex + 1) % len(coinFrames)
    coinTimer = currentCoinTime

moveCoinSpeed -= 15
coinX = width + moveCoinSpeed
if coinX + coinFrames[0].get_width() < 0:
    moveCoinSpeed = 0
    randomHeight = random.randint(0, 331 - coinFrames[0].get_height())

if timeSinceLastCoin >= coinSpawnInterval:
    print ("Coin interval reached, resetting timer")
    coinTimer = currentCoinTime
else:
    print ("Time Elapsed is " + str(timeSinceLastCoin) + " Seconds")