#!/usr/bin/env python3
import time
import psutil
import json
import subprocess
from datetime import datetime

OUT_FILE = "/output/system_info.json"
UPDATE_INTERVAL = 10

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_ram_usage():
    return psutil.virtual_memory().percent


def get_disk_usage():
    return psutil.disk_usage("/").percent


def get_temperature():
    try:
        result = subprocess.run(
            ["vcgencmd", "measure_temp"], capture_output=True, text=True
        )
        temp_str = result.stdout.strip()
        temp = temp_str.split("=")[1].replace("'C", "")
    except Exception:
        temp = "N/A"
    return temp


def get_internet_speed():
    """Пробуем через speedtest-cli, иначе считаем локально (KB/s)."""
    try:
        result = subprocess.run(
            ["speedtest-cli", "--json"], capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {
                "download_mbps": round(data["download"] / 1e6, 2),
                "upload_mbps": round(data["upload"] / 1e6, 2),
            }
    except Exception:
        pass

    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()
    sent_kbps = (net2.bytes_sent - net1.bytes_sent) / 1024
    recv_kbps = (net2.bytes_recv - net1.bytes_recv) / 1024
    return {"upload_kbps": round(sent_kbps, 2), "download_kbps": round(recv_kbps, 2)}


def get_system_info():
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_usage_percent": get_cpu_usage(),
        "ram_usage_percent": get_ram_usage(),
        "disk_usage_percent": get_disk_usage(),
        "temperature_celsius": get_temperature(),
        "internet_speed": get_internet_speed(),
    }


def main():
    while True:
        with open(OUT_FILE, "w") as f:
            json.dump(get_system_info(), f, indent=4)
        time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    main()
