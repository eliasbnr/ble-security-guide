---
sidebar_position: 1
title: "Summary"
---

# Smart Scale - Security Analysis

## Device Profile

| Property | Value |
|----------|-------|
| **Device Name** | Yoda1 / QN-Scale |
| **Companion App** | "Yolanda Health" |
| **Manufacturer ID** | 0x05C0 |

## Executive Summary

The smart scale sends **weight data unencrypted** in BLE advertising packets. Anyone with a BLE scanner in range (~10m) can read the weight in real-time.

### Finding

| Finding | CVSS | Severity |
|---------|------|----------|
| F-001: Weight in Advertising | 5.3 | Medium |

## Privacy Impact

An attacker can:
- ✗ Read weight in real-time
- ✗ Track weight over time
- ✗ Identify person via MAC
- ✗ Purely passive, no connection needed!
