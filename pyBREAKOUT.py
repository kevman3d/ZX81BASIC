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
# GAME:			BREAKOUT, page 8,9
# DESCRIPTION:	Use M and N to keep the ball in play long enough to smash the
#				Wall...
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
def breakout():

	# Define the variables
	C = 6
	E = 1
	B = 5
	F,D = 1,1
	
	# Draw the screen
	for x in range(6):
		zx.PRINT_AT(x,0,'|i             ')
	for x in range(5):
		zx.PRINT_AT(5 + x, 0,'|i ')
		zx.PRINT_AT(5 + x, 12,'|i ')

	zx.screenRefresh()

	# Game loop
	while True:
		
		zx.PRINT_AT(11,B,'|t  ')
		
		B = B + (zx.INKEY('m') - zx.INKEY('n'))
		
		if B < 1:
			B = 1
		elif B > 10:
			B = 10
	
		zx.PRINT_AT(11,B,'|gss')
		zx.PRINT_AT(int(C),int(D),'|t ')
		
		# Is the game over?  Note that there is a problem with the original
		# game in that only half the paddle is detected. Have added a B + 1
		# check as well to compensate
		if (C == 0 or C == 10) and (B != D and D != B+1):
			return
		
		C = C + E
		D = D + F
		
		if D < (abs(E) + abs(F)) or D > 11-abs(F):
			F = -F
			
		if C == 10:
			E = -E
			F = zx.SGN(F) * (int(zx.RND() + zx.RND()) + abs(E))
		else:
			# Check for impact
			if zx.peekCharacter('i ',int(D),int(C)):
				E = abs(E)
		
		zx.PRINT_AT(int(C),int(D),'|t.')
		
		zx.screenRefresh()
		fpsClock.tick(4)
		
# GAME LOOP
while True:
	breakout()
	
	# Print the score
	zx.PRINT_AT(14,0,"|tGAME OVER")
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