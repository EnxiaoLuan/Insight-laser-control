# =========================================================================================================
# This script is used to convert the Insight sweep laser SCPI commands to python commands
# The laser is connected through Ethernet (IP address: 137.82.251.151; address name: insight-laser; port: 23) 
# Verison 2.0 (Modified by Jonas)
# Enxiao 2019-07-26
# =========================================================================================================

import telnetlib
import logging


class insightLaser:
    
    def __init__(self, host='insight-laser'):
	
        self.port = 23
        self.host = host
		
		# Logger 
        logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)
        self._log = logging.getLogger()
		
        self.tn = None	# handle for telnet object -> initialize empty
		

    def connect(self):
        self.tn = telnetlib.Telnet(self.host,self.port)
        self.tn.read_until(b'atlas ready>')

    def sendCommand(self, cmd):
        '''
        cmd: SCPI command as string
        return: return if successful otherwise rasise error
        '''
        self.tn.write((cmd+'\n\r').encode('ascii'))
		
    def readResponse(self):
        '''
        Convert the bytes back to a proper string
        return: response from instrument as string
        '''
        return self.tn.read_until(b'atlas ready>').decode().strip('atlas ready>')

##############################################################################
# commonly used commands for the laser.
        
    def cmd_CLS(self): 
        '''
        Clears status/results queue.
        '''  
        self.sendCommand('*CLS')
        reply = self.readResponse()
        self._log.info(reply) # error check?
        return reply


    def cmd_ESE(self,onoff): 
        '''
        Enables or disables Extended Status/Results.
        ''' 
        if(onoff.upper() == 'ON'):
            self.sendCommand('*ESE ON')
        elif(onoff.upper() == 'OFF'):
            self.sendCommand('*ESE OFF')
        else:
            print('Please enter "ON/OFF" to enable/disable Extended Status/Results')
            return
        reply = self.readResponse()
        return reply
    
            
    def cmd_ESE_q(self):
        '''
        Extended status enable query.
        '''
        self.sendCommand('*ESE?')
        reply = self.readResponse()
        self._log.info(reply)
        return reply


    def command_ESR(self):
        '''
        Extended status report query.
        ''' 
        self.sendCommand('*ESR?')
        reply = self.readResponse()
        self._log.info(reply)
        return reply

 
    def cmd_IDN_q(self):    
        '''
        Get instrument identi
        cation information.
        '''
        self.sendCommand('*IDN?')
        reply = self.readResponse()
        self._log.info(reply) 
        return reply


    def cmd_OPC(self):    
        '''
        Query the status of the operation complete bit.
        '''
        self.sendCommand('*OPC?')
        reply = self.readResponse()
        self._log.info(reply)
        return reply



    def cmd_RST(self):    
        '''
        This command resets the system to the values stored in the
        User Conguration file and the Factory Calibration file.
        '''    
        self.sendCommand('*RST')
        reply = self.readResponse()
        self._log.info(reply)
        return reply
  
    
    def cmd_STB_q(self):    
        '''
        Returns laser status.
        Bit 0: Laser is EMITTING
        Bit 1: Status LED is ON
        Bit 2: (control thread is) BUSY
        Bit 3: LED2 is ON
        Bit 4: Optical switch to USER output
        Bit 5: Laser is ON
        Bit 6: Reserved
        Bit 7: Reserved
        '''
        self.sendCommand('*STB?')
        reply = self.readResponse()
        self._log.info(reply)
        return reply
   
    
    def cmd_TST_q(self):    
        '''    
        Test query.    
        '''    
        self.sendCommand('*TST?')
        reply = self.readResponse()
        self._log.info(reply)
        return reply


    def cmd_WAI(self):  
        '''    
        Waits for the laser to complete any pending operations.
        When no delayed operations are being performed "Idle" is
        output and the command returns immediately.
        '''
        self.sendCommand('*WAI')
        reply = self.readResponse()
        self._log.info(reply)
        return reply

##############################################################################
# Start a sweep.

## 1) Synchronize the sweep of the laser with the data acquisition system
 
    def cmd_SOUR_SYNC_POW(self,amplitude,start_delay,pulse_width,wavelength):   
        '''
        This commands the laser to produce a sweep of the laser in
        which the optical wavelength is constant, but the optical
        power steps in a pulse of amplitude <Amplitude>, lasting
        for a width of <Pulse Width> nanoseconds, where the pulse
        begins at <Start Delay> nanoseconds after Start Sweep.
        The Power Synchronization pulse repeats with an interval
        equal to the Number of Sample points times the step period
        of the sweep, nominally 2.5 nanoseconds per step.
        Use this function to synchronize the electronic triggers Start
        Sweep and Data Valid with the acquisition of optical
        information from the sweep.
        '''    
        self.sendCommand(':SOURce:SYNChronize:POWer %a,%s,%s,%s'%(amplitude,start_delay,pulse_width,wavelength))
        reply = self.readResponse()
        self._log.info(reply)
        return reply

    def cmd_SOUR_SYNC_POW_q(self):
        '''
        This queries the laser for the parameters of the optical
        power pulse at the start of the sweep of the laser. The
        synchronization power pulse enables the user to perform a
        synchronization of the arrival time of the pulse with the
        arrival time of triggers: Sweep Start, Sample Clock and Data
        Valid.
        '''
        self.sendCommand(':SOURce:SYNChronize:POWer?')
        reply = self.readResponse()
        self._log.info(reply)
        return reply

####################
## 2) Use the sweep synchronization procedure to adjust delays on the 
##    Sweep Start, Sample Clock and Data Valid Trigge
    
    def cmd_SOUR_CORR_DVD(self,delay):
        '''
        This command sets the delay of the data valid pulses that
        are sent to the user, in units of ns. The resolution of the
        delay value is 0.15 nsec.
        '''
        self.sendCommand(':SOURce:CORRection:DVDelay %s'%(delay))
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_SOUR_CORR_DVD_q(self):
        '''
        This command returns the delay of the data valid pulses
        that are sent to the user.
        '''
        self.sendCommand(':SOURce:CORRection:DVDelay?')
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_SOUR_CORR_DVD_TOT_q(self):
        '''
        This command returns the total delay of the data valid signal
        sent to the user, in units of ns. The total delay is defined as
        the user specified part plus the factory specified part.
        '''
        self.sendCommand(':SOURce:CORRection:DVDelay:TOTal?')
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_SOUR_CORR_SCD(self,delay):
        '''
        This command sets the delay of the sample clock that is
        sent to the user, in units of nanoseconds. The resolution is
        0.178 ns.
        '''
        self.sendCommand(':SOURce:CORRection:SCDelay %s'%(delay))
        reply = self.readResponse()
        self._log.info(reply)
        return


    def cmd_SOUR_CORR_SCD_q(self):
        '''
        This command returns the delay of the sample clock that is
        sent to the user.
        '''
        self.sendCommand(':SOURce:CORRection:SCDelay?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_SOUR_CORR_SSD(self,delay):
        '''
        This command sets the delay of the sweep start that is sent
        to the user, in units of ns. The resolution is 0.15 ns.
        For this command, because of the discretization
        requirement, the laser returns to the user the actual delay
        the system will execute.
        '''
        self.sendCommand(':SOURce:CORRection:SSDelay %s'%(delay))
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_SOUR_CORR_SSD_q(self):
        '''
        This command returns the delay of the sweep start that is
        sent to the user.
        '''
        self.sendCommand(':SOURce:CORRection:SSDelay?')
        reply = self.readResponse()
        self._log.info(reply)
        return
        
    def cmd_SOUR_CORR_SSD_TOT_q(self):
        '''
        This command returns the total delay of the sweep start
        signal sent to the user, in units of ns. The total delay is
        defined as the user specified part plus the factory specified part.
    '''
        self.sendCommand(':SOURce:CORRection:SSDelay:TOTal?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
#####################
## 3) Set the Sweep Parameters

    def cmd_CONF_SWE_WMIN(self,wavelength):
        '''
        Set the minimum wavelength of a sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:WMINimum %s'%(wavelength))
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_WMIN_q(self):
        '''
        Returns the minimum wavelength of a sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:WMINimum?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_FMIN(self,frequency):
        '''
        Set the minimum optical frequency of a sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:FMINimum %s'%(frequency))
        reply = self.readResponse()
        self._log.info(reply)
        return
        
    def cmd_CONF_SWE_FMIN_q(self):
        '''
        Returns the minimum optical frequency of a sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:FMINimum?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_DIR(self,direct):
        '''
        This command sets the direction of the wavelength sweeps
        of the laser. Options are to sweep the laser with increasing
        wavelength, decreasing wavelength, bidirectionally with
        increasing wavelength first or bidirectionally with decreasing
        wavelength first.
        '''
        if(direct.upper() == 'INCR'):
            self.sendCommand(':CONFigure:SWEep:DIRection INCReasing')
        elif(direct.upper() == 'DECR'):
            self.sendCommand(':CONFigure:SWEep:DIRection DECReasing')
        elif(direct.upper() == 'BINC'):
            self.sendCommand(':CONFigure:SWEep:DIRection BINCreasing')
#        self.sendCommand(':CONFigure:SWEep:FMINimum %s'%(direction.upper()))
        else:
            print('Please enter "INCR/DECR/BINC" to select the increasing/decreasing/bidirectional sweep of the laser.')
            return
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_DIR_q(self):
        '''
        This command returns the direction of the wavelength
        sweep of the laser.
        '''
        self.sendCommand(':CONFigure:SWEep:DIRection?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_POIN(self,points):
        '''
        This command sets the number of measurement points in a
        sweep.
        The number of points to use to compose a sweep. Use the
        keyword "MAXimum" in place of the number of <Points>
        to perform a non-decimated sweep of the
        laser with the largest number of sweep points. (integer,
        1-131071).
        '''
        self.sendCommand(':CONFigure:SWEep:POINts %s'%(points))
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_POIN_q(self):
        '''
        Returns the number of measurement points in a sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:POINts?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_WMAX(self,wavelength):
        '''
        Set the maximum wavelength of a sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:WMAXimum %s'%(wavelength))
        reply = self.readResponse()
        self._log.info(reply)
        return
        
    def cmd_CONF_SWE_WMAX_q(self):
        '''
        Returns the maximum wavelength of a sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:WMAXimum?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_FMAX(self,frequency):
        '''
        Set the maximum optical frequency of a sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:FMAXimum %s'%(frequency))
        reply = self.readResponse()
        self._log.info(reply)
        return
        
    def cmd_CONF_SWE_FMAX_q(self):
        '''
        Returns the maximum optical frequency of a sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:FMAXimum?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_RAT(self,rate):
        '''
        This command sets the sweep repetition rate.
        Sweep repetition rate (float, 1-10000, kHz).
        '''
        self.sendCommand(':CONFigure:SWEep:RATe %s'%(rate))
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_RAT_q(self):
        '''
        Returns the sweep repetition rate.
        '''
        self.sendCommand(':CONFigure:SWEep:RATe?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_DEL(self,delay):
        '''
        This command sets the inter-sweep delay time, during this
        time the laser output is attenuated until the next sweep
        starts.
        The inter-sweep delay time, during this time the laser output
        is attenuated
        (float, 0-655350, nanoseconds).
        '''
        self.sendCommand(':CONFigure:SWEep:DELay %s'%(delay))
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_DEL_q(self):
        '''
        This command queries the inter-sweep delay time, during
        this time the laser output is attenuated until the next sweep
        starts.
        '''
        self.sendCommand(':CONFigure:SWEep:DELay?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_POW(self,power):
        '''
        This command sets the average power level of the sweep.
        For a flat power profile, the average power = the flat power
        level. For a Gaussian profile with a full-width half-maximum
        equal to the scan range, the peak power of the Gaussian =
        1.235 * Average Power. Using the power calibration of
        milliwatts of power to counts, the entered average power is
        converted to counts, which the power-level routine uses as
        its target value.
        The average power level to set the laser to for sweeping
        (float, mW).
        '''
        self.sendCommand(':CONFigure:SWEep:POWer %s'%(power))
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_POW_q(self):
        '''
        Returns the average power of a sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:POWer?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_PROF(self,profile):
        '''
        This command set the power vs. table index profile.
        The Flat profile sets the optical power at each wavelength in
        a sweep equal to the average power level set in
        :CONFigure:SWEep:POWer.
        The Gaussian power profile sets the peak optical power at
        the center of the sweep range, with the peak power value
        determined by the average power requested with
        :CONFigure:SWEep:POWer.
        
        If CUSTom is the Profile Type, this is the data file to use.
        The data file should contain only floating point numbers in
        one column. When reading the data file: blank lines are
        ignored; the data is scaled to the number of points in the
        sweep; if the values are not in the range [0, 1], they will be
        normalized to the range [0, 1]; negative values are not
        accepted; more than 1 million entries are not accepted. If
        GAUSsian is the ProfileType, this is the power rollo at the
        beginning and end of the laser wavelength range, relative to
        the peak power at the center of the range
        
        (float, 1-10, dB). If not entered, the previously entered value
        will be used, or the default if there was no previously entered
        value.
        '''
        if(profile.upper() == 'FLAT'):
           self.sendCommand(':CONFigure:SWEep:PROFile FLAT')
        elif(profile.upper() == 'GAUSSIAN'):
           self.sendCommand(':CONFigure:SWEep:PROFile GAUSsian')
        elif(profile.upper() == 'CUSTOM'):
           self.sendCommand(':CONFigure:SWEep:PROFile CUSTom')
        else:
            print('Please enter "FLAT/GAUSSIAN/CUSTOM" to select the power profile type: flat, gaussian or custom.')
            return
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_PROF_q(self):
        '''
        Returns the power vs. wavelength profile.
        '''
        self.sendCommand(':CONFigure:SWEep:PROFile?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_TRIG(self,edge):
        '''
        This command sets the edge of the Start Sweep trigger that
        corresponds to the start of a wavelength sweep.
        Trigger edge setting (RISing, FALLing, BOTH).
        '''
        if(edge.upper() == 'RIS'):
           self.sendCommand(':CONFigure:SWEep:TRIGger RISing')
        elif(edge.upper() == 'FALL'):
           self.sendCommand(':CONFigure:SWEep:TRIGger FALLing')
        elif(edge.upper() == 'BOTH'):
           self.sendCommand(':CONFigure:SWEep:TRIGger BOTH')
        else:
            print('Please enter "RIS/FALL/BOTH" to set the edge of the Start Sweep trigger: rising, falling or both.')
            return
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_TRIG_q(self):
        '''
        This command returns the edge of the Start Sweep trigger
        that corresponds to the start of a wavelength sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:TRIGger?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    
####################
## 3) Calibrate the laser

    def cmd_CAL_SWE(self):    
        '''   
        This command initiates immediate calibration of a laser
        sweep. Also referred to as sweep calibration.
        '''
        self.sendCommand(':CALibrate:SWEep')
        reply = self.readResponse()
        self._log.info(reply)
        return reply
    
    def cmd_CONF_SWE_STEP(self,step):
        '''
        This command sets the sweep optical frequency step 
        between points in a sweep.
        Sweep step size (fl􏰥oat, .05-10000, GHz).
        '''
        self.sendCommand(':CONFigure:SWEep:STEP %s'%(step))
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_STEP_q(self):
        '''
        This command reads the optical frequency step 
        between points in a sweep.
        '''
        self.sendCommand(':CONFigure:SWEep:STEP?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
####################
## 4) Read the Data Invalid Vector (DIV) 
##    and the total number of points in the sweep
    
    def cmd_CONF_SWE_DIV_q(self):
        '''
        Reads the Data Invalid Vector (DIV) from the laser. 
        The DIV indicates in Sample Clocks where the optical
        frequency has not stepped and the data is invalid.
        '''
        self.sendCommand(':CONFigure:SWEep:DIVector?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SWE_POIN_TOT_q(self):
        '''
        This command returns the total number of points in
        the sweep, which equals the number of measurement 
        points (at which the optical frequency has changed 
        by a de􏰤ned interval) + the number of invalid points 
        (at which the optical frequency of the laser is not changing).
        '''
        self.sendCommand(':CONFigure:SWEep:POINts:TOTal?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
####################
## 5) Start a sweep
        
    def cmd_INIT_SWE(self):
        '''
        This command starts the laser sweep.
        '''
        self.sendCommand(':INITiate:SWEep')
        reply = self.readResponse()
        self._log.info(reply)
        return   

###################
## 6) To end the sweep and diable output  
        
    def cmd_ABOR(self):    
        '''    
        This command aborts the current operation and returns the
        laser to standby mode with no light exiting the laser to the
        user. This includes aborting calibration operations, such as:
        :CALibrate:SWEep
        :CALibrate:FACTory
        :CALibrate:RELAtive:SPLitref
        :CALibrate:DARK
        '''
        self.sendCommand(':ABORt')
        reply = self.readResponse()
        self._log.info(reply)
        return reply

#%% Command from the Insight-laser UI

    def cmd_SYST_CONT(self,mode):
        '''
        This sets the control mode of the device
        '''
        if(mode.upper() == 'HARD'):
           self.sendCommand(':SYSTem:CONTrol HARDware')
        elif(mode.upper() == 'SOFT'):
           self.sendCommand(':SYSTem:CONTrol SOFTware')
        else:
            print('Please enter "HARD/SOFT" to set the control mode of the device: Hardware or Software')
            return
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SCL_RAT(self,rate):
        '''
        This command speci􏰤es the rate of the external sample clock, 
        which is used for communicating to other instrumentation when 
        to sample data measured with a sweep of the laser.
        This command does not affect any other commands regarding points, 
        per point, or indices. Those commands will use the :SYSTem:CLOCk rate.
        See :SYSTem:CLOCk for the internal sample clock.
        A value below 112 MHz may result in undefined behavior.
        The rate to operate the external sample clock. 
        A value below 112 MHz may result in
        undefi􏰤ned behavior (float, 1-400, MHz).
        '''
        self.sendCommand(':CONFigure:SCLock:RATe %s'%(rate))
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SCL_RAT_q(self):
        '''
        This command returns the rate of the external sample clock, 
        which is used for communicating to other instrumentation 
        when to sample data measured with a sweep of the laser. 
        This command does not affect any other commands regarding points, 
        per point, or indices. Those commands will use the :SYSTem:CLOCk rate.
        See :SYSTem:CLOCk for the internal sample clock.
        '''
        self.sendCommand(':CONFigure:SCLock:RATe?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_SYST_ERR_ALL_q(self):
        '''
        Queries the error/event queue for all unread items and removes them 
        from the queue.
        '''
        self.sendCommand(':SYSTem:ERRor:ALL?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    
    def cmd_SYST_ERR_q(self):
        '''
        Queries the error/event queue for the next item and removes it from 
        the queue.
        '''
        self.sendCommand(':SYSTem:ERRor?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_SYST_ERR_NEXT_q(self):
        '''
        Queries the error/event queue for the next item and removes it from 
        the queue.
        '''
        self.sendCommand(':SYSTem:ERRor:NEXT?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_SYST_ERR_CODE_q(self):
        '''
        Queries the error/event queue for the next item, returns only the error 
        code and removes it from the queue.
        '''
        self.sendCommand(':SYSTem:ERRor:CODE?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_SYST_ERR_CODE_NEXT_q(self):
        '''
        Queries the error/event queue for the next item, returns only the error 
        code and removes it from the queue.
        '''
        self.sendCommand(':SYSTem:ERRor:CODE:NEXT?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_SYST_ERR_CODE_ALL_q(self):
        '''
        Queries the error/event queue for all unread items, returns only the error 
        codes and removes them from the queue.
        '''
        self.sendCommand(':SYSTem:ERRor:CODE:ALL?')
        reply = self.readResponse()
        self._log.info(reply)
        return
 
#######################################
        
### increasing
    def cmd_CONF_INCR_SBP(self,points,minwvl,maxwvl,interdelay):
        '''
        This command sets up an increasing sweep configuration
        with an emphasis on points.
        :CAL:SWE must be performed after issuing this command
        to get the desired effect.
        E.G. atlas ready> :CONF:SBP MAX, 1550 nm, 1555 nm, 0 ns
        :CONFigure:INCReasing:SBPoints 1033, 1550 nm, 1551 nm,
        0 ns
        =>
        '''
        self.sendCommand(':CONFigure:SBPoints %a,%s,%s,%s'%(points,minwvl,maxwvl,interdelay))
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_CONF_INCR_SBP_q(self):
        '''
        This command queries the current increasing sweep
        configuration with an emphasis on points.
        '''
        self.sendCommand(':CONFigure:SBPoints?')
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_CONF_INCR_SBR(self,rate,minwvl,maxwvl,interdelay):
        '''
        This command sets up an increasing sweep configuration
        with an emphasis on sweep rate.
        :CAL:SWE must be performed after issuing this command
        to get the desired effect.
        atlas ready> :CONF:SBR MIN
        :CONFigure:INCReasing:SBRate 8.57753 kHz, 1524.41 nm,
        1562.07 nm, 0 ns
        =>
        '''
        self.sendCommand(':CONFigure:SBRate %a,%s,%s,%s'%(rate,minwvl,maxwvl,interdelay))
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_CONF_INCR_SBR_q(self):
        '''
        This command queries the current increasing sweep
        configuration with an emphasis on rate.
        '''
        self.sendCommand(':CONFigure:SBRate?')
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_CONF_INCR_SBS(self,step,minwvl,maxwvl,interdelay):
        '''
        This command sets up an increasing sweep configuration
        with an emphasis on optical
        frequency step. :CAL:SWE must be performed after issuing
        this command to get the desired effect.
        atlas ready> :CONF:SBST .1, MIN, MAX, MIN
        :CONFigure:INCReasing:SBSTep .1 GHz, 1524.41 nm,
        1562.07 nm, 0 ns
        =>
        '''
        self.sendCommand(':CONFigure:SBSTep %a,%s,%s,%s'%(step,minwvl,maxwvl,interdelay))
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_CONF_INCR_SBS_q(self):
        '''
        This command queries the current increasing sweep
        configuration with an emphasis on optical frequency step.
        '''
        self.sendCommand(':CONFigure:SBSTep?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
#### decreasing    
    def cmd_CONF_DECR_SBP(self,points,minwvl,maxwvl,interdelay):
        '''
        This command sets up a decreasing sweep configuration
        with an emphasis on points.
        :CAL:SWE must be performed after issuing this command
        to get the desired effect.
        atlas ready> :CONF:DECR:SBP MAX, 1550 nm, 1555 nm,
        0 ns
        :CONFigure:DECReasing:SBPoints 1033, 1550 nm, 1551
        nm, 0 ns
        =>
        '''
        self.sendCommand(':CONFigure:DECReasing:SBPoints %a,%s,%s,%s'%(points,minwvl,maxwvl,interdelay))
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_CONF_DECR_SBP_q(self):
        '''
        This command queries the current decreasing sweep
        con
guration with an emphasis on points.
        '''
        self.sendCommand(':CONFigure:DECReasing:SBPoints?')
        reply = self.readResponse()
        self._log.info(reply)
        return		

    def cmd_CONF_DECR_SBR(self,rate,minwvl,maxwvl,interdelay):
        '''
        This command sets up an decreasing sweep configuration
        with an emphasis on sweep rate.
        :CAL:SWE must be performed after issuing this command
        to get the desired effect.
        atlas ready> :CONF:SBR MIN
        :CONFigure:INCReasing:SBRate 8.57753 kHz, 1524.41 nm,
        1562.07 nm, 0 ns
        =>
        '''
        self.sendCommand(':CONFigure:DECReasing:SBRate %a,%s,%s,%s'%(rate,minwvl,maxwvl,interdelay))
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_CONF_DECR_SBR_q(self):
        '''
        This command queries the current decreasing sweep
        configuration with an emphasis on rate.
        '''
        self.sendCommand(':CONFigure:DECReasing:SBRate?')
        reply = self.readResponse()
        self._log.info(reply)
        return	
		
    def cmd_CONF_DECR_SBS(self,step,minwvl,maxwvl,interdelay):
        '''
        This command sets up an decreasing sweep configuration
        with an emphasis on optical
        frequency step. :CAL:SWE must be performed after issuing
        this command to get the desired effect.
        atlas ready> :CONF:SBST .1, MIN, MAX, MIN
        :CONFigure:INCReasing:SBSTep .1 GHz, 1524.41 nm,
        1562.07 nm, 0 ns
        =>
        '''
        self.sendCommand(':CONFigure:DECReasing:SBSTep %a,%s,%s,%s'%(step,minwvl,maxwvl,interdelay))
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_CONF_DECR_SBS_q(self):
        '''
        This command queries the current decreasing sweep
        configuration with an emphasis on optical frequency step.
        '''
        self.sendCommand(':CONFigure:DECReasing:SBSTep?')
        reply = self.readResponse()
        self._log.info(reply)
        return   
    
#### bincreasing   
    def cmd_CONF_BINC_SBP(self,points,minwvl,maxwvl,interdelay):
        '''
        This command sets up a bidirectional sweep configuration
        with an emphasis on points.
        :CAL:SWE must be performed after issuing this command
        to get the desired effect.
        atlas ready> :CONF:DECR:SBP MAX, 1550 nm, 1555 nm,
        0 ns
        :CONFigure:DECReasing:SBPoints 1033, 1550 nm, 1551
        nm, 0 ns
        =>
        '''
        self.sendCommand(':CONFigure:BINCreasing:SBPoints %a,%s,%s,%s'%(points,minwvl,maxwvl,interdelay))
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_CONF_BINC_SBP_q(self):
        '''
        This command queries the current bidirectional sweep
        con
guration with an emphasis on points.
        '''
        self.sendCommand(':CONFigure:BINCreasing:SBPoints?')
        reply = self.readResponse()
        self._log.info(reply)
        return		

    def cmd_CONF_BINC_SBR(self,rate,minwvl,maxwvl,interdelay):
        '''
        This command sets up an bidirectional sweep configuration
        with an emphasis on sweep rate.
        :CAL:SWE must be performed after issuing this command
        to get the desired effect.
        atlas ready> :CONF:SBR MIN
        :CONFigure:INCReasing:SBRate 8.57753 kHz, 1524.41 nm,
        1562.07 nm, 0 ns
        =>
        '''
        self.sendCommand(':CONFigure:BINCreasing:SBRate %a,%s,%s,%s'%(rate,minwvl,maxwvl,interdelay))
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_CONF_BINC_SBR_q(self):
        '''
        This command queries the current bidirectional sweep
        configuration with an emphasis on rate.
        '''
        self.sendCommand(':CONFigure:BINCreasing:SBRate?')
        reply = self.readResponse()
        self._log.info(reply)
        return	
		
    def cmd_CONF_BINC_SBS(self,step,minwvl,maxwvl,interdelay):
        '''
        This command sets up an bidirectional sweep configuration
        with an emphasis on optical
        frequency step. :CAL:SWE must be performed after issuing
        this command to get the desired effect.
        atlas ready> :CONF:SBST .1, MIN, MAX, MIN
        :CONFigure:INCReasing:SBSTep .1 GHz, 1524.41 nm,
        1562.07 nm, 0 ns
        =>
        '''
        self.sendCommand(':CONFigure:BINCreasing:SBSTep %a,%s,%s,%s'%(step,minwvl,maxwvl,interdelay))
        reply = self.readResponse()
        self._log.info(reply)
        return

    def cmd_CONF_BINC_SBS_q(self):
        '''
        This command queries the current bidirectional sweep
        configuration with an emphasis on optical frequency step.
        '''
        self.sendCommand(':CONFigure:BINCreasing:SBSTep?')
        reply = self.readResponse()
        self._log.info(reply)
        return     
    
    def cmd_CONF_SWE_POIN_INCR(self,multiple):
        '''
        This command sets the number of points by which the
        sweep should be divisible. Valid options
        are from 4-256 in increments of 4.
        '''
        self.sendCommand(':CONFigure:SWEep:POINts:INCRement %s'%(multiple))
        reply = self.readResponse()
        self._log.info(reply)
        return 
    
    def cmd_CONF_SWE_POIN_INCR_q(self):
        '''
        Returns the number of points by which the sweep is divisible.
        '''
        self.sendCommand(':CONFigure:SWEep:POINts:INCRement?')
        reply = self.readResponse()
        self._log.info(reply)
        return   
    
###############################################
## Sequence mode 
    def cmd_CONF_SEQ_q(self):
        '''
        This command queries the list of wavelength/frequency data
        in the sequence sweep and how much time is spent on each
        wavelength/frequency before moving on to the next point.
        '''
        self.sendCommand(':CONFigure:SEQuence?')
        reply = self.readResponse()
        self._log.info(reply)
        return 
    
    def cmd_CONF_SEQ_CLEA(self):
        '''
        This command clears all the wavelengths/frequencies in the
        sequence sweep.
        '''
        self.sendCommand(':CONFigure:SEQuence:CLEAr')
        reply = self.readResponse()
        self._log.info(reply)
        return         
    
    def cmd_CONF_SEQ_ADD_WST(self,step,length,startwvl,stopwvl,position=-1): 
        '''
        This command appends a series of wavelengths to the
        sequence sweep and sets the amount of time to spend at
        each desired wavelength/frequency.
        STEP: The step value to increment by to add entries to the
        sequence sweep (in nanometers).
        LENGTH: The amount of time, in nanoseconds, to sit at the desired
        wavelength.
        STARWVL: The starting wavelength for the new entries (nanometers,
        defaults to minimum wavelength).
        STOPWVL: The stopping wavelength for the new entries (nanometers,
        defaults to maximum wavelength).
        POSITION: The position in the sequence table to add the wavelength
        (defaults to the end: -1).
        '''
        self.sendCommand(':CONFigure:SEQuence:ADD:WSTep %a,%s,%s,%s,%g' %(step,length,startwvl,stopwvl,position))
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SEQ_ADD_FST(self,step,length,startfqc,stopfqc,position=-1):    
        '''
        This command appends a series of wavelengths to the
        sequence sweep and sets the amount of time to spend at
        each desired wavelength/frequency.
        STEP: The step value to increment by to add entries to the
        sequence sweep (in nanometers).
        LENGTH: The amount of time, in nanoseconds, to sit at the desired
        wavelength.
        STARFQC: The starting frequency for the new entries (nanometers,
        defaults to minimum wavelength).
        STOPFQC: The stopping frequency for the new entries (nanometers,
        defaults to maximum wavelength).
        POSITION: The position in the sequence table to add the wavelength
        (defaults to the end: -1).
        '''
        self.sendCommand(':CONFigure:SEQuence:ADD:FSTep %a,%s,%s,%s,%g' %(step,length,startfqc,stopfqc,position))
        reply = self.readResponse()
        self._log.info(reply)
        return    
    
    def cmd_CONF_SEQ_INT(self,onoff):
        '''
        Whether or not wavelength interpolation will be performed
        for sequence mode (boolean). Default to o.
        '''
        if(onoff.upper() == 'ON'):
           self.sendCommand(':CONFigure:SEQuence:INTerpolation ON')
        elif(onoff.upper() == 'OFF'):
           self.sendCommand(':CONFigure:SEQuence:INTerpolation OFF')
        else:
            print('Please enter "ON/OFF" to set turn on/off the wavelength interpolation for sequence mode')
            return
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SEQ_ADD_WAV(self,value,length,position=-1):
        '''
        This command appends a wavelength to the
        sequence sweep and sets the amount of time to spend at
        that desired wavelength/frequency. It can be used to created 
        step-by-step via command
        '''
        self.sendCommand(':CONFigure:SEQuence:ADD:WAVelength %a,%s,%s' %(value,length,position))
        reply = self.readResponse()
        self._log.info(reply)
        return   
    
    def cmd_CONF_SEQ_LOAD(self,filename):
        '''
        This command imports the sequence sweep table containing
        the set of wavelengths/frequencies and how much time to
        spend at each desired wavelength/frequency.
        '''
        self.sendCommand(':CONFigure:SEQuence:LOAD %a' %(filename))
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_SEQ_SAV(self,filename):
        '''
        This command exports the sequence sweep table containing
        the set of wavelengths/frequencies and how much time to
        spend at each desired wavelength/frequency.
        '''
        self.sendCommand(':CONFigure:SEQuence:SAVe %a' %(filename))
        reply = self.readResponse()
        self._log.info(reply)
        return    
    
    def cmd_CONF_SEQ_POW(self,power):
        '''
        This command sets the output power of the laser in
        sequence mode, using units of mW.
        For the new power value to take effect, the user must
        command the laser to calibrate the power for all sequence
        wavelengths using :CALibrate:SEQuence.
        The average power level to set the laser to for sequence
        mode (float, mW).
        '''
        self.sendCommand(':CONFigure:SEQuence:POWer %s' %(power))
        reply = self.readResponse()
        self._log.info(reply)
        return 
        
    def cmd_CONF_SEQ_POW_q(self):
        '''
        This command returns the output power of the laser in
        sequence wavelength mode, using units of mW.
        '''
        self.sendCommand(':CONFigure:SEQuence:POWer?')
        reply = self.readResponse()
        self._log.info(reply)
        return     
    
    def cmd_CONF_SEQ_REM(self,ID):
        '''
        This command removes the requested entry from the
        sequence sweep table, the id is a zero-based row index
        indicating which entry to remove (0 removes the 
        rst entry).
        The special value '-1' removes the last entry from the table.
        '''
        self.sendCommand(':CONFigure:SEQuence:REMove %s' %(ID))
        reply = self.readResponse()
        self._log.info(reply)
        return         
    
    def cmd_CAL_SEQ(self):
        '''
        This command calibrates the laser to operate at the specified
        average power and profile in Sequence Mode. User input
        values for sequences of wavelengths/frequencies to sweep
        are not applied until :CALibrate:SEQuence is executed.
        '''
        self.sendCommand(':CALibrate:SEQuence')
        reply = self.readResponse()
        self._log.info(reply)
        return    

    def cmd_CAL_SEQ_q(self):
        '''
        This command queries the results of the last sequence
        calibration.
        '''
        self.sendCommand(':CALibrate:SEQuence?')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_INIT_SEQ(self):
        '''
        This command sets the laser into Sequence mode. In
        Sequence mode the laser steps between a a predefined set of
        wavelengths/frequencies.
        '''
        self.sendCommand(':INITiate:SEQuence')
        reply = self.readResponse()
        self._log.info(reply)
        return        
###############################################################################
## For fixed wavelength mode
    def cmd_CAL_FIX(self):
        '''
        This command calibrates the laser to operate at the
        specified average power and profile in Fixed Wavelength
        Mode. User input values for average power and profile are
        not changed until :CALibrate:FIXed is executed.
        '''
        self.sendCommand(':CALibrate:FIXed')
        reply = self.readResponse()
        self._log.info(reply)
        return   
    def cmd_CAL_FIX_q(self):
        '''
        This command queries the state of the last 
xed calibration.
        '''
        self.sendCommand(':CALibrate:FIXed?')
        reply = self.readResponse()
        self._log.info(reply)
        return     
 
    def cmd_CONF_FIX_DEL(self,Delay):
        '''
        The delay time between receiving a wavelength value and
        when the Data Valid signal will
        be set to a logic high value (float, 0-100000, microseconds).
        '''
        self.sendCommand(':CONFigure:FIXed:DELay %s' %(Delay))
        reply = self.readResponse()
        self._log.info(reply)
        return      
    
    def cmd_CONF_FIX_DEL_q(self):
        '''
        This command queries the delay between receiving a set
        wavelength value and when the Data Valid trigger is raised
        to high, indicating to external user hardware that the laser
        has reached the desired wavelength.
        '''
        self.sendCommand(':CONFigure:FIXed:DELay?')
        reply = self.readResponse()
        self._log.info(reply)
        return      

    def cmd_CONF_FIX_FREQ(self,frequency):
        '''
        This commands the laser to a 
xed optical frequency in
        units of THz.
        '''
        self.sendCommand(':CONFigure:FIXed:FREQuency %s' %(frequency))
        reply = self.readResponse()
        self._log.info(reply)
        return  
    
    def cmd_CONF_FIX_FREQ_q(self):
        '''
        This command returns the optical frequency of the laser in
        Terahertz when in Fixed wavelength mode.
        '''
        self.sendCommand(':CONFigure:FIXed:FREQuency?')
        reply = self.readResponse()
        self._log.info(reply)
        return     
    
    def cmd_CONF_FIX_WAV(self,wavelength):
        '''
        This commands the laser to a fixed optical wavelength in
        units of nm.
        '''
        self.sendCommand(':CONFigure:FIXed:WAVelength %s' %(wavelength))
        reply = self.readResponse()
        self._log.info(reply)
        return  
    
    def cmd_CONF_FIX_WAV_q(self):
        '''
        This command returns the optical wavelength of the laser in
        nm when in Fixed wavelength mode.
        '''
        self.sendCommand(':CONFigure:FIXed:WAVelength?')
        reply = self.readResponse()
        self._log.info(reply)
        return     
    
    def cmd_CONF_FIX_POW(self,power):
        '''
        This command sets the output power of the laser in 
xed
        wavelength mode, using units of mW.
        For the new power value to take eect, the user must
        command the laser to calibrate the power for all 
xed
        wavelengths using :CALibrate:FIXed.
        '''
        self.sendCommand(':CONFigure:FIXed:POWer %s' %(power))
        reply = self.readResponse()
        self._log.info(reply)
        return     
    
    def cmd_CONF_FIX_POW_q(self):
        '''
        This command returns the output power of the laser in 
xed
        wavelength mode, using units of mW.
        '''
        self.sendCommand(':CONFigure:FIXed:POWer?')
        reply = self.readResponse()
        self._log.info(reply)
        return  
    
    def cmd_CONF_FIX_PROF(self,profile,power=3):
        '''
        If CUSTom is the Profile Type, this is the data file to use.
        The data file should contain only floating point numbers in
        one column. When reading the data file: blank lines are
        ignored; the data is scaled to the number of points in the
        sweep; if the values are not in the range [0, 1], they will be
        normalized to the range [0, 1]; negative values are not
        accepted; more than 1 million entries are not accepted. If
        GAUSsian is the Profile Type, this is the power rolloff at the
        beginning and end of the laser wavelength range, relative to
        the peak power at the center of the range.
        (float, 1-10, dB). If not entered, the previously entered value
        will be used, or the default if there was no previously entered
        value.
        ''' 
        if(profile.upper() == 'FLAT'):
           self.sendCommand(':CONFigure:FIXed:PROFile FLAT')
        elif(profile.upper() == 'GAUSSIAN'):
           self.sendCommand(':CONFigure:FIXed:PROFile GAUSsian,%s' %(power))
        elif(profile.upper() == 'CUSTOM'):
           self.sendCommand(':CONFigure:FIXed:PROFile CUSTom,%s' %(power))
        else:
            print('Please enter "FLAT/GAUSSIAN/CUSTOM" to set profile type for fixed wavelength mode')
            return
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    def cmd_CONF_FIX_PROF_q(self):
        '''
        This command returns the power vs. wavelength profile of
        the laser in Fixed Wavelength mode.
        '''
        self.sendCommand(':CONFigure:FIXed:PROFile?')
        reply = self.readResponse()
        self._log.info(reply)
        return    
    
    def cmd_INIT_FIX(self):
        '''
        This command sets the laser into a fixed wavelength mode.
        In Fixed mode, the laser may be output to the user or
        switched off to the user and remain internal to the laser.
        Fixed mode has its own Calibration that must be performed
        when the average power, power spectral profile or coherence
        length is changed.
        '''
        self.sendCommand(':INITiate:FIXed')
        reply = self.readResponse()
        self._log.info(reply)
        return
    
    
    
    
    
    
    
    
    
    
    
    
# this part needs to be at the end of the file. 
		
if __name__ == "__main__": 
	laser = insightLaser()
	
#	a.connect()
#	a.cmd_CLS()
    
