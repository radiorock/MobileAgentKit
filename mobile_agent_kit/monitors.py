"""
Device Health and Power Management Module for MobileAgentKit.
Monitors battery level, device temperature, and maintains screen stay-awake state.
"""

import re
from typing import Dict, Any
from .driver import AndroidDriver

class DeviceHealthMonitor:
    def __init__(self, driver: AndroidDriver):
        self.driver = driver

    def get_battery_status(self) -> Dict[str, Any]:
        out = self.driver.run_adb(["shell", "dumpsys", "battery"])
        level_m = re.search(r"level:\s*(\d+)", out)
        temp_m = re.search(r"temperature:\s*(\d+)", out)
        status_m = re.search(r"status:\s*(\d+)", out)
        
        level = int(level_m.group(1)) if level_m else None
        # Android dumpsys battery temperature is in tenths of a degree Celsius
        temp_c = float(temp_m.group(1)) / 10.0 if temp_m else None
        
        return {
            "battery_percent": level,
            "temperature_celsius": temp_c,
            "raw_status": status_m.group(1) if status_m else None
        }

    def keep_screen_awake(self, enable: bool = True):
        # 3 = stay awake while plugged into AC/USB
        val = "3" if enable else "0"
        self.driver.run_adb(["shell", "svc", "power", "stayon", "usb" if enable else "false"])
        self.driver.run_adb(["shell", "settings", "put", "global", "stay_on_while_plugged_in", val])
