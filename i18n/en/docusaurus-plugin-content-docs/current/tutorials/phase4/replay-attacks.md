---
sidebar_position: 2
title: "Replay Attacks"
---

# Replay Attacks

Test if the device is vulnerable to replay attacks.

## Concept

1. Capture legitimate traffic
2. Replay exact same packets
3. Observe device reaction

```python
# From Wireshark capture
captured = bytes.fromhex("7e0404010001ff00ef")
char.write(captured).wait()
# If device reacts -> Vulnerable!
```

---

:::tip Next Step
Continue with [Authentication Bypass](./auth-bypass).
:::
