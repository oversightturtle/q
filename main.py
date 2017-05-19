print "\nGRBL/TLC > Automater > Welcome!\n"

import time

from setup import config
config()

from termcolor import colored

print "\n",

try:
    from setup import tlc
except ImportError:
    print "tlc\t", colored("[NOT FOUND]", "red")
    pass

try:
    from setup import grbl
except ImportError:
    print "main\t", colored("[NOT FOUND]", "red")
    pass
 
from auto import *  #looper

from options import *

from optionslist import *

commit() # wakes up grbl.

from mosfet import *

#sets all relay to OFF, if possible
try:
    mos_init()
except NameError:
    pass

disp_opt = True

while True:

        
    commit()

    # list out all available options  below 
    if disp_opt == True:

        mos_p_short()

        print "\navailible options:"
        opt_print()    

        print "\n\n"

    a = raw_input('main >> ')
    
    net = False # bool function that states weather a valid function has been inputted
    
    #if the input matches an alias it sets the input to the alias pointer
    for x in poption.instances:
        escape = False
        for y in option.instances:
            if a == x.name:
                if x.upper == y.name:
                    a = y.name
    #executes the command
    for x in (option.instances):
        if a == x.name:
  #          print "!" 
            net = True
            if x.loop == False:
                disp_opt = False # does not reprint options
                x.func() ###
            elif x.loop == True:
                try:
                    while 1 == 1:
                        try:
                            x.func() ###
                        except ValueError:
                            print "value not accepted"
                except KeyboardInterrupt:
                    print " >> halting > "
            break
    if net == False:
        print " >> command not found"
