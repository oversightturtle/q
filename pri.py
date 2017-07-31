import time
from gops import movex, movez, homex, homez, movexz_instant
from tops import operatestage
import options
from termcolor import colored



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
    def verbose_wait(delaytime):
        for x in range (0, delaytime):
            time.sleep(1)
            print "waiting > ", x
    
    print colored("[WARNING} ENSURE HOMED", "red")
    time.sleep(5)
    tlc_init()
    movex(19)
    movez(97)
    tstage(26) # FOLD1FOLD2 MOVEOUT

    movez(101)
    vac_on()
    tstage(27) # RAISE S2PLACE to 160
    time.sleep(3)
    movez(97)
    movexz_instant(14, 60)
    verbose_wait(6)

    tstage(29)

    SX_LOW

    movez(20)
    movey(52)
    
    S3 __ >> UP UPPLACE

    movez(102 - ish)
    '''

    
    

    
