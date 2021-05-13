#FSE - Platformer
from pygame import *
from random import *
size=(800,435)
screen = display.set_mode(size)
#=====================================================================music
mixer.init()
mixer.Channel(0).play(mixer.Sound("sound/level_1.ogg"))

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
    for i in range(vx):
        if getPixel(maskPic,guy[X]+30,guy[Y]+20) not in MASK and getPixel(maskPic,guy[X]+30,guy[Y]+10) not in MASK:           
            if keys[K_LSHIFT]:
                guy[X] += 0.5
                if guy[SCREENX] < 400:
                    guy[SCREENX] += 0.5
            else:
                guy[X] += 0.25
                if guy[SCREENX] < 400:
                    guy[SCREENX] += 0.25
            
def moveLeft(guy,vx):
    for i in range(vx):
        if getPixel(maskPic,guy[X],guy[Y]+20) not in MASK and getPixel(maskPic,guy[X],guy[Y]+10) not in MASK:
            if keys[K_LSHIFT]:
                guy[X] -= 0.5
                if guy[SCREENX] > 400:
                    guy[SCREENX] -= 0.5
            else:
                guy[X] -= 0.25
                if guy[SCREENX] > 400:
                    guy[SCREENX] -= 0.25

def moveUp(guy,vy):
    global hitBlock,offset,coinBlockDraw,RNG_coin,powerUps,powerUpX,powerUpY,powerUpMovement,RNG_powerUp
    
    for i in range(vy):
        if getPixel(maskPic,guy[X]+7,guy[Y]-5) in MASK or getPixel(maskPic,guy[X]+17,guy[Y]-5) in MASK or getPixel(maskPic,guy[X]+28,guy[Y]-5) in MASK:
            guy[VY] = 1
            
        if getPixel(maskPic,guy[X]+10,guy[Y]) in YELLOW or getPixel(maskPic,guy[X]+15,guy[Y]) in YELLOW or getPixel(maskPic,guy[X]+20,guy[Y]) in YELLOW:
            guy[VY] = 7
            
            if getPixel(maskPic,guy[X]+10,guy[Y]) == YELLOW[1] or getPixel(maskPic,guy[X]+15,guy[Y]) == YELLOW[1] or getPixel(maskPic,guy[X]+20,guy[Y]) == YELLOW[1]:
                RNG_coin=randint(0,10000)
                if RNG_coin%20==0:
                    hitBlock="coin"
                    coinBlockDraw=True

            else:
                powerUps+=1
                RNG_powerUp=randint(1,10)
                if move==0 or move==2:
                    powerUpMovement=1
                else:
                    powerUpMovement=0
                powerUpX=player[0]+15
                powerUpY=player[1]-90
                if powerUps>0:
                    hitBlock="power up"
                else:
                    hitBlock=False

        else:
            hitBlock=False

def moveDown(guy,vy):
    for i in range(vy):
        if getPixel(maskPic,guy[X]+7,guy[Y]+35) in MASK or getPixel(maskPic,guy[X]+17,guy[Y]+35) in MASK or getPixel(maskPic,guy[X]+28,guy[Y]+35) in MASK:
            guy[ONGROUND]=True
            guy[VY]=0
            
#=====================================================================player movement
def moveGuy(guy):
    'moves the player and animations'
    global move,playerFrame,direction,powerUpped
    
    keys = key.get_pressed()

    moveUp(player,10)
    
    moveDown(player,10)
    
    if keys[K_d] and guy[X] < 5821:
        moveRight(player,10)
        direction="right"
        
    elif keys[K_a] and guy[X] > 250:
        moveLeft(player,10)
        direction="left"
        
    else:
        playerFrame = 0
#=====================================================================direction and movement
    if guy[ONGROUND]:
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
        if powerUpped==False:
            if guy[ONGROUND]:
                guy[VY] = -13
                guy[ONGROUND]=False
                mixer.Channel(1).play(mixer.Sound("sound/jump.ogg"))

        else:
            if guy[X]<5000 and getPixel(maskPic,guy[X]+7,guy[Y]-5) not in MASK and getPixel(maskPic,guy[X]+17,guy[Y]-5) not in MASK and getPixel(maskPic,guy[X]+28,guy[Y]-5) not in MASK:
                guy[VY] = -5
            else:
                powerUpped=False
                
    guy[Y]+=guy[VY]     # add current speed to Y

    if getPixel(maskPic,guy[X]+17,guy[Y]+35) in MASK:
        if guy[Y] >= 346: #player on the ground
            guy[Y] = 346
            guy[VY] = 0
            guy[ONGROUND]=True
    else:
        if guy[Y] >= 800:
            guy[Y] = 800
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
    if guy[Y]>700:
        guy[0]=250
        guy[1]=343
        guy[2]=0
        guy[3]=True
        guy[4]=250
        health -= 1
        
#=====================================================================
def findOffset(guy):
    if guy[SCREENX] - guy[X] <= 0:
        return guy[SCREENX] - guy[X]
    else:
        return (0)

#=============================================================PAUSE

run = True
def pause():
    global run,sound_flag
    #sound_flag = False
    run = True

    clear_background = Surface((350,500),SRCALPHA)
    draw.rect(clear_background,(0,0,0,90),(0,0,800,210))       #orange back ground
    screen.blit(clear_background,(200,100))
    
    pause_word = image.load("images/pause.png")
    pause_word = transform.smoothscale(pause_word,(275,100))
    screen.blit(pause_word,(230,110))

    play = image.load("images/play.png")
    play = transform.smoothscale(play,(60,60))
    screen.blit(play,(345,220))
    play_rect = Rect(345,220,60,60)
    draw.rect(screen,(RED),play_rect,1)
    
    setting_rect = Rect(760,0,37,47)
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

        display.flip()

#=====================================================================
def hud():
    font.init()
    smallFont = font.SysFont("Comic Sans MS", 15)
    global comicFont
#=================================================timer    
    minutes = time.get_ticks()//1000//60
    seconds = time.get_ticks()//1000
    if seconds>=60:
        seconds = 0
#=======================================================
    output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
 
    # Blit to the screen
    text = comicFont.render(output_string, True, WHITE)
    screen.blit(text, [600, 7])

#=================================================================world

    world = comicFont.render("WORLD",True,WHITE)
    screen.blit(world,[380,7])

    world_text = smallFont.render("1-1",True,WHITE)
    screen.blit(world_text,[400,21]) 
 
#=====================================================================
    score_string = "X {:04}".format(points)
    score = comicFont.render(score_string,True,WHITE)
    screen.blit(score,[233,7])



#=====================================================================
def enemyFrames():
    global enemyFrame
    enemyFrame+=0.01
    if enemyFrame>=2:
        enemyFrame=0
    return enemyFrame

#=====================================================================
def goombaCheck(goomba,number):
    if enemyList[number]==0:
        if movementList[number]==0:
            if getPixel(maskPic,goomba,343)!= WHITE:
                goomba-=0.3
            else:
                movementList[number]=1
        else:
            if getPixel(maskPic,goomba+35,343)!= WHITE:
                goomba+=0.3
            else:
                movementList[number]=0
    else:
        goomba=-10

    return goomba

#=====================================================================
def goombaPos():
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
def sprite(name,start,end):
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move

def sprite_resize(name,start,end):
    move = []
    for i in range(start,end+1):
        img = (image.load("%s/%s%03d.png" % (name,name,i)))
        img = transform.scale(img,(21,21))
        move.append(img)
        
    return move

#=====================================================================
flag = True
poleflag = True
def flagpole(guy):
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
def playerCollision():
    global enemyPos0,enemyPos1,enemyPos2,coinList,health,points,offset,playerRect,powerUpped
    
    playerTopRect=Rect(playerRect.left-8,playerRect.top,46,10)
    playerBottomRect=Rect(playerRect.left,playerRect.bottom,30,-10)
    playerRightRect=Rect(playerRect.right,playerRect.top+10,8,25)
    playerLeftRect=Rect(playerRect.left,playerRect.top+10,-8,25)
    
    for i in goombaPos():
        goombaRect=Rect(i+(35,35))
        goombaTopRect=Rect(goombaRect.left,goombaRect.top,35,10)
        goombaRightRect=Rect(goombaRect.right,goombaRect.top,8,35)
        goombaLeftRect=Rect(goombaRect.left,goombaRect.top,-8,35)
        
        if playerBottomRect.colliderect(goombaTopRect):
            player[ONGROUND]=False
            if keys[K_SPACE]:
                player[VY]=-13
                points += 30
            else:
                player[VY]=-10
                points+=30

            mixer.Channel(2).play(mixer.Sound("sound/stomp.ogg"))
            
            if player[0]<1200:
                enemyList[0]=1
            elif 1200<=player[0]<=2000:
                enemyList[1]=1
            elif 2500<=player[0]<=4070:
                enemyList[2]=1
            elif 4500<=player[0]<=4735:
                enemyList[3]=1
                
        if playerRightRect.colliderect(goombaLeftRect) or playerLeftRect.colliderect(goombaRightRect):
            start()
            health-=1
            points-= 25
            powerUpped=False
            mixer.Channel(0).pause()
            mixer.Channel(4).play(mixer.Sound("sound/1down.ogg"))
    if mixer.Channel(4).get_busy()==0:
        mixer.Channel(0).unpause()
            
def start():
    player[0],player[1],player[2],player[3],player[4]=250,343,0,True,250
    
#=====================================================================on ground platforms
def checkCollide(guy,plats):
    rec = Rect(guy[X],guy[Y],20,31)
    for p in plats:
        if rec.colliderect(p):
            if guy[VY]>0 and rec.move(0,-guy[VY]).colliderect(p)==False:
                guy[ONGROUND]=True
                guy[VY] = 0
                guy[Y] = p.y - 32

                
#=====================================================================
def getPixel(mask,x,y):
    if 0<= x < mask.get_width() and 0 <= y < mask.get_height():
        return mask.get_at((int(x),int(y)))[:3] 
   
    else:
        return False

#=========================================================================

#=====================================================================blitting everything (background, sprites)
def drawScene(picture,guy):
    global enemyList,coinList,character,health,coinBlockTime,powerUps,powerUpX,powerUpY,playerRect
    offset = findOffset(player)
    characterSwapRect=Rect(298+offset,120,1,1)
    screen.blit(back, (offset,0))
#===============================================================
    Coins()
    if coinBlockDraw:
        coinBlockTime+=1
        coinBlockImage()
    if powerUps>0:
        powerUpSpawn()
#===============================================================
    if character=="mario":
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

    for index in range(len(goombaPos())):
        if enemyList[index]==0:
            screen.blit(goomba[0][int(enemyFrames())],goombaPos()[index])

    
    screen.blit(smallcoin[0][int(coinFrames())],(200,10))

    x = 10
    for i in range(health):
        screen.blit(heart_pic,(x+i,10))
        x+= 20

    hud()
    
    display.flip()
#================================================================================
def Coins():
    global points,offset,playerRect
    
    coinRect=[[641,223,0],[2295,225,1],[2640,107,2],[2933,225,3],[3511,107,4],[3976,224,5],[4743,286,6],[4965,226,7]]
    for i in coinRect:
        i[0]+=offset
        if coinDraw[coinRect.index(i)]==0:
            screen.blit(coin[0][int(coinFrames())],i[:2])

    for i in coinRect:
        if playerRect.colliderect(i[:2]+[24,35]):
            takenCoin=i[-1]
            if coinDraw[coinRect.index(i)]==0:
                mixer.Channel(3).play(mixer.Sound("sound/coin.ogg"))
                points += 15
            coinDraw[takenCoin]=1

def randomCoins():

    randCoinX,randCoinY=randint(300,500),randint(0,300)
    if getPixel(maskPic,randCoinX,randCoinY)!=WHITE and getPixel(maskPic,randCoinX+24,randCoinY+35)!=WHITE and getPixel(maskPic,randCoinX+24,randCoinY)!=WHITE and getPixel(maskPic,randCoinX,randCoinY+35)!=WHITE:
        if getPixel(maskPic,randCoinX,randCoinY)!=YELLOW and getPixel(maskPic,randCoinX+24,randCoinY+35)!=WHITE and getPixel(maskPic,randCoinX+24,randCoinY)!=WHITE and getPixel(maskPic,randCoinX,randCoinY+35)!=WHITE:
            return [randCoinX,randCoinY,i+8]
        else:
            returnList.append([420+i*10,340,i+8])
    else:
        returnList.append([420+i*20,340,i+8])


def coinFrames():
    global coinFrame
    
    coinFrame+=0.03
    if coinFrame>=5:
        coinFrame=0    
    return coinFrame

def coinBlockFrames():
    global coinBlockSpriteFrame
    
    coinBlockSpriteFrame+=0.1
    if coinBlockSpriteFrame>=5:
        coinBlockSpriteFrame=0
    return coinBlockSpriteFrame

def coinBlockImage():
    global coinBlockTime,coinBlockSpriteFrame
    
    coinBlockX=player[0]+17+offset
    coinBlockY=player[1]-100
    screen.blit(coinBlockSprite[0][int(coinBlockFrames())],(coinBlockX,coinBlockY-coinBlockTime*1.5))

def coinBlock():
    global points
    
    mixer.Channel(3).play(mixer.Sound("sound/coin.ogg"))
    points+=15

#=====================================================================
def powerUpSpawn():
    global powerUpX,powerUpY,powerUpMovement,playerRect,RNG_powerUp
    
    if getPixel(maskPic,powerUpX+21,powerUpY+43) not in MASK:
        powerUpY+=5
    if getPixel(maskPic,powerUpX+43,powerUpY) in MASK:
        powerUpMovement=1
    elif getPixel(maskPic,powerUpX,powerUpY) in MASK:
        powerUpMovement=0

    if powerUpMovement==0:
        powerUpX+=1
        if RNG_powerUp==5:
            screen.blit(propeller[0][int(powerUpFrames())],(powerUpX+offset,powerUpY))
        elif RNG_powerUp<5:
            screen.blit(powerUp_life_right,(powerUpX+offset,powerUpY))
    else:
        powerUpX-=1
        if RNG_powerUp==5:
            screen.blit(propeller[0][int(powerUpFrames())],(powerUpX+offset,powerUpY))
        elif RNG_powerUp<5:
            screen.blit(powerUp_life_left,(powerUpX+offset,powerUpY))

    powerUpRect=Rect(powerUpX+offset,powerUpY,43,43)

    if powerUpRect.colliderect(playerRect):
        powerUpPickUp()

def powerUpFrames():
    global powerUpFrame
    
    powerUpFrame+=0.03
    if powerUpFrame>=4:
        powerUpFrame=0
    return powerUpFrame

def powerUpPickUp():
    global powerUpX,powerUpY,powerUps,RNG_powerUp,health,powerUpped,points
    
    del powerUpX
    del powerUpY
    powerUps=0
    if RNG_powerUp<5:
        points+=30
        if health!=5:
            health+=1
            mixer.Channel(5).play(mixer.Sound("sound/1up.ogg"))
    elif RNG_powerUp==5:
        points+=50
        powerUpped=True
            
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

goomba=[]
goomba.append(sprite("goomba",1,3))

coin=[]
coin.append(sprite("coin",1,5))

coinBlockSprite=[]
coinBlockSprite.append(sprite("coinBlock",1,5))

smallcoin = []
smallcoin.append(sprite_resize("coin",1,5))

propeller=[]
propeller.append(sprite("propeller",1,4))
#=====================================================================player sprite variables
playerFrame=0
move=0
hitBlock=False

#=====================================================================coins
coinFrame=0
coinBlockSpriteFrame=0
coinDraw = [0,0,0,0,0,0,0,0]
coinBlockDraw=False
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
#=====================================================================
powerUps=0
powerUpEntity=[]
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
running = True
myClock = time.Clock()

while running:
    keys=key.get_pressed()
    for evt in event.get():  
        if evt.type == QUIT: 
            running = False
        if evt.type == KEYDOWN:
            if keys[112]:
                pause()

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    keys=key.get_pressed()
    offset=findOffset(player)
    px,py=player[0]+offset,player[1]
    playerRect=Rect(px,py,30,35)

    if keys[K_ESCAPE]:
        running = False
    if mb[0]==1:
        print(mouse.get_pos()[0]-offset,mouse.get_pos()[1])
    
    drawScene(screen, player)
        
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
    fallDeath(player)

    #hud(frame_rate)
    playerCollision()
    
    myClock.tick(frame_rate)
    display.flip() 
quit() 

