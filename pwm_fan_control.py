#!/usr/bin/python
#-*-coding: utf-8 -*-

from datetime import datetime
import pigpio
import time

temperature_file = "/sys/class/thermal/thermal_zone0/temp"
log_file = "/var/log/pwm_fan_control.log"


# duryは0~1000000(1M)で指定する
hz = 100 # [Hz]
duty = 100 # [%]
sleep_time = 30 # [s]
pin_1 = 18


# class FanControlLogger:
#    self._save_dir = "var/log/"
#    self._file_name = self._generate_file_name()
#
#    def _file_path():
#        return self._save_dir + self._file_name
#
#    def _create_file():
#        self._file_name = self._generate_file_name()
#
#    def _generate_file_name():
#        now = datetime.now()
#        date_str = now.strftime("%Y%m%d%H%M%S")
#        new_name = date_str + "_pwm_fan_control.log"
#        return new_name
#
#    def write(temp, duty):
#        now = datetime.now()
#        log = now.strftime('[%Y/%m/%d %H:%M:%S]') \
#              + " temp: " + str(temp) \
#              + " duty set: " + str(duty) \
#              + "\n"
#        with open(self._file_path(), "a") as f:
#            f.writelines(log)

def get_temp():
    with open(temperature_file, "r") as f:
        data = f.readline()
        temp = float(data)/1000.0
    return temp


def main():
    pig = pigpio.pi()
    pig.set_mode(pin_1, pigpio.OUTPUT)
    
    while(True):
        temp = get_temp()
        duty = 100

        if temp >= 90:
            duty = 100
        elif 80 > temp and temp >= 70:
            duty = 75
        elif 70 > temp and temp >= 50:
            duty = 60
        elif 50 > temp:
            duty = 0

        pig.hardware_PWM(pin_1, hz, duty * 10000)

        now = datetime.now()
        log = now.strftime('[%Y/%m/%d %H:%M:%S]') \
              + " temp: " + str(temp) \
              + " duty set: " + str(duty) \
              + "\n"
        with open(log_file, "a") as f:
            f.writelines(log)

        time.sleep(sleep_time)


if __name__ == "__main__":
    main()

