#!/usr/bin/env python3
from DL3021 import DL3021
import pyvisa
import time
import json

if __name__ == "__main__":

    modeSend = input("Enter modeSend\nChoose from [Continuous, Burst, File]\n")

    # Setting Load mode and initial output values
    modeSet = "CURRENT"
    power = 0
    current = 0

    # Slew Rate settings for corresponding Current Range:
    # 2.5A/us is max for 40A range
    # 0.25A/us is max for 4A range
    slewRate = 2.5
    rangeVal = 6

    # Finding resource(instrument) from pyvisa resource manager
    # Using found resource to create object of DL3021 class
    rm = pyvisa.ResourceManager()
    res = rm.open_resource('USB0::6833::3601::DL3A26CM00318::0::INSTR')
    DL3021load = DL3021(res=res,
                        mode_set=modeSet,
                        power=power,
                        current=current,
                        slew_rate=slewRate,
                        range_val=rangeVal)

    

    match modeSend:
        case "1":

            use_old_data = input("Use Old Data (y or n)?\n")
            print(type(use_old_data))

            if use_old_data == "y":
                with open('input_data_continuous_mode.json', 'r') as f:
                    input_data = json.load(f)
                    t_period = input_data["data"]['t_period']
                    current_step = input_data["data"]['current_step']
                    current = input_data["data"]["current"]
                    current_limit = input_data["data"]["current_limit"]

            elif use_old_data == "n":
                print("Using New Data")
                t_period, current_step, current, current_limit = map(float, (input(
                    "[t_period (Seconds)]  [current step (Amps)]  [initial current value (Amps)]  [upper current limit (Amps)]\n").split()))

                with open('input_data_continuous_mode.json', 'w') as f:
                    json.dump({"data": {"t_period": t_period,
                                        "current_step": current_step,
                                        "current": current,
                                        "current_limit": current_limit}},
                              fp=f, indent=2)
            else:
                print(f"Unexpected Character: {use_old_data}\n")
                quit()

            DL3021load.DL3KOBJ.set_cc_current(current)
            v_init = DL3021load.DL3KOBJ.voltage()
            DL3021load.DL3KOBJ.enable()

            while ((DL3021load.DL3KOBJ.voltage()/v_init) > 0.80
                   and (current < current_limit)):
                try:
                    current += current_step
                    DL3021load.DL3KOBJ.set_cc_current(
                        current
                    )
                    print(f'Set C: {current}')

                    if (DL3021load.DL3KOBJ.voltage() / v_init) < 0.80:

                        print("Voltage Out Of Spec")
                        print(DL3021load.DL3KOBJ.current())
                    time.sleep(t_period)
                    print(f'Load C: {DL3021load.DL3KOBJ.current()}')

                except KeyboardInterrupt:
                    print("Ending Program Manually")
                    DL3021load.DL3KOBJ.disable()
                    break

            DL3021load.DL3KOBJ.disable()

        case "2":
            use_old_data = input("Use Old Data (y or n)?\n")
            print(type(use_old_data))

            if use_old_data == "y":
                with open('input_data_burst_mode.json', 'r') as f:
                    input_data = json.load(f)
                    idle_current = input_data["data"]['idle_current']
                    t_period = input_data["data"]['t_period']
                    t_period_decrement = input_data["data"]["t_period_decrement"]
                    burst_current_list = input_data["data"]["burst_current_list"]
                    t_blip = input_data["data"]["t_blip"]

            elif use_old_data == "n":
                print("Use New Data")
                idle_current, t_period, t_period_decrement, t_blip =
                map(
                    float, (
                        input("[idle_current (Amps)]  [t_period (seconds)]  [t_period_decrement (seconds)]  [t_blip (seconds)]\n").split()))
                burst_current_list = map(
                    float, input("[burst_current_list (Amps)]"))

                with open('input_data_continuous_mode.json', 'w') as f:
                    json.dump({"data":
                               {"idle_current": idle_current,
                                "t_period": t_period,
                                "t_period_decrement": t_period_decrement,
                                "t_blip": t_blip,
                                "burst_current_list": burst_current_list}},
                              fp=f, indent=2)
            else:
                print(f"Unexpected Character: {use_old_data}\n")
                quit()

            idle_current = float(input("Idle current in Amps\n"))
            t_period = float(input("t_period in seconds\n"))
            t_period_decrement = float(
                input("Decrement value for t_period in seconds\n"))
            burst_current_list = map(float, input(
                "Burst current in Amps\n").split())
            t_blip = float(input("t_blip in seconds\n"))

            temp_t_period = t_period

            DL3021load.DL3KOBJ.enable()
            try:
                for burst_current in burst_current_list:
                    while (temp_t_period > 0):
                        DL3021load.DL3KOBJ.set_cc_current(idle_current)
                        time.sleep(temp_t_period)
                        DL3021load.DL3KOBJ.set_cc_current(burst_current)
                        time.sleep(t_blip)
                        temp_t_period -= t_period_decrement

                    DL3021load.DL3KOBJ.set_cc_current(burst_current)
                    temp_t_period = t_period
                    time.sleep(temp_t_period)
                    idle_current = burst_current

            except KeyboardInterrupt:
                print("Ending Program Manually")
                DL3021load.DL3KOBJ.disable()

            DL3021load.DL3KOBJ.disable()

        case "3":
            
            # File with averaged output values
            filename = "conv.csv"
            DL3021load.fileRead(filename=filename)
            try:
                print("Attempting Send Sequence")
                DL3021load.loadSndSqnce(modeSet)

            except KeyboardInterrupt:
                print("Program Exited Manually")
