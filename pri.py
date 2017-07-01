import time
from gops import movex, movez, homex, homez, movexz_instant
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

def partz():
    '''
    movexz_instant(0, 0)
    time.sleep(3)
    movexz_instant(10, 10)
    time.sleep(3)
    movexz_instant(20, 20)
    time.sleep(3)
    '''
    movez(10)
    movez(20)
    movez(30)
    movez(40)
    movez(20)




