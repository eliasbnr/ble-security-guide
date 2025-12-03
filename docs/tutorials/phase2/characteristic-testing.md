---
sidebar_position: 2
title: "Characteristic Testing"
---

# Characteristic Testing

Nach der GATT-Enumeration testen wir die Characteristics systematisch.

## Read-Tests

```python
# Alle lesbaren Characteristics lesen
for svc in peer.database.services:
    for char in svc.characteristics:
        if char.readable:
            try:
                result = char.read().wait(timeout=5)
                print(f"{char.uuid}: {result.value.hex()}")
            except Exception as e:
                print(f"{char.uuid}: Error - {e}")
```

## Write-Tests

```python
# Test-Payloads
test_payloads = [
    b'\x00',                    # Null byte
    b'\x01',                    # Single byte
    b'\xff' * 20,              # Max ATT payload
    b'TEST',                   # ASCII
]

for payload in test_payloads:
    try:
        char.write(payload).wait()
        print(f"✓ Accepted: {payload.hex()}")
    except Exception as e:
        print(f"✗ Rejected: {payload.hex()} - {e}")
```

## Notification-Tests

```python
received = []

def on_notify(char, args):
    received.append(args.value)
    print(f"RX: {args.value.hex()}")

char.subscribe(on_notify).wait()
time.sleep(10)  # Warte auf Notifications
char.unsubscribe().wait()

print(f"Received {len(received)} notifications")
```

---

:::tip Nächster Schritt
Weiter zum [Security Level Testing](./security-level-testing).
:::
