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
# GAME:			UFO, page 8
# DESCRIPTION:	Use 0 and 8 to move your laser beneath the descending UFO
#				You score when you hit it by pressing 1. Game over when it lands
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
def ufo():
	# define variables.  P is player position, L is length of river
	P = 1
	Q = 7
	S = 0
	X = 1
	
	zx.PRINT_AT(0,0,"|i               ")
	for x in range(1,15):
		zx.PRINT_AT(x,0,"|i |t             |i ")

	# Refresh the screen
	zx.screenRefresh()

	while True:

		# wipe the player and UFO
		zx.PRINT_AT(int(P),int(Q),'|t ')
		zx.PRINT_AT(16,X,'|t ')
		
		# Work out the movement of our barrel by checking the keys
		X = X + (zx.INKEY('0') - zx.INKEY('8'))
		
		# Move the alien
		P = P + zx.RND() / 3
		Q = Q + 2 * zx.RND() - 1
		
		# if the UFO has landed, we exit
		if P > 15:
			return True

		# Check for bounds
		if Q < 1 or Q > 13:
			Q = 7
		if X < 1 or X > 13:
			X = 1
			
		# Print our game graphics
		zx.PRINT_AT(int(P),int(Q),'|tX')
		zx.PRINT_AT(16,X,'|g7')
		
		# Check if we fired and hit
		if zx.INKEY('1') and X == int(Q + 0.5):
			S = S + 10
			zx.PRINT_AT(int(P),int(Q),'|iX')
			zx.PRINT_AT(0,5,'|t%s' % S)
		
		# Refresh the screen and loop
		zx.screenRefresh()
		fpsClock.tick(4)
	
	
while True:
	ufo()
	
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