---
sidebar_position: 3
title: "UUID Extraction"
---

# UUID Extraction

Extract all UUIDs from the decompiled code.

```bash
grep -rEo "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}" sources/
```

---

:::tip Next Step
Continue with [Crypto Analysis](./crypto-analysis).
:::
