#! /usr/bin/python
# -*- coding: utf-8 -*-
# """
#   braille-this, a little CLI tool for emitting Unicode Braille art
#   YOU SHOULD NOT USE THIS, EVER. I do not think people with visual
#   impairments will appreciate this abuse. So think long and hard about
#   whether the image you are converting really should be.
#
#   © 2015 John Drinkwater <john@nextraweb.com>
#
import sys,os.path,Image

__version__ = "0.01"

def printusage():
    print "braille-this %s" % __version__
    print "Usage: %s <IMAGE> [OUTPUT]" % os.path.basename( __file__ )
    print "where IMAGE is a filename, OUTPUT can be a filename, or omitted to \
print to stdout"
    sys.exit(-1)


if __name__ == '__main__':

    buffer = False
    ofilename = '-'

    if len(sys.argv) < 2:
        printusage()

    ifilename = sys.argv[1]
    ifile = Image.open(ifilename)
    # TODO does it exist?
    idata = ifile.convert('RGB')

    if len(sys.argv) > 2:
        ofilename = sys.argv[2]

    if ofilename != '-':
        ofile = open(ofilename, 'w')
    else:
        ofile = sys.stdout

    (width, height) = idata.size
    (x, y) = idata.size
    # get our braille character bounds
    x += x%2 if y%2 else 0
    y += 4-y%4 if y%4 else 0
    x /= 2
    y /= 4

    if buffer:
        x += 2
        y += 2

    canvas = Image.new('RGB', (x*2,y*4), 'white')

    if not buffer:
        canvas.paste(idata, (0,0))
    else:
        canvas.paste(idata, (2,4))

#    braille = {
#        (0,0,0,0,0,0,0,0): '⠀',
#        (1,0,0,0,0,0,0,0): '⠁',
#        (0,1,0,0,0,0,0,0): '⠂',
#        (1,1,0,0,0,0,0,0): '⠃',
#        … LOL NO
#    }
    white = (255,255,255)

    for row in range(0,y*4,4):
        currentrow = ''
        for col in range(0,x*2,2):
            char = [canvas.getpixel((col+1, row+3)) != white,
                    canvas.getpixel((col,   row+3)) != white,
                    canvas.getpixel((col+1, row+2)) != white,
                    canvas.getpixel((col+1, row+1)) != white,
                    canvas.getpixel((col+1, row  )) != white,
                    canvas.getpixel((col,   row+2)) != white,
                    canvas.getpixel((col,   row+1)) != white,
                    canvas.getpixel((col,   row  )) != white]
            char = ''.join([str(int(cx)) for cx in char])
            char = unichr( 10240+int( char,2 ) )
            currentrow+=char
        print >>ofile, currentrow.encode('utf8')
