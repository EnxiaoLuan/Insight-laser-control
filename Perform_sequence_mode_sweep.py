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
#laser.cmd_INIT_SWE()

#%% Sequence mode

#This command clears all the wavelengths/frequencies in the sequence sweep.       
laser.cmd_CONF_SEQ_CLEA()        
laser.cmd_CONF_SEQ_q()


#Create an equally spaced, equal dwell time sequence via a single command
# STEP: The step value to increment by to add entries to the
        #sequence sweep (in nanometers).
#LENGTH: The amount of time, in nanoseconds, to sit at the desired
        #wavelength.
#STARWVL: The starting wavelength for the new entries (nanometers,
        #defaults to minimum wavelength).
#STOPWVL: The stopping wavelength for the new entries (nanometers,
        #defaults to maximum wavelength).
#POSITION: The position in the sequence table to add the wavelength
        #(defaults to the end: -1).
 

step = 0.01
length = 500
startwvl = 1531
stopwvl = 1531.5
position = 0

laser.cmd_CONF_SEQ_ADD_WST(step,length,startwvl,stopwvl,position)
# or more customized sequences can be created step-by-step via command
### laser.cmd_CONF_SEQ_ADD_WAV(1549,500,-1)
# or by uploading a file of wavelengths and dwell times
### laser.cmd_CONF_sEQ_LOAD(filename.csv)

# The user can verify the programmed sequence of wavelengths by the query
laser.cmd_CONF_SEQ_q()

# The power at each wavelength of the sequence is set by
laser.cmd_CONF_SEQ_POW(2)
laser.cmd_CONF_SEQ_POW_q()
#%%

#The sequence must then be calibrated to that power using the
laser.cmd_CAL_SEQ()
laser.cmd_CAL_SEQ_q()
laser.cmd_SYST_ERR_ALL_q()
#Start the sweep in the designated sequence
laser.cmd_INIT_SEQ()
laser.cmd_ABOR()

