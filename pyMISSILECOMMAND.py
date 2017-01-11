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
# GAME:			MISSILE COMMAND, page 21
# DESCRIPTION:	Prevent the missile from destroying the city using the D,A,W,X
#				keys to move your cursor in its path
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

# Experiment in retro-ising the screen refresh.  Everything in pygame is double-
# buffered, which keeps things clean and smooth.  The TV set on the other hand was
# not, making graphics blink more.  By calling the refresh and pause after drawing
# and erasing each time, we get a more '80's vibe.  Note that due to being called
# more then once in a game loop, the fps tick has been made faster.
def tvUpdate():
	zx.screenRefresh()
	fpsClock.tick(6)

# Define game as a function
# We will use functions for all games, as some of the games have
# options to restart.  This makes more sense if called from a games loop
# in the main program.
def missileCommand():

	# Define the variables
	S = 0

	# New missile loop goes here
	while True:
	
		Y,X,F = 4,4,43
		B = int(zx.RND() * 14 + 1)
	
		# Print city
		zx.PRINT_AT(12,B,"|gq4")
		
		C = int(zx.RND() * 25)
		zx.PRINT_AT(13,0,"|gsssssssssssssssss")
		
		# Refresh the screen
		tvUpdate()
		
		# Game play loop
		while not (F == 18 or (X*2 == C and 43-Y*2 == F)):

			zx.PRINT_AT(Y,X,"|t ")

			tvUpdate()
			
			X = X + (zx.INKEY('d')) - (zx.INKEY('a'))
			Y = Y + (zx.INKEY('x')) - (zx.INKEY('w'))
			
			zx.PRINT_AT(Y,X,"|t+")
			
			F -= 1
			C = C + (C < B * 2) - (C > B*2)
			
			zx.PLOT(C,F)
			
			tvUpdate()
			
		# Missile game loop should jump out at this stage
		
		# If the missile hit the ground, blow it up and exit the game
		if F == 18:
			zx.PRINT_AT(11,B-2,"|gyytt")
			zx.PRINT_AT(12,B-1,"|gy|t |gt")
			zx.PRINT_AT(13,B,"|g7")
			tvUpdate()
			return S
		else:
			# increase the score, pause and then start a new missile
			S = S + 1
			zx.PRINT_AT(Y,X,"|t%d" % S)
			zx.screenRefresh()
			for paused in range(10):
				fpsClock.tick(4)
			zx.CLS()

	
# GAME LOOP
while True:
	score = missileCommand()
	
	# Print the score
	zx.PRINT_AT(14,0,"|tSCORE:%d" % score)
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