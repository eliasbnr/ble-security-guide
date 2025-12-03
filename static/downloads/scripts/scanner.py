#!/usr/bin/env python3
"""
LED Brille Scanner
Scannt nach LED-Brillen mit dem spezifischen Manufacturer Data Pattern
"""

import logging
from blatann import BleDevice
from blatann.gap.advertising import AdvertisingData

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Manufacturer Data Pattern der LED-Brille (aus BleConfig.java)
GLASSES_PATTERN = bytes([84, 82, 0, 58, 12])  # [0x54, 0x52, 0x00, 0x3A, 0x0C]

def check_manufacturer_data(adv_data):
    """
    Prüft ob das Advertising Data das LED-Brille Pattern enthält
    """
    if not adv_data.manufacturer_data:
        return False
    
    # manufacturer_data ist ein bytearray mit dem kompletten AD Structure
    # Format: [length, type, company_id_low, company_id_high, ...data...]
    mfg_data = adv_data.manufacturer_data
    
    if isinstance(mfg_data, (bytes, bytearray)):
        # Prüfe ob das Pattern irgendwo im Data enthalten ist
        if GLASSES_PATTERN in bytes(mfg_data):
            return True
        
        # Alternativ: Prüfe ab Byte 3 (nach Type und Company ID)
        if len(mfg_data) >= 3 + len(GLASSES_PATTERN):
            # Skip Type (0xFF) und Company ID (2 Bytes)
            data_part = bytes(mfg_data[3:])
            if data_part.startswith(GLASSES_PATTERN):
                return True
    
    return False

def format_mac_address(address):
    """Formatiert die MAC-Adresse für bessere Lesbarkeit"""
    # Entferne ",p" oder andere Suffixe wenn vorhanden
    addr_str = str(address)
    if ',' in addr_str:
        addr_str = addr_str.split(',')[0]
    return addr_str

def format_bytes(data):
    """Formatiert Bytes als Hex-String"""
    return ' '.join([f'{b:02X}' for b in data])

def main():
    """
    Scannt nach LED-Brillen und zeigt Details an
    """
    COM_PORT = "/dev/ttyACM0"  # Für Linux; Windows: "COM3"
    SCAN_TIMEOUT = 15  # Sekunden
    
    logger.info("=" * 70)
    logger.info("LED Brille Scanner")
    logger.info("=" * 70)
    logger.info(f"COM Port: {COM_PORT}")
    logger.info(f"Scan Dauer: {SCAN_TIMEOUT} Sekunden")
    logger.info(f"Suche nach Manufacturer Pattern: {format_bytes(GLASSES_PATTERN)}")
    logger.info("-" * 70)
    
    # BLE Device initialisieren
    try:
        ble_device = BleDevice(COM_PORT)
        ble_device.configure()
        ble_device.open()
        logger.info("✓ BLE Device geöffnet\\n")
    except Exception as e:
        logger.error(f"Fehler beim Öffnen des BLE Device: {e}")
        logger.error("Überprüfe:")
        logger.error("  1. Ist der nRF52840 Dongle angeschlossen?")
        logger.error("  2. Ist der COM-Port korrekt?")
        logger.error("  3. Ist die Connectivity Firmware geflasht?")
        return
    
    try:
        # Scan starten
        logger.info(f"Starte Scan für {SCAN_TIMEOUT} Sekunden...")
        logger.info("(Stelle sicher, dass die LED-Brille eingeschaltet ist!)\\n")
        
        scan_reports = ble_device.scanner.start_scan().wait(timeout=SCAN_TIMEOUT)
        
        logger.info(f"\\n✓ Scan abgeschlossen. {len(scan_reports.advertising_peers_found)} Geräte gefunden.\\n")
        logger.info("=" * 70)
        
        # Geräte analysieren
        glasses_found = []
        other_devices = []
        
        for report in scan_reports.advertising_peers_found:
            if check_manufacturer_data(report.advertise_data):
                glasses_found.append(report)
            else:
                other_devices.append(report)
        
        # LED-Brillen anzeigen
        if glasses_found:
            logger.info("🎉 LED-Brille(n) gefunden!")
            logger.info("=" * 70)
            
            for i, report in enumerate(glasses_found, 1):
                logger.info(f"\\nBrille #{i}")
                logger.info("-" * 70)
                logger.info(f"MAC-Adresse:     {format_mac_address(report.peer_address)}")
                logger.info(f"Name:            {report.advertise_data.local_name or '(Unbekannt)'}")
                logger.info(f"RSSI:            {report.rssi} dBm")
                logger.info(f"Adresstyp:       {report.peer_address.addr_type}")
                
                # Manufacturer Data Details
                if report.advertise_data.manufacturer_data:
                    logger.info("\\nManufacturer Data:")
                    mfg_data = report.advertise_data.manufacturer_data
                    if isinstance(mfg_data, (bytes, bytearray)):
                        logger.info(f"  Raw: {format_bytes(mfg_data)}")
                        # Parse: [length, type, company_id_low, company_id_high, ...data...]
                        if len(mfg_data) >= 3:
                            ad_type = mfg_data[0] if len(mfg_data) > 0 else 0
                            company_id = (mfg_data[2] << 8) | mfg_data[1] if len(mfg_data) >= 3 else 0
                            data_bytes = mfg_data[3:] if len(mfg_data) > 3 else b''
                            logger.info(f"  Type: 0x{ad_type:02X}")
                            logger.info(f"  Company ID: 0x{company_id:04X}")
                            if data_bytes:
                                logger.info(f"  Data: {format_bytes(data_bytes)}")
                    else:
                        logger.info(f"  {mfg_data}")
                
                # Service UUIDs
                if report.advertise_data.service_uuid16s:
                    logger.info("\\n16-bit Service UUIDs:")
                    for uuid in report.advertise_data.service_uuid16s:
                        logger.info(f"  {uuid}")
                
                if report.advertise_data.service_uuid128s:
                    logger.info("\\n128-bit Service UUIDs:")
                    for uuid in report.advertise_data.service_uuid128s:
                        logger.info(f"  {uuid}")
                
                # Service Data
                if report.advertise_data.service_data:
                    logger.info("\\nService Data:")
                    for uuid, data in report.advertise_data.service_data.items():
                        logger.info(f"  UUID {uuid}: {format_bytes(data)}")
                
                # Flags
                if report.advertise_data.flags is not None:
                    logger.info(f"\\nFlags:           0x{report.advertise_data.flags:02X}")
                
                logger.info("\\n" + "=" * 70)
                
                # Empfehlung
                logger.info("\\n📝 Verwende diese MAC-Adresse im POC-Skript:")
                logger.info(f"   GLASSES_ADDRESS = \\\"{format_mac_address(report.peer_address)}\\\"")
                logger.info("=" * 70)
        
        else:
            logger.info("❌ Keine LED-Brille gefunden!")
            logger.info("=" * 70)
            logger.info("\\nPrüfe:")
            logger.info("  1. Ist die Brille eingeschaltet?")
            logger.info("  2. Ist die Brille in Reichweite?")
            logger.info("  3. Ist die Brille bereits mit einem anderen Gerät verbunden?")
            logger.info("  4. Befindest du dich in einer Umgebung mit vielen BLE-Geräten?")
        
        # Andere gefundene Geräte (optional anzeigen)
        if other_devices and len(other_devices) <= 10:
            logger.info("\\n\\nAndere gefundene BLE-Geräte:")
            logger.info("=" * 70)
            for report in other_devices[:10]:  # Max 10 anzeigen
                logger.info(f"\\n{format_mac_address(report.peer_address)}")
                logger.info(f"  Name: {report.advertise_data.local_name or '(Unbekannt)'}")
                logger.info(f"  RSSI: {report.rssi} dBm")
                if report.advertise_data.manufacturer_data:
                    mfg_data = report.advertise_data.manufacturer_data
                    if isinstance(mfg_data, (bytes, bytearray)) and len(mfg_data) >= 3:
                        company_id = (mfg_data[2] << 8) | mfg_data[1]
                        data_bytes = mfg_data[3:] if len(mfg_data) > 3 else b''
                        logger.info(f"  Mfg (0x{company_id:04X}): {format_bytes(data_bytes) if data_bytes else '(empty)'}")
        
        elif other_devices:
            logger.info(f"\\n\\n({len(other_devices)} andere BLE-Geräte gefunden)")
    
    except Exception as e:
        logger.error(f"\\nFehler während des Scans: {e}", exc_info=True)
    
    finally:
        logger.info("\\nSchließe BLE Device...")
        ble_device.close()
        logger.info("✓ Fertig!")

if __name__ == "__main__":
    main()
