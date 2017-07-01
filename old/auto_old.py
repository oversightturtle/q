
def autoposition( initial, offset, limit, inc):
    
    __delay = 3
    escape = False
    current = initial

    while (escape == False) and (current != limit):
        movez_direct(current)
        time.sleep( __delay )
        movez_direct(current - offset)
        time.sleep( __delay )
        tlc.write("5")
        det = read_pps()
        if det == False:
            print "no obs"
        else:
            print "obs found"
            escape = True
            global pickuplevel
            pickuplevel = (current - inc)
        current += inc


def autotest():
    grbl.write("G28 Z")
    dcommit()
    vac_off() ###
    autoposition(
        offset = 28,
        initial = 245,
        limit = 267,
        inc = 1
    )
        
def autoset(initial, offset, limit, inc):
    time.sleep(1)
    vac_on()
    escape = False
    current = initial
    while escape == False:
        movez_direct(current)
        try: 
            a = input(" press enter to continue >> (type any key to halt) >> ")
            print "uhoh!"
            vac_off()
            return ( current - inc)
        except SyntaxError:   
            current += inc
        except NameError:
            vac_off()
            return ( current - inc)


            
def pri_init():

    tlc_initsafe()
    movex(3)
    #######################################
    vac_on()
    initialx = autoset(
        initial = 243,
        offset = 0,
        limit = 267,
        inc = 4)

    movez_direct(240)

    initialxx = autoset(
        initial = initialx,
        offset = 0,
        limit = 267,
        inc = 1)

    movez_direct(240)
    
    vac_on()
    autoposition(
        initialxx,
        offset = 28,
        limit = 267,
        inc = 0.25
    )

    def pulse(mx):
    def movex( xval ):
        movex_ins_del( xval , 1)
    def movez( zval ):
        movez_ins_del( zval, 1.5)
    upper = mx - 8
    movex(35)
    movez(mx)
    movez(upper)
    movex(36)
    movez(mx)
    movez(upper)
    movex(37)
    movez(mx)
    movez(upper)
    movex(38)
    movez(mx)
    movez(upper)
    movex(38.5)

def pulse_concat(mx):
    def movex( xval ):
        movex_ins_del( xval , 1)
    def movez( zval ):
        movez_ins_del( zval, 1.5)
    upper = mx - 8
    movex(35.5)
    movez(mx)
    movez(upper)
    movex(36)
    movez(mx)
    movez(upper)
    movex(37)
    movez(mx)
    movez(upper)
    movex(38)
    movez(mx)
    movez(upper)
    movex(38.5)