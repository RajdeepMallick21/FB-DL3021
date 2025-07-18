#!/usr/bin/env python3

__all__ = ["DL3000"]

class DL3000(object):
    """
    Rigol DL3000 command wrapper.
    """
    def __init__(self, inst):
        """
        Initialize the DL3000 wrapper with a specific PyVISA resource.
        This class does NOT open the resource, you have to open it for yourself!
        """
        self.inst = inst

    def voltage(self):
        # My DL3021 returns a string like '0.000067\n0'
        return float(self.inst.query(":MEAS:VOLT?").partition("\n")[0])

    def current(self):
        # My DL3021 returns a string like '0.000067\n0'
        return float(self.inst.query(":MEAS:CURR?").partition("\n")[0])

    def power(self):
        # My DL3021 returns a string like '0.000067\n0'
        return float(self.inst.query(":MEAS:POW?").partition("\n")[0])

    def resistance(self):
        # My DL3021 returns a string like '0.000067\n0'
        return float(self.inst.query(":MEAS:RES?").partition("\n")[0])

    def set_cc_slew_rate(self, slew):
        # My DL3021 returns a string like '0.000067\n0'
        self.inst.write(f":SOURCE:CURRENT:SLEW {slew}")
    
    def is_enabled(self):
        """
        Enable the electronic load
        Equivalent to pressing "ON/OFF" when the load is ON
        """
        return self.inst.query(":SOURCE:INPUT:STAT?").strip() == "1"

    def enable(self):
        """
        Enable the electronic load
        Equivalent to pressing "ON/OFF" when the load is ON
        """
        self.inst.write(":SOURCE:INPUT:STAT ON")

    def disable(self):
        """
        Disable the electronic load
        Equivalent to pressing "ON/OFF" when the load is ON
        """
        self.inst.write(":SOURCE:INPUT:STAT OFF")

    def set_mode(self, mode="CC"):
        """
        Set the load mode to "CURRENT", "VOLTAGE", "RESISTANCE", "POWER"
        """
        self.inst.write(":SOURCE:FUNCTION {}".format(mode))

    def query_mode(self):
        """
        Get the mode:
        "CC", "CV", "CR", "CP"
        """
        return self.inst.query(":SOURCE:FUNCTION?").strip()

    def set_cc_current(self, current):
        """
        Set CC current limit
        """
        return self.inst.write(":SOUR:CURR:LEV:IMM {}".format(current))

    def set_cp_power(self, power):
        """
        Set CP power limit
        """
        return self.inst.write(":SOURCE:POWER:LEV:IMM {}".format(power))

    def set_cp_ilim(self, ilim):
        """
        Set CP current limit
        """
        return self.inst.query(":SOURCE:POWER:ILIM {}".format(ilim))

    def cc(self, current, activate=True):
        """
        One-line constant-current configuration.
        if activate == True, also turns on the power supply
        """
        self.set_mode("CC")
        self.set_cc_current(current)
        self.enable()
        
    def cp(self, power, activate=True):
        """
        One-line constant-current configuration.
        if activate == True, also turns on the power supply
        """
        self.set_mode("POWER")
        self.set_cp_power(power)
        self.enable()

    def reset(self):
        self.inst.write("*RST")
    
    def identity(self):
        return self.inst.query("*IDN?")
    
    def self_test(self):
        return self.inst.query("*TST?")
    
    def set_cc_range(self, set_range):
        self.inst.write(f":SOUR:CURR:RANG {set_range}")

    def check_error(self):
        print("Checking Error")
        print(self.inst.query(f"*ESR?"))
        print("Done Checking")

    
    # Sets running mode of load in list operation
    def set_list_mode(self, mode):
        self.inst.write(f":SOUR:LIST:MODE {mode}")
        # print(f"List Mode: {self.inst.query(":SOUR:LIST:MODE?")}")

    # Sets range for each running mode
    def set_list_range(self, range):
        self.inst.write(f":SOUR:LIST:RANG {range}")
        # print(f"List Range: {self.inst.query(":SOUR:LIST:RANGE?")}")
    
    # Sets number of times the list is cycled
    def set_list_count_infinity(self):
        self.inst.write(":SOUR:LIST:COUN 0")
        # print(f"List Count: {self.inst.query(":SOUR:LIST:COUNT?")}")

    def set_list_step(self, steps):
        self.inst.write(f":SOUR:LIST:STEP {steps}")
        # print(f"List Step:{self.inst.query(":SOUR:LIST:STEP?")}")

    def set_list_level(self, steps, levelList):
        for step in range(steps):
            self.inst.write(f":SOUR:LIST:LEV {step},{levelList[step]}")
        
    def set_list_width(self, steps, listWidth):
        for step in range(steps):
            self.inst.write(f":SOUR:LIST:WID {step},{listWidth}")
    
    def set_list_slew(self, steps, listSlew):
        for step in range(steps):
            self.inst.write(f":SOUR:LIST:SLEW {step},{listSlew}")
    
    def set_list_end(self, endState):
        self.inst.write(f":SOUR:LIST:END {endState}")

    def trig_immediate(self):
        print("Triggering Immediately")
        self.inst.write(":TRIG:IMM")
        # self.inst.write("*TRG")

    def trig_source(self, trigSrc):
        self.inst.write(f":TRIG:SOUR {trigSrc}")
    
    def get_trig_mode(self):
        return self.inst.query(f":TRIGGER:SOURCE?")
    
    def set_tran(self):
        self.inst.write(":SOUR:TRAN:STAT 1")
        print(f"Tran status is {self.inst.query(":SOUR:TRAN:STAT?")}")
    



