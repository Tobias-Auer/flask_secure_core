# flask-secure-login

> ⚠️ **Hinweis:** Dieses Projekt befindet sich aktuell in der **Entwicklungsphase**.  
> Viele Funktionen sind noch nicht vollständig implementiert und können sich ändern.  
> Die Nutzung erfolgt auf eigene Verantwortung. Feedback ist willkommen!

**`flask-secure-login`** ist eine modulare Flask-Library zur schnellen Integration von User-Login, Rechteverwaltung und Admin-UI in deine Flask-Projekte.

---

## ✨ Features

- 🔐 Benutzer-Authentifizierung (Login, Logout, Registrierung, Passwort ändern)
- 🛡️ Zugriffskontrolle mit `@secure(<accessLevel>)` Decorator
- 🗂️ Admin-Panel mit Nutzerübersicht, Rollenverwaltung, Passwortänderung und Benutzerverwaltung
- ⚙️ Konfigurierbare Einstellungen über eine Web-Oberfläche
- 🗃️ Flexible Datenbankwahl:
  - Eigene SQLite-Datei
  - Bestehende PostgreSQL-Datenbank
- 🎨 Anpassbare Templates und Webpfade
- 🔒 Sicherheit per Default (CSRF, Hashing, Session-Control)

---

## ⚙️ Installation

```bash
pip install flask-secure-login
```

---


## 🔐 Benutzerrollen

Standardmäßig enthalten:

- `admin`
- `moderator`
- `user`

Eigene Rollen und Hierarchien können in der Admin-Konfiguration oder per Code definiert werden.

---

## 🛠️ Admin-Konfigurationsseite

- Aktivieren/Deaktivieren der Registrierung
- Freie Konfiguration der internen Routen wie `/admin`, `/login`, `/register`, etc.
- viele Einstellungen bezüglich des Login verhaltens

---

## 🖥️ Admin-Panel (`/admin`)

- Aktive Nutzer einsehen
- Accounts deaktivieren, löschen, oder Passwörter zurücksetzen
- Neue Nutzer erstellen
- Rollen verwalten
- Letzter Login und Account-Aktivität anzeigen

---


## 🔐 Sicherheitsfeatures

- CSRF-Schutz für alle Formulare
- Passwort-Hashing mit sicherem Algorithmus (Standard: bcrypt)
- Session-Timeout & Auto-Logout
- Brute-Force-Schutz mit Login-Limits (optionale Integration mit Flask-Limiter)
- Email-basiertes Passwort-Zurücksetzen (via Token-Link)

---

## 📦 Roadmap (geplant)

- Zwei-Faktor-Authentifizierung (TOTP, via App)s
- Benutzer-Aktivitätsprotokoll (Audit Log)
- SSO-Unterstützung
- JWT-Tokens anstelle von session cookies

---


## 💬 Kontakt

Entwickelt von **Tobias Auer**  
🌐 [www.t-auer.com](https://www.t-auer.com)  
📫 Bei Fragen, Feature-Wünschen oder Bugreports GitHub Issues benutzen

