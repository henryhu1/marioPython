#FSE - Platformer
from pygame import *
from random import *
size=(800,435)
screen = display.set_mode(size)
#=====================================================================music
mixer.init()
mixer.Channel(0).play(mixer.Sound("sound/level_1.wav"))
mute_flag = True

#=====================================================================pictures and transforming
back = image.load("images/LEVEL_1-1.png")
maskPic = image.load("images/LEVEL_1-1_mask.png")
heart_pic = image.load("images/heart.png")
heart_pic = transform.scale(heart_pic,(15,15))
powerUp_life_right=image.load("images/1upr.png")
powerUp_life_left=image.load("images/1upl.png")
#=====================================================================colours
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW_power=(255,201,14)
YELLOW_coin=(255,255,0)
YELLOW=[YELLOW_power,YELLOW_coin]
MASK=[WHITE,YELLOW_power,YELLOW_coin]
#============================================================================font
font.init()
comicFont = font.SysFont("Comic Sans MS", 18)

#=====================================================================list indices and what they are
X=0
Y=1
VY=2
ONGROUND=3
SCREENX = 4

frame_rate = 60

#=====================================================================entity lists
player=[250,343,0,True,250]
#=====================================================================functions
#=====================================================================
def moveRight(guy,vx):
    keys = key.get_pressed()
    for i in range(vx):
        if getPixel(maskPic,guy[X]+30,guy[Y]+20) not in MASK and getPixel(maskPic,guy[X]+30,guy[Y]+10) not in MASK: #checks if player can move right       
            if keys[K_LSHIFT]: #running speed (faster)
                guy[X] += 0.5
                if guy[SCREENX] < 400:
                    guy[SCREENX] += 0.5
            else:
                guy[X] += 0.25 #normal speed
                if guy[SCREENX] < 400:
                    guy[SCREENX] += 0.25
            
def moveLeft(guy,vx):
    keys = key.get_pressed()
    for i in range(vx):
        if getPixel(maskPic,guy[X],guy[Y]+20) not in MASK and getPixel(maskPic,guy[X],guy[Y]+10) not in MASK: #checks if player can move left
            if keys[K_LSHIFT]: #running speed (faster)
                guy[X] -= 0.5
                if guy[SCREENX] > 400:
                    guy[SCREENX] -= 0.5
            else:
                guy[X] -= 0.25 #normal speed
                if guy[SCREENX] > 400:
                    guy[SCREENX] -= 0.25

def moveUp(guy,vy): #checks to see if player's head hits a platform (blocks)
    keys = key.get_pressed()
    global hitBlock,offset,coinBlockDraw,RNG_coin,powerUps,powerUpX,powerUpY,powerUpMovement,RNG_powerUp
    
    for i in range(vy):
        if getPixel(maskPic,guy[X]+7,guy[Y]-5) in MASK or getPixel(maskPic,guy[X]+17,guy[Y]-5) in MASK or getPixel(maskPic,guy[X]+28,guy[Y]-5) in MASK: #there is a platform over player
            guy[VY] = 1
            
        if getPixel(maskPic,guy[X]+10,guy[Y]) in YELLOW or getPixel(maskPic,guy[X]+15,guy[Y]) in YELLOW or getPixel(maskPic,guy[X]+20,guy[Y]) in YELLOW: #block
            guy[VY] = 7 #made it so that player goes down faster to prevent repeats
            
            if getPixel(maskPic,guy[X]+10,guy[Y]) == YELLOW[1] or getPixel(maskPic,guy[X]+15,guy[Y]) == YELLOW[1] or getPixel(maskPic,guy[X]+20,guy[Y]) == YELLOW[1]: #coin block hit
                RNG_coin=randint(0,10000) #decides if player will get a coin
                if RNG_coin%20==0:
                    #for coin block functions
                    hitBlock="coin" 
                    coinBlockDraw=True

            else: #power up block hit
                powerUps+=1 #power up is in the game and moving around
                RNG_powerUp=randint(1,10) #decides if player will get a power up and what type
                if move==0 or move==2: #direction of power up movement is decided by player's movement
                    powerUpMovement=1 #if player is moving/facing right, power up will move left
                else:
                    powerUpMovement=0 #if player is moving/facing left, power up will move right
                powerUpX=player[0]+15 #finds power up's X pos
                powerUpY=player[1]-90 #finds power up's Y pos
                if powerUps>0: #if there's a power up in the game (there's a chance of no power up spawning)
                #for power up functions
                    hitBlock="power up"
                else:
                    hitBlock=False

        else:
            hitBlock=False

def moveDown(guy,vy): #checks to see if player is on a platform (mask colours)
    keys = key.get_pressed()
    for i in range(vy):
        if getPixel(maskPic,guy[X]+7,guy[Y]+35) in MASK or getPixel(maskPic,guy[X]+17,guy[Y]+35) in MASK or getPixel(maskPic,guy[X]+28,guy[Y]+35) in MASK:
            guy[ONGROUND]=True
            guy[VY]=0
            
#=====================================================================player movement
def moveGuy(guy):
    'moves the player and animations'
    global move,playerFrame,direction,powerUpped,mute_flag
    
    keys = key.get_pressed()

    moveUp(player,10) #calls the function
    
    moveDown(player,10) #calls the function
    
    if keys[K_d] and guy[X] < 5821: #allows player to move right, according to restrictions set in game
        moveRight(player,10)
        direction="right"
        
    elif keys[K_a] and guy[X] > 250: #allows player to move left, according to restrictions set in game
        moveLeft(player,10)
        direction="left"
        
    else: #if there is no movement, the player will stand still and the frames will not change (stay in standing frame)
        playerFrame = 0
#=====================================================================direction and movement
    if guy[ONGROUND]: #finding the direction of the player
        if direction=="right":
            newMove=RIGHT
        else:
            newMove=LEFT
    else:
        if direction=="right":
            newMove=JUMPR
        else:
            newMove=JUMPL
            
#=====================================================================jumping
    if keys[K_SPACE]:
        if powerUpped==False: #if player has no power up (propeller)
            if guy[ONGROUND]: #player will only jump if they are on the ground
                guy[VY] = -13
                guy[ONGROUND]=False
                if mute_flag: #if sound is not muted
                    mixer.Channel(1).play(mixer.Sound("sound/jump.ogg")) #jumping sound

        else: #if player has power up (propeller)
            #only restrictions on it is if player is not too far right (less than 5000 pixels) and if their head doesn't hit a platform
            if guy[X]<5000 and getPixel(maskPic,guy[X]+7,guy[Y]-5) not in MASK and getPixel(maskPic,guy[X]+17,guy[Y]-5) not in MASK and getPixel(maskPic,guy[X]+28,guy[Y]-5) not in MASK:
                guy[VY] = -5 #player will be able to move upward, even if they aren't on the ground (flying)
            else: #if restrictions are not met 
                powerUpped=False #lose power up
                
    guy[Y]+=guy[VY]     # add current speed to Y

    if getPixel(maskPic,guy[X]+17,guy[Y]+35) in MASK: #on the mask (to prevent player from sinking into the ground)
        if guy[Y] >= 346: #player on the ground
            guy[Y] = 346
            guy[VY] = 0
            guy[ONGROUND]=True
    else: #player fell into a hole
        if guy[Y] >= 800:
            guy[Y] = 800 #keep his Y at 800
            guy[VY] = 0
        guy[ONGROUND]=False
        
    if flag:
        guy[VY]+=0.7     # add current speed to Y

#=====================================================================sprite and frame
    if newMove!=JUMPR and newMove!=JUMPL: #making sure that jumping isn't
                                          #interfering with other movement and sprite animations
        
        if move == newMove: # 0 is a standing pose, so we want to skip over it when we are moving
            if keys[K_LSHIFT]:
                playerFrame += 0.2
            else:
                playerFrame += 0.15

            if playerFrame >= len(marioSprite[move]):
                playerFrame = 1
        elif newMove != -1:     # a move was selected
            move = newMove      # make that our current move
            playerFrame = 1

    else:
        move = newMove
        playerFrame = 0

#=====================================================================
def fallDeath(guy):
    global goombaPos0,goombaPos1,goombaPos2,enemyList,health
    if guy[Y]>700: #if player Y is over 700 (which means if player fell into a hole, this function works)
        guy[0]=250
        guy[1]=343
        guy[2]=0                        #resets player position to what it would be in the beginning of the game
        guy[3]=True
        guy[4]=250
        health -= 1
        
#=====================================================================
def findOffset(guy):
    if guy[SCREENX] - guy[X] <= 0:
        return guy[SCREENX] - guy[X]        #finds offset of player
    else:
        return (0)

#=============================================================PAUSE
run = True
mute_flag = True
exit_flag = False
def pause():
    global run,sound_flag,exit_flag,mute_flag
    #sound_flag = False
    run = True

    clear_background = Surface((350,500),SRCALPHA)
    draw.rect(clear_background,(0,0,0,90),(0,0,800,210))       #claea back ground
    screen.blit(clear_background,(200,100))
    
    pause_word = image.load("images/pause.png")
    pause_word = transform.smoothscale(pause_word,(275,100))
    screen.blit(pause_word,(230,110))

    play = image.load("images/play.png")
    play = transform.smoothscale(play,(60,60))
    screen.blit(play,(345,220))
    play_rect = Rect(345,220,60,60)


    exit = image.load("images/exit.png")
    exit = transform.scale(exit,(60,60))
    screen.blit(exit,(245,220))
    exit_rect = Rect(245,220,60,60)
    setting_rect = Rect(760,0,37,47)

    mute_icon = image.load("images/mute.png")
    mute_icon = transform.scale(mute_icon,(60,60))
    screen.blit(mute_icon,(445,220))
    mute_rect = Rect(445,220,60,60)

    while run:
        click = False
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        
        for evnt in event.get():   
            if evnt.type == MOUSEBUTTONDOWN:
                click = True

            if evnt.type == KEYDOWN:
                #print(evnt.key)
                if evnt.key== 112:
                    run = False
                    sound_flag = True 
            if click:
                if play_rect.collidepoint(mx,my):
                    run = False

            if click:
                if exit_rect.collidepoint(mx,my):
                    exit_flag = True
                    run = False

            if click:
                if mute_rect.collidepoint(mx,my):
                    mute_flag = False

                    


        display.flip()
    if exit_flag:
        return main_menu() #makes you go back to main menu
#=====================================================================
def hud():
    global timer_flag
    font.init()
    smallFont = font.SysFont("Comic Sans MS", 15)
    global comicFont
#=================================================timer    
    minutes = time.get_ticks()//1000//60
    seconds = time.get_ticks()//1000        #getting how many seconds since the program ran
##    if seconds>=60:
##        seconds = 0
#=======================================================time blitting
    output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
 
    # Blit to the screen
    text = comicFont.render(output_string, True, WHITE)
    
    screen.blit(text, [600, 7])

#=================================================================world

    world = comicFont.render("WORLD",True,WHITE)
    screen.blit(world,[380,7])

    world_text = smallFont.render("1-1",True,WHITE)
    screen.blit(world_text,[400,21]) 
 
#=====================================================================score blitting
    score_string = "X {:04}".format(points)
    score = comicFont.render(score_string,True,WHITE)
    screen.blit(score,[233,7])
    
#======================================================================settings picture (top right of game play screen)

    settings_icon = image.load("images/settings2.png")

    settings_icon = transform.smoothscale(settings_icon,(37,47))
    screen.blit(settings_icon,(760,0))
    
#=====================================================================
def enemyFrames():
    global enemyFrame
    enemyFrame+=0.01
    if enemyFrame>=2:    #enemy sprite movement function
        enemyFrame=0
    return enemyFrame

#=====================================================================
def goombaCheck(goomba,number):  #cheeks to see if enememy path is clear and returns position
    if enemyList[number]==0:
        if movementList[number]==0:  #index's enemylist positon to the flag list and if the index position is 0 gomba moves left and if index is 1 gomba moves right
            if getPixel(maskPic,goomba,343)!= WHITE: #if goomba isn't next to mask colour (on the left of enemy)
                goomba-=0.3
            else:
                movementList[number]=1
        else: 
            if getPixel(maskPic,goomba+35,343)!= WHITE: #if goomba isn't next to mask colour (on the right of enemy)
                goomba+=0.3
            else:
                movementList[number]=0
    else:
        goomba=-10

    return goomba

#=====================================================================
def goombaPos():#cheeks all the goomba positons and appends them all to a central goomba list
    global enemyPos0,enemyPos1,enemyPos2,enemyPos3,offset

    enemyPos=[]

    enemyPos0=goombaCheck(enemyPos0,0)
    enemyPos1=goombaCheck(enemyPos1,1)
    enemyPos2=goombaCheck(enemyPos2,2)
    enemyPos3=goombaCheck(enemyPos3,3)

    enemyPos.append((enemyPos0+offset,343))
    enemyPos.append((enemyPos1+offset,343))
    enemyPos.append((enemyPos2+offset,343))
    enemyPos.append((enemyPos3+offset,343))
    
    return enemyPos
    
#=====================================================================
def sprite(name,start,end):   #Gets all the sprites and appends them to a list
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move

def sprite_resize(name,start,end): #same as sprite but makes the sprite smaller too
    move = []
    for i in range(start,end+1):
        img = (image.load("%s/%s%03d.png" % (name,name,i)))
        img = transform.scale(img,(21,21))
        move.append(img)
        
    return move

#=====================================================================flagpole function
flag = True
poleflag = True
def flagpole(guy): #this is performed once the player reaches the end
    x=0
    global flag, poleflag,running
    flagrect = Rect(5645,72,10,277)
    #draw.rect(screen,(255,0,0),flagrect,10)
    if guy[X]>5731:    
        flag = False
        guy[X] = 5753
        if poleflag:
            if guy[Y] <= 70:
                guy[VY] = 0
                poleflag = False
            else:
                guy[VY] = +1

#=====================================================================
def playerCollision(): #checks to see if player collides with an enemy
    global enemyPos0,enemyPos1,enemyPos2,coinList,health,points,offset,playerRect,powerUpped,mute_flag
    
    playerTopRect=Rect(playerRect.left-8,playerRect.top,46,10) #defining each section of player's body
    playerBottomRect=Rect(playerRect.left,playerRect.bottom,30,-10)
    playerRightRect=Rect(playerRect.right,playerRect.top+10,8,25)
    playerLeftRect=Rect(playerRect.left,playerRect.top+10,-8,25)
    
    for i in goombaPos():  #makes a rect for collision for each of the goomba's body sections
        goombaRect=Rect(i+(35,35))
        goombaTopRect=Rect(goombaRect.left,goombaRect.top,35,10)
        goombaRightRect=Rect(goombaRect.right,goombaRect.top,8,35)
        goombaLeftRect=Rect(goombaRect.left,goombaRect.top,-8,35)
        
        if playerBottomRect.colliderect(goombaTopRect): #player steps on goomba
            player[ONGROUND]=False
            if keys[K_SPACE]:
                player[VY]=-13   #if player colldes player gets moves 13 unnits up (jumps again)
                points += 30
            else:
                player[VY]=-10
                points+=30
                if mute_flag:
                    mixer.Channel(2).play(mixer.Sound("sound/stomp.ogg")) #stomping sound

            #checks to see which goomba is hit, each is in a restricted X portion
            if player[0]<1200:
                enemyList[0]=1
            elif 1200<=player[0]<=2000:
                enemyList[1]=1
            elif 2500<=player[0]<=4070:
                enemyList[2]=1
            elif 4500<=player[0]<=4735:
                enemyList[3]=1
                
        if playerRightRect.colliderect(goombaLeftRect) or playerLeftRect.colliderect(goombaRightRect): #player gets hit on the side
            start()
            health-=1 
            points-= 25            #loose health and points if collide with gomba and dont jump on top
            powerUpped=False
            if mute_flag:
                mixer.Channel(0).pause() #pauses the background music so the "death sound" can play
                mixer.Channel(4).play(mixer.Sound("sound/1down.ogg")) #death sound
    if mute_flag:
        if mixer.Channel(4).get_busy()==0: #if the death sound is finished
            mixer.Channel(0).unpause() #background music resumes
            
def start():
    #resets all variables when game goes back to menu or player dies
    global health,points,enemyList,enemyPos0,enemyPos1,enemyPos2,enemyPos3,coinDraw
    player[0],player[1],player[2],player[3],player[4]=250,343,0,True,250
    if health==0:
        health=5
    points=0
    enemyList=[0,0,0,0]
    enemyPos0=1000
    enemyPos1=1500
    enemyPos2=4004
    enemyPos3=4700
    for i in range(8):
        coinDraw[i]=0
                
#=====================================================================
def getPixel(mask,x,y): #gets pixel rgb
    if 0<= x < mask.get_width() and 0 <= y < mask.get_height():
        return mask.get_at((int(x),int(y)))[:3] 
   
    else:
        return False

#=========================================================================

#=====================================================================blitting everything (background, sprites)
def drawScene(picture,guy): #blits evvery sprite and image in the game
    global enemyList,coinList,character,health,coinBlockTime,powerUps,powerUpX,powerUpY,playerRect
    offset = findOffset(player)
    characterSwapRect=Rect(298+offset,120,1,1) # rect that swaps our player sprite
    draw.rect(screen,GREEN,characterSwapRect)
    screen.blit(back,(offset,0))
#===============================================================
    Coins() #coin blitting
    if coinBlockDraw: #checks if a coin block is hit
        coinBlockTime+=1 #time that coin stays in air after hitting block
        coinBlockImage() #blitting coin block coin
    if powerUps>0: #powr up sprite
        powerUpSpawn()
#===============================================================
    if character=="mario":  #variable that indicates what player sprite we will use
        pic = marioSprite[move][int(playerFrame)]
    else:
        pic = luigiSprite[move][int(playerFrame)]

    if playerRect.colliderect(characterSwapRect):
        player[VY]=100
        if character=="mario":
            character="luigi"
        else:
            character="mario"
            
    if offset<0:
        screen.blit(pic,(guy[SCREENX],guy[Y]))
    else:
        screen.blit(pic,(guy[X],guy[Y]))

    for index in range(len(goombaPos())):  #blits goomba
        if enemyList[index]==0:
            screen.blit(goomba[0][int(enemyFrames())],goombaPos()[index])

    
    screen.blit(smallcoin[0][int(coinFrames())],(200,10))

    x = 10
    for i in range(health):   #blits hearts
        screen.blit(heart_pic,(x+i,10))
        x+= 20

    hud()
    
    display.flip()
#================================================================================
def Coins():
    global points,offset,playerRect,mute_flag
    
    coinRect=[[641,223,0],[2295,225,1],[2640,107,2],[2933,225,3],[3511,107,4],[3976,224,5],[4743,286,6],[4965,226,7]] #coins
    for i in coinRect:
        i[0]+=offset
        if coinDraw[coinRect.index(i)]==0:
            screen.blit(coin[0][int(coinFrames())],i[:2])  #blitting of sprite

    for i in coinRect:
        if playerRect.colliderect(i[:2]+[24,35]):
            takenCoin=i[-1] #cheeks positon of coin in list
            if coinDraw[coinRect.index(i)]==0:
                points += 15
                if mute_flag:
                    mixer.Channel(3).play(mixer.Sound("sound/coin.ogg"))
            coinDraw[takenCoin]=1 #changes the flag variable to 1 if coin taken this way coin will not be blitted again

def coinFrames(): #coin sprite position in list function
    global coinFrame
    
    coinFrame+=0.03
    if coinFrame>=5:
        coinFrame=0    
    return coinFrame

def coinBlockFrames(): #sprite function for coin in blocks
    global coinBlockSpriteFrame
    
    coinBlockSpriteFrame+=0.1
    if coinBlockSpriteFrame>=5:
        coinBlockSpriteFrame=0
    return coinBlockSpriteFrame

def coinBlockImage():  #blits coins in the block
    global coinBlockTime,coinBlockSpriteFrame
    
    coinBlockX=player[0]+17+offset
    coinBlockY=player[1]-100
    screen.blit(coinBlockSprite[0][int(coinBlockFrames())],(coinBlockX,coinBlockY-coinBlockTime*1.5))

def coinBlock(): #plays the sound when con is found and gives points
    global points
    if mute_flag:
        mixer.Channel(3).play(mixer.Sound("sound/coin.ogg"))
    points+=15

#=====================================================================
def powerUpSpawn(): #blits the power up
    global powerUpX,powerUpY,powerUpMovement,playerRect,RNG_powerUp,mute_flag
    
    if getPixel(maskPic,powerUpX+21,powerUpY+43) not in MASK: #constant down motion
        powerUpY+=5
    if getPixel(maskPic,powerUpX+43,powerUpY) in MASK: #changing left and right
        powerUpMovement=1
    elif getPixel(maskPic,powerUpX,powerUpY) in MASK:
        powerUpMovement=0

    if powerUpMovement==0:
        powerUpX+=1
        if RNG_powerUp==5: #propeller sprite
            screen.blit(propeller[0][int(powerUpFrames())],(powerUpX+offset,powerUpY))
        elif RNG_powerUp<5: #1-up image
            screen.blit(powerUp_life_right,(powerUpX+offset,powerUpY))
    else:
        powerUpX-=1
        if RNG_powerUp==5: #propeller sprite 
            screen.blit(propeller[0][int(powerUpFrames())],(powerUpX+offset,powerUpY))
        elif RNG_powerUp<5: #1-up image
            screen.blit(powerUp_life_left,(powerUpX+offset,powerUpY))

    powerUpRect=Rect(powerUpX+offset,powerUpY,43,43) #power up rect

    if powerUpRect.colliderect(playerRect): #touching the power up
        powerUpPickUp()

def powerUpFrames(): #power up frames
    global powerUpFrame
    
    powerUpFrame+=0.03
    if powerUpFrame>=4:
        powerUpFrame=0
    return powerUpFrame

def powerUpPickUp(): #picking up power up
    global powerUpX,powerUpY,powerUps,RNG_powerUp,health,powerUpped,points

    del powerUpX #removes the power up positions
    del powerUpY
    powerUps=0
    if RNG_powerUp<5: #1-up power up effects
        points+=30
        if health!=5:
            health+=1
            if mute_flag:
                mixer.Channel(5).play(mixer.Sound("sound/1up.ogg")) #1-up sound
    elif RNG_powerUp==5: #propeller power up effects
        points+=50
        powerUpped=True

#=====================================================================
def main_menu():
    global sound_flag
    running = True
    myClock = time.Clock()
    buttons = [Rect(600,y*70+120,150,40) for y in range(4)] #rect positions for buttons
    
    text_pos = [(620,y*70+120) for y in range(4)] #blitting positions for text

    vals = ["main_game","instructions","credits","story"]

    labels = ["Play","Instructions","Credits","Story"]
   
    menu_back = image.load("images/mario_menu.jpg")
    menu_back = transform.smoothscale(menu_back,(800,435))
    screen.blit(menu_back,(0,0))
    draw.rect(screen,(1,71,167),(600,400,400,100))
    
    mario_title = image.load("images/Super_Mario_Bros_Logo.png")
    mario_title = transform.scale(mario_title,(400,80))
    screen.blit(mario_title,(320,10))
    
    luigi_back = image.load("images/Luigi_back.png")
    luigi_back = transform.scale(luigi_back,(180,290))
    screen.blit(luigi_back,(380,125))

    bigFont = font.SysFont("Comic Sans MS", 20)
#text = comicFont.render(output_string, True, WHITE)


    
    while running:
        #sound_flag = False
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"

        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        
        for r,v in zip(buttons,vals):
            draw.rect(screen,(222,55,55),r)
            if r.collidepoint(mpos):
                draw.rect(screen,(0,255,0),r,2)
                if mb[0]==1: #if mouse collides with buttons, it returns the value
                    return v
            else:
                draw.rect(screen,(255,255,0),r,2)

        for i in range(4): #text blitting
            textrender = bigFont.render(labels[i],True,WHITE)
            screen.blit(textrender,(text_pos[i]))
                
        display.flip()

#=====================================================================
def game_complete(): #when game is completed, this function works
    global run,sound_flag,exit_flag,health,page
    #sound_flag = False
    run = True
    

    clear_background = Surface((350,500),SRCALPHA)
    draw.rect(clear_background,(0,0,0,90),(0,0,800,210))       #black back ground
    screen.blit(clear_background,(200,100))

    bigFont = font.SysFont("Comic Sans MS", 30)
    textrender = bigFont.render("LEVEL 1-1 Complete",True,WHITE)
    screen.blit(textrender,(260,115))
    

    exit = image.load("images/exit.png")
    exit = transform.scale(exit,(60,60))
    screen.blit(exit,(345,220))
    exit_rect = Rect(345,220,60,60)

    mario_flag = image.load("images/mario_flag.png")
    mario_flag = transform.smoothscale(mario_flag,(40,30))
    screen.blit(mario_flag,(5731,70))
    
    while run:
        click = False
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        if health != -30:
            mario_flag = image.load("images/mario_flag.png")
            mario_flag = transform.smoothscale(mario_flag,(40,30))
            screen.blit(mario_flag,(401,70))
        
        for evnt in event.get():   
            if evnt.type == MOUSEBUTTONDOWN:
                click = True

            if click:
                if exit_rect.collidepoint(mx,my):
                    exit_flag = True
                    run = False

        display.flip()
    if exit_flag: #returns to main menu after finished
        page="main_menu"
        start()
        return main_menu()


def game_death(): #if player has 0 health, this function works
    global run,sound_flag,exit_flag,page
    #sound_flag = False
    run = True

    clear_background = Surface((350,500),SRCALPHA)
    draw.rect(clear_background,(0,0,0,90),(0,0,800,210))       #black back ground
    screen.blit(clear_background,(200,100))

    bigFont = font.SysFont("Comic Sans MS", 30)
    textrender = bigFont.render("You Died",True,WHITE)
    screen.blit(textrender,(260,115))


    exit = image.load("images/exit.png")
    exit = transform.scale(exit,(60,60))
    screen.blit(exit,(345,220))
    exit_rect = Rect(345,220,60,60)

    while run:
        click = False
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        
        for evnt in event.get():   
            if evnt.type == MOUSEBUTTONDOWN:
                click = True


            if click:
                if exit_rect.collidepoint(mx,my):
                    exit_flag = True
                    run = False

                    


        display.flip()
    if exit_flag: #returns to main menu after finished
        page="main_menu"
        start()
        
        return main_menu()

def instructions(): #blits instruction pic
    running = True
    story = image.load("images/story1.png")
    story = transform.scale(story, screen.get_size())
    screen.blit(story,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[K_ESCAPE]: running = False
        display.flip()
    return "main_menu" #returns to main menu after finished

def credit(): #blits credit pic
    running = True
    story = image.load("images/credits1.png")
    story = transform.scale(story, screen.get_size())
    screen.blit(story,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[K_ESCAPE]: running = False
        display.flip()
    return "main_menu" #returns to main menu after finished

def story(): #blits story pic
    running = True
    story = image.load("images/story.jpg")
    story = transform.scale(story, screen.get_size())
    screen.blit(story,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[K_ESCAPE]: running = False
        display.flip()
    return "main_menu" #returns to main menu after finished

#=====================================================================2D lists for sprites
marioSprite=[]
marioSprite.append(sprite("mario",1,4)) #right
marioSprite.append(sprite("mario",5,8)) #leftd
marioSprite.append(sprite("mario",9,9)) #jumping to the right
marioSprite.append(sprite("mario",10,10)) #jumping to the left

luigiSprite=[]
luigiSprite.append(sprite("luigi",1,4)) #right
luigiSprite.append(sprite("luigi",5,8)) #leftd
luigiSprite.append(sprite("luigi",9,9)) #jumping to the right
luigiSprite.append(sprite("luigi",10,10)) #jumping to the left

goomba=[] #enemy sprite
goomba.append(sprite("goomba",1,3))

coin=[] #in-game coin sprite
coin.append(sprite("coin",1,5))

coinBlockSprite=[] #coin block sprite
coinBlockSprite.append(sprite("coinBlock",1,5))

smallcoin = [] #small coin (top of game play screen) sprite
smallcoin.append(sprite_resize("coin",1,5))

propeller=[] #propeller mushroom power up sprite
propeller.append(sprite("propeller",1,4))
#=====================================================================player sprite variables
playerFrame=0 #frame of player
move=0 #default move for player (facing right)
hitBlock=False

#=====================================================================coins
coinFrame=0
coinBlockSpriteFrame=0
coinDraw = [0,0,0,0,0,0,0,0] #checks if coin is taken or not (0 is not, 1 is taken)
coinBlockDraw=False #coin block flag
coinBlockTime=0
RNG_coin=0

#=========================================================================health
health = 5 
#=================================================================================points
points = 0
#=====================================================================movement identities
RIGHT=0
LEFT=1
JUMPR=2
JUMPL=3

direction="right"
character="mario"
offset=findOffset(player)

px,py=player[0]+offset,player[1]
playerRect=Rect(px,py,30,35)
#=====================================================================power up variables (setting them to 0, to prevent program from crashing)
powerUps=0 #power ups in game
powerUpX=0
powerUpY=0
RNG_powerUp=0
powerUpped=False
powerUpFrame=0

if move==0 or move==2:
    powerUpMovement=1
else:
    powerUpMovement=0

#=====================================================================enemy things
enemyFrame=0
enemyPos0=1000
enemyPos1=1500
enemyPos2=4004
enemyPos3=4700
movementList=[0,0,0,0]
enemyList=[0,0,0,0]

#=====================================================================game loop

page = "main_menu"
while page != "exit":
    if page == "main_menu":
        page = main_menu()
    if page == "main_game":
        setting_rect = Rect(760,0,37,47)
        running = True
        myClock = time.Clock()
        while running:
            #sound_flag = True
            keys=key.get_pressed()
            for evt in event.get():  
                if evt.type == QUIT: 
                    running = False
                    page = "main_menu"
                    health=5
                    points=0
                    enemyList=[0,0,0,0]
                    enemyPos0=1000
                    enemyPos1=1500
                    enemyPos2=4004
                    enemyPos3=4700
                    for i in range(8):
                        coinDraw[i]=0
                    
                    start()
                if evt.type == KEYDOWN:
                    if evt.key == 112:
                        pause()

            mx,my=mouse.get_pos()
            mb=mouse.get_pressed()
            keys=key.get_pressed()
            offset=findOffset(player)
            px,py=player[0]+offset,player[1]
            playerRect=Rect(px,py,30,35)

            if mb[0] == 1 and setting_rect.collidepoint(mx,my):
                pause()

            if keys[K_ESCAPE]:
                running = False
                page = "main_menu"
                start()
        
            drawScene(screen, player)

            if mute_flag==False:
                mixer.quit()
            else:
                mixer.init()
            
            if coinBlockDraw:
                coinBlockTime+=1
                coinBlockImage()
            if coinBlockTime==50:
                coinBlockDraw=False
                coinBlockTime=0
                
            hitBlock=False
            
            moveGuy(player)

            if hitBlock=="coin":
                coinBlock()
            
            flagpole(player)

            if health==0:
                game_death()

            if player[X]>5721:
                game_complete()
            
            fallDeath(player)

            #hud(frame_rate)
            playerCollision()
            
            myClock.tick(240)
            display.flip() 
        sound_flag = True    
    if page == "instructions":
        page = instructions()    
    if page == "story":
        page = story()    
    if page == "credits":
        page = credit()
quit() 

