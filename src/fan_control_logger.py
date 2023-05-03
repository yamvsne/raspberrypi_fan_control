import os
import subprocess
import time
from datetime import datetime


TIME_SYNC_WAIT_TIME = 3  # [s]


class FanControlLogger:
    def __init__(
        self,
        save_dir: str,
        file_lines_max: int,
        wait_for_time_sync: bool = True,
    ):
        if wait_for_time_sync:
            self._wait_for_time_sync()

        self._save_dir = save_dir
        self._file_name = self._generate_file_name()
        self._file_lines_max = file_lines_max
        self._create_file()

    def write(self, temp: str, duty: str):
        """温度とデューティー比をログファイルに書き込む"""
        log = self._generate_log_string(temp, duty)
        self._write_to_file(log)
        if self._count_file_lines() >= self._file_lines_max:
            self._file_name = self._generate_file_name()
            self._create_file()

    @property
    def _file_path(self):
        return self._save_dir + self._file_name

    def _create_file(self):
        print(f"Create New File: {self._file_path}")
        self._make_save_directory_if_not_exists()
        with open(self._file_path, "w", encoding="utf-8") as f:
            f.write("")

    def _make_save_directory_if_not_exists(self):
        if not os.path.exists(self._save_dir):
            os.makedirs(self._save_dir)

    def _generate_file_name(self):
        now = datetime.now()
        date_str = now.strftime("%Y%m%d%H%M%S")
        new_name = "pwm_fan_control.log-" + date_str
        return new_name

    def _count_file_lines(self):
        with open(self._file_path, encoding="utf-8") as f:
            count = sum(1 for _ in f)
        return count

    def _generate_log_string(self, temp: str, duty: str):
        now = datetime.now()
        log = (
            f"{now.strftime('[%Y/%m/%d %H:%M:%S]')} "
            f"temp: {str(temp)}, duty: {str(duty)}\n"
        )
        return log

    def _write_to_file(self, log: str):
        with open(self._file_path, "a", encoding="utf-8") as f:
            f.write(log)

    def _wait_for_time_sync(self):
        while True:
            print("Check Time Sync...")
            result = subprocess.run(
                (
                    "/usr/bin/timedatectl"
                    "| grep synchronized"
                    "| cut -d':' -f2"
                    "| tr -d ' '",
                ),
                shell=True,
                stdout=subprocess.PIPE,
                check=False,
            )
            print(result.stdout.decode("utf-8"))
            if result.stdout.decode("utf-8") == "yes\n":
                print("Time Sync is completed!")
                break

            print("Time Sync is not completed.")
            print("Wait for Time Sync...")
            time.sleep(TIME_SYNC_WAIT_TIME)
