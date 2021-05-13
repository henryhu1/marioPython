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

guyPic = image.load("guy.png")
##back = transform.scale(back,(3072,800))

#=====================================================================colours
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,201,14)

#=====================================================================list indices and what they are
X=0
Y=1
VY=2
ONGROUND=3
SCREENX = 4

#=====================================================================entity lists
player=[250,343,0,True,250]
#=====================================================================functions
#=====================================================================
def moveRight(guy,vx):
    for i in range(vx):
        if getPixel(maskPic,guy[X]+30,guy[Y]+20) != WHITE and getPixel(maskPic,guy[X]+30,guy[Y]+10) != WHITE:
            if getPixel(maskPic,guy[X]+30,guy[Y]+20) != YELLOW and getPixel(maskPic,guy[X]+30,guy[Y]+10) != YELLOW:            
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
        if getPixel(maskPic,guy[X],guy[Y]+20) != WHITE and getPixel(maskPic,guy[X],guy[Y]+10) != WHITE:
            if getPixel(maskPic,guy[X],guy[Y]+20) != YELLOW and getPixel(maskPic,guy[X],guy[Y]+10) != YELLOW:
                if keys[K_LSHIFT]:
                    guy[X] -= 0.5
                    if guy[SCREENX] > 400:
                        guy[SCREENX] -= 0.5
                else:
                    guy[X] -= 0.25
                    if guy[SCREENX] > 400:
                        guy[SCREENX] -= 0.25

def moveUp(guy,vy):
    for i in range(vy):
        if getPixel(maskPic,guy[X]+7,guy[Y]-5) == WHITE or getPixel(maskPic,guy[X]+17,guy[Y]-5) == WHITE or getPixel(maskPic,guy[X]+28,guy[Y]-5) == WHITE:
            guy[VY] = 1
        if getPixel(maskPic,guy[X]+7,guy[Y]-5) == YELLOW or getPixel(maskPic,guy[X]+17,guy[Y]-5) == YELLOW or getPixel(maskPic,guy[X]+28,guy[Y]-5) == YELLOW:
            guy[VY] = 1
                    
def moveDown(guy,vy):
    for i in range(vy):
        if getPixel(maskPic,guy[X]+7,guy[Y]+35) == WHITE or getPixel(maskPic,guy[X]+17,guy[Y]+35) == WHITE or getPixel(maskPic,guy[X]+28,guy[Y]+35) == WHITE:
            guy[ONGROUND]=True
            guy[VY]=0
        if getPixel(maskPic,guy[X]+7,guy[Y]+35) == YELLOW or getPixel(maskPic,guy[X]+17,guy[Y]+35) == YELLOW or getPixel(maskPic,guy[X]+28,guy[Y]+35) == YELLOW:
            guy[ONGROUND]=True
            guy[VY]=0
#=====================================================================player movement
def moveGuy(guy):
    'moves the player and animations'
    global move,playerFrame,direction
    
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
    if keys[K_SPACE] and guy[ONGROUND]:
        guy[VY] = -13
        guy[ONGROUND]=False
        mixer.Channel(1).play(mixer.Sound("sound/jump.ogg"))

    guy[Y]+=guy[VY]     # add current speed to Y
    
    if guy[Y] >= 800: #player on the ground
        guy[Y] = 800
        guy[VY] = 0
        guy[ONGROUND]=True

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
    global goombaPos0,goombaPos1,goombaPos2,enemyList
    if guy[Y]>700:
        guy[0]=250
        guy[1]=343
        guy[2]=0
        guy[3]=True
        guy[4]=250
        
#=====================================================================
def findOffset(guy):
    if guy[SCREENX] - guy[X] <= 0:
        return guy[SCREENX] - guy[X]
    else:
        return (0)

#=====================================================================
def coinFrames():
    global coinFrame
    coinFrame+=0.03
    if coinFrame>=5:
        coinFrame=0    
    return coinFrame

#=====================================================================

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
            if getPixel(maskPic,goomba,353)!= WHITE:
                goomba-=0.3
            else:
                movementList[number]=1
        else:
            if getPixel(maskPic,goomba+35,353)!= WHITE:
                goomba+=0.3
            else:
                movementList[number]=0
    else:
        goomba=-10

    return goomba

#=====================================================================
def goombaPos():
    global enemyPos0,enemyPos1,enemyPos2,enemyPos3,enemyPos4

    enemyPos=[]

    enemyPos0=goombaCheck(enemyPos0,0)
    enemyPos1=goombaCheck(enemyPos1,1)
    enemyPos2=goombaCheck(enemyPos2,2)
    enemyPos3=goombaCheck(enemyPos3,3)
    enemyPos4=goombaCheck(enemyPos4,4)
        
    offset=findOffset(player)
    enemyPos.append((enemyPos0+offset,343))
    enemyPos.append((enemyPos1+offset,343))
    enemyPos.append((enemyPos2+offset,343))
    enemyPos.append((enemyPos3+offset,343))
    enemyPos.append((enemyPos4+offset,343))
    
    return enemyPos
    
#=====================================================================
def sprite(name,start,end):
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move

#=====================================================================
def playerCollision():
    global enemyPos0,enemyPos1,enemyPos2,enemyPos3,enemyPos4
    
    offset=findOffset(player)
    px,py=player[0]+offset,player[1]
    
    playerRect=Rect(px,py,30,35)
    playerTopRect=Rect(playerRect.left-8,playerRect.top,46,10)
    playerBottomRect=Rect(playerRect.left,playerRect.bottom,30,-10)
    playerRightRect=Rect(playerRect.right,playerRect.top+10,8,25)
    playerLeftRect=Rect(playerRect.left,playerRect.top+10,-8,25)
    
##    draw.rect(screen,(0,255,0),playerTopRect,1)
##    draw.rect(screen,(0,255,0),playerBottomRect,1)
##    draw.rect(screen,(0,255,0),playerRightRect,1)
##    draw.rect(screen,(0,255,0),playerLeftRect,1)
    
    for i in goombaPos():
        goombaRect=Rect(i+(35,35))
        goombaTopRect=Rect(goombaRect.left,goombaRect.top,35,10)
        goombaRightRect=Rect(goombaRect.right,goombaRect.top,8,35)
        goombaLeftRect=Rect(goombaRect.left,goombaRect.top,-8,35)
        
##        draw.rect(screen,(255,0,0),goombaTopRect,1)
##        draw.rect(screen,(255,0,0),goombaRightRect,1)
##        draw.rect(screen,(255,0,0),goombaLeftRect,1)
        
        if playerBottomRect.colliderect(goombaTopRect):
            player[ONGROUND]=False
            if keys[K_SPACE]:
                player[VY]=-13
            else:
                player[VY]=-10
                
            mixer.Channel(2).play(mixer.Sound("sound/stomp.ogg"))
            
            if player[0]<1200:
                enemyList[0]=1
            elif 1200<=player[0]<=1680:
                enemyList[1]=1
            elif 1700<=player[0]<=3960:
                enemyList[2]=1
            elif 3970<=player[0]<=4070:
                enemyList[3]=1
            elif 4500<=player[0]<=4735:
                enemyList[4]=1
                
        if playerRightRect.colliderect(goombaLeftRect):
            player[0]-=40
            player[4]-=40
        elif playerLeftRect.colliderect(goombaRightRect):
            player[0]+=40
            player[4]+=40



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
##        print(mask.get_at((int(x),int(y)))[:3])
        return mask.get_at((int(x),int(y)))[:3]
   
    else:
        return (-1,-1,-1)
    
#=====================================================================blitting everything (background,sprites)
def drawScene(picture,guy):
    global enemyList,coinList,character
    offset = findOffset(player)
    playerRect=Rect(guy[0]+offset,guy[1],30,35)
    characterSwapRect=Rect(1955+offset,45,60,60)
    screen.blit(back, (offset,0))
#=====================================================================
    Coins()
#=====================================================================

    if character=="mario":
        pic = marioSprite[move][int(playerFrame)]
    else:
        pic = luigiSprite[move][int(playerFrame)]

    if playerRect.colliderect(characterSwapRect):
        guy[VY]=-10
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
    
##    screen.blit(pic,(player[0],player[1]))            
##    screen.blit(guyPic, (guy[SCREENX],guy[Y]))
    
    display.flip()

def randomCoins(times):
    returnList=[]
    for i in range(times):
        randCoinX,randCoinY=randint(300,500),randint(0,300)
        if getPixel(maskPic,randCoinX,randCoinY)!=WHITE and getPixel(maskPic,randCoinX+24,randCoinY+35)!=WHITE and getPixel(maskPic,randCoinX+24,randCoinY)!=WHITE and getPixel(maskPic,randCoinX,randCoinY+35)!=WHITE:
            if getPixel(maskPic,randCoinX,randCoinY)!=YELLOW and getPixel(maskPic,randCoinX+24,randCoinY+35)!=WHITE and getPixel(maskPic,randCoinX+24,randCoinY)!=WHITE and getPixel(maskPic,randCoinX,randCoinY+35)!=WHITE:
                returnList.append([randCoinX,randCoinY,i+8])
            else:
                returnList.append([420+i*10,340,i+8])
        else:
            returnList.append([420+i*20,340,i+8])
    return returnList

coinSpawns=randomCoins(43)

def Coins():

    coinRect=[[641,223,0],[2295,225,1],[2640,107,2],[2933,225,3],
              [3511,107,4],[3976,224,5],[4743,286,6],[4965,226,7]]+coinSpawns
    
    for i in coinSpawns:
        coinRect.append(i)

    offset=findOffset(player)
    
    for i in coinRect:
        i[0]+=offset
        if coinDraw[coinRect.index(i)]==0:
            screen.blit(coin[0][int(coinFrames())],i[:2])

    px,py=player[0]+offset,player[1]
    playerRect=Rect(px,py,30,35)
    for i in coinRect:
        if playerRect.colliderect(i[:2]+[24,35]):
            takenCoin=i[-1]
            if coinDraw[coinRect.index(i)]==0:
                mixer.Channel(3).play(mixer.Sound("sound/coin.ogg"))
            coinDraw[takenCoin]=1
            

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
#=====================================================================player sprite variables
playerFrame=0
move=0

#=====================================================================coins
coinFrame=0

coinDraw=[0 for i in range(51)]

#=====================================================================movement identities
RIGHT=0
LEFT=1
JUMPR=2
JUMPL=3

direction="right"
character="mario"
#=====================================================================enemy things
enemyFrame=0
enemyPos0=1000
enemyPos1=1500
enemyPos2=2000
enemyPos3=4004
enemyPos4=4700
movementList=[0,0,0,0,0]
enemyList=[0,0,0,0,0]

#=====================================================================game loop
running = True
myClock = time.Clock()

while running:
    for evt in event.get():  
        if evt.type == QUIT: 
            running = False

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    keys=key.get_pressed()

    if keys[K_ESCAPE]:
        running = False
    if mb[0]==1:
        offset=findOffset(player)
        print(mouse.get_pos()[0]-offset,mouse.get_pos()[1])

##    print(player[0],player[1])
##    print(enemyList)
    moveGuy(player)
    
    fallDeath(player)
    drawScene(screen, player)
    playerCollision()
    myClock.tick(60)
    display.flip()
quit() 
