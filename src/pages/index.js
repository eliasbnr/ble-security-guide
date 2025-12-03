import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Translate, {translate} from '@docusaurus/Translate';
import styles from './index.module.css';

function HomepageHeader() {
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">
          🔐 <Translate id="homepage.title">BLE Security Guide</Translate>
        </h1>
        <p className="hero__subtitle">
          <Translate id="homepage.tagline">
            Leitfaden zur Sicherheitsanalyse von BLE IoT-Geräten
          </Translate>
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/tutorials/intro">
            <Translate id="homepage.tutorial.button">📘 Tutorial starten</Translate>
          </Link>
          <Link
            className="button button--outline button--lg"
            to="/docs/reference/ble-basics"
            style={{marginLeft: '1rem'}}>
            <Translate id="homepage.reference.button">🧠 BLE Grundlagen</Translate>
          </Link>
        </div>
      </div>
    </header>
  );
}

function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <div className={clsx('col col--4')}>
            <div className="padding-horiz--md padding-vert--lg">
              <h3><Translate id="homepage.feature1.title">🎓 Für Einsteiger</Translate></h3>
              <p><Translate id="homepage.feature1.desc">Keine BLE-Vorkenntnisse nötig. Wir erklären alles von GATT bis Pairing.</Translate></p>
            </div>
          </div>
          <div className={clsx('col col--4')}>
            <div className="padding-horiz--md padding-vert--lg">
              <h3><Translate id="homepage.feature2.title">🔬 Praxis-orientiert</Translate></h3>
              <p><Translate id="homepage.feature2.desc">Echte Fallstudien: LED-Brille, Smart Waage, LED-Strips mit funktionierenden PoCs.</Translate></p>
            </div>
          </div>
          <div className={clsx('col col--4')}>
            <div className="padding-horiz--md padding-vert--lg">
              <h3><Translate id="homepage.feature3.title">⚖️ Rechtlich fundiert</Translate></h3>
              <p><Translate id="homepage.feature3.desc">Rechtlicher Rahmen für Deutschland inkl. StGB §202a/b/c und geplanter Reform.</Translate></p>
            </div>
          </div>
          <div className={clsx('col col--4')}>
            <div className="padding-horiz--md padding-vert--lg">
              <h3><Translate id="homepage.feature4.title">🛠️ Tool-Fokus</Translate></h3>
              <p><Translate id="homepage.feature4.desc">nRF52840 Dongle, blatann, Wireshark, JADX - alles was du brauchst.</Translate></p>
            </div>
          </div>
          <div className={clsx('col col--4')}>
            <div className="padding-horiz--md padding-vert--lg">
              <h3><Translate id="homepage.feature5.title">📝 Report-Ready</Translate></h3>
              <p><Translate id="homepage.feature5.desc">CVSS-Scoring, Templates und Best Practices für professionelle Berichte.</Translate></p>
            </div>
          </div>
          <div className={clsx('col col--4')}>
            <div className="padding-horiz--md padding-vert--lg">
              <h3><Translate id="homepage.feature6.title">🌍 Zweisprachig</Translate></h3>
              <p><Translate id="homepage.feature6.desc">Verfügbar auf Deutsch und Englisch mit vollständiger Übersetzung.</Translate></p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  return (
    <Layout
      title={translate({id: 'homepage.meta.title', message: 'Home'})}
      description={translate({id: 'homepage.meta.description', message: 'Leitfaden zur Sicherheitsanalyse von BLE IoT-Geräten'})}>
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <section className="container margin-vert--xl">
          <div className="row">
            <div className="col col--8 col--offset-2">
              <h2>🚀 <Translate id="homepage.quickstart.title">Schnellstart</Translate></h2>
              <pre style={{padding: '1rem', borderRadius: '8px'}}>
{`# Hardware: nRF52840 USB Dongle (~10€)

# Software installieren
pip install blatann pycryptodome

# Ersten Scan starten
python3 scanner.py /dev/ttyACM0`}
              </pre>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
