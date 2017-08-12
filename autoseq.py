w_val = 40
w_v_offset = x # CHANGE THIS VAL
set_master = 10
set_length = int (7) #10, 2.5, 0.62, 0.16
w_set_length = 0
w_set = set_master


movex_fast(6)
while w_set_length != set_length:
    l_escape = False
    while l_escape == False:
        movez(w_val)
        if tmp_esc == 1:
            l_escape == True:
        else:
            w_val = w_val + w_set
    w_set = w_set / 2
    w_set_length += 1
  
'''
    
#   this part creates the initial value of the vac
    movex_fast(6)

    # initial z value for homing
    hip_init = (46.4 + ZOFFSET)
    # homing increment for each step
    hip_inc_05= 0.6
    hip_inc_0005 = 0.15
    global hip_last
    hip_escape_05 = False
    hip_escape_0005 = False

    vac_on()

#0.02 accuracy
    # obtain hipvalues to 0.6 unit accuracy
    while hip_escape_05 == False:
        movez_instant(hip_init)
        a = raw_input("press enter to continue (no suction), press any key to stop")
        if a == '':
            hip_init = hip_init + hip_inc_05
        else:
            hip_init = hip_init - hip_inc_05
            hip_escape_05 = True
            vac_off()
            
        time.sleep(2)
        movez_instant(hip_init)
        vac_on()
        time.sleep(1)

    #obtain hipvalues to 0.15 unit accuracy
    while hip_escape_0005 == False:
        movez_instant(hip_init)
        a = raw_input("press any key to end. press enter to lower")
        if a == '':
            hip_init = hip_init + hip_inc_0005
        else:
            hip_init = hip_init - hip_inc_0005
            hip_escape_0005 = True
    
        hip_last = hip_init
    '''    