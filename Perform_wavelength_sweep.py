# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 12:45:00 2019

@author: edison
"""
#import sys
#sys.path.append("****************")

import insightLaser_instr

laser = insightLaser_instr.insightLaser()

laser.connect() # connect the laser through the telnet

   # query the instrument identification information.
   
laser.cmd_SYST_CONT('soft') # change the control state: software (soft) or hardware (hard)
laser.cmd_INIT_SWE()
#%% Perform a wavelength sweep (sweep mode)

# 1. set the sweep configuration
##sweep by points in the direction of increasing
   
points = 1000 
startwvl = 1530
stopwvl = 1532
delay = 0

laser.cmd_CONF_INCR_SBP(points,startwvl,stopwvl,delay)
laser.cmd_CONF_INCR_SBR_q()
laser.cmd_CONF_SWE_RAT_q()





#==========================================================
# Set the clock rate of the laser
clockrate = 10 # MHz
laser.cmd_CONF_SCL_RAT (clockrate)
#==========================================================
# 2. Set the sweep point increment 

laser.cmd_CONF_SWE_POIN_INCR(4)
#==========================================================
# 3. Set the peak power
#The average power level to set the laser to for sweeping (float, mW).
power = 2.1

laser.cmd_CONF_SWE_POW(power)
#==========================================================
# 4. Power profile

profile = 'flat' # Power profile type (FLAT, GAUSsian, or CUSTom).
laser.cmd_CONF_SWE_PROF(profile)
#==========================================================
# 5. Set the edge of the start sweep trigger when sweeps begin

edge = 'ris' # Trigger edge setting (RIS, FALL, BOTH).

laser.cmd_CONF_SWE_TRIG(edge)
#==========================================================
#%% Starting and stopping sweeps

# calibration
laser.cmd_CAL_SWE()
#Start a sweep
laser.cmd_INIT_SWE()
#==========================================================
#Stop a sweep
laser.cmd_ABOR()







