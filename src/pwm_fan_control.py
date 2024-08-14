#!/usr/bin/python3
# -*-coding: utf-8 -*-

import time

import pigpio

from fan_control_logger import FanControlLogger


TEMPERATURE_FILE_PATH = "/sys/class/thermal/thermal_zone0/temp"
LOG_SAVE_DIR = "/var/log/pwm_fan_control/"
FILE_LINES_MAX = 10000

PIN_1 = 18
PWM_HZ = 100  # なんで100に設定してるのか忘れてしまった…

SLEEP_TIME = 10  # [s]
HYSTERESIS_STEPS = 30  # 10秒 * 30ステップ = 5分


def _get_hw_temp() -> int:
    with open(TEMPERATURE_FILE_PATH, "r", encoding="utf-8") as f:
        data = f.readline()
        temp = float(data) / 1000.0
    return int(temp)


def _get_duty(temp: int) -> int:
    duty = 100
    if 90 <= temp:
        duty = 100
    elif 70 <= temp < 90:
        duty = 75
    elif 50 <= temp < 70:
        duty = 60
    elif temp < 50:
        duty = 0
    return duty


def main():
    pig = pigpio.pi()
    pig.set_mode(PIN_1, pigpio.OUTPUT)
    fc_logger = FanControlLogger(LOG_SAVE_DIR, FILE_LINES_MAX)

    while True:
        temp = _get_hw_temp()
        duty = _get_duty(temp)
        fc_logger.write(temp, duty)
        pig.hardware_PWM(PIN_1, PWM_HZ, duty * 10000)

        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
