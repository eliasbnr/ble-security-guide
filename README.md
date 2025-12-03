# BLE Security Guide

Leitfaden zur Sicherheitsanalyse von BLE IoT-Geräten.

## 🚀 Quick Start

```bash
# Abhängigkeiten installieren
npm install

# Development Server starten
npm start

# Für deutsche Version
npm run start:de

# Produktion-Build
npm run build
```

## 📁 Struktur

```
ble-security-guide/
├── docs/                  # Dokumentation (Markdown)
│   ├── tutorials/         # Schritt-für-Schritt Anleitungen
│   ├── reference/         # BLE Grundlagen (Knowledge Base)
│   └── downloads/         # Scripts, Templates
├── i18n/                  # Übersetzungen
│   └── en/                # Englische Version
├── src/                   # React-Komponenten
├── static/                # Statische Dateien
│   └── downloads/         # Herunterladbare Skripte
└── docusaurus.config.js   # Konfiguration
```

## 🔧 Konfiguration

### Sprachen hinzufügen

1. `docusaurus.config.js` → `i18n.locales` erweitern
2. `npm run write-translations -- --locale <code>`
3. Dateien in `i18n/<code>/` übersetzen

### Neue Seiten

1. Markdown-Datei in `docs/` erstellen
2. Frontmatter hinzufügen:
   ```yaml
   ---
   sidebar_position: 1
   title: "Seitentitel"
   ---
   ```
3. In `sidebars.js` eintragen

## 📝 Lizenz

MIT

## 👤 Autor

Elias Bennour - Abschlussarbeit "Schwachstellen im Dialog"
