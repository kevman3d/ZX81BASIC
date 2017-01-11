# ZX81BASIC
A handful of code created by me while creating ZX81 BASIC game listing "remakes" in Python.  Any updates or new tools will
be added to this repository over time.  So if you're a child of the 80's, sit back and enjoy that nostalgiac journey back to when life
was great and computing was for nerds.
## The back story...
As a child I learnt to code through typing in hundreds of software listings (in BASIC) found in books and magazines.  Through
experimentation and tweaking of the code and graphics, I (and the many other kids of that era) quickly picked up those skills needed
to start developing our own games.

I believe that learning through games and experimenting with others code can be a creative and exciting experience.  Today, Python
offers an easy-to-learn language that is a lot of fun to work with and very powerful.  While BASIC and Python are different, problem
solving and computational thinking is the same no matter what language you are using.  Translating BASIC to Python is easy when you
understand the fundamentals of programming.

### Read about my BASIC project on my blog
http://kevman3d.blogspot.co.nz/2015/07/basic-games-in-python-1982-would-be.html
### Watch my presentation (and download project files)
http://kevman3d.blogspot.co.nz/2015/09/python-and-basic-games-mumble-mumble.html

# Python and external modules
The scripts were developed in python 2.7 (well, 2.7.9 if you want to be specific) and external modules/fonts

### Python
https://www.python.org/downloads/

### pygame (1.9.1)
http://www.pygame.org/wiki/GettingStarted

###ZX81 monospaced font
http://www.dafont.com/zx81.font

# Files description
This repository contains the files needed to easily translate simple ZX81 BASIC programs into Python.  You will need the ZXBasic.py module (provides a simple class), and unzip all of the png glyphs (ZX81_glyphs.7z) into the same folder.

You should also install the ZX81 Monospace font.  It first checks the installed fonts to see if it is installed.  You can tweak the source code to use the font file directly (if placed into the same folder). You will find line 132 in ZXBasic.py is commented out. Uncomment this line.

		# Search for ZX81 font, otherwise use Courier
		# This expects the ZX81 font to have been properly installed
		# on your system and no longer looks for it in the directory
		FONTPATH = pygame.font.match_font('zx81')
		if not FONTPATH:
			#FONTPATH = "zx81.ttf"
			FONTPATH = pygame.font.match_font('courier')
		self.charFont = pygame.font.Font(FONTPATH, self.charScale)		

After that, make sure to comment out line 133 below - this selects Courier monospace font if the ZX81 font is not installed (its not great, but it was a backup option).  If you're never planning to ever select Courier, this line can be completely deleted.

All other files (pyBREAKOUT.py, pyDOGFIGHT.py, etc) are games that were translated and should provide plenty of examples on how to develop your own.  All code is heavily commented to make it easy to follow.

## The games
All games are translated from listings in the book "34 Amazing games for the 1K ZX81".  Book and game design (C) 1982,
Alastair Gourlay, Mark Ramshaw and Interface publishing.

This was THE book that started it all (for me).
