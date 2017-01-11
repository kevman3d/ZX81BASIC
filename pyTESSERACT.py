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
# GAME:			TESSERACT, page 25
# DESCRIPTION:	Simple pattern generator creates an endless series of
#				symmetrical patterns.
#
# From the book "34 Amazing games for the 1K ZX81"
# Original book and game design (C) 1982, Alastair Gourlay, Mark Ramshaw and
# Interface publishing.
#
# ----------------------------------------------------------------------------
from ZXBasic import ZXBasic
from random import randint
import pygame.time

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
def tesseract():

	# The BASIC code uses RUN to go back to the first line, rather then GOTO
	# therefore we simply need to use a while loop in here
	while True:
		P = 20
		X = int(zx.RND() * P)
		Y = int(zx.RND() * P)
		# Draw pattern
		zx.PLOT(P+X,P+Y)
		zx.PLOT(P+Y,P+X)
		zx.PLOT(P-X,P+Y)
		zx.PLOT(P+Y,P-X)
		zx.PLOT(P-X,P-Y)
		zx.PLOT(P-Y,P-X)
		zx.PLOT(P+X,P-Y)
		zx.PLOT(P-Y,P+X)
		# Update the screen
		zx.screenRefresh()
		fpsClock.tick(6)

		#Randomly clear the screen
		if zx.RND() < 0.02:
			zx.CLS()
			
		# NOTES : The last line just re-runs the code - it made lines 110-130
		# seem redundant in the original software listing (for those who have
		# access to this book...)
	
# GAME LOOP
while True:
	tesseract()