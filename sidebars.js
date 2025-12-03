/**
 * Sidebars Configuration
 */

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // Tutorials Sidebar
  tutorialSidebar: [
    'tutorials/intro',
    'tutorials/prerequisites',
    'tutorials/methodology',
    'tutorials/legal-framework',
    {
      type: 'category',
      label: '🔧 Setup',
      collapsed: false,
      items: [
        'tutorials/setup/hardware',
        'tutorials/setup/software',
        'tutorials/setup/nrf-sniffer',
        'tutorials/setup/blatann',
      ],
    },
    {
      type: 'category',
      label: '📡 Phase 1: Reconnaissance',
      collapsed: true,
      items: [
        'tutorials/phase1/passive-scanning',
        'tutorials/phase1/advertising-analysis',
        'tutorials/phase1/wireshark-capture',
      ],
    },
    {
      type: 'category',
      label: '🔍 Phase 2: Aktive Analyse',
      collapsed: true,
      items: [
        'tutorials/phase2/gatt-enumeration',
        'tutorials/phase2/characteristic-testing',
        'tutorials/phase2/security-level-testing',
      ],
    },
    {
      type: 'category',
      label: '📱 Phase 3: App-Analyse',
      collapsed: true,
      items: [
        'tutorials/phase3/apk-extraction',
        'tutorials/phase3/jadx-decompilation',
        'tutorials/phase3/uuid-extraction',
        'tutorials/phase3/crypto-analysis',
        'tutorials/phase3/ghidra-native',
      ],
    },
    {
      type: 'category',
      label: '💥 Phase 4: Exploitation',
      collapsed: true,
      items: [
        'tutorials/phase4/poc-development',
        'tutorials/phase4/replay-attacks',
        'tutorials/phase4/auth-bypass',
      ],
    },
    {
      type: 'category',
      label: '📝 Phase 5: Reporting',
      collapsed: true,
      items: [
        'tutorials/phase5/vulnerability-assessment',
        'tutorials/phase5/cvss-scoring',
        'tutorials/phase5/report-writing',
        'tutorials/phase5/responsible-disclosure',
      ],
    },
  ],
  
  // BLE Grundlagen / Reference Sidebar
  referenceSidebar: [
    'reference/ble-basics',
    'reference/gatt-architecture',
    'reference/att-protocol',
    'reference/uuid-system',
    {
      type: 'category',
      label: '🔐 Security',
      collapsed: false,
      items: [
        'reference/security-modes',
        'reference/pairing-mechanisms',
        'reference/encryption',
      ],
    },
    {
      type: 'category',
      label: '⚠️ Schwachstellen',
      collapsed: false,
      items: [
        'reference/vulnerability-taxonomy',
        'reference/known-attacks',
        'reference/cwe-mappings',
      ],
    },
    'reference/glossary',
  ],
  
  // Fallstudien / Case Studies Sidebar
  casestudySidebar: [
    'casestudies/overview',
    {
      type: 'category',
      label: '🕶️ LED Brille',
      collapsed: false,
      items: [
        'casestudies/led-glasses/summary',
        'casestudies/led-glasses/reconnaissance',
        'casestudies/led-glasses/app-analysis',
        'casestudies/led-glasses/crypto-analysis',
        'casestudies/led-glasses/poc',
        'casestudies/led-glasses/findings',
      ],
    },
    {
      type: 'category',
      label: '💡 LED Strips',
      collapsed: false,
      items: [
        'casestudies/led-strips/summary',
        'casestudies/led-strips/protocol',
        'casestudies/led-strips/encryption',
        'casestudies/led-strips/poc',
        'casestudies/led-strips/findings',
      ],
    },
    {
      type: 'category',
      label: '⚖️ Smart Waage',
      collapsed: false,
      items: [
        'casestudies/smart-scale/summary',
        'casestudies/smart-scale/advertising-leak',
        'casestudies/smart-scale/poc',
        'casestudies/smart-scale/findings',
      ],
    },
  ],
  
  // Downloads Sidebar
  downloadsSidebar: [
    'downloads/scripts',
    'downloads/templates',
    'downloads/pcap-samples',
    'downloads/cheatsheets',
  ],
};

export default sidebars;
