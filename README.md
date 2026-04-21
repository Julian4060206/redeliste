# Redeliste

English version below.

Eine leichtgewichtige Echtzeit-Webanwendung zur Verwaltung von Wortmeldungen bei Versammlungen, Konferenzen oder Meetings. Das Backend basiert auf Python (FastAPI) und WebSockets, das Frontend ist pures HTML/JS mit TailwindCSS. 

---

## Funktionen

* Echtzeit-Synchronisation: Alle Clients aktualisieren sich über WebSockets sofort (kein Polling).
* Zwei-Stufen-Passwortschutz: Separate Passwörter für die Versammlungsleitung (Admin) und die regulären Teilnehmer (User).
* GO-Anträge: Geschäftsordnungsanträge werden priorisiert behandelt, schieben sich automatisch vor und sind auch bei gesperrter Liste möglich.
* Drag & Drop: Die Reihenfolge der Redner kann im Admin-Bereich per Maus oder Touch umsortiert werden.
* Freeze-Funktion: Die Liste kann für reguläre Neuanmeldungen serverseitig gesperrt werden.
* Aktiver Sprecher: Aufgerufene Personen werden bei allen Teilnehmern visuell hervorgehoben.
* Dark Mode: Das UI passt sich automatisch an die Systemeinstellungen der Nutzer an.

---

## Installation & Start

Das Projekt bietet zwei fertige Docker-Setups, je nach Einsatzzweck. Voraussetzung ist ein installiertes Docker und Docker Compose.

### Option A: Lokal oder VPN (Standard)
Der schnelle Weg für Tests, das eigene Heimnetzwerk oder VPNs (wie Tailscale). Die App lauscht unverschlüsselt auf Port 5005.

1. Repository klonen:
   `git clone https://github.com/Julian4060206/redeliste.git && cd redeliste`
2. Konfiguration anlegen/anpassen:
   Erstelle oder bearbeite die Datei `config.json` und setze den Titel sowie die Passwörter:
   ```json
   {
       "title": "Meine Redeliste",
       "admin_password": "dein_sicheres_admin_passwort",
       "user_password": "dein_sicheres_user_passwort"
   }
   ```
3. Container starten:
   `docker compose up -d --build`
4. Die App ist nun unter `http://localhost:5005` erreichbar. Der Admin-Bereich liegt unter `/admin`.

---

### Option B: Produktiv-Server (Webserver mit eigener Domain)
Das Setup für echte Webserver. Es nutzt Caddy als Reverse Proxy, um WebSockets sauber weiterzuleiten und vollautomatisch ein kostenloses SSL-Zertifikat (HTTPS) von Let's Encrypt zu beziehen.

1. Repository klonen:
   `git clone https://github.com/Julian4060206/redeliste.git && cd redeliste`
2. Umgebungsvariablen vorbereiten:
   `cp .env.example .env`
   Öffne die `.env` und trage deine Zieldomain ein (z.B. `DOMAIN=redeliste.mein-verein.de`). 
   Wichtig: Der DNS-A-Record der Domain muss zwingend auf die Server-IP zeigen, bevor der Container gestartet wird, da sonst die SSL-Ausstellung fehlschlägt.
3. Konfiguration anpassen:
   Setze Passwörter und Titel in der `config.json` (siehe Option A).
4. Produktiv-Setup starten:
   `docker compose -f docker-compose.prod.yml up -d --build`
5. Die App ist nun verschlüsselt unter `https://deine-domain.de` erreichbar.


---
---


# Speakers' List (Redeliste)

A lightweight, real-time web application to manage speaker queues during meetings, conferences, or assemblies. Built with Python (FastAPI), WebSockets, and TailwindCSS.

---

## Features

* Real-Time Synchronization: All connected devices update instantly via WebSockets (no polling).
* Two-Tier Password Protection: Separate passwords for the moderator dashboard (Admin) and the regular attendees (User).
* Procedural Motions (GO-Anträge): Priority requests that automatically bypass regular queues and can be submitted even if the list is locked.
* Drag & Drop: Easily reorder the speakers' list in the admin panel using mouse or touch.
* Freeze Function: Admins can lock the list, preventing new regular requests.
* Active Speaker Tracking: The currently speaking person is highlighted for all users.
* Dark Mode: The UI automatically adapts to the user's system preferences.

---

## Installation & Setup

This project provides two Docker deployment methods depending on your use case. Docker and Docker Compose are required.

### Option A: Local / VPN (Standard)
Ideal for testing, local networks, or VPNs (like Tailscale). The app runs unencrypted on port 5005.

1. Clone the repository:
   `git clone https://github.com/Julian4060206/redeliste.git && cd redeliste`
2. Configure the App:
   Create or edit the `config.json` file to set your custom title and passwords:
   ```json
   {
       "title": "My Speakers' List",
       "admin_password": "your_secure_admin_password",
       "user_password": "your_secure_user_password"
   }
   ```
3. Start the container:
   `docker compose up -d --build`
4. The app is now available at `http://localhost:5005`. Access the admin panel at `/admin`.

---

### Option B: Production Server (Public Domain via Caddy)
The setup for actual web servers. This uses Caddy as a reverse proxy to handle WebSocket routing and automatically fetch a free SSL certificate (HTTPS) via Let's Encrypt.

1. Clone the repository:
   `git clone https://github.com/Julian4060206/redeliste.git && cd redeliste`
2. Prepare Environment Variables:
   `cp .env.example .env`
   Open `.env` and set your domain (e.g., `DOMAIN=redeliste.my-domain.com`). 
   Important: Ensure your domain's DNS A-Record points to your server's IP address before starting, otherwise the SSL certificate provisioning will fail.
3. Configure the App:
   Edit `config.json` to set your passwords and title (see Option A).
4. Start the Production Setup:
   `docker compose -f docker-compose.prod.yml up -d --build`
5. The app is now securely available at `https://your-domain.com`.
