# ----------------------------------------------------------------------------
# "34 Amazing Games in Python from the 1K ZX81"
# Python Code redevelopment Kevin Phillips, 2015
#
# Recreation of classic ZX81 games using python and pygame
# ----------------------------------------------------------------------------
# Requires:
# ----------------------------------------------------------------------------
# Python 2.7	-	www.python.org
# pygame 1.91	-	www.pygame.org
# ZXBasic.py	-	ZX Basic class (import module)
# ZX81.ttf		-	ZX81 Font (http://www.dafont.com/zx81.font) - installed
# g1.png, etc	-	A collection of 20 .png files representing key graphics
# ----------------------------------------------------------------------------
#
# GAME:			NIAGARA, page 40
# DESCRIPTION:	Use 1 and 4 to guide your barrel through the rapids
#
# From the book "34 Amazing games for the 1K ZX81"
# Original book and game design (C) 1982, Alastair Gourlay, Mark Ramshaw and
# Interface publishing.
#
# ----------------------------------------------------------------------------
import ZXBasic
from random import randint
from pygame.locals import *
import pygame.time

# Note that all pygame functionality is managed in class.  We do however need
# to import the pygame.time module here to control the speed of the game
fpsClock = pygame.time.Clock()
	
zx = ZXBasic.ZXBasic()
zx.createScreen()
zx.CLS()


# Define game as a function
# We will use functions for all games, as some of the games have
# options to restart.  This makes more sense if called from a games loop
# in the main program.
def niagara():
	# define variables.  P is player position, L is length of river
	P = 10
	L = 40 + int(30*zx.RND())
	
	while True:

		# Refresh the screen
		zx.screenRefresh()
		
		# Scroll the screen up
		zx.SCROLL()

		# Work out the movement of our barrel by checking the keys
		P = P + (zx.INKEY('4') - zx.INKEY('1'))
		
		# Check for bounds
		if P > 19:
			P = 19
		if P < 0:
			P = 0
			
		# Check to see if we've hit a rock (inverted space)
		# and if so, we exit the game back to the main loop
		if zx.peekCharacter('i ',P,0):
			return "YOU HIT THE ROCKS"
			
		# Lets print our barrel
		zx.PRINT_AT(0,P,'|iO')
		
		# Decrease our length counter
		L = L - 1
		
		# Check to see if we've made it to the end of the river
		if L == -13:
			return "YOU REACHED THE FALLS"
		
		# We're close to the water falls, so start to draw them
		if L <= 0:
			zx.PRINT_AT(13,int(zx.RND() * 5), "|gttttttttttttttt")
			
		if L > 0:
			zx.PRINT_AT(13,int(zx.RND() * 15), "|i    ")
		
		fpsClock.tick(4)
	
	
while True:
	message = niagara()
	
	# Print the message
	zx.PRINT_AT(5,0,"|t%s" % message)
	# Refresh the display
	zx.screenRefresh()
	
	# When the game has completed, wait here until the space bar is pressed.
	# Because of the key press repeat, we may find that allowing any key (like the ZX81)
	# will instantly restart the game.  We need to also keep an eye on events here for
	# QUIT as well.
	
	# Lets just set a flag and use a while loop to keep the game paused
	replay = True
	
	while replay:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					replay = False
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
	
	zx.CLS()
	# The game will now return to the top of the while loop (ie start a new game)
	# Easily done