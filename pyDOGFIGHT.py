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
# GAME:			DOGFIGHT, page 5
# DESCRIPTION:	Press F to fire at the right moment to destroy the enemy ships
#				but avoid hitting your own.
#				GREY
#				Grey square is a friendly ship.  Loses 1 point
#				BLACK
#				Black square. Empty space - earn 1 point
#				INVERSE +
#				An inverse + is an alien ship. Hit for 20 points, miss ends game
#				INVERSE *
#				An inverse * is an asteroid. Hit for 10 points, miss ends game
#
# From the book "34 Amazing games for the 1K ZX81"
# Original book and game design (C) 1982, Alastair Gourlay, Mark Ramshaw and
# Interface publishing.
#
# ----------------------------------------------------------------------------
from ZXBasic import ZXBasic
import pygame.time
from pygame.locals import *
import sys

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
def dogfight():

	# Define the variables
	S, T = 0,0
	
	# Collection of possible targets.  Unlike others, I've not tried
	# to enforce a close 'copy' of the basic program structure
	AS = ['i ','ga','i*','i+']
	
	zx.PRINT('|ge77777r')
	zx.PRINT('|g5|t  -  |g8')
	zx.PRINT('|g5|t-----|g8')
	zx.PRINT('|g5|t  -  |g8')
	zx.PRINT('|gw66666q')
	zx.screenRefresh()
	
	while True:
	
		R = int(zx.RND() * 4)
		T = T + 1
		if T == 50:
			return (T,S)
	
		# Print the target
		zx.PRINT_AT(0,20,AS[R])
		zx.screenRefresh()
	
		# Delay while we wait on a key to be pressed (or time to run out)
		# We can increase this value to make the game easier (slower).
		ticker = 5
		f_pressed = False
		while ticker > 0:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					
					if event.key == K_f:
						f_pressed = True
					
					ticker = 0
					
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

			ticker -= 1
			fpsClock.tick(4)

		# See if we hit anything
		if R == 0:		# Empty Space
			S += 1
		if R > 1:		# Asteroid or Alien?
			if f_pressed:
				if R == 2:
					S += 10
				else:
					S += 20
			else:
				return (T,S)
		# Note that the program was buggy and missed this detail
		if R == 1:		# Hit friendly ship?
			if f_pressed:
				S -= 5
			
	zx.screenRefresh()
	fpsClock.tick(4)
		
# GAME LOOP
while True:
	result = dogfight()
	
	# Unlike previous games, dogfight returns a small tuple with time,score
	
	# Print the end
	if result[0] >= 50:
		zx.PRINT_AT(14,0,"|iTIME UP")
	
	zx.PRINT_AT(16,0,"|iGAME OVER")
	zx.PRINT_AT(18,0,"|iYOU SCORE %d" % result[1])
	
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