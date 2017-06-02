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

'''
todo:
1. 
'''




def main():
    commit()
    print "\nWelcome! >> availible options:"
    
    # list out all available options  below 
    for x in option.instances:
        print x.name,
        
        #list out all aliases below
        exist = False
        for y in poption.instances:
            if y.upper == x.name:
                exist = True
        #lists out all aliases
        if exist == True:
            print "(",
        
        for y in poption.instances:
            if y.upper == x.name:
                print y.name,

        if exist == True:
            print ")",        

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


def main_loop():
    while True:
        try:
            main()
        except IndexError: # ignores an "enter" key press without inputting a new command
            pass

if __name__ == "__main__":
    main_loop()