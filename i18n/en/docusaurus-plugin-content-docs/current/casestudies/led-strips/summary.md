---
sidebar_position: 1
title: "Summary"
---

# LED Strips - Security Analysis

## Device Profile

| Property | Value |
|----------|-------|
| **Device Name** | LEDnetWF... |
| **Companion App** | "Magic Home" |
| **BLE Service** | 0xFFE0 |

## Executive Summary

The LED strips use **XOR-based "encryption"** with a **hardcoded 19-byte key**. The encryption is trivial to break.

### Critical Findings

| Finding | CVSS | Severity |
|---------|------|----------|
| F-001: Hardcoded XOR Key | 9.8 | Critical |
| F-002: Trivial Encryption | 9.1 | Critical |
| F-003: No Authentication | 8.8 | High |
