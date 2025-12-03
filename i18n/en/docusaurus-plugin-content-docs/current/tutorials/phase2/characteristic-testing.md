---
sidebar_position: 2
title: "Characteristic Testing"
---

# Characteristic Testing

Test all characteristics systematically.

## Read Test

```python
for char in service.characteristics:
    if char.readable:
        value = char.read().wait()
        print(f"{char.uuid}: {value.value.hex()}")
```

## Write Test

```python
test_payloads = [b'\x00', b'\x01', b'\xff' * 20]
for payload in test_payloads:
    char.write(payload).wait()
```

---

:::tip Next Step
Continue with [Security Level Testing](./security-level-testing).
:::
