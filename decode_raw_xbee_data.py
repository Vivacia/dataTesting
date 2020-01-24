import sys
import datetime
import binascii
from cobs import cobs
import codecs
import struct

def main():
    if len(sys.argv) != 2:
        print('Usage:')
        print('debug.py <raw xbee file>')
        quit()
    # countGood = 0
    # countBad = 0
    f = open(sys.argv[1])
    next(f)
    for line in f.readlines():
        """
        need only one for loop as opposed to two in the previous code;
        it gets rid of the 0x00 for me and I need not deal with it
        """
        raw_data = line.split(",")
        """
        So, here I have:
        raw_data[0] = timestamp
        raw_data[1] = CAN ID
        raw_data[2] = length of data
        raw_data[3] = actual data
        as of now, no use for the timestamp
        """
        print("CAN ID:        0x" + raw_data[1])
        print("MSG LEN:       " + raw_data[2])
        print(raw_data)

        #to segregate the data
        if (raw_data[1] == "A0"):
            #Motor Controller Temperatures #1, ID_MC_TEMPERATURES_1
            print("MODULE A TEMP: " + str(int(hex(raw_data[3][0:2])) / 10.) + " C")
            print("MODULE B TEMP: " + str(int(hex(raw_data[3][2:4])) / 10.) + " C")
            print("MODULE C TEMP: " + str(int(hex(raw_data[3][4:6])) / 10.) + " C")
            print("GATE DRIVER BOARD TEMP: " + str(int(hex(raw_data[3][6:8])) / 10.) + " C")
        elif (raw_data[1] == "A1"):
            #Motor Controller Temperatures #2, ID_MC_TEMPERATURES_2
        elif (raw_data[1] == "A2"):
            print("RTD 4 TEMP: " + str(int(hex(raw_data[3][0:2])) / 10.) + " C")
            print("RTD 5 TEMP: " + str(int(hex(raw_data[3][2:4])) / 10.) + " C")
            print("MOTOR TEMP: " + str(int(hex(raw_data[3][4:6])) / 10.) + " C")
            print("TORQUE SHUDDER: " + str(int(hex(raw_data[3][6:8])) / 10.) + " Nm")
        elif (raw_data[1] == "A3"):
            #MC Analog Inputs Voltages, ID_MC_ANALOG_INPUTS_VOLTAGES
            print("ANALOG INPUT 1: " + str(int(hex(raw_data[3][0:2])) / 1.) + " V")
            print("ANALOG INPUT 2: " + str(int(hex(raw_data[3][2:4])) / 1.) + " V")
            print("ANALOG INPUT 3: " + str(int(hex(raw_data[3][4:6])) / 1.) + " V")
            print("ANALOG INPUT 4: " + str(int(hex(raw_data[3][6:8])) / 1.) + " V")
        elif (raw_data[1] == "A4"):
            #A4: MC Digital Input Status, ID_MC_DIGITAL_INPUT_STATUS
            print("DIGITAL INPUT 1: " + raw_data[3][0])
            print("DIGITAL INPUT 2: " + raw_data[3][1])
            print("DIGITAL INPUT 3: " + raw_data[3][2])
            print("DIGITAL INPUT 4: " + raw_data[3][3])
            print("DIGITAL INPUT 5: " + raw_data[3][4])
            print("DIGITAL INPUT 6: " + raw_data[3][5])
            print("DIGITAL INPUT 7: " + raw_data[3][6])
            print("DIGITAL INPUT 8: " + raw_data[3][7])
        elif (raw_data[1] == "A5"):
            #A5: MC Motor Position Information, ID_MC_MOTOR_POSITION_INFORMATION
            print("MOTOR ANGLE: " + str(int(hex(raw_data[3][0:2]) / 10.)))
            print("MOTOR SPEED: " + str(int(hex(raw_data[3][2:4]))) + " RPM")
            print("ELEC OUTPUT FREQ: " + str(int(hex(raw_data[3][4:6])) / 10.))
            print("DELTA RESOLVER FILT: " + str(int(hex(raw_data[3][6:8]))))
        elif (raw_data[1] == "A6"):
            #A6: MC Current Information, ID_MC_CURRENT_INFORMATION
            print("PHASE A CURRENT: " + str(int(hex(raw_data[3][0:2])) / 10.) + " A")
            print("PHASE B CURRENT: " + str(int(hex(raw_data[3][2:4])) / 10.) + " A")
            print("PHASE C CURRENT: " + str(int(hex(raw_data[3][4:6])) / 10.) + " A")
            print("DC BUS CURRENT: " + str(int(hex(raw_data[3][6:8])) / 10.) + " A")
        elif (raw_data[1] == "A7"):
            #A7: MC Voltage Information, ID_MC_VOLTAGE_INFORMATION
            print("DC BUS VOLTAGE: " + str(int(hex(raw_data[3][0:2])) / 1.) + " V")
            print("OUTPUT VOLTAGE: " + str(int(hex(raw_data[3][2:4])) / 10.) + " V")
            print("PHASE AB VOLTAGE: " + str(int(hex(raw_data[3][4:6])) / 10.) + " V")
            print("PHASE BC VOLTAGE: " + str(int(hex(raw_data[3][6:8])) / 10.) + " V")
        elif (raw_data[1] == "A8"):
            #A8: MC Flux Information, ID_MC_FLUX_INFORMATION
            print("MODULATION INDEX: " + str(int(hex(raw_data[3][0:2]))))
            print("FLUX WEAKENING OUTPUT: " + str(int(hex(raw_data[3][2:4]))))
            print("ID COMMAND: " + str(int(hex(raw_data[3][4:6]))))
            print("IQ COMMAND: " + str(int(hex(raw_data[3][6:8]))))
        elif (raw_data[1] == "A9"):
            #A9: MC Internal Voltages, ID_MC_INTERNAL_VOLTAGES
            print("VSM STATE: " + str(int(hex(raw_data[3][0:2]))))
            print("INVERTER STATE: " + str(int(hex(raw_data[3][2]))))
            print("RELAY STATE: " + str(int(hex(raw_data[3][3]))))
            print("INVERTER RUN MODE DISCHARGE STATE: " + str(int(hex(raw_data[3][4]))))
            print("INVERTER COMMAND MODE: " + str(int(hex(raw_data[3][5]))))
            print("INVERTER ENABLE: " + str(int(hex(raw_data[3][6]))))
            print("DIRECTION COMMAND: " + str(int(hex(raw_data[3][7]))))
        elif (raw_data[1] == "AA"):
            #AA: MC Internal States: ID_MC_INTERNAL_STATES
            print("VSM STATE: " + str(int(raw_data[3][0:2])))
            print("INVERTER STATE: " + str(int(raw_data[3][2])))
            #'{0:08b}'.format(6)
            print("INVERTER RUN MODE: " + str(int(hex(raw_data[3][4])) & 0x1))
            print("INVERTER ACTIVE DISCHARGE STATE: " + str((int(hex(raw_data[3][4])) & 0xE0) >> 5))
            print("INVERTER COMMAND MODE: " + str(int(hex(raw_data[3][5]))))
            print("INVERTER ENABLE: " + str(int(hex(raw_data[3][6]) & 0x1)))
            print("INVERTER LOCKOUT: " + str((int(hex(raw_data[3][6])) & 0x80) >> 7))
            print("DIRECTION COMMAND: " + str(int(hex(raw_data[3][7]))))
        elif (raw_data[1] == "AB"):
            #AB: MC Fault Codes, ID_MC_FAULT_CODES
            print("POST FAULT LO: 0x" + raw_data[3][1].upper() + raw_data[3][0].upper())
            print("POST FAULT HI: 0x" + raw_data[3][3].upper() + raw_data[3][2].upper())
            print("RUN FAULT LO: 0x" + raw_data[3][5].upper() + raw_data[3][4].upper())
            print("RUN FAULT HI: 0x" + raw_data[3][7].upper() + raw_data[3][6].upper())
        elif (raw_data[1] == "AC"):
            #AC: MC Torque Timer Information, ID_MC_TORQUE_TIMER_INFORMATION
            print("COMMANDED TORQUE: " + str(int(hex(raw_data[3][0:2])) / 10.) + " Nm")
            print("TORQUE FEEDBACK: " + str(int(hex(raw_data[3][2:4])) / 10.) + " Nm")
            print("RMS UPTIME: " + str(int(hex(raw_data[3][4:8])) * .003) + " s")
        elif (raw_data[1] == "AD"):
            #AD: MC Modulation Index Flux Weakening Output Information,
            #ID_MC_MODULATION_INDEX_FLUX_WEAKENING_OUTPUT_INFORMATION
        elif (raw_data[1] == "AE"):
            #AE: MC Firmware Information, ID_MC_FIRMWARE_INFORMATION
        elif (raw_data[1] == "AF"):
            #AF: MC Diagnostic Data, ID_MC_DIAGNOSTIC_DATA
        elif (raw_data[1] == "C0"):
            #C0: MC Command Message, ID_MC_COMMAND_MESSAGE
            print("FCU REQUESTED TORQUE: " + str(int(hex(raw_data[3][0:2])) / 10.) + " N")
            #print("FCU REQUESTED INVERTER ENABLE: " + str(ord(msg[10]) & 0x1))
        elif (raw_data[1] == "C1"):
            #C1: MC Read/Write Parameter Command, ID_MC_READ_WRITE_PARAMETER_COMMAND
        elif (raw_data[1] == "C2"):
            #C2: MC Read/Write Parameter Response, ID_MC_READ_WRITE_PARAMETER_RESPONSE
        elif (raw_data[1] == "C3"):
            #stuff
        elif (raw_data[1] == "C4"):
            #stuff
        elif (raw_data[1] == "CC"):
            #CC: GLV Current Readings, ID_GLV_CURRENT_READINGS
        """
        obsolete:
        elif (raw_data[1] == "D0"):
            #D0: Rear Control Unit Status, ID_RCU_STATUS
            print("RCU STATE: " + str(int(hex(raw_data[3][5]))))
            print("RCU FLAGS: 0x" + raw_data[3][1].upper())
            print("GLV BATT VOLTAGE: " + str(int(hex(raw_data[3][2:4])) / 100.) + " V")
            print("RCU BMS FAULT: " + str(not (bin(int(hex(raw_data[3][1]))) & 0x1)))
            print("RCU IMD FAULT: " + str(not (bin(int(hex(raw_data[3][1]))) & 0x2) >> 1))
        elif (raw_data[1] == "D2"):
            #D2: Front Control Unit Status, ID_FCU_STATUS
            print("FCU STATE: " + str(int(hex(raw_data[3][0]))))
            print("FCU FLAGS: 0x" + raw_data[3][1].upper())
            print("FCU START BUTTON ID: " + str(int(hex(raw_data[3][2]))))
            print("FCU BRAKE ACT: " + str(bin(int(raw_data[3][1])) & 0x8) >> 3)
            print("FCU IMPLAUS ACCEL: " + str(bin(int(hex(raw_data[3][1]))) & 0x1))
            print("FCU IMPLAUS BRAKE: " + str((bin(int(hex(raw_data[3][1]))) & 0x4) >> 2))
        """
        elif (raw_data[1] == "D3"):
            #D3: ID_FCU_READINGS
            print("FCU PEDAL ACCEL 1: " + str(int(hex(raw_data[3][0:2]))))
            print("FCU PEDAL ACCEL 2: " + str(int(hex(raw_data[3][2:4]))))
            print("FCU PEDAL BRAKE: " + str(int(hex(raw_data[3][4:6]))))
        elif (raw_data[1] == "D5"):
            #D5: Battery Monitoring System Onboard Temps, ID_BMS_ONBOARD_TEMPERATURES
        elif (raw_data[1] == "D6"):
            #D6: BMS Onboard Detailed Temps, ID_BMS_ONBOARD_DETAILED_TEMPERATURES
        elif (raw_data[1] == "D7"):
            #D7: BMS Voltages, ID_BMS_VOLTAGES
            print("BMS VOLTAGE AVERAGE: " + str(int(hex(raw_data[3][0:2])) / 10e3) + " V")
            print("BMS VOLTAGE LOW: " + str(int(hex(raw_data[3][2:4])) / 10e3) + " V")
            print("BMS VOLTAGE HIGH: " + str(int(hex(raw_data[3][4:6])) / 10e3) + " V")
            print("BMS VOLTAGE TOTAL: " + str(int(hex(raw_data[3][6:8])) / 100.) + " V")
        elif (raw_data[1] == "D8"):
            #D8: BMS Detailed Voltages, ID_BMS_DETAILED_VOLTAGES
        elif (raw_data[1] == "D9"):
            #D9: BMS Temperatures, ID_BMS_TEMPERATURES
            print("BMS AVERAGE TEMPERATURE: " + str(int(hex(raw_data[3][0:2])) / 100.) + " C")
            print("BMS LOW TEMPERATURE: " + str(int(hex(raw_data[3][2:4])) / 100.) + " C")
            print("BMS HIGH TEMPERATURE: " + str(int(hex(raw_data[3][4:6])) / 100.) + " C")
        elif (raw_data[1] == "DA"):
            #DA: BMS Detailed Temperatures, ID_BMS_DETAILED_TEMPERATURES
        elif (raw_data[1] == "DB"):
            #DB: BMS Status, ID_BMS_STATUS
            print("BMS STATE: " + str(int(hex(raw_data[3][0]))))
            print("BMS ERROR FLAGS: 0x" + raw_data[3][2].upper() + raw_data[3][1].upper())
            print("BMS CURRENT: " + str(int(hex(raw_data[3][3:5])) / 100.) + " A")
        print("___________________________________")
        elif (raw_data[1] == "DC"):
            #DC: FH Watchdog Test, ID_FH_WATCHDOG_TEST
        elif (raw_data[1] == "DD"):
            #DD: Charge Control Unit Status, ID_CCU_STATUS
        elif (raw_data[1] == "DE"):
            #DE: BMS Balancing Status, ID_BMS_BALANCING_STATUS
        elif (raw_data[1] == "DF"):
            #DF: ID_FCU_ACCELEROMETER
        elif (raw_data[1] == "E1"):
            #E1: ID_BMS_PARAMETER_RESPONSE
        elif (raw_data[1] == "E2"):
            #E2: BMS Coulomb Counts, ID_BMS_COULOMB_COUNTS
        elif (raw_data[1] == "E7"):
            #E7: ID_ECU_GPS_READINGS_ALPHA
        elif (raw_data[1] == "E8"):
            #E8: ID_ECU_GPS_READINGS_BETA 
        elif (raw_data[1] == "E9"):
            #stuff
    f.close()
    # print("Processed " + str(countGood) + " messages")
    # print("Failed to process " + str(countBad) + " messages")

def hex(data):
        return int("0x" + data, 16)

main()
