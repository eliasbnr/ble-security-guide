// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'BLE Security Guide',
  tagline: 'Leitfaden zur Sicherheitsanalyse von BLE IoT-Geräten',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://ble.eliasbnr.me',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/',

  // GitHub pages deployment config (if needed)
  organizationName: 'eliasbnr',
  projectName: 'ble-security-guide',
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Internationalization
  i18n: {
    defaultLocale: 'de',
    locales: ['de', 'en'],
    localeConfigs: {
      de: {
        htmlLang: 'de-DE',
        label: 'Deutsch',
      },
      en: {
        htmlLang: 'en-US',
        label: 'English',
      },
    },
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Remove or configure editUrl if needed
          // editUrl: 'https://github.com/your-org/ble-security-guide/tree/main/',
        },
        blog: false, // Disable blog
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  // Mermaid support
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Social card image
      image: 'img/social-card.jpg',
      navbar: {
        title: 'BLE Security Guide',
        logo: {
          alt: 'BLE Security Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: '📘 Tutorials',
          },
          {
            type: 'docSidebar',
            sidebarId: 'referenceSidebar',
            position: 'left',
            label: '🧠 BLE Grundlagen',
          },
          {
            type: 'docSidebar',
            sidebarId: 'casestudySidebar',
            position: 'left',
            label: '🔬 Fallstudien',
          },
          {
            type: 'docSidebar',
            sidebarId: 'downloadsSidebar',
            position: 'left',
            label: '📂 Downloads',
          },
          {
            to: '/docs/sources',
            position: 'left',
            label: '📚 Quellen',
          },
          {
            type: 'localeDropdown',
            position: 'right',
          },
          {
            href: 'https://github.com/eliasbnr/ble-security-guide',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Dokumentation',
            items: [
              {
                label: 'Tutorials',
                to: '/docs/tutorials/intro',
              },
              {
                label: 'BLE Grundlagen',
                to: '/docs/reference/ble-basics',
              },
              {
                label: 'Fallstudien',
                to: '/docs/casestudies/overview',
              },
            ],
          },
          {
            title: 'Ressourcen',
            items: [
              {
                label: 'Downloads',
                to: '/docs/downloads/scripts',
              },
              {
                label: 'Quellen',
                to: '/docs/sources',
              },
            ],
          },
          {
            title: 'Extern',
            items: [
              {
                label: 'OWASP ISTG',
                href: 'https://owasp.org/www-project-iot-security-testing-guide/',
              },
              {
                label: 'Bluetooth SIG',
                href: 'https://www.bluetooth.com/specifications/',
              },
              {
                label: 'blatann Docs',
                href: 'https://blatann.readthedocs.io/',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} BLE Security Guide. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['bash', 'python', 'java', 'json', 'latex'],
      },
      mermaid: {
        theme: {light: 'neutral', dark: 'dark'},
      },
    }),
};

export default config;
