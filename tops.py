import time

import config

if config.con_VIRTUAL == True:
    from virtual import tlc

try:
    from setup import tlc
except ImportError:
    pass


def operatestage( x ):
    tlc.write(b"0 %d" %x)
    print "stage : " + str(x)
    return

def operateservo( p, pos) :
    tlc.write(b"1 %d %d" %(p, pos))
    return
