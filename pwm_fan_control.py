#-*-coding: utf-8 -*-

import pigpio
import time

temperature_file = "/sys/class/thermal/thermal_zone0/temp"

# duryは0~1000000(1M)で指定する
hz = 100 # [Hz]
duty = 100 # [%]
sleep_time = 20 # [s]
pin_1 = 18

pig = pigpio.pi()
pig.set_mode(pin_1, pigpio.OUTPUT)

def get_temp():
    with open(temperature_file, "r") as f:
        data = f.readline()
        temp = float(data)/1000.0
    return temp

def main():
    while(True):
        temp = get_temp()
        duty = 50

        if temp >= 90:
            duty = 100
        elif 80 > temp and temp >= 70:
            duty = 80
        elif 70 > temp and temp >= 50:
            duty = 70
        elif 50 > temp and temp >= 30:
            duty = 60
        elif 30 > temp:
            duty = 40

        # print "temp: " + str(temp)
        print "duty set: " + str(duty)
        pig.hardware_PWM(pin_1, hz, duty * 10000)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()

