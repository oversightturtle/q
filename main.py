print "\nGRBL/TLC > Automater > Welcome!\n"

import config


from termcolor import colored

if config.con_VIRTUAL == True:
    from virtual import grbl, tlc
    print colored( "[MASTER] VIRTUAL ON" ,"yellow")   


import time

from setup import tty_config
tty_config()


print "\n",

try:
    from setup import tlc
except ImportError:
    if config.con_VIRTUAL == False:
        print "tlc\t", colored("[NOT FOUND]", "red")
    else:
        print "tlc\t", colored("[VIRTUAL]", "yellow")
    pass

try:
    from setup import grbl
except ImportError:
    if config.con_VIRTUAL == False:
        print "grbl\t", colored("[NOT FOUND]", "red")
    else:
        print "grbl\t", colored("[VIRTUAL]", "yellow")
    pass

if config.con_VAC == False:
    print colored("VAC DISABLED",  "white", "on_red")
 
from auto import *  #looper

from options import *

from optionslist import *

from mosfet import *

def main():

    commit() # wakes up grbl

    print "\nWelcome! >> availible options:"
    pOpt()

    a = raw_input('\nINPUT >> ')
    
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
       #     print "!" 
            net = True
            if x.loop == False:
                try:
                    x.func() ###
                except KeyboardInterrupt:
                    print "... halting >> "
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

def main_loop():
    while True:
        try:
            main()
        except IndexError: # ignores an "enter" key press without inputting a new command
            pass

if __name__ == "__main__":
    main_loop()
