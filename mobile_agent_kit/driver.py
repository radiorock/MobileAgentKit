"""
Android Driver Module for MobileAgentKit.
Handles direct ADB interaction with bare-metal physical Android devices.
"""

import subprocess
import time
import os
import re
import xml.etree.ElementTree as ET
from typing import Optional, Tuple, Dict, Any, List

class AndroidDriver:
    def __init__(self, serial: Optional[str] = None):
        self.serial = serial
        self._base_cmd = ["adb"]
        if self.serial:
            self._base_cmd.extend(["-s", self.serial])

    def run_adb(self, args: List[str], timeout: int = 15) -> str:
        cmd = self._base_cmd + args
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return res.stdout.strip()
        except subprocess.TimeoutExpired:
            return ""
        except Exception as e:
            return ""

    def get_device_info(self) -> Dict[str, str]:
        model = self.run_adb(["shell", "getprop", "ro.product.model"])
        brand = self.run_adb(["shell", "getprop", "ro.product.brand"])
        android_ver = self.run_adb(["shell", "getprop", "ro.build.version.release"])
        sdk_ver = self.run_adb(["shell", "getprop", "ro.build.version.sdk"])
        return {
            "model": model,
            "brand": brand,
            "android_version": android_ver,
            "sdk_version": sdk_ver
        }

    def tap(self, x: int, y: int) -> bool:
        res = self.run_adb(["shell", "input", "tap", str(x), str(y)])
        return True

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> bool:
        self.run_adb(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms)])
        return True

    def keyevent(self, keycode: int) -> bool:
        self.run_adb(["shell", "input", "keyevent", str(keycode)])
        return True

    def input_text(self, text: str) -> bool:
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if line:
                escaped = line.replace(" ", "%s")
                for char in [r"&", r"(", r")", r"<", r">", r"|", r";", r"$", r"'", r'"', r"\\", r"`"]:
                    escaped = escaped.replace(char, f"\\{char}")
                self.run_adb(["shell", f"input text {escaped}"])
                time.sleep(0.15)
            if i < len(lines) - 1:
                self.keyevent(66) # Enter
                time.sleep(0.15)
        return True

    def capture_screenshot(self, local_dest: str) -> bool:
        cmd = self._base_cmd + ["exec-out", "screencap", "-p"]
        try:
            with open(local_dest, "wb") as f:
                subprocess.run(cmd, stdout=f, timeout=10)
            return os.path.exists(local_dest) and os.path.getsize(local_dest) > 0
        except Exception:
            return False

    def dump_hierarchy(self) -> Optional[ET.Element]:
        self.run_adb(["shell", "uiautomator", "dump", "/sdcard/_window_dump.xml"])
        xml_content = self.run_adb(["shell", "cat", "/sdcard/_window_dump.xml"])
        if not xml_content or "<hierarchy" not in xml_content:
            return None
        try:
            return ET.fromstring(xml_content)
        except Exception:
            return None

    def find_node(self, root: ET.Element, text: Optional[str] = None, desc: Optional[str] = None) -> Optional[Dict[str, Any]]:
        for node in root.iter("node"):
            node_text = node.attrib.get("text", "")
            node_desc = node.attrib.get("content-desc", "")
            bounds = node.attrib.get("bounds", "")
            
            matched = False
            if text and text in node_text:
                matched = True
            elif desc and desc in node_desc:
                matched = True
                
            if matched:
                nums = [int(n) for n in re.findall(r"\d+", bounds)]
                if len(nums) == 4:
                    cx = (nums[0] + nums[2]) // 2
                    cy = (nums[1] + nums[3]) // 2
                    return {
                        "text": node_text,
                        "desc": node_desc,
                        "bounds": nums,
                        "center": (cx, cy),
                        "node": node
                    }
        return None
