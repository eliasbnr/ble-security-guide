---
sidebar_position: 4
title: "Findings"
---

# Smart Scale - Findings

## F-001: Weight Data in Advertising

**CVSS: 5.3 (Medium)**

```
Vector: CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N
```

### Impact

| Aspect | Assessment |
|--------|------------|
| Privacy | Weight is sensitive health data |
| Tracking | MAC address allows identification |
| Range | ~10m, through walls |
| Effort | Minimal (standard BLE scanner) |

### GDPR Relevance

Weight data is considered **health data** (Art. 9 GDPR):
> "special categories of personal data"

### Remediation

1. Do NOT send weight in advertising
2. Transfer data only after connection + auth
3. Rotate MAC address (BLE Privacy)
