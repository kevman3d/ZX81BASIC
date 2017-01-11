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
# GAME:			MOTORBIKE, page 13
# DESCRIPTION:	Use Z and M to drive your bike along the track
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
def motorbike():
	# define variables.
	A,B = 10,10
	Z = 1
	T = 2
	C = 15
	Q = 25
	M = 8
	K = 136
	W = 10
	S = -9
		
	while True:

		M = M + T * zx.RND() - T * zx.RND()
		zx.PRINT_AT(19,int(M),'|gh|t   |gh')
		zx.PRINT_AT(9,W,'|t ')
		zx.PRINT_AT(A,B,'|iH')

		zx.screenRefresh()
		
		W = B
		B = B - (zx.INKEY('z') and B>T) + (zx.INKEY('m') and B<Q)
		
		if M < T:
			M = T
		if M > Q:
			M = Q
			
		S = S + Z
	
		# Scroll the screen up
		zx.SCROLL()
		zx.screenRefresh()
		
		# Check to see if we've hit a rock (inverted space)
		# and if so, we exit the game back to the main loop
		if zx.peekCharacter('gh',B,A):
			return S
		
		fpsClock.tick(4)
	
	
while True:
	score = motorbike()
	
	# Print the score
	zx.PRINT_AT(5,0,"|t%d" % score)
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