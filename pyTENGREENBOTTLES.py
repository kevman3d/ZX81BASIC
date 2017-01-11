# ----------------------------------------------------------------------------
# "34 Amazing Games in Python from the 1K ZX81 Era"
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
# GAME:			TEN GREEN BOTTLES, page 43
# DESCRIPTION:	Try to shoot down the bottles at the top of the screen in the
#				shortest amount of time. Press "1" to fire when lined up
#
# From the book "34 Amazing games for the 1K ZX81"
# Original book and game design (C) 1982, Alastair Gourlay, Mark Ramshaw and
# Interface publishing.
#
# ----------------------------------------------------------------------------
from ZXBasic import ZXBasic
from random import randint
import pygame.time
from pygame.locals import *
import time

# Note that all pygame functionality is managed in class.  We do however need
# to import the pygame.time module here to control the speed of the game
fpsClock = pygame.time.Clock()
	
zx = ZXBasic()
zx.createScreen()
zx.CLS()

# Define game as a function
# We will use functions for all games, as some of the games have
# options to restart.  This makes more sense if called from a games loop
# in the main program.
def tenGreenBottles():

	# Define the variables
	P,H,T = 0,0,0
	E = 1
	# DIM A$ - called AS in Python
	AS = ['0','0','0','0','0','0','0','0','0','0']
	
	# Print the 10 bottles.  In BASIC we use the ; to make text print side by side
	# however in this example, I'll use a PRINT_AT
	for x in range(0,10):
		zx.PRINT_AT(0,x*3,"|gqw|t ")
	zx.PRINT_AT(2,0,"|gssssssssssssssssssssssssssssss")
	
	# Game loop goes here
	while H < 10:
	
		# keyP flag = signifies that a key was pressed
		keyP = False
		
		# Erase player 
		zx.PRINT_AT(20,int(P),"|t  ")
		# Move the player
		P = P + E
		# If the player has exceeded screen bounds, reverse it
		if P == 0 or P == 28:
			E = -E
		# Print the player
		zx.PRINT_AT(20,int(P),"|gty")
		# Update the screen
		zx.screenRefresh()
		
		# Check for a keypress,  We need to make sure that the player is
		# below a bottle as well. 
		if zx.INKEY('1'):
			keyP = True
			
			if P == float((P/3) * 3):
				# Increase the hits if the bottle is not hit
				if AS[P/3] == '0':
					zx.PRINT_AT(0,P,"|t//")
					AS[int(P/3)] = '1'
					H = H + 1

		# Hold the game until the keyboard is not pressed
		while keyP:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == KEYUP:
					keyP = False

		fpsClock.tick(4)
		T = T + 1
	# On game finish, return the Time taken
	return T
	
# GAME LOOP
while True:
	timeTaken = tenGreenBottles()
	
	# Print the score
	zx.PRINT_AT(5,0,"|tTIME:%d" % timeTaken)
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