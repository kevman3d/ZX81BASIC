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
# GAME:			WUMPUS, page 10
# DESCRIPTION:	You are looking for the WUMPUS in a 5 x 8 system of caves.
#				Beware there are also giant bats, and a bottomless pit. When
#				you are near the Wumpus, you can shoot arrows.  Your aim is to
#				kill the Wumpus.  After each move, the computer will tell you
#				which cave you are in, and may also mention:
#				"SNIFF SNIFF"
#				You are near the Wumpus.  Move onto the Wumpus' square and die
#				Shoot your arrows ahead before moving
#				"DRAUGHTY"
#				You are next to the bottomless pit. Move onto the same square
#				and you will fall forever
#				"FLAP FLAP"
#				You are next to the bats.  If you move into the same square,
#				they will drop you at a random Map location
#
#				CAVE STRUCTURE (Numbers you can enter). Move left, right, up
#				and down by entering the cave number.  Invalid numbers are
#				just rejected
#				
#				33	34	35	36	37	38	39	40
#				25	26	27	28	29	30	31	32
#				17	18	19	20	21	22	23	24
#				9	10	11	12	13	14	15	16
#				1	2	3	4	5	6	7	8
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
# The Wumpus game in BASIC had multiple GOTO commands to exit the game
# and using a function method allows this to be done by simply returning
# the game result string back to the main game loop.
def wumpus():

	# Define the variables, place the Wumpus, Pit and Bats
	P = 1
	W = int(zx.RND() * 39) + 2
	E = int(zx.RND() * 39) + 2
	B = int(zx.RND() * 39) + 2
	
	# debug
	print 'Wumpus, bats, pit'
	print W,' , ',B,' , ',E

	# Game loop runs here
	while True:
		zx.PRINT('|tCAVE %d' % P)
		Q = abs(W-P)
		if Q == 1 or Q == 8:
			zx.PRINT('|tSNIFF, SNIFF')
		Q = abs(P-E)
		if Q == 1 or Q == 8:
			zx.PRINT('|tDRAUGHTY')
		Q = abs(P-B)
		if Q == 1 or Q == 8:
			zx.PRINT('|tFLAP, FLAP')
		if not(abs(W-P) != 1 and abs(W-P) != 8):
			zx.PRINT('|tSHOOT?')
			Q = int(zx.INPUT())
		A = abs(W-P)
		if (A == 1 or A == 8) and Q == W:
			return 'DEAD WUMPUS'
		zx.PRINT('|tWHERE?')
		Q = int(zx.INPUT())
		A = abs(P-Q)
		# If an invalid cave number was entered
		# then loop and keep asking until one was
		while A != 1 and A != 8:
			zx.PRINT('|tWHERE?')
			zx.screenRefresh()
			Q = int(zx.INPUT())
			A = abs(P-Q)
		P = Q
		if P == B:
			P = int(zx.RND() * 40) + 1
			zx.CLS()
			zx.PRINT('|tDROPPED AT %d' % P)
		if P == W:
			return 'WUMPUS EATS YOU'
		elif P == E:
			return 'DOWN A PIT'

	# Even though this is not a moving game, going to keep the fps
	# to match the rest of the other conversions.
	zx.screenRefresh()
	fpsClock.tick(4)
		
# GAME LOOP
while True:
	result = wumpus()
	
	# Print the outcome.  Note that have made this text inverted to be more
	# obvious we've finished the game.
	zx.PRINT("|i%s" % result)
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