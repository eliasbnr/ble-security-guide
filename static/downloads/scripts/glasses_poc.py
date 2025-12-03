#!/usr/bin/env python3
"""
BLE LED Glasses Text Update PoC - IMPROVED VERSION
Uses blatann library with nRF52840 dongle
Target: LED Glasses (GLASSES-XXXXXX)

✅ AES Key Extracted and Verified!
✅ Column-major AES transformation implemented!
✅ Multiple display modes supported!

Requirements:
    pip install blatann pycryptodome

Hardware:
    nRF52840 USB Dongle

Usage:
    python3 glasses_poc_improved.py --text "HELLO" --device "GLASSES-12B008" --display-mode static
    python3 glasses_poc_improved.py --text "HELLO" --device "GLASSES-12B008" --display-mode scroll-left
"""

import sys
import time
import struct
import argparse
from Crypto.Cipher import AES

# ========== VERIFIED AES KEY ==========
AES_KEY = bytes.fromhex("34522a5b7a6e492c08090a9d8d2a23f8")

print(f"[INFO] Using verified AES key: {AES_KEY.hex()}")

# ========== BLE UUIDs ==========
SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
SERVICE_UUID_SHORT = "fff0"
CHAR_CONTROL_UUID = "d44bc439-abfd-45a2-b575-925416129600"
CHAR_DATA_UUID = "d44bc439-abfd-45a2-b575-92541612960a"
CHAR_NOTIFY_UUID = "d44bc439-abfd-45a2-b575-925416129601"

# ========== Display Modes ==========
DISPLAY_MODES = {
    'static': (1, 0, "Static display"),
    'scroll-left': (2, 0, "Scroll left"),
    'scroll-right': (2, 1, "Scroll right"),
    'scroll-down': (3, 0, "Scroll down"),
    'scroll-up': (3, 1, "Scroll up"),
}


# ========== Column-Major AES Cipher ==========
class ColumnMajorAESCipher:
    """
    AES-128 ECB Cipher with column-major byte arrangement.
    
    The native libAES.so arranges bytes in column-major order before encryption.
    Standard order:  00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
    Column-major:    00 04 08 0C 01 05 09 0D 02 06 0A 0E 03 07 0B 0F
    """
    
    def __init__(self):
        self.key = AES_KEY
        print(f"[AES] Initialized with column-major transformation")
    
    def _to_column_major(self, data):
        """Convert standard byte order to column-major."""
        if len(data) != 16:
            raise ValueError("Data must be exactly 16 bytes")
        
        # Rearrange into 4x4 column-major matrix
        result = bytearray(16)
        for i in range(16):
            row = i % 4
            col = i // 4
            new_index = col + (row * 4)
            result[new_index] = data[i]
        
        return bytes(result)
    
    def _from_column_major(self, data):
        """Convert column-major byte order back to standard."""
        if len(data) != 16:
            raise ValueError("Data must be exactly 16 bytes")
        
        # Rearrange back from column-major
        result = bytearray(16)
        for i in range(16):
            row = i // 4
            col = i % 4
            old_index = col + (row * 4)
            result[i] = data[old_index]
        
        return bytes(result)
    
    def encrypt(self, data):
        """Encrypt with column-major byte arrangement."""
        if len(data) != 16:
            raise ValueError("Data must be exactly 16 bytes")
        
        # Convert to column-major
        column_major_data = self._to_column_major(data)
        
        # Encrypt
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted = cipher.encrypt(column_major_data)
        
        # Convert back from column-major
        result = self._from_column_major(encrypted)
        
        print(f"[ENCRYPT] Plaintext:  {data.hex()}")
        print(f"[ENCRYPT] Ciphertext: {result.hex()}")
        
        return result
    
    def decrypt(self, data):
        """Decrypt with column-major byte arrangement."""
        if len(data) != 16:
            raise ValueError("Data must be exactly 16 bytes")
        
        # Convert to column-major
        column_major_data = self._to_column_major(data)
        
        # Decrypt
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted = cipher.decrypt(column_major_data)
        
        # Convert back from column-major
        result = self._from_column_major(decrypted)
        
        print(f"[DECRYPT] Ciphertext: {data.hex()}")
        print(f"[DECRYPT] Plaintext:  {result.hex()}")
        
        return result


# ========== Character Font Data ==========
CHAR_FONT = {
    'A': bytes([0x7F, 0x00, 0x7F, 0x00, 0x68, 0x00, 0x7F, 0x00, 0x00, 0x00]),
    'B': bytes([0x7F, 0x00, 0x7F, 0x00, 0x49, 0x00, 0x36, 0x00, 0x00, 0x00]),
    'C': bytes([0x3E, 0x00, 0x7F, 0x00, 0x41, 0x00, 0x41, 0x00, 0x00, 0x00]),
    'D': bytes([0x7F, 0x00, 0x7F, 0x00, 0x41, 0x00, 0x3E, 0x00, 0x00, 0x00]),
    'E': bytes([0x7F, 0x00, 0x7F, 0x00, 0x49, 0x00, 0x49, 0x00, 0x00, 0x00]),
    'F': bytes([0x7F, 0x00, 0x7F, 0x00, 0x48, 0x00, 0x48, 0x00, 0x00, 0x00]),
    'G': bytes([0x3E, 0x00, 0x7F, 0x00, 0x41, 0x00, 0x49, 0x00, 0x0E, 0x00, 0x00, 0x00]),
    'H': bytes([0x7F, 0x00, 0x7F, 0x00, 0x08, 0x00, 0x08, 0x00, 0x7F, 0x00, 0x00, 0x00]),
    'I': bytes([0x41, 0x00, 0x7F, 0x00, 0x7F, 0x00, 0x41, 0x00, 0x00, 0x00]),
    'J': bytes([0x42, 0x00, 0x41, 0x00, 0x7F, 0x00, 0x7E, 0x00, 0x00, 0x00]),
    'K': bytes([0x7F, 0x00, 0x7F, 0x00, 0x0C, 0x00, 0x17, 0x00, 0x23, 0x00, 0x00, 0x00]),
    'L': bytes([0x7F, 0x00, 0x7F, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00]),
    'M': bytes([0x7F, 0x00, 0x7F, 0x00, 0x60, 0x00, 0x7E, 0x00, 0x60, 0x00, 0x7F, 0x00, 0x00, 0x00]),
    'N': bytes([0x7F, 0x00, 0x7F, 0x00, 0x18, 0x00, 0x0C, 0x00, 0x7F, 0x00, 0x00, 0x00]),
    'O': bytes([0x3E, 0x00, 0x7F, 0x00, 0x41, 0x00, 0x3E, 0x00, 0x00, 0x00]),
    'P': bytes([0x7F, 0x00, 0x7F, 0x00, 0x48, 0x00, 0x78, 0x00, 0x00, 0x00]),
    'Q': bytes([0x3E, 0x00, 0x7F, 0x00, 0x41, 0x00, 0x3E, 0x00, 0x03, 0x00, 0x00, 0x00]),
    'R': bytes([0x7F, 0x00, 0x7F, 0x00, 0x48, 0x00, 0x37, 0x00, 0x00, 0x00]),
    'S': bytes([0x32, 0x00, 0x79, 0x00, 0x49, 0x00, 0x26, 0x00, 0x00, 0x00]),
    'T': bytes([0x60, 0x00, 0x7F, 0x00, 0x7F, 0x00, 0x60, 0x00, 0x00, 0x00]),
    'U': bytes([0x7E, 0x00, 0x7F, 0x00, 0x01, 0x00, 0x7E, 0x00, 0x00, 0x00]),
    'V': bytes([0x7C, 0x00, 0x7E, 0x00, 0x03, 0x00, 0x02, 0x00, 0x7C, 0x00, 0x00, 0x00]),
    'W': bytes([0x7E, 0x00, 0x7F, 0x00, 0x01, 0x00, 0x3E, 0x00, 0x01, 0x00, 0x7E, 0x00, 0x00, 0x00]),
    'X': bytes([0x63, 0x00, 0x36, 0x00, 0x1C, 0x00, 0x36, 0x00, 0x63, 0x00, 0x00, 0x00]),
    'Y': bytes([0x70, 0x00, 0x79, 0x00, 0x0F, 0x00, 0x08, 0x00, 0x70, 0x00, 0x00, 0x00]),
    'Z': bytes([0x63, 0x00, 0x65, 0x00, 0x6D, 0x00, 0x73, 0x00, 0x00, 0x00]),
    '0': bytes([0x3E, 0x00, 0x7F, 0x00, 0x41, 0x00, 0x3E, 0x00, 0x00, 0x00]),
    '1': bytes([0x21, 0x00, 0x7F, 0x00, 0x7F, 0x00, 0x01, 0x00, 0x00, 0x00]),
    '2': bytes([0x27, 0x00, 0x4F, 0x00, 0x59, 0x00, 0x31, 0x00, 0x00, 0x00]),
    '3': bytes([0x22, 0x00, 0x49, 0x00, 0x7F, 0x00, 0x36, 0x00, 0x00, 0x00]),
    '4': bytes([0x0C, 0x00, 0x1C, 0x00, 0x34, 0x00, 0x6F, 0x00, 0x04, 0x00, 0x00, 0x00]),
    '5': bytes([0x7A, 0x00, 0x59, 0x00, 0x4F, 0x00, 0x46, 0x00, 0x00, 0x00]),
    '6': bytes([0x3E, 0x00, 0x7F, 0x00, 0x49, 0x00, 0x2E, 0x00, 0x00, 0x00]),
    '7': bytes([0x63, 0x00, 0x4F, 0x00, 0x7C, 0x00, 0x70, 0x00, 0x00, 0x00]),
    '8': bytes([0x3E, 0x00, 0x7F, 0x00, 0x49, 0x00, 0x3E, 0x00, 0x00, 0x00]),
    '9': bytes([0x3A, 0x00, 0x79, 0x00, 0x49, 0x00, 0x3E, 0x00, 0x00, 0x00]),
    ' ': bytes([0x00, 0x00, 0x00, 0x00]),
}


def encode_text(text):
    """Encode text string into LED matrix byte array."""
    result = bytearray()
    
    for char in text.upper():
        if char in CHAR_FONT:
            result.extend(CHAR_FONT[char])
        else:
            print(f"[WARNING] Character '{char}' not in font, using space")
            result.extend(CHAR_FONT[' '])
    
    return bytes(result)


def create_packet(data):
    """Create a 16-byte packet with proper padding."""
    if len(data) > 16:
        raise ValueError("Packet data cannot exceed 16 bytes")
    return data + b'\x00' * (16 - len(data))


def send_text(control_char, data_char, notify_char, text, cipher, display_mode='static'):
    """Send text to glasses with specified display mode."""
    
    print(f"\n[TEXT] Encoding '{text}' for display...")
    encoded_data = encode_text(text)
    data_size = len(encoded_data)
    print(f"    Encoded {len(text)} chars -> {data_size} bytes")
    
    # Get display mode settings
    if display_mode not in DISPLAY_MODES:
        print(f"[WARNING] Unknown mode '{display_mode}', using 'static'")
        display_mode = 'static'
    
    mode_value, move_type, mode_desc = DISPLAY_MODES[display_mode]
    print(f"    Display mode: {mode_desc}")
    
    # Step 1: ATATS command
    print("\n[1] Sending ATATS command...")
    size_hi = (data_size >> 8) & 0xFF
    size_lo = data_size & 0xFF
    atats_packet = create_packet(bytes([7, 65, 84, 65, 84, 83, 1, size_hi, size_lo]))
    encrypted_atats = cipher.encrypt(atats_packet)
    control_char.write(encrypted_atats)
    print("    ✓ Sent ATATS")
    time.sleep(0.5)
    
    # Step 2: Data packets
    print(f"\n[2] Sending {data_size} bytes in chunks...")
    offset = 0
    packet_num = 0
    
    while offset < data_size:
        remaining = data_size - offset
        chunk_size = min(15, remaining)
        chunk_data = encoded_data[offset:offset + chunk_size]
        data_packet = create_packet(bytes([chunk_size]) + chunk_data)
        encrypted_data = cipher.encrypt(data_packet)
        data_char.write(encrypted_data)
        packet_num += 1
        offset += chunk_size
        print(f"    Packet {packet_num}: {chunk_size} bytes")
        time.sleep(0.05)
    
    print(f"    ✓ Sent {packet_num} packets")
    
    # Step 3: ATCP command
    print("\n[3] Sending ATCP command...")
    atcp_packet = create_packet(bytes([5, 65, 84, 67, 80]))
    encrypted_atcp = cipher.encrypt(atcp_packet)
    control_char.write(encrypted_atcp)
    print("    ✓ Sent ATCP")
    time.sleep(0.5)
    
    # Step 4: MODE command
    print(f"\n[4] Activating display ({mode_desc})...")
    mode_packet = create_packet(bytes([6, 0x4D, 0x4F, 0x44, 0x45, mode_value, move_type]))
    encrypted_mode = cipher.encrypt(mode_packet)
    control_char.write(encrypted_mode)
    print(f"    ✓ Sent MODE {mode_value} (moveType {move_type})")
    time.sleep(0.2)
    
    print(f"\n[SUCCESS] Text '{text}' displayed with mode '{mode_desc}'!")


def main():
    parser = argparse.ArgumentParser(
        description='BLE LED Glasses Text Update PoC',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Display Modes:
  static        Text stays in one place
  scroll-left   Text scrolls from right to left
  scroll-right  Text scrolls from left to right
  scroll-down   Text scrolls from top to bottom
  scroll-up     Text scrolls from bottom to top

Examples:
  %(prog)s --text "HELLO" --display-mode static
  %(prog)s --text "HELLO" --display-mode scroll-left
  %(prog)s --text "TEST 123" --display-mode scroll-right
        """
    )
    parser.add_argument('--text', type=str, default='HELLO', help='Text to display')
    parser.add_argument('--device', type=str, default='GLASSES-12B008', help='Device name')
    parser.add_argument('--port', type=str, default='/dev/ttyACM0', help='Serial port')
    parser.add_argument('--scan-time', type=int, default=3, help='Scan duration (seconds)')
    parser.add_argument('--display-mode', type=str, default='static',
                        choices=list(DISPLAY_MODES.keys()),
                        help='Display mode (default: static)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("BLE LED Glasses Text Update PoC - IMPROVED VERSION!")
    print("=" * 70)
    print(f"Target Device:  {args.device}")
    print(f"Text to Send:   {args.text}")
    print(f"Display Mode:   {args.display_mode}")
    print(f"AES Key:        {AES_KEY.hex()}")
    print("=" * 70)
    
    try:
        try:
            from blatann import BleDevice
        except ImportError:
            print("\n[ERROR] blatann library not found!")
            print("Install with: pip install blatann")
            return 1
        
        print("\n[INIT] Initializing BLE adapter...")
        ble_device = BleDevice(args.port)
        ble_device.configure()
        ble_device.open()
        print("✓ BLE adapter ready")
        
        # Initialize cipher
        cipher = ColumnMajorAESCipher()
        
        # Scan for device
        print(f"\n[SCAN] Scanning for '{args.device}'...")
        target_address = None
        
        def on_scan_result(sender, scan_report):
            nonlocal target_address
            if scan_report.device_name == args.device:
                print(f"✓ Found: {scan_report.peer_address} ({scan_report.device_name})")
                target_address = scan_report.peer_address
                ble_device.scanner.stop()
        
        ble_device.scanner.on_scan_received.register(on_scan_result)
        ble_device.scanner.start_scan().wait(timeout=args.scan_time, exception_on_timeout=False)
        
        if not target_address:
            print(f"✗ Device not found in {args.scan_time}s")
            return 1
        
        # Connect
        print(f"\n[CONNECT] Connecting to {target_address}...")
        conn = ble_device.connect(target_address).wait()
        print("✓ Connected")
        
        # Discover services
        print("\n[DISCOVER] Discovering services...")
        conn.discover_services().wait()
        db = conn.database
        print(f"✓ Found {len(db.services)} services")
        
        # Find characteristics
        print(f"\n[SERVICE] Finding characteristics...")
        target_service = None
        for service in db.services:
            service_uuid_str = str(service.uuid).lower()
            if service_uuid_str == SERVICE_UUID_SHORT or service_uuid_str == SERVICE_UUID.lower():
                target_service = service
                print(f"✓ Matched service: {service_uuid_str}")
                break
        
        if not target_service:
            print("✗ Service not found")
            conn.disconnect()
            return 1
        
        control_char = None
        data_char = None
        notify_char = None
        
        for char in target_service.characteristics:
            uuid_str = str(char.uuid).lower()
            if uuid_str == CHAR_CONTROL_UUID.lower():
                control_char = char
                print(f"✓ Control characteristic: {char.value_attribute.handle}")
            elif uuid_str == CHAR_DATA_UUID.lower():
                data_char = char
                print(f"✓ Data characteristic: {char.value_attribute.handle}")
            elif uuid_str == CHAR_NOTIFY_UUID.lower():
                notify_char = char
                print(f"✓ Notify characteristic: {char.value_attribute.handle}")
        
        if not (control_char and data_char and notify_char):
            print("✗ Missing characteristics")
            conn.disconnect()
            return 1
        
        # Enable notifications
        print("\n[NOTIFY] Enabling notifications...")
        def on_notification(characteristic, event_args):
            data = event_args.value
            print(f"    RX: {data.hex()}")
            # Try to decrypt and show response
            try:
                decrypted = cipher.decrypt(data)
                # Check if it's a text response
                if decrypted[0] > 0 and decrypted[0] < 16:
                    length = decrypted[0]
                    text = decrypted[1:length+1]
                    # Try to decode as ASCII
                    try:
                        ascii_text = text.decode('ascii', errors='ignore')
                        if ascii_text.isprintable():
                            print(f"    Decoded: {ascii_text}")
                    except:
                        pass
            except:
                pass
        
        notify_char.subscribe(on_notification).wait()
        print("✓ Notifications enabled")
        
        print("\n[START] Sending text to glasses in 2 seconds...")
        time.sleep(2)
        
        # Send text
        send_text(control_char, data_char, notify_char, args.text, cipher, args.display_mode)
        
        # Wait a bit to see the result
        print("\n[WAIT] Waiting 2 seconds to observe display...")
        time.sleep(2)
        
        # Disconnect
        print("\n[DISCONNECT] Disconnecting...")
        conn.disconnect().wait()
        print("✓ Disconnected")
        
        print("\n" + "=" * 70)
        print("✅ COMPLETE! Check your glasses!")
        print("=" * 70)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        try:
            ble_device.close()
        except:
            pass


if __name__ == '__main__':
    sys.exit(main())
