import sys
import struct
import logging
from blatann import BleDevice
from blatann.utils import setup_logger

# Logger konfigurieren
logger = setup_logger(level="INFO")

# --- Konfiguration ---
TARGET_DEVICE_NAME = "Yoda1"
TARGET_MANUFACTURER_ID = 0x05C0

def process_scan_report(scan_report):
    """
    Verarbeitet einen einzelnen Scan-Report.
    """
    adv_data = scan_report.advertise_data
    local_name = adv_data.local_name
    
    # 1. Filter: Name prüfen
    if local_name and TARGET_DEVICE_NAME.lower() in local_name.lower():
        
        # 2. Filter: Manufacturer Data
        mfg_data = adv_data.manufacturer_data
        
        # Wir erwarten mindestens 6 Bytes (2 Byte ID + 4 Byte Daten)
        if mfg_data and len(mfg_data) >= 6:
            
            # Wir greifen direkt auf die identifizierten Offsets zu
            # Basierend auf Analyse: Index 2-3 ist Gewicht, Index 4-5 ist Impedanz
            
            # Gewicht (Byte 2-3, Big Endian)
            raw_weight = struct.unpack('>H', mfg_data[2:4])[0]
            weight_kg = raw_weight / 100.0
            
            # Impedanz (Byte 4-5, Big Endian)
            raw_impedance = struct.unpack('>H', mfg_data[4:6])[0]
            
            # Filter für "Leermessungen" oder Einschalt-Werte
            if weight_kg > 5.0:
                print("\n" + "="*40)
                print(f"[!] DATEN-LECK DETEKTIERT!")
                print(f"    Gerät:    {scan_report.peer_address}")
                print(f"    Name:     {local_name}")
                print(f"    RSSI:     {scan_report.rssi} dBm")
                print("-" * 40)
                print(f"    GEWICHT:  {weight_kg:.2f} kg")
                print(f"    IMPEDANZ: {raw_impedance} Ohm")
                print("="*40 + "\n")

def main(serial_port):
    logger.info(f"Initialisiere Dongle an {serial_port}...")
    ble_device = BleDevice(serial_port)
    ble_device.configure()
    ble_device.open()
    
    logger.info(f"[*] Starte Privacy-Scanner für '{TARGET_DEVICE_NAME}'...")
    logger.info("[*] Warte auf Broadcast-Pakete...")
    
    try:
        ble_device.scanner.set_default_scan_params(timeout_seconds=0) 
        scan_waitable = ble_device.scanner.start_scan()
        
        for report in scan_waitable.scan_reports:
            process_scan_report(report)
            
    except KeyboardInterrupt:
        logger.info("\n[*] Beendet.")
    except Exception as e:
        logger.error(f"Fehler: {e}")
    finally:
        ble_device.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Aufruf: python3 {sys.argv[0]} <SERIAL_PORT>")
        sys.exit(1)
        
    main(sys.argv[1])
