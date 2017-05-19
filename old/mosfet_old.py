#this module is created for the relay controlling the power supply.

try:
    from setup import grbl
except ImportError:
    pass

from gops import commit

#define mosfet pins below
mosfet_pins = [11, 6, 5, 4]
mosfet_names = ['name1', 'name2', 'name3', 'name4']
mosfet_status = [False, False, False, False]

def mos_status( x ):
    return mosfet_status[ x ]

def mos_print_all_long( ):
    print "current outlets :"
    for x in range(0, len(mosfet_pins))
        print mosfet_names[ x ],
        if mosfet_status == True:
            print "[ON]"
        else:
            print "[OFF]"
    print "\n"

def mos_print_all_short( ):
    print " << "
    for x in range(0, len(mosfet_pins))
        print mosfet_names[ x ],
        if mosfet_status == True:
            print "[ON] > ",
        else:
            print "[OFF] > ",

def mos_on( x ):
    pin = mosfet_pins[ x ]
    grbl.write("M42 P%d S0" %pin)
    commit()
    mosfet_status[ x ] = True

def mos_off( x ):
    pin = mosfet_pins[ x ]
    grbl.write("M42 P%d S0" %pin)
    commit()
    mosfet_status[ x ] = False

def mos_init():
    for x in range(0, len(mosfet_pins))
        mos_off(x)