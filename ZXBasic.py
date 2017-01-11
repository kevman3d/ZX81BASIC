# ----
#
# ZX81 BASIC MODULE
# (C)opyright 2015, Kevin Phillips
#
# A module containing functions that replicate various commands from
# Sinclair Basic, using pygame.  Developed to assist in making BASIC
# conversion easier.  This is *not* a complete language conversion.
#
# USAGE:
#		import ZXBasic.py
#		(write your game - see example at end of this code)
#
# NOTE : This code has only been mildly tested so may be buggy, but
#        Hopefully will inspire you to develop your own awesome
#        library of functions.
#
# PRINT MODES:
# The ZX81 had a graphics mode, as well as INVERSE.  This would allow
# white-on-black text characters, and ANSI graphics to be displayed.
#
# To utilize this in code, strings must be specified with start tags
# to identify the 'mode' so that ASCII is interpretted correctly
#
# |t (pipe t) - Normal Text
# |i (pipe i) - Inverted Text
# |g (pipe g) - Graphics mode
#
# Graphics mode relies upon all graphic character PNG files being present
# as they are loaded into the class at the start and mapped via a Dictionary
#
# DEMO:
# A demonstration of using ZXBasic is included at the bottom of this
# python scripts and can be used to familiarise yourself with using it.
#
# ----

import pygame
from pygame.locals import *
import sys
from random import random,randint
import math

BLACK = (0,0,0)
WHITE = (255,255,255)

# Make sure pygame is loaded
pygame.init()
		
# ZXBasic class
#
# Attributes
#
# .TV			- (pygame.display) game surface object
# .charFont		- (pygame.font) screen font to use
# .charScale	- (int) size of a single character in pixels
# .border		- (int) pixel size for gutter around screen
# .cursor		- (int) cursor line location
# .scrMap		- (list) Map of characters on screen (ints)
# .scrCodes		- (dict) Dictionary mapping all ZX81 characters to codes
#
# Methods:
#
# --
# SYSTEM FUNCTIONS:
# --
#
# .createScreen()
#		Creates a display surface for pygame, stored in .TV
# .blank_border()
#		Draws a white border around screen (if border > 0)
#		to clear any over-printing issues
# .screenRefresh()
#		Performs a screen update (pygame.display.update)
# .printString(str,x,y)
#		Analyses printing modes and prints strings of text
#		or graphics characters.  Used internally by PRINT,PRINT_AT
# .peekCharacter(str,x,y)
#		Checks character at print location x,y if it is str
#		Returns true or false
# .redrawScrMap()
#		Redraw the whole screen from the scrMap list
#
# --
# BASIC COMMANDS:
# --
#
# .PRINT_AT(y,x,str)
#		Prints str at the character locations specified
# .INKEY(str)
#		Returns the true/false result of a key press
# .CLS()
#		Clears screen by filling surface with white
# .PLOT(x,y)
#		Plots a black pixel (0-63, 0-43) block
# .UNPLOT(x,y)
#		Unplot (essentially plot a white pixel)
# .INPUT()
#		Allow the user to type text into the bottom line
#		Returns the string
# .PRINT(str)
#		Prints text to the screen. Scrolls when text reaches
#		bottom (though ZX81 never really did that)
# .SCROLL()
#		Scrolls the screen up one character line
# .RND()
#		Returns a random value between 0 and 1 (simply python's
#		own 'random' function)
# .SGN(value)
#		Returns the sign of a number (signum)

class ZXBasic():

	def __init__(self):
	
		self.TV = None
		self.charFont = None
		self.charScale = 16
		self.border = 32
		self.cursor = 0

		# Screen map holds the byte values for each character
		self.scrMap = []
		for loop in range(768):
			self.scrMap.append(0)

		# Search for ZX81 font, otherwise use Courier
		# This expects the ZX81 font to have been properly installed
		# on your system and no longer looks for it in the directory
		FONTPATH = pygame.font.match_font('zx81')
		if not FONTPATH:
			#FONTPATH = "zx81.ttf"
			FONTPATH = pygame.font.match_font('courier')
		self.charFont = pygame.font.Font(FONTPATH, self.charScale)		

		# ----
		#
		# Define the keyboard graphics
		#
		# ----
		self.gKeys = {}
		
		# Load up the graphics characters from disk
		for letter in ['1','2','3','4','5','6','7','8','a','d',
						'e','f','g','h','q','r','s','t','w','y']:
			self.gKeys['g%s' % letter] = pygame.image.load("g%s.png" % letter)
			
		# ----
		#
		# Define character codes (ZX81) for look-up
		# Easiest way to set up all the codes here is to use lists. Saves on
		# typing piles of data...
		#
		# ----
		self.scrCodes = {}
		self.scrCodes["t "] = 0
		self.scrCodes["i "] = 128
		listChars = "\"~$:?()><=+-*/;,.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		charCode = 11
		invCode = 139
		for letter in listChars:
			self.scrCodes["t%s" % letter] = charCode
			self.scrCodes["i%s" % letter] = invCode
			charCode += 1
			invCode += 1
		# Define graphics codes
		listChars = "12745t3hds"
		charCode = 1
		for letter in listChars:
			self.scrCodes["g%s" % letter] = charCode
			charCode += 1
		listChars = "qw6r8yeagf"
		charCode = 129
		for letter in listChars:
			self.scrCodes["g%s" % letter] = charCode
			charCode += 1


	# Helper function - draw border around screen (used when screen is scrolled)
	def blank_border(self):
		if self.TV and self.border > 0:
		
			# Define some constants for screen
			pixelSize = self.charScale
			scrBottom = (24 * pixelSize) + self.border
			scrRight = (32 * pixelSize) + self.border
			scrWide = 32 * pixelSize
			scrHigh = 24 * pixelSize
			bdrWide = scrWide + 2*self.border
			bdrHigh = scrHigh + 2*self.border
			
			pygame.draw.rect(self.TV, WHITE, (0, 0, bdrWide, self.border + 1))
			pygame.draw.rect(self.TV, WHITE, (0, 0, self.border, bdrHigh))
			pygame.draw.rect(self.TV, WHITE, (scrRight, 0, self.border, bdrHigh))
			pygame.draw.rect(self.TV, WHITE, (0, scrBottom, bdrWide, self.border))
	
	
	# Redraw the screen from the scrMap list
	def redrawScrMap(self):
		cX = 0
		cY = 0
		theText = ''
		for codes in self.scrMap:
			for codeName,codeVal in self.scrCodes.items():
				if codeVal == codes:
					self.printString('|%s' % codeName, cX, cY)
					theText = theText + ('%s' % codeName[1])
			cX += 1
			if cX > 31:
				print theText
				theText = ''
				cX = 0
				cY += 1
				
	# Look-up character at a location on screen
	# Refers to the scrMap list, scrCodes dictionary
	# Term 'peek' refers to ZX81 screen memory look up 
	def peekCharacter(self, strChar, cX, cY):
		getCode = self.scrMap[cX + cY * 32]
		if getCode == self.scrCodes[strChar]:
			return True
		else:
			return False


	# Print string function - called by PRINT and PRINT_AT functions
	# to handle graphics and invert modes.  Arguments:
	# strToPrint : string to print
	# pX, pY : Print locations (in character space)
	def printString(self, strToPrint, pX, pY):
		if self.TV:
			# First separate the string into its chunks
			printBlocks = strToPrint.split("|")
			
			# Work through each block
			for printMode in printBlocks:
			
				if printMode:
					# Text mode - print letter by letter
					if printMode[0] == 't':
						printMode = printMode.upper()
						for letter in printMode[1:]:
							tX = self.border + pX * self.charScale
							tY = self.border + pY * self.charScale
							bText = self.charFont.render(letter, True, BLACK, WHITE)
							self.TV.blit(bText,(tX,tY))
							
							# Add the character to our screen map
							self.scrMap[pX + (pY * 32)] = self.scrCodes["t%s" % letter]
							
							pX += 1
							if pX > 31:
								pX = 1
			
							
					if printMode[0] == 'g':
						printMode = printMode.lower()
						for letter in printMode[1:]:
							tX = self.border + pX * self.charScale
							tY = self.border + pY * self.charScale
							gfx = pygame.transform.scale(self.gKeys['g%s'% letter],
													(self.charScale, self.charScale))
							self.TV.blit(gfx,(tX,tY))

							# Add the character to our screen map
							self.scrMap[pX + (pY * 32)] = self.scrCodes["g%s" % letter]

							pX += 1
							if pX > 31:
								pX = 1
						
					if printMode[0] == 'i':
						printMode = printMode.upper()
						for letter in printMode[1:]:
							tX = self.border + pX * self.charScale
							tY = self.border + pY * self.charScale
							
							# Invert simply means swapping BG/FG colours.  simple
							bText = self.charFont.render(letter, True, WHITE, BLACK)
							self.TV.blit(bText,(tX,tY))

							# Add the character to our screen map
							self.scrMap[pX + (pY * 32)] = self.scrCodes["i%s" % letter]

							pX += 1
							if pX > 31:
								pX = 1
							
		
	# Create game surface based on ZX81 screen size (32 x 24 chars)
	# The bottom two lines (22,23) are for input, no print or plot
	def createScreen(self):
		self.TV = pygame.display.set_mode((32*self.charScale + 2*self.border,
										   24*self.charScale + 2*self.border))
	
	# PRINT AT (row(Y), column(X), string)
	def PRINT_AT(self,y,x,strText):
		if self.charFont and self.TV:
			self.printString(strText, x, y)
			# Clear border to prevent spill over it
			self.blank_border()

	# INKEY$ function (strChar)
	def INKEY(self, strChar):
		if strChar:
			if strChar == " ":
				strChar = "SPACE"
			strChar = "K_" + strChar
			value = eval(strChar)
			
			keysPressed = pygame.key.get_pressed()
			if keysPressed[value]:
				return True
			else:
				return False
			
	# CLS
	def CLS(self):
		if self.TV:
			self.TV.fill(WHITE)
			self.cursor = 0
			# Clear the scrMap
			for loop in range(768):
				self.scrMap[loop] = 0
			
	# Screen refresh
	# Have added the event check in here to allow for better
	# handling of QUIT events (since screenRefresh is called
	# literally all the time)
	def screenRefresh(self):
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
	
	# Plot a pixel
	def PLOT(self, x,y):
		pixelSize = self.charScale / 2
		# Update Y (Y coordinate starts at bottom, not top of screen, plus skip bottom 2 input lines)
		y = 43 - y
		pX = x*pixelSize + self.border
		pY = y*pixelSize + self.border
		if self.TV:
			pygame.draw.rect(self.TV, BLACK, (pX,pY,pixelSize,pixelSize))


    # UNPLOT a pixel
	def UNPLOT(self, x,y):
		pixelSize = self.charScale / 2
		# Update Y (Y coordinate starts at bottom, not top of screen)
		y = 43 - y
		pX = x*pixelSize + self.border
		pY = y*pixelSize + self.border
		if self.TV:
			pygame.draw.rect(self.TV, WHITE, (pX,pY,pixelSize,pixelSize))


	# INPUT
	# Very simple function - any non letter/numeric key is converted to a space
	# and input is limited to the bottom line of the screen.
	def INPUT(self):
		inputText = ""
		cursorLoc = 0
		cursorLine = 23
		finished = False
		
		# Blank line for input
		self.PRINT_AT(cursorLine, 0, "|t" + " "*32)
		self.screenRefresh()
		
		# Loop through until enter key is pressed
		while not finished:
		
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN:
					if event.key == K_RETURN:
						finished = True
					elif event.key == K_BACKSPACE:
						inputText = inputText[:-1]
						self.PRINT_AT(cursorLine, 0, "|t" + inputText + "  ")
						self.screenRefresh()
						cursorLoc -= 1
						if cursorLoc < 0:
							cursorLoc = 0
					else:
						charInput = str(pygame.key.name(event.key))
						if len(charInput) > 1:
							charInput = " "
						inputText += charInput.upper()
						self.PRINT_AT(cursorLine, 0, "|t" + inputText)
						self.screenRefresh()
						cursorLoc += 1
						if cursorLoc > 31:
							cursorLoc = 31
			
				# When using the ZX81 font, lower case characters are reversed caps.
				self.PRINT_AT(cursorLine,cursorLoc,"|iL")
				self.screenRefresh()
				
		self.PRINT_AT(23,0,"|t" + " "*32)
		self.screenRefresh()
	
		return inputText


	# PRINT(Text)
	# Prints to the screen, at line specified by self.cursor
	# Will scroll the screen if enters the input line area (line 22/23)
	def PRINT(self,str):
		if self.TV:
			self.PRINT_AT(self.cursor,0,str)
			self.cursor += 1
			if self.cursor > 21:
				# Scroll the screen
				self.TV.scroll(0, -self.charScale)
				# Move the cursor back one line
				self.cursor = 21
				
			# Clear border to prevent spill over it
			self.blank_border()
			self.screenRefresh()

	
	# SCROLL()
	# Scrolls the screen up one character at a time
	def SCROLL(self):
		if self.TV:
			# Scroll the screen
			self.TV.scroll(0, -self.charScale)
			self.blank_border()
			# Scroll up the scrMap list
			newScrMap = self.scrMap[32:]
			for loop in range(32):
				newScrMap.append(0)
			self.scrMap = newScrMap
			
			
	# RND()
	# Returns a random number between 0 and 1
	def RND(self):
		return (random())
		
	# SGN()
	# Returns the signum (sign) +1, 0, -1
	def SGN(self, value):
		return math.copysign(1,value)
		
	
		
# TEST code - example of how this class is used
if __name__ == '__main__':
	
	fpsClock = pygame.time.Clock()
	print "Clock set"
	ZXProgram = ZXBasic()
	print "ZXBasic init"
	ZXProgram.createScreen()
	print "Screen drawn"
	ZXProgram.CLS()
	print "CLS"
	
	counter = 0
	
	print "About to enter loop"
	
	# Testing the text printing with new 'modes' implemented
	# Normal text should always start with pipe-t ie.  "|t"
	# Graphics mode starts with "|g"
	# Inverted text starts with "|i"
	while counter < 30:
		print "Looping ", counter
		ZXProgram.PRINT_AT(int(20 * ZXProgram.RND()), int(31 * ZXProgram.RND()),"|tZ")
		ZXProgram.PRINT_AT(randint(0,20), randint(0,31),"|iX")
		ZXProgram.PRINT_AT(randint(0,20), randint(0,31),"|t8")
		ZXProgram.PRINT_AT(randint(0,20), randint(0,31),"|i1")
		ZXProgram.PRINT_AT(10,10,"|tGFX :|g12345678adefghqrstwy")
		ZXProgram.SCROLL()
		counter += 1
		ZXProgram.screenRefresh()
		fpsClock.tick(6)
	
	print "pausing"
	counter = 0
	while counter < 10:
		counter += 1
		fpsClock.tick(6)
	
	pygame.quit()
	sys.exit()