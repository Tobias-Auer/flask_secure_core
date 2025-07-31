# flask-secure-core

> ⚠️ **Hinweis:** Dieses Projekt befindet sich aktuell in der **Entwicklungsphase**.  
> Viele Funktionen sind noch nicht vollständig implementiert und können sich ändern.  
> Die Nutzung erfolgt auf eigene Verantwortung. Feedback und Mitarbeit sind willkommen!

**`flask-secure-core`** ist eine modulare Flask-Library zur schnellen Integration von User-Login, Rechteverwaltung und Admin-UI in deine Flask-Projekte.

---

## ✨ Features

- 🔐 Benutzer-Authentifizierung (Login, Logout, Registrierung, Passwort ändern)
- 🛡️ Zugriffskontrolle mit `@secure(<accessLevel>)` Decorator
- 🗂️ Admin-Panel mit Nutzerübersicht, Rollenverwaltung, Passwortänderung und Benutzerverwaltung
- ⚙️ Konfigurierbare Einstellungen über eine Web-Oberfläche (`/adminConfig`)
- 🗃️ Flexible Datenbankwahl:
  - Eigene SQLite-Datei
  - Bestehende PostgreSQL-Datenbank
  - Bestehende MySQL/MariaDB-Datenbank
- 🎨 Anpassbare Templates und Webpfade
- 🔒 Sicherheit per Default (CSRF, Hashing, Session-Control)

---

## ⚙️ Installation

```bash
pip install flask-secure-core
```

---

## 🚀 Schnellstart

```python
from flask import Flask
import flask_secure_core as flsec

app = Flask(__name__)
flsec.init_app(
    app,
    db_type="sqlite",         # "sqlite", "postgresql" oder "mysql"
    db_path="users.db"        # Nur bei SQLite notwendig
)

app.run()
```

---

## 🔧 Zugriffskontrolle per Decorator

```python
@flsec.secure("admin")
@app.route("/admin/dashboard")
def dashboard():
    return "Nur Admins dürfen das sehen"
```

Zugriffslevel sind vollständig konfigurierbar.

---

## 🔐 Benutzerrollen

Standardmäßig enthalten:

- `admin`
- `moderator`
- `user`

Eigene Rollen und Hierarchien können in der Admin-Konfiguration oder per Code definiert werden.

---

## 🛠️ Admin-Konfigurationsseite (`/adminConfig`)

- Aktivieren/Deaktivieren der Registrierung
- Template-Auswahl (z. B. Light/Dark Themes, eigene HTML-Dateien)
- Auswahl des Hashing-Algorithmus (`bcrypt`, `argon2`, `pbkdf2`)
- Freie Konfiguration der internen Routen wie `/admin`, `/login`, `/register`, etc.
- Weitere Lib-spezifische Optionen (API aktivieren, Rate-Limit setzen, etc.)

---

## 🖥️ Admin-Panel (`/admin`)

- Aktive Nutzer einsehen
- Accounts deaktivieren, löschen, oder Passwörter zurücksetzen
- Neue Nutzer erstellen
- Rollen verwalten
- Letzter Login und Account-Aktivität anzeigen

---

## 🧩 Optional: REST-API Endpunkte

Diese können in der Konfiguration aktiviert werden:

- `POST /api/login`
- `POST /api/logout`
- `POST /api/register`
- `GET  /api/userinfo`

Antworten im JSON-Format – ideal für SPAs oder mobile Clients.

---


## 🔐 Sicherheitsfeatures

- CSRF-Schutz für alle Formulare
- Passwort-Hashing mit sicherem Algorithmus (Standard: bcrypt)
- Session-Timeout & Auto-Logout
- Brute-Force-Schutz mit Login-Limits (optionale Integration mit Flask-Limiter)
- Email-basiertes Passwort-Zurücksetzen (via Token-Link)

---

## 📦 Roadmap (geplant)

- Zwei-Faktor-Authentifizierung (TOTP, via App)
- Gruppenbasierte Rechteverwaltung
- Benutzer-Aktivitätsprotokoll (Audit Log)
- SSO-Unterstützung

---


## 💬 Kontakt

Entwickelt von **Tobias Auer**  
🌐 [www.t-auer.com](https://www.t-auer.com)  
📫 Bei Fragen, Feature-Wünschen oder Bugreports GitHub Issues benutzen

