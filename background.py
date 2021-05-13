from pygame import*
from random import*


background_x = 0
box_x = 0

  		
def box(box,screen):
	keys = key.get_pressed()
	if keys[K_LEFT] and background_x != 0 :
		if box == 150:
			box == 150
		box += 10

	if keys[K_RIGHT]:
		if box == 150:
			box == 150
		box += 10


	draw.rect(screen,(255,0,0),(150,100,30,30))


def movebackground(x):
	keys = key.get_pressed()

	if keys[K_LEFT] and background_x != 0 :
		x += 10
	if keys[K_RIGHT] and background_x <= 30:
		x -= 10
	return x
	

def background_blit(screen,image,x,grasspic):
	screen.blit(image,(x,0))
	draw.rect(screen,(121,178,51),(0,240,3584,240))
	
	for i in range(10,3000,20):
		screen.blit(grasspic,(i,250))

'''def grass(grasspic):
	grass_surface = Surface((3984,200),SRCALPHA)
	for i in range(10,3000,20):
		screen.blit(grasspic,(i,250))

	#screen.blit(grass_surface,(0,0))'''

	
#-------------------------------------------------------------------

screen = display.set_mode((800,300))

running = True
level = image.load("images/LEVEL_1-1.png")
draw.rect(screen,(121,178,51),(0,200,3984,400))
#level = transform.scale(level,(3584,300))

myclock = time.Clock()

#grass()
#grasspic = image.load("images/grass.png")
#screen.blit(grasspic,(10,50))
w = 0



while running:

	for e in event.get():
		if e.type == QUIT:
			running = False
		keys = key.get_pressed()

		if keys[K_RIGHT]:
			w += 10
			print(w)



	grasspic = image.load("images/grass.png")	
	background_x = movebackground(background_x)
	background_blit(screen,level,background_x,grasspic)
	box(box_x,screen)
	#grass(grasspic)



	

	

	myclock.tick(60)
	display.flip()

quit()
