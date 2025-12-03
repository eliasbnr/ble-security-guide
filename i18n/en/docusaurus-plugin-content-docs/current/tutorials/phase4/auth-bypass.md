---
sidebar_position: 3
title: "Authentication Bypass"
---

# Authentication Bypass

Test if authentication can be bypassed.

## Test

```python
# Without pairing
peer = device.connect(target).wait()
peer.discover_services().wait()

# Direct write
cmd_char = peer.database.find_characteristic(CMD_UUID)
cmd_char.write(b'\x01\x02\x03').wait()

# If successful -> No Authentication!
```

---

:::tip Next Step
Continue with [Phase 5: Vulnerability Assessment](../phase5/vulnerability-assessment).
:::
