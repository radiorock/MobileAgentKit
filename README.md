# 📱 MobileAgentKit

> **Bare-Metal Physical Android AI Agent Framework with Security-First Baseline.**  
> 基于真实实体手机硬件的原生 AI Agent 自动化与安全防护套件。

---

## 🌟 Why Bare-Metal Android? (为什么选择物理实体机？)

1. **Hardware Trust & Fingerprinting (硬件级真实信任)**:  
   物理真机（如夏普 AQUOS R5G）具备原生硬件序列号、基带与指纹，杜绝云端模拟器 / 沙箱频繁被封禁的风控风险。
2. **Physical Sensor Awareness (真实物理感知)**:  
   直接采集物理电池电量、工作温控、USB 常亮模式与充电状态，保障 24/7 常驻稳定。
3. **SlowMist-Inspired Security Baseline (慢雾安全基线)**:  
   硬编码级隐私守卫，在任何外部应用调用或发帖前，强制过滤私钥、助记词、内网敏感 IP 与关键资产数据。

---

## 🚀 Quickstart (快速上手)

### 1. Requirements (环境要求)
- Python 3.8+
- Android Debug Bridge (`adb`)
- 开启 USB 调试的物理 Android 手机

### 2. Run Demo (运行演示)
```bash
python3 quickstart.py
```

### 3. Basic Usage (代码调用)
```python
from mobile_agent_kit import AndroidDriver, PrivacyGuard, DeviceHealthMonitor

driver = AndroidDriver()
monitor = DeviceHealthMonitor(driver)

# 1. 检查物理机状态
health = monitor.get_battery_status()
print(f"Battery: {health['battery_percent']}%, Temp: {health['temperature_celsius']}°C")

# 2. 慢雾安全过滤
safe_text, is_clean, violations = PrivacyGuard.sanitize("Your text...")
if is_clean:
    driver.input_text(safe_text)
```

---

## 💎 Pricing & Edition (版本与商业权益)

| Feature (功能特性) | Community (开源版) | Pro Edition (商业版 - \$19) |
| :--- | :---: | :---: |
| Native ADB Automation (基础控制) | ✅ Included | ✅ Included |
| Physical Health Monitoring (硬件巡检) | ✅ Included | ✅ Included |
| Privacy Guard (慢雾基线硬拦截) | ✅ Included | ✅ Included |
| **24/7 Unattended Daemon (后台守护进程)** | ❌ | ✅ **Full Access** |
| **Social Auto-Engagement (X/TG 自动化流水线)** | ❌ | ✅ **Full Access** |
| **Web3 Anti-Phishing Guard (防钓鱼/防恶意签名)** | ❌ | ✅ **Full Access** |
| **Private Discord / VIP 咨询支持** | ❌ | ✅ **Lifetime** |

👉 **Support the Project & Get Pro Access**: [Gumroad / VIP Access Link Coming Soon]

---

## 🛡️ Security & Privacy
Licensed under MIT. Zero data collection.
All interactions execute locally via your local ADB bridge.
