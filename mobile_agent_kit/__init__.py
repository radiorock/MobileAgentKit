"""
MobileAgentKit: Bare-Metal Android AI Agent Framework with Security-First Baseline.
"""

from .driver import AndroidDriver
from .guard import PrivacyGuard
from .monitors import DeviceHealthMonitor

__version__ = "0.1.0"
__all__ = ["AndroidDriver", "PrivacyGuard", "DeviceHealthMonitor"]
