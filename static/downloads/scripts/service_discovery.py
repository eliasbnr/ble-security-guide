#!/usr/bin/env python3
"""
Service Discovery für LED-Brille
Zeigt alle verfügbaren Services und Charakteristiken an
"""

import logging
from blatann import BleDevice

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)
logger = logging.getLogger(__name__)

# Konfiguration
COM_PORT = "/dev/ttyACM0"
GLASSES_MAC = "00:3A:FE:12:B0:08"

def main():
    logger.info("=" * 70)
    logger.info("Service Discovery - LED Brille")
    logger.info("=" * 70)
    logger.info(f"COM Port: {COM_PORT}")
    logger.info(f"Gerät: {GLASSES_MAC}")
    logger.info("-" * 70)
    
    # BLE Device initialisieren
    ble_device = BleDevice(COM_PORT)
    ble_device.configure()
    ble_device.open()
    logger.info("✓ BLE Device geöffnet\n")
    
    try:
        # Normalisiere MAC-Adresse für Vergleich
        target_mac_norm = GLASSES_MAC.replace(":", "").replace("-", "").lower()
        
        # Scanne nach dem Gerät
        logger.info(f"Scanne nach {GLASSES_MAC} (Timeout: 5s)...")
        ble_device.scanner.set_default_scan_params(timeout_seconds=5)
        scan_results = ble_device.scanner.start_scan().wait()
        logger.info("Scan beendet.\n")
        
        # Finde das Gerät im Scan
        peer_info = next(
            (d for d in scan_results.advertising_peers_found if
             str(d.peer_address).split(',')[0].replace(":", "").replace("-", "").lower() == target_mac_norm),
            None
        )
        
        if not peer_info:
            logger.error(f"Gerät mit MAC {GLASSES_MAC} wurde im Scan nicht gefunden.")
            logger.info("\nGefundene Geräte:")
            for device in scan_results.advertising_peers_found[:5]:
                logger.info(f"  {device.peer_address} - {device.advertise_data.local_name or '(Unbekannt)'}")
            return
        
        logger.info(f"✓ Gerät gefunden: {peer_info.peer_address} (RSSI: {peer_info.rssi} dBm)")
        logger.info(f"  Name: {peer_info.advertise_data.local_name or '(Unbekannt)'}\n")
        
        # Verbinden mit dem gefundenen peer_address
        logger.info(f"Verbinde mit {peer_info.peer_address}...")
        peer = ble_device.connect(peer_info.peer_address).wait(timeout=15)
        
        if not peer:
            logger.error("Verbindung fehlgeschlossen!")
            return
        
        logger.info("✓ Verbunden!\n")
        
        # MTU austauschen
        logger.info("Tausche MTU aus...")
        peer.exchange_mtu(185).wait(timeout=5)
        logger.info(f"✓ MTU: {peer.mtu_size}\n")
        
        # Services entdecken
        logger.info("Entdecke Services...")
        peer.discover_services().wait(timeout=10)
        logger.info("✓ Service Discovery abgeschlossen\n")
        
        # Services anzeigen
        logger.info("=" * 70)
        logger.info("GEFUNDENE SERVICES UND CHARAKTERISTIKEN")
        logger.info("=" * 70)
        
        for service in peer.database.services:
            logger.info(f"\n📦 Service: {service.uuid}")
            logger.info(f"   Handle: 0x{service.start_handle:04X} - 0x{service.end_handle:04X}")
            
            if not service.characteristics:
                logger.info("   (Keine Charakteristiken)")
                continue
            
            for char in service.characteristics:
                logger.info(f"\n   📝 Characteristic: {char.uuid}")
                logger.info(f"      Declaration Handle: 0x{char.declaration_handle:04X}")
                logger.info(f"      Value Handle: 0x{char.value_handle:04X}")
                
                # Properties anzeigen
                props = []
                if char.readable:
                    props.append("READ")
                if char.writable:
                    props.append("WRITE")
                if char.write_no_response:
                    props.append("WRITE_NO_RESPONSE")
                if char.notifiable:
                    props.append("NOTIFY")
                if char.indicatable:
                    props.append("INDICATE")
                
                logger.info(f"      Properties: {', '.join(props) if props else 'None'}")
                
                # CCCD (Client Characteristic Configuration Descriptor)
                if char.cccd_handle:
                    logger.info(f"      CCCD Handle: 0x{char.cccd_handle:04X}")
                
                # Versuche zu lesen wenn möglich
                if char.readable:
                    try:
                        logger.info("      Lese Wert...")
                        result = char.read().wait(timeout=3)
                        if result.status.name == "SUCCESS":
                            value = result.value
                            hex_str = ' '.join([f'{b:02X}' for b in value])
                            logger.info(f"      Wert: {hex_str}")
                            # Als String wenn möglich
                            try:
                                ascii_str = ''.join([chr(b) if 32 <= b < 127 else '.' for b in value])
                                logger.info(f"      ASCII: '{ascii_str}'")
                            except:
                                pass
                    except Exception as e:
                        logger.warning(f"      Lesen fehlgeschlagen: {e}")
        
        logger.info("\n" + "=" * 70)
        
        # Empfehlungen
        logger.info("\n📋 EMPFOHLENE KONFIGURATION FÜR POC:")
        logger.info("=" * 70)
        
        # Suche nach Write/Notify Charakteristik
        write_chars = []
        for service in peer.database.services:
            for char in service.characteristics:
                if char.writable and char.notifiable:
                    write_chars.append((service.uuid, char.uuid))
        
        if write_chars:
            logger.info("\nGefundene Write/Notify Charakteristiken:")
            for svc_uuid, char_uuid in write_chars:
                logger.info(f"  Service: {svc_uuid}")
                logger.info(f"  Characteristic: {char_uuid}")
                logger.info("")
                logger.info("  → Verwende diese in config.py:")
                logger.info(f"     SERVICE_UUID = \"{svc_uuid}\"")
                logger.info(f"     CHARACTERISTIC_UUID = \"{char_uuid}\"")
                logger.info("")
        else:
            logger.warning("Keine Write/Notify Charakteristik gefunden!")
        
        logger.info("=" * 70)
        
        # Kurz warten bevor trennen
        import time
        time.sleep(1)
        
        # Trennen
        logger.info("\nTrenne Verbindung...")
        peer.disconnect()
        logger.info("✓ Getrennt")
        
    except Exception as e:
        logger.error(f"Fehler: {e}", exc_info=True)
    
    finally:
        logger.info("\nSchließe BLE Device...")
        ble_device.close()
        logger.info("✓ Fertig!")

if __name__ == "__main__":
    main()
