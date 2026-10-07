"""
Privacy and Security Guard Module for MobileAgentKit.
Enforces SlowMist-inspired security baseline:
- Redacts or rejects private keys, seed phrases, sensitive internal IPs, and confidential credentials.
- Audits outbound text before any transmission to external networks or apps.
"""

import re
from typing import Tuple, List

class SecurityViolationError(Exception):
    pass

class PrivacyGuard:
    # 敏感模式正则硬防御
    PATTERNS = {
        "ETH_PRIVATE_KEY": r"(?i)\b(?:0x)?[0-9a-f]{64}\b",
        "MNEMONIC_PHRASE": r"\b(?:[a-z]{3,8}\s+){11,23}[a-z]{3,8}\b",
        "AWS_KEY": r"(?i)\b(?:akid|akia|aws)[0-9a-z]{16,}\b",
        "PRIVATE_IP": r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3})\b",
        "MINING_PROFIT": r"(?i)\b(?:¥\s*\d+(?:\.\d+)?\s*/\s*天|¥\s*\d+(?:\.\d+)?\s*/\s*月|聪\s*BTC|LTC\s*\+\s*\d+\s*DOGE)\b",
        "PASSWORDS_TOKENS": r"(?i)(?:password|passwd|secret|api_key|access_token)\s*[:=]\s*['\"][^'\"]{6,}['\"]"
    }

    @classmethod
    def sanitize(cls, text: str) -> Tuple[str, bool, List[str]]:
        """
        Sanitize text by replacing sensitive matches with [REDACTED].
        Returns (sanitized_text, is_clean, list_of_violations).
        """
        violations = []
        clean_text = text
        for rule_name, pattern in cls.PATTERNS.items():
            matches = re.findall(pattern, clean_text)
            if matches:
                violations.append(rule_name)
                clean_text = re.sub(pattern, f"[{rule_name}_REDACTED]", clean_text)
        
        is_clean = len(violations) == 0
        return clean_text, is_clean, violations

    @classmethod
    def assert_clean(cls, text: str):
        """
        Raise SecurityViolationError if any sensitive rule is violated.
        """
        _, is_clean, violations = cls.sanitize(text)
        if not is_clean:
            raise SecurityViolationError(f"Security Alert: Blocked sensitive content matching {violations}!")
        return True
