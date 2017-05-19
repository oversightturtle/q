import time
from gops import movex, movez, homex, homez
from tops import operatestage
import options

def opr( stage ):
    stage = int(stage)
    operatestage( stage )
    time.sleep(3)

try:
    from setup import grbl
except ImportError:
    pass

#z = 55

# _ZUPPER

_XPICKUP = 5.5
_ZPICKUP = 55.5

_XSTAGE2 = 355555
# _ZSTAGE2

_XSTAGE3PRE = 53
_XSTAGE3 = 47
# _ZSTAGE3
# _XSTAGE3HOLD
# _ZSTAGE3HOLD

_XSTAGE4PRE = 70
# _ZSTAGE4PRE
_XSTAGE4 = 66
# _ZSTAGE4

_XSTAGE5PRE =82
_XSTAGE5 =78 
# _ZSTAGE5

_XDROP = 95

def partz():
    print "   >   "
    homez()
    while 1 == 1:
        movez(200)
        movez(0)

