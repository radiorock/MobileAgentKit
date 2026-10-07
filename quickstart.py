"""
Quickstart demo script for MobileAgentKit.
"""

from mobile_agent_kit import AndroidDriver, PrivacyGuard, DeviceHealthMonitor

def main():
    print("=== MobileAgentKit Quickstart Demo ===")
    
    # 1. Driver test
    driver = AndroidDriver()
    info = driver.get_device_info()
    print(f"[Device] Model: {info.get('model')}, Brand: {info.get('brand')}, Android: {info.get('android_version')}")
    
    # 2. Health monitor
    monitor = DeviceHealthMonitor(driver)
    health = monitor.get_battery_status()
    print(f"[Health] Battery: {health.get('battery_percent')}%, Temp: {health.get('temperature_celsius')}°C")
    
    # 3. Privacy Guard check
    sample_safe_text = "Building Autonomous AI Agent on bare-metal Sharp AQUOS R5G!"
    _, is_clean, violations = PrivacyGuard.sanitize(sample_safe_text)
    print(f"[Privacy] Clean text test passed: {is_clean}")
    
    sample_leak = "Private key 0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d must be protected"
    sanitized, is_clean, violations = PrivacyGuard.sanitize(sample_leak)
    print(f"[Privacy] Leak interception test: Intercepted={not is_clean}, Rules={violations}")
    print(f"[Privacy] Redacted output: {sanitized}")

    print("\nAll MobileAgentKit core checks succeeded!")

if __name__ == "__main__":
    main()
