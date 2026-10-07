"""
Web3 Security and Anti-Phishing Guard for MobileAgentKit.
Inspired by SlowMist Web3 Security Guidelines.

Protects Android AI Agents and physical devices from:
1. Clipboard Hijacking (Address Replacement Attack)
2. Malicious App Overlay & Excessive Permissions
3. Dangerous RPC and Phishing Domain Detection
"""

import re
from typing import Dict, Any, List, Optional

class Web3SecurityGuard:
    # 典型链上地址格式匹配
    ETH_ADDR_REGEX = r"^0x[a-fA-F0-9]{40}$"
    SOL_ADDR_REGEX = r"^[1-9A-HJ-NP-Za-km-z]{32,44}$"
    BTC_ADDR_REGEX = r"^(?:1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,39}$"

    # 已知钓鱼与恶意域名模式
    PHISHING_PATTERNS = [
        r"(?i).*\-claim\.(?:xyz|top|vip|cc)",
        r"(?i).*\-airdrop\.(?:xyz|top|vip|cc)",
        r"(?i).*(?:metamask|phantom|okx|binance).*\.(?:xyz|top|vip|cc|tk|ml)",
        r"(?i).*revoke.*cash.*"
    ]

    @classmethod
    def verify_clipboard_integrity(cls, original_address: str, current_clipboard: str) -> bool:
        """
        慢雾安全基线：剪贴板防篡改校验。
        防止安卓后台恶意 APK 监听剪贴板并在复制时替换加密货币收款地址。
        """
        orig = original_address.strip()
        curr = current_clipboard.strip()
        if orig != curr:
            # 严重警报：剪贴板内容已被修改
            return False
        return True

    @classmethod
    def is_phishing_domain(cls, domain: str) -> bool:
        """
        慢雾安全基线：钓鱼与假空投域名嗅探。
        """
        for pattern in cls.PHISHING_PATTERNS:
            if re.search(pattern, domain):
                return True
        return False

    @classmethod
    def audit_app_permissions(cls, granted_permissions: List[str]) -> Dict[str, Any]:
        """
        移动端权限安全审计：识别高危权限组合。
        如：同时获取 ACCESSIBILITY_SERVICE（无障碍）和 READ_SMS（读取短信）常为恶意假钱包特征。
        """
        high_risk_flags = []
        dangerous = {
            "android.permission.BIND_ACCESSIBILITY_SERVICE": "Accessibility Hijacking Risk",
            "android.permission.RECEIVE_SMS": "SMS OTP Interception Risk",
            "android.permission.READ_SMS": "SMS Sniffing Risk",
            "android.permission.SYSTEM_ALERT_WINDOW": "Phishing Overlay Risk"
        }
        for perm in granted_permissions:
            if perm in dangerous:
                high_risk_flags.append(dangerous[perm])
                
        return {
            "is_safe": len(high_risk_flags) == 0,
            "risk_flags": high_risk_flags
        }
