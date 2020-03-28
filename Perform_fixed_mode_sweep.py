# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 15:03:07 2019

@author: edison
"""
import insightLaser_instr

laser = insightLaser_instr.insightLaser()

laser.connect() # connect the laser through the telnet

   # query the instrument identification information.
   
laser.cmd_SYST_CONT('soft') # change the control state: software (soft) or hardware (hard)
laser.cmd_INIT_SWE()

#%% Fixed wavelength mode

# Return the laser to Standby Mode
laser.cmd_ABOR()

#1. The first time the laser is turned on, or the fixed power value is changed or
# the power spectral profile is changed, calibrate the power profile for all 
# fixed wavelengths

## Calibrate the laser in the fixed mode
#laser.cmd_CAL_FIX()
## Query the state of the last fixed calibration
#laser.cmd_CAL_FIX_q()

#2. Set the time delay between when wavelength is set and Wavelength Ready Trigger 
# is generated on Data Valid Trigger output, in microseconds
delay = 0 # time delay in microsecond
laser.cmd_CONF_FIX_DEL(delay)

laser.cmd_CONF_FIX_DEL_q()


laser.cmd_CONF_SCL_RAT(10)
laser.cmd_CONF_SCL_RAT_q()



#3. Set the fixed wavelength or frequency

# In frequency
#laser.cmd_CONF_FIX_FREQ(193)
#laser.cmd_CONF_FIX_FREQ_q()

# In wavelength
laser.cmd_CONF_FIX_WAV(1550)
laser.cmd_CONF_FIX_WAV_q()

#4. Set the power in milliwatts

laser.cmd_CONF_FIX_POW(0)
laser.cmd_CONF_FIX_POW_q()
#5. Set the power profile

#For flat profile

profile = 'flat'
laser.cmd_CONF_FIX_PROF(profile)

#for gaussian profile, a second input is needed for power

#profile = 'gaussian'
#gauspower = 3
#laser.cmd_CONF_FIX_PROF(profile,gauspower)

laser.cmd_CONF_FIX_PROF_q()

# 6. Calibration

# Calibrate the laser in the fixed mode
laser.cmd_CAL_FIX()
# Query the state of the last fixed calibration
laser.cmd_CAL_FIX_q()

#7. Send the light out of the box
laser.cmd_INIT_FIX()


laser.cmd_ABOR()