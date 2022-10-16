#!/usr/bin/python3
# -*-coding: utf-8 -*-

from datetime import datetime
import pigpio
import time

TEMPERATURE_FILE_PATH = "/sys/class/thermal/thermal_zone0/temp"
LOG_SAVE_DIR = "/var/log/"
SLEEP_TIME = 30  # [s]
PIN_1 = 18
FILE_LINES_MAX = 10000


class FanControlLogger:
    def __init__(self, save_dir: str, file_lines_max: int):
        self._save_dir = save_dir
        self._file_name = self._generate_file_name()
        self._file_lines_max = file_lines_max
        self._create_file()

    @property
    def _file_path(self):
        return self._save_dir + self._file_name

    def _create_file(self):
        print(f"Create New File: {self._file_path}")
        open(self._file_path, "w")

    def _generate_file_name(self):
        now = datetime.now()
        date_str = now.strftime("%Y%m%d%H%M%S")
        new_name = "pwm_fan_control.log-" + date_str
        return new_name

    def _count_file_lines(self):
        count = sum(1 for _ in open(self._file_path))
        return count

    def _generate_log_string(self, temp: str, duty: str):
        now = datetime.now()
        log = now.strftime('[%Y/%m/%d %H:%M:%S]') \
            + " temp: " + str(temp) \
            + " duty set: " + str(duty) \
            + "\n"
        return log

    def _write_to_file(self, log: str):
        with open(self._file_path, "a") as f:
            f.write(log)

    def write(self, temp: str, duty: str):
        log = self._generate_log_string(temp, duty)
        self._write_to_file(log)
        if self._count_file_lines() >= self._file_lines_max:
            self._file_name = self._generate_file_name()
            self._create_file()


def get_temp():
    with open(TEMPERATURE_FILE_PATH, "r") as f:
        data = f.readline()
        temp = float(data)/1000.0
    return temp


def main():
    pig = pigpio.pi()
    pig.set_mode(PIN_1, pigpio.OUTPUT)
    fc_logger = FanControlLogger(LOG_SAVE_DIR, FILE_LINES_MAX)

    while (True):
        temp = get_temp()
        duty = 100
        hz = 100  # なんで100に設定してるのか忘れてしまった…

        if temp >= 90:
            duty = 100
        elif 80 > temp and temp >= 70:
            duty = 75
        elif 70 > temp and temp >= 50:
            duty = 60
        elif 50 > temp:
            duty = 0

        pig.hardware_PWM(PIN_1, hz, duty * 10000)

        fc_logger.write(temp, duty)

        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
