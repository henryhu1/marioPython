from pygame import *

size=(800,600)
screen = display.set_mode(size) 
screen.fill((255,255,255))

testRect=Rect(100,200,50,100)
draw.rect(screen,(0,0,0),testRect)

running = True
while running:
    for evt in event.get():  
        if evt.type == QUIT: 
            running = False

    print(testRect.top)
    
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    
    display.flip() 
quit() 
