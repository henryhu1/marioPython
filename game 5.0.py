#FSE - Platformer
from pygame import *
from random import *
size=(800,435)
screen = display.set_mode(size)
#=====================================================================music
mixer.init()

#sound_flag = False
#if sound_flag:
game_sound = mixer.Sound('sound/level_1.wav')
mixer.Channel(6).play(game_sound)

#=====================================================================pictures and transforming
back = image.load("images/LEVEL_1-1.png")
maskPic = image.load("images/LEVEL_1-1_mask.png")
##back = transform.scale(back,(3072,800))\
heart_pic = image.load("images/heart.png")
heart_pic = transform.scale(heart_pic,(15,15))
#=====================================================================colours
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,201,14)
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
    keys = key.get_pressed()
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
        if getPixel(maskPic,guy[X]+15,guy[Y]-5) == WHITE:
            guy[VY] = 1
        if getPixel(maskPic,guy[X]+15,guy[Y]-5) == YELLOW:
            guy[VY] = 1
                    
def moveDown(guy,vy):
    for i in range(vy):
        if getPixel(maskPic,guy[X]+5,guy[Y]+35) == WHITE or getPixel(maskPic,guy[X]+25,guy[Y]+35) == WHITE:
            guy[ONGROUND]=True
            guy[VY]=0
        if getPixel(maskPic,guy[X]+15,guy[Y]+35) == YELLOW:
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
def coinFrames():
    global coinFrame
    coinFrame+=0.03
    if coinFrame>=5:
        coinFrame=0    
    return coinFrame


def hud():
    global timer_flag
    font.init()
    smallFont = font.SysFont("Comic Sans MS", 15)
    global comicFont
#=================================================timer    

    minutes = time.get_ticks()//1000//60
    seconds = time.get_ticks()//1000
    #if seconds>=60:
        #seconds = 0
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
#======================================================================

    settings_icon = image.load("images/settings2.png")

    settings_icon = transform.smoothscale(settings_icon,(37,47))
    screen.blit(settings_icon,(760,0))


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
    global flag, poleflag,running,timer_flag
    flagrect = Rect(5645,72,10,277)
    #draw.rect(screen,(255,0,0),flagrect,10)
    if guy[X]>5731: 
        timer_flag = False   
        flag = False
        guy[X] = 5753
        if poleflag:
            if guy[Y] <= 70:
                guy[VY] = 0
                poleflag = False
            else:
    
                guy[VY] = -1

#=====================================================================
def playerCollision():
    global enemyPos0,enemyPos1,enemyPos2,coinList,health,points
    keys = key.get_pressed()
    
    offset=findOffset(player)
    px,py=player[0]+offset,player[1]
    
    playerRect=Rect(px,py,30,35)
    playerTopRect=Rect(playerRect.left-8,playerRect.top,46,10)
    playerBottomRect=Rect(playerRect.left,playerRect.bottom,30,-10)
    playerRightRect=Rect(playerRect.right,playerRect.top+10,8,25)
    playerLeftRect=Rect(playerRect.left,playerRect.top+10,-8,25)
    
##    draw.rect(screen,(0,255,0),playerTopRect,1)
    ##draw.rect(screen,(0,255,0),playerBottomRect,1)
##    draw.rect(screen,(0,255,0),playerRightRect,1)
##    draw.rect(screen,(0,255,0),playerLeftRect,1)
    
    for i in goombaPos():
        goombaRect=Rect(i+(35,35))
        goombaTopRect=Rect(goombaRect.left,goombaRect.top,35,10)
        goombaRightRect=Rect(goombaRect.right,goombaRect.top,8,35)
        goombaLeftRect=Rect(goombaRect.left,goombaRect.top,-8,35)

##        draw.line(screen,(0,0,255),(enemyPos0,343),(enemyPos1,343),3)
##        draw.line(screen,(244,241,66),(enemyPos1,343),(enemyPos2,343),3)
##        draw.line(screen,(125,0,125),(enemyPos0,0),(enemyPos0,400),3)
##        draw.line(screen,(125,0,125),(enemyPos1,0),(enemyPos1,400),3)
##        draw.line(screen,(125,0,125),(enemyPos2,0),(enemyPos2,400),3)
        
##        draw.rect(screen,(255,0,0),goombaTopRect,1)
##        draw.rect(screen,(255,0,0),goombaRightRect,1)
##        draw.rect(screen,(255,0,0),goombaLeftRect,1)
        
        if playerBottomRect.colliderect(goombaTopRect):
            player[ONGROUND]=False
            if keys[K_SPACE]:
                player[VY]=-13
                points += 30
            else:
                player[VY]=-10
                points+=30
                
            mixer.Channel(2).play(mixer.Sound("sound/stomp.ogg"))
            
            if enemyPos0>player[0] or enemyPos0<=player[0]<=enemyPos1:
                enemyList[0]=1
            elif enemyPos1<=player[0]<=enemyPos2:
                enemyList[1]=1
            elif enemyPos2<=player[0]:
                enemyList[2]=1
                
        if playerRightRect.colliderect(goombaLeftRect):
            player[0]-=40
            player[4]-=40
            health-=1
            points-= 25
        elif playerLeftRect.colliderect(goombaRightRect):
            player[0]+=40
            player[4]+=40
            health -=1
            points-=25
            
    
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

#=====================================================================blitting everything (background,sprites)
def drawScene(picture,guy):
    global enemyList,coinList,character
    offset = findOffset(player)
    screen.blit(back, (offset,0))
    playerRect=Rect(guy[0]+offset,guy[1],30,35)
    characterSwapRect=Rect(1955+offset,45,60,60)
#===============================================================
    Coins()
#===============================================================

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

    
    screen.blit(smallcoin[0][int(coinFrames())],(200,10))

    x = 10
    for i in range(health):
        screen.blit(heart_pic,(x+i,10))
        x+= 20

    hud()
    
    display.flip()
#================================================================================
def Coins():
    global points
    coinRect=[[641,223,0],[2295,225,1],[2640,107,2],[2933,225,3],[3511,107,4],[3976,224,5],[4743,286,6],[4965,226,7]]
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
                points += 15
            coinDraw[takenCoin]=1

def main_game():
    global sound_flag
    setting_rect = Rect(760,0,37,47)
    running = True
    myClock = time.Clock()
    while running:
        #sound_flag = True
        keys=key.get_pressed()
        for evt in event.get():  
            if evt.type == QUIT: 
                running = False
            if evt.type == KEYDOWN:
                if evt.key == 112:
                    pause()





        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        keys=key.get_pressed()

        if mb[0] == 1 and setting_rect.collidepoint(mx,my):
            pause()

    
##        print(sound_flag)


        if keys[K_ESCAPE]:
            running = False
        if mb[0]==1:
            offset=findOffset(player)
            print(mouse.get_pos()[0]-offset,mouse.get_pos()[1])
    ##    print(enemyList)
        moveGuy(player)
        flagpole(player)

            
        fallDeath(player)
        drawScene(screen, player)
        #hud(frame_rate)
        playerCollision()
        
        myClock.tick(240)
        display.flip()
    player[0] = 250
    player[1] = 343
    player[2]=0
    player[3]=True
    player[4]=250
    #for i in coi
    #sound_flag = False  
    return "main_menu"


def main_menu():
    global sound_flag
    running = True
    myClock = time.Clock()
    buttons = [Rect(600,y*70+120,150,40) for y in range(4)]
    
    text_pos = [(620,y*70+120) for y in range(4)]

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
                if mb[0]==1:
                    return v
            else:
                draw.rect(screen,(255,255,0),r,2)

        for i in range(4):
            textrender = bigFont.render(labels[i],True,WHITE)
            screen.blit(textrender,(text_pos[i]))
                
        display.flip()
            
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

smallcoin = []
smallcoin.append(sprite_resize("coin",1,5))
#=====================================================================player sprite variables
playerFrame=0
move=0
character = "mario"
#====================================================================timer
timer_flag = True

#=====================================================================coins
coinFrame=0

coinDraw = [0,0,0,0,0,0,0,0]

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

page = "main_menu"
while page != "exit":
    if page == "main_menu":
        page = main_menu()
    if page == "main_game":
        page = main_game()
        sound_flag = True    
    if page == "instructions":
        page = instructions()    
    if page == "story":
        page = story()    
    if page == "credits":
        page = credit()     
quit() 

