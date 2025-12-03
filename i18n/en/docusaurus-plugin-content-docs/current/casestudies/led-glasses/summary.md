---
sidebar_position: 1
title: "Summary"
---

# LED Glasses - Security Analysis

## Device Profile

| Property | Value |
|----------|-------|
| **Device Name** | GLASSES-12B008 |
| **Manufacturer** | Unknown (China) |
| **Companion App** | "LED Glasses" (Android) |
| **BLE Service** | 0xFFF0 (Custom) |

## Executive Summary

The LED glasses use **AES-128 ECB encryption** with a **hardcoded key** that could be extracted from the Android app. Additionally, a proprietary **column-major byte transformation** is applied before and after encryption.

### Critical Findings

| Finding | CVSS | Severity |
|---------|------|----------|
| F-001: Hardcoded AES Key | 9.8 | Critical |
| F-002: ECB Mode Usage | 4.7 | Medium |
| F-003: No BLE Authentication | 8.8 | High |
