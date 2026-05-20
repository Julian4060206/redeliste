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

### Option C: Beliebig viele Instanzen auf einem Server (Multi-Setup)
Das ideale Setup, wenn du die Redeliste für verschiedene Gruppen (z. B. mehrere Gremien, Ausschüsse oder Events) parallel auf demselben Server betreiben möchtest. Ein zentraler Caddy-Proxy leitet den Traffic anhand von Subdomains an die richtigen Container weiter und sorgt vollautomatisch für HTTPS. Du kannst dieses Setup auf beliebig viele Instanzen erweitern.

1. Zentrales Verzeichnis anlegen:
   `mkdir -p /opt/redeliste_master && cd /opt/redeliste_master`
2. Konfigurationsdateien vorbereiten:
   Lade die `config.example.json` aus dem Repository herunter und benenne sie für jede deiner Gruppen lokal um. Wiederhole diesen Schritt für jede weitere Gruppe, die du benötigst:
   ```bash
   curl -o config_gruppe1.json [https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json](https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json)
   curl -o config_gruppe2.json [https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json](https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json)
   curl -o config_gruppe3.json [https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json](https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json)
   ```
   
Passe anschließend die Passwörter und Titel in den jeweiligen Dateien an.
3. docker-compose.yml erstellen:
Lege die Datei an. Die App wird hierbei direkt aus dem GitHub-Repository gebaut und deine lokalen Konfigurationsdateien werden im Container als config.json eingebunden. Füge für jede weitere Gruppe einfach einen neuen Block hinzu:

YAML
version: '3.8'
services:
  gruppe1:
    build: [https://github.com/Julian4060206/redeliste.git#main](https://github.com/Julian4060206/redeliste.git#main)
    container_name: redeliste_gruppe1
    restart: unless-stopped
    volumes:
      - ./config_gruppe1.json:/app/config.json
  
  gruppe2:
    build: [https://github.com/Julian4060206/redeliste.git#main](https://github.com/Julian4060206/redeliste.git#main)
    container_name: redeliste_gruppe2
    restart: unless-stopped
    volumes:
      - ./config_gruppe2.json:/app/config.json

  gruppe3:
    build: [https://github.com/Julian4060206/redeliste.git#main](https://github.com/Julian4060206/redeliste.git#main)
    container_name: redeliste_gruppe3
    restart: unless-stopped
    volumes:
      - ./config_gruppe3.json:/app/config.json

  caddy_proxy:
    image: caddy:2-alpine
    container_name: redeliste_proxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config

volumes:
  caddy_data:
  caddy_config:

Caddyfile erstellen:
Erstelle die Datei, um deine Subdomains den jeweiligen Containern zuzuordnen. Wichtig: Die DNS-A-Records aller Subdomains müssen vor dem Start auf die Server-IP zeigen, damit die HTTPS-Zertifikate ausgestellt werden können.

Code-Snippet
gruppe1.deine-domain.de {
    reverse_proxy redeliste_gruppe1:5005
}

gruppe2.deine-domain.de {
    reverse_proxy redeliste_gruppe2:5005
}

gruppe3.deine-domain.de {
    reverse_proxy redeliste_gruppe3:5005
}

5. Multi-Setup starten:
   `docker compose up -d --build`
   Die Instanzen sind nun sicher und verschlüsselt unter ihren jeweiligen Subdomains erreichbar.

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

---

### Option C: Any Number of Instances on One Server (Multi-Setup)
The ideal setup if you want to run the application for multiple groups (e.g., various committees, events, or boards) simultaneously on the same server. A centralized Caddy proxy routes traffic to the correct containers based on subdomains and handles HTTPS automatically. You can scale this setup to as many instances as you need.

1. Create a Master Directory:
   `mkdir -p /opt/redeliste_master && cd /opt/redeliste_master`
2. Prepare Configuration Files:
   Download the `config.example.json` from the repository and rename it locally for each of your groups. Repeat this step for any additional groups you need:
   ```bash
   curl -o config_group1.json [https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json](https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json)
   curl -o config_group2.json [https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json](https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json)
   curl -o config_group3.json [https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json](https://raw.githubusercontent.com/Julian4060206/redeliste/main/config.example.json)
   ```
   
Edit these files to set custom passwords and titles for each instance.
3. Create the docker-compose.yml:
Create the file. The app builds directly from the GitHub repository, and your local config files are mapped into the containers as the required config.json. Just add a new block for any additional group you need:

YAML
version: '3.8'
services:
  group1:
    build: [https://github.com/Julian4060206/redeliste.git#main](https://github.com/Julian4060206/redeliste.git#main)
    container_name: redeliste_group1
    restart: unless-stopped
    volumes:
      - ./config_group1.json:/app/config.json
  
  group2:
    build: [https://github.com/Julian4060206/redeliste.git#main](https://github.com/Julian4060206/redeliste.git#main)
    container_name: redeliste_group2
    restart: unless-stopped
    volumes:
      - ./config_group2.json:/app/config.json

  group3:
    build: [https://github.com/Julian4060206/redeliste.git#main](https://github.com/Julian4060206/redeliste.git#main)
    container_name: redeliste_group3
    restart: unless-stopped
    volumes:
      - ./config_group3.json:/app/config.json

  caddy_proxy:
    image: caddy:2-alpine
    container_name: redeliste_proxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config

volumes:
  caddy_data:
  caddy_config:

Create the Caddyfile:
Create the file to map your subdomains to the respective containers. Important: The DNS A-Records for all your subdomains must point to your server's IP before starting to ensure successful HTTPS provisioning.

Code-Snippet
group1.your-domain.com {
    reverse_proxy redeliste_group1:5005
}

group2.your-domain.com {
    reverse_proxy redeliste_group2:5005
}

group3.your-domain.com {
    reverse_proxy redeliste_group3:5005
}

5. Start the Multi-Setup:
   `docker compose up -d --build`
   The instances are now securely available under their respective subdomains.