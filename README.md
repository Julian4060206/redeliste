# Redeliste

English version below.

Eine leichtgewichtige Echtzeit-Webanwendung zur Verwaltung von Wortmeldungen bei Versammlungen, Konferenzen oder Meetings. Das Backend basiert auf Python (FastAPI) und WebSockets, das Frontend ist pures HTML/JS mit TailwindCSS. 

---

## Funktionen

* Echtzeit-Synchronisation: Alle Clients aktualisieren sich über WebSockets sofort (kein Polling).
* GO-Anträge: Geschäftsordnungsanträge werden priorisiert behandelt, schieben sich automatisch vor und sind auch bei gesperrter Liste möglich.
* Admin-Bereich: Passwortgeschütztes Dashboard für die Versammlungsleitung.
* Drag & Drop: Die Reihenfolge der Redner kann per Maus oder Touch umsortiert werden.
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
   Erstelle oder bearbeite die Datei `config.json` und setze Titel sowie Admin-Passwort:
   ```json
   {
       "title": "Meine Redeliste",
       "admin_password": "dein_sicheres_passwort"
   }
   ```
3. Container starten:
   `docker compose up -d`
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
   Setze Passwort und Titel in der `config.json` (siehe Option A).
4. Produktiv-Setup starten:
   `docker compose -f docker-compose.prod.yml up -d`
5. Die App ist nun verschlüsselt unter `https://deine-domain.de` erreichbar.


---
---


# Speakers' List (Redeliste)

A lightweight, real-time web application to manage speaker queues during meetings, conferences, or assemblies. Built with Python (FastAPI), WebSockets, and TailwindCSS.

---

## Features

* Real-Time Synchronization: All connected devices update instantly via WebSockets (no polling).
* Procedural Motions (GO-Anträge): Priority requests that automatically bypass regular queues and can be submitted even if the list is locked.
* Admin Dashboard: Password-protected control panel for moderators.
* Drag & Drop: Easily reorder the speakers' list using mouse or touch.
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
   Create or edit the `config.json` file to set your custom title and admin password:
   ```json
   {
       "title": "My Speakers' List",
       "admin_password": "your_secure_password"
   }
   ```
3. Start the container:
   `docker compose up -d`
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
   Edit `config.json` to set your admin password and title (see Option A).
4. Start the Production Setup:
   `docker compose -f docker-compose.prod.yml up -d`
5. The app is now securely available at `https://your-domain.com`.