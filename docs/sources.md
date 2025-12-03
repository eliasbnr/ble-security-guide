---
sidebar_position: 12
title: "Quellen & Referenzen"
---

# Quellen & Referenzen

Diese Seite listet alle verwendeten Quellen, weiterführende Literatur und nützliche Ressourcen.

## Offizielle Spezifikationen

### Bluetooth SIG

| Dokument | Version | Link |
|----------|---------|------|
| Bluetooth Core Specification | 5.4 | [bluetooth.com/specifications](https://www.bluetooth.com/specifications/specs/core-specification-5-4/) |
| GATT Specification | - | [bluetooth.com/specifications](https://www.bluetooth.com/specifications/specs/generic-attribute-profile/) |
| Assigned Numbers | - | [bluetooth.com/specifications/assigned-numbers](https://www.bluetooth.com/specifications/assigned-numbers/) |
| Security Manager Specification | - | Teil der Core Spec |

### Zitierweise

```bibtex
@techreport{bluetooth_core_5_4,
  title = {Bluetooth Core Specification},
  version = {5.4},
  year = {2023},
  institution = {Bluetooth SIG},
  url = {https://www.bluetooth.com/specifications/specs/core-specification-5-4/}
}
```

## Security Standards & Frameworks

### OWASP

| Dokument | Beschreibung | Link |
|----------|--------------|------|
| **OWASP ISTG v1.0** | IoT Security Testing Guide | [owasp.org/istg](https://owasp.org/www-project-iot-security-testing-guide/) |
| OWASP IoT Top 10 | Häufigste IoT-Schwachstellen | [owasp.org/iot-top-10](https://owasp.org/www-project-internet-of-things/) |
| OWASP Mobile Security | Mobile App Testing | [owasp.org/mastg](https://mas.owasp.org/MASTG/) |

```bibtex
@techreport{owasp_istg,
  title = {OWASP IoT Security Testing Guide},
  version = {1.0},
  year = {2024},
  institution = {OWASP Foundation},
  url = {https://owasp.org/www-project-iot-security-testing-guide/}
}
```

### NIST

| Dokument | Beschreibung | Link |
|----------|--------------|------|
| **NIST SP 800-213** | IoT Device Cybersecurity | [nist.gov](https://csrc.nist.gov/publications/detail/sp/800-213/final) |
| NIST SP 800-183 | Networks of Things | [nist.gov](https://csrc.nist.gov/publications/detail/sp/800-183/final) |
| NISTIR 8259 | IoT Device Manufacturers | [nist.gov](https://csrc.nist.gov/publications/detail/nistir/8259/final) |

```bibtex
@techreport{nist_sp800_213,
  title = {IoT Device Cybersecurity Guidance for the Federal Government},
  number = {SP 800-213},
  year = {2021},
  institution = {NIST},
  url = {https://csrc.nist.gov/publications/detail/sp/800-213/final}
}
```

### BSI

| Dokument | Beschreibung | Link |
|----------|--------------|------|
| **BSI TR-03148** | Secure Broadband Router | [bsi.bund.de](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr03148/tr03148_node.html) |
| BSI-Grundschutz | IT-Grundschutz-Kompendium | [bsi.bund.de](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/IT-Grundschutz-Kompendium/it-grundschutz-kompendium_node.html) |

### EU/ETSI

| Dokument | Beschreibung | Link |
|----------|--------------|------|
| **ETSI EN 303 645** | Cyber Security for Consumer IoT | [etsi.org](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/) |
| **EU CRA 2024/2847** | Cyber Resilience Act | [eur-lex.europa.eu](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R2847) |

```bibtex
@techreport{etsi_en_303645,
  title = {Cyber Security for Consumer Internet of Things: Baseline Requirements},
  number = {ETSI EN 303 645},
  version = {2.1.1},
  year = {2020},
  institution = {ETSI},
  url = {https://www.etsi.org/deliver/etsi_en/303600_303699/303645/}
}
```

## Wissenschaftliche Publikationen

### BLE Security Research

| Titel | Autoren | Jahr | Konferenz/Journal |
|-------|---------|------|-------------------|
| **Breaking BLE Beacons for Fun but Mostly Profit** | Zuo et al. | 2019 | WiSec |
| **SweynTooth: Unleashing Mayhem over Bluetooth Low Energy** | Garbelini et al. | 2020 | USENIX Security |
| **KNOB Attack** | Antonioli et al. | 2019 | USENIX Security |
| **BLESA: Spoofing Attacks against Reconnections in BLE** | Wu et al. | 2020 | WOOT |
| **Method Confusion Attack on Bluetooth Pairing** | von Tschirschnitz et al. | 2021 | IEEE S&P |

```bibtex
@inproceedings{sweyntooth2020,
  title = {SweynTooth: Unleashing Mayhem over Bluetooth Low Energy},
  author = {Garbelini, Matheus E. and others},
  booktitle = {USENIX Security Symposium},
  year = {2020}
}

@inproceedings{knob2019,
  title = {The KNOB is Broken: Exploiting Low Entropy in the Encryption Key Negotiation of Bluetooth BR/EDR},
  author = {Antonioli, Daniele and Tippenhauer, Nils Ole and Rasmussen, Kasper},
  booktitle = {USENIX Security Symposium},
  year = {2019}
}

@inproceedings{blesa2020,
  title = {BLESA: Spoofing Attacks against Reconnections in Bluetooth Low Energy},
  author = {Wu, Jianliang and others},
  booktitle = {WOOT},
  year = {2020}
}
```

### IoT Security

| Titel | Autoren | Jahr | Konferenz/Journal |
|-------|---------|------|-------------------|
| Internet of things Security: A Survey | Alaba et al. | 2017 | IJCSI |
| IoT Security: Review, Blockchain Solutions, and Open Challenges | Khan & Salah | 2018 | Future Generation Computer Systems |

## Bücher

### BLE-Entwicklung

| Titel | Autor | Jahr | ISBN |
|-------|-------|------|------|
| **Getting Started with Bluetooth Low Energy** | Townsend et al. | 2014 | 978-1491949511 |
| **Bluetooth Low Energy: The Developer's Handbook** | Heydon | 2012 | 978-0132888363 |
| **Inside Bluetooth Low Energy** | Gupta | 2016 | 978-1630810894 |

```bibtex
@book{townsend2014ble,
  title = {Getting Started with Bluetooth Low Energy},
  author = {Townsend, Kevin and Cufí, Carles and Davidson, Robert},
  year = {2014},
  publisher = {O'Reilly Media},
  isbn = {978-1491949511}
}
```

### Security & Reverse Engineering

| Titel | Autor | Jahr | ISBN |
|-------|-------|------|------|
| **The IoT Hacker's Handbook** | Gupta | 2019 | 978-1484242995 |
| **Practical IoT Hacking** | Chantzis et al. | 2021 | 978-1718500907 |
| **Android Security Internals** | Elenkov | 2014 | 978-1593275815 |
| **Practical Reverse Engineering** | Dang et al. | 2014 | 978-1118787311 |

```bibtex
@book{practical_iot_hacking,
  title = {Practical IoT Hacking: The Definitive Guide to Attacking the Internet of Things},
  author = {Chantzis, Fotios and others},
  year = {2021},
  publisher = {No Starch Press},
  isbn = {978-1718500907}
}
```

## Tools & Dokumentation

### BLE-Analyse

| Tool | Beschreibung | Link |
|------|--------------|------|
| **blatann** | Python BLE Library für nRF52 | [blatann.readthedocs.io](https://blatann.readthedocs.io/) |
| **Wireshark** | Netzwerk-Protokollanalyse | [wireshark.org](https://www.wireshark.org/) |
| **nRF Sniffer** | BLE Packet Sniffer | [nordicsemi.com](https://www.nordicsemi.com/Products/Development-tools/nRF-Sniffer-for-Bluetooth-LE) |
| BlueZ | Linux Bluetooth Stack | [bluez.org](http://www.bluez.org/) |
| Ubertooth | Open-Source BLE Sniffer | [greatscottgadgets.com](https://greatscottgadgets.com/ubertoothone/) |

### Reverse Engineering

| Tool | Beschreibung | Link |
|------|--------------|------|
| **JADX** | Android APK Decompiler | [github.com/skylot/jadx](https://github.com/skylot/jadx) |
| **Ghidra** | NSA Reverse Engineering Suite | [ghidra-sre.org](https://ghidra-sre.org/) |
| **Frida** | Dynamic Instrumentation | [frida.re](https://frida.re/) |
| APKTool | APK Unpacker | [apktool.org](https://apktool.org/) |
| Radare2 | Reverse Engineering Framework | [radare.org](https://rada.re/n/) |

### Vulnerability Databases

| Ressource | Beschreibung | Link |
|-----------|--------------|------|
| **CVE** | Common Vulnerabilities and Exposures | [cve.mitre.org](https://cve.mitre.org/) |
| **NVD** | National Vulnerability Database | [nvd.nist.gov](https://nvd.nist.gov/) |
| **FIRST CVSS** | CVSS Calculator | [first.org/cvss](https://www.first.org/cvss/calculator/3.1) |
| CWE | Common Weakness Enumeration | [cwe.mitre.org](https://cwe.mitre.org/) |
| CAPEC | Attack Pattern Enumeration | [capec.mitre.org](https://capec.mitre.org/) |

## Rechtliche Grundlagen

### Deutschland

| Gesetz | Beschreibung | Link |
|--------|--------------|------|
| **StGB §202a** | Ausspähen von Daten | [gesetze-im-internet.de](https://www.gesetze-im-internet.de/stgb/__202a.html) |
| **StGB §202b** | Abfangen von Daten | [gesetze-im-internet.de](https://www.gesetze-im-internet.de/stgb/__202b.html) |
| **StGB §202c** | Vorbereiten des Ausspähens | [gesetze-im-internet.de](https://www.gesetze-im-internet.de/stgb/__202c.html) |
| **DSGVO** | Datenschutz-Grundverordnung | [eur-lex.europa.eu](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32016R0679) |
| **BDSG** | Bundesdatenschutzgesetz | [gesetze-im-internet.de](https://www.gesetze-im-internet.de/bdsg_2018/) |

### Gesetzentwurf zur Modernisierung

| Dokument | Datum | Link |
|----------|-------|------|
| RefE Modernisierung Computerstrafrecht | Nov 2024 | [bmj.de](https://www.bmjv.de/SharedDocs/Downloads/DE/Gesetzgebung/RefE/RefE_ComputerStrafR.pdf) |

## Disclosure & Koordination

| Organisation | Beschreibung | Kontakt |
|--------------|--------------|---------|
| **BSI** | Koordinierte Schwachstellenoffenlegung | vulnerability@bsi.bund.de |
| **CERT/CC** | US-CERT Coordination Center | cert@cert.org |
| **FIRST** | Forum of Incident Response Teams | [first.org](https://www.first.org/) |
| **ZDI** | Zero Day Initiative | [zerodayinitiative.com](https://www.zerodayinitiative.com/) |

## Online-Ressourcen

### Tutorials & Blogs

| Ressource | Beschreibung | Link |
|-----------|--------------|------|
| Bluetooth SIG Blog | Offizielle News | [bluetooth.com/blog](https://www.bluetooth.com/blog/) |
| Nordic DevZone | nRF Development | [devzone.nordicsemi.com](https://devzone.nordicsemi.com/) |
| Adafruit BLE Guide | Einsteiger-Tutorial | [learn.adafruit.com](https://learn.adafruit.com/introduction-to-bluetooth-low-energy) |
| Reverse Engineering BLE | Blog-Serie | Diverse |

### CTF & Challenges

| Ressource | Beschreibung | Link |
|-----------|--------------|------|
| HackTheBox | Security Challenges | [hackthebox.com](https://www.hackthebox.com/) |
| DVID | Damn Vulnerable IoT Device | [github.com/Vulcainreo/DVID](https://github.com/Vulcainreo/DVID) |

## Hardware-Bezugsquellen

| Händler | Produkt | Preis | Link |
|---------|---------|-------|------|
| Mouser | nRF52840 Dongle | ~10€ | [mouser.de](https://www.mouser.de/ProductDetail/Nordic-Semiconductor/nRF52840-Dongle) |
| DigiKey | nRF52840 Dongle | ~10€ | [digikey.de](https://www.digikey.de/) |
| Nordic | Direkt | ~10€ | [nordicsemi.com](https://www.nordicsemi.com/Products/Development-hardware/nRF52840-Dongle) |

---

:::tip Hinweis
Alle Links wurden zuletzt im November 2025 überprüft. Bei toten Links bitte Issue erstellen.
:::
