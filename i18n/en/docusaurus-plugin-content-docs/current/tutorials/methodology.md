---
sidebar_position: 2
title: "Methodology"
---

# Test Methodology

A structured methodology is essential for reproducible security analyses.

## The 5-Phase Process

```mermaid
flowchart TB
    subgraph P1["Phase 1: Passive"]
        P1A["Scanning"]
        P1B["Adv Analysis"]
        P1C["Capture"]
    end
    
    subgraph P2["Phase 2: Active"]
        P2A["GATT Enum"]
        P2B["Char Test"]
        P2C["Security Test"]
    end
    
    subgraph P3["Phase 3: App"]
        P3A["APK Extract"]
        P3B["Decompile"]
        P3C["Crypto Find"]
    end
    
    subgraph P4["Phase 4: Exploit"]
        P4A["PoC Dev"]
        P4B["Replay"]
        P4C["Auth Bypass"]
    end
    
    subgraph P5["Phase 5: Report"]
        P5A["CVSS"]
        P5B["Document"]
        P5C["Disclosure"]
    end
    
    P1 --> P2 --> P3 --> P4 --> P5
```

## Phase Overview

| Phase | Duration | Output |
|-------|----------|--------|
| Phase 1 | 2-4h | Device profile, PCAP |
| Phase 2 | 2-3h | GATT database |
| Phase 3 | 4-8h | Protocol, Keys |
| Phase 4 | 3-6h | Working PoC |
| Phase 5 | 2-4h | Security report |

---

:::tip Next Step
Continue with [Hardware Setup](./setup/hardware).
:::
