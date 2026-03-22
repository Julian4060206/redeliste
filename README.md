# Redeliste / Speaker List

[English version below](#english-version)

Eine einfache Echtzeit-Webanwendung zur Verwaltung von Wortmeldungen in Gremien, Vereinen oder Meetings. Entwickelt für den schnellen Einsatz via Docker.


## Funktionen

* **Echtzeit-Updates:** Durch die Nutzung von WebSockets sehen alle Teilnehmer Änderungen an der Liste in Echtzeit, ohne die Seite neu laden zu müssen.
* **Niedrige Hürde:** Teilnehmer benötigen keinen Account und keinen Login, um sich auf die Liste zu setzen.
* **Selbstverwaltung:** Wer auf der Liste steht, kann seine Wortmeldung jederzeit eigenständig wieder zurückziehen.
* **Admin-Panel:** Der Sitzungsleiter hat Zugriff auf einen passwortgeschützten Bereich. Dort können Personen aufgerufen, manuell hinzugefügt, gelöscht oder in ihrer Reihenfolge per Drag & Drop verschoben werden.
* **Responsive & Dark Mode:** Die Benutzeroberfläche passt sich an mobile Endgeräte sowie an die systemweite Dark-Mode-Einstellung des Nutzers an.
* **Zustandslos (Stateless):** Die Anwendung speichert alle Daten im Arbeitsspeicher. Nach Beendigung der Sitzung und einem Neustart des Containers ist das System wieder im Ausgangszustand.

## Tech-Stack

* Backend: Python 3, FastAPI, WebSockets
* Frontend: HTML5, Vanilla JavaScript, Tailwind CSS, SortableJS
* Deployment: Docker & Docker Compose

## Installation (Docker)

1. Repository klonen:
   ```bash
   git clone [https://github.com/Julian4060206/redeliste.git](https://github.com/Julian4060206/redeliste.git)
   cd redeliste
   ```

2. Konfiguration anlegen:
   Erstelle eine Kopie der Beispielkonfiguration und trage den gewünschten Titel sowie ein sicheres Admin-Passwort ein.
   ```bash
   cp config.example.json config.json
   ```

3. Container starten:
   ```bash
   docker compose up -d --build
   ```

Die Anwendung ist nun unter `http://localhost:5005` (bzw. unter der IP deines Servers) erreichbar.

## Nutzung

* **Teilnehmer:** Rufen die Haupt-URL auf (`http://localhost:5005`).
* **Admin:** Ruft das Unterverzeichnis `/admin` auf (`http://localhost:5005/admin`) und loggt sich mit dem in der `config.json` definierten Passwort ein.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Details sind in der [LICENSE](LICENSE) Datei zu finden.

---

<a name="english-version"></a>
# English Version

A simple, real-time web application for managing speaker lists in meetings, committees, or clubs. Designed for quick deployment using Docker.

## Features

* **Real-time updates:** Powered by WebSockets, all participants see changes to the list instantly without reloading the page.
* **No barriers:** Participants do not need an account or login to add their name to the list.
* **Self-management:** Participants can withdraw their request to speak at any time.
* **Admin Panel:** The session leader has access to a password-protected dashboard. From there, they can call on speakers, manually add or remove people, and reorder the list using drag and drop.
* **Responsive & Dark Mode:** The UI is fully responsive and automatically adapts to the user's system-wide dark mode preference.
* **Stateless:** The application stores all data in memory. Once the meeting is over, simply restarting the container clears the data and resets the system.

## Tech Stack

* Backend: Python 3, FastAPI, WebSockets
* Frontend: HTML5, Vanilla JavaScript, Tailwind CSS, SortableJS
* Deployment: Docker & Docker Compose

## Installation (Docker)

1. Clone the repository:
   ```bash
   git clone [https://github.com/Julian4060206/redeliste.git](https://github.com/Julian4060206/redeliste.git)
   cd redeliste
   ```

2. Create the configuration:
   Copy the example configuration file and set your desired session title and a secure admin password.
   ```bash
   cp config.example.json config.json
   ```

3. Start the container:
   ```bash
   docker compose up -d --build
   ```

The application is now accessible at `http://localhost:5005` (or via your server's IP address).

## Usage

* **Participants:** Access the root URL (`http://localhost:5005`).
* **Admin:** Access the `/admin` path (`http://localhost:5005/admin`) and log in using the password defined in your `config.json`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.