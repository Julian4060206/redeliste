import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Header, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()
# Verzeichnis für die HTML-Dateien festlegen
templates = Jinja2Templates(directory="templates")

# --- Config ---
CONFIG_FILE = "config.json"

def load_config():
    # Versuche die Config zu laden. Falls sie nicht existiert (z.B. frischer Start),
    # gib Standardwerte zurück, damit mir die App nicht um die Ohren fliegt.
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"title": "Redeliste", "admin_password": "admin"}

config = load_config()

# --- Globaler State ---
# Ich halte den Zustand der Redeliste einfach im Arbeitsspeicher.
state: List[Dict] = []
client_counter = 1  # Fortlaufende ID, damit jeder Client eindeutig identifizierbar ist
is_frozen = False   # Flag: Ist die Redeliste gerade für neue Anmeldungen gesperrt?

# --- WebSockets ---
class ConnectionManager:
    """
    Klassischer WebSocket-Manager.
    Hält alle aktiven Verbindungen und pusht Updates an alle Clients, sobald sich der State ändert.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Direkt den aktuellen Stand pushen, wenn sich jemand neu verbindet
        await self.broadcast()

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self):
        # Verteilt die aktuelle Liste und den Freeze-Status an alle verbundenen Browser
        for connection in self.active_connections:
            await connection.send_json({"list": state, "is_frozen": is_frozen})

manager = ConnectionManager()

# --- Frontend Routes ---
@app.get("/")
async def get_public(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": config["title"]})

@app.get("/admin")
async def get_admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, "title": config["title"]})

# --- API Models ---
class JoinRequest(BaseModel):
    name: str
    is_go: bool = False  # Flag für Geschäftsordnungsantrag (Standard: false)

class LeaveRequest(BaseModel):
    id: int

# --- API Routes ---
@app.post("/api/join")
async def join_list(req: JoinRequest):
    global client_counter, state, is_frozen
    
    # Wichtig: Normale Meldungen blockieren, wenn die Liste zu ist.
    # Aber GO-Anträge müssen immer durchgehen.
    if is_frozen and not req.is_go:
        raise HTTPException(status_code=403, detail="Die Liste ist gesperrt.")

    new_id = client_counter
    new_entry = {"id": new_id, "name": req.name, "active": False, "is_go": req.is_go}
    
    if req.is_go:
        # GO-Anträge drängeln sich vor.
        # Suche den ersten Platz nach dem aktuell Sprechenden und nach älteren GO-Anträgen.
        insert_idx = 0
        for i, p in enumerate(state):
            if p.get("active") or p.get("is_go"):
                insert_idx = i + 1
            else:
                break
        state.insert(insert_idx, new_entry)
    else:
        # Normale Meldung: Einfach hinten anfügen
        state.append(new_entry)
        
    client_counter += 1
    await manager.broadcast()
    
    # ID zurückgeben, damit das Frontend (Client) sich selbst erkennt
    return {"status": "ok", "id": new_id}

@app.post("/api/leave")
async def leave_list(req: LeaveRequest):
    global state
    # Filtere den Client anhand seiner ID aus der Liste
    state = [p for p in state if p["id"] != req.id]
    await manager.broadcast()
    return {"status": "ok"}

@app.post("/api/admin/action")
async def admin_action(action: str, target_id: int = None, new_order: List[int] = None, new_name: str = None, x_admin_token: str = Header(None)):
    global state, client_counter, is_frozen
    
    # Admin-Passwort checken
    if x_admin_token != config["admin_password"]:
        raise HTTPException(status_code=401, detail="Falsches Passwort")

    # Routing der verschiedenen Admin-Befehle
    if action == "ping":
        # Wird nur vom Frontend genutzt, um das Passwort direkt beim Login zu validieren
        return {"status": "ok"}
        
    elif action == "toggle_freeze":
        is_frozen = not is_frozen
        
    elif action == "clear":
        # Liste komplett plattmachen
        state.clear()
        client_counter = 1
        
    elif action == "activate":
        # Nur die gewählte Person auf "active" (spricht) setzen, alle anderen auf False
        for p in state:
            p["active"] = (p["id"] == target_id)
            
    elif action == "remove":
        # Jemanden manuell von der Liste kicken
        state = [p for p in state if p["id"] != target_id]
        
    elif action == "reorder" and new_order:
        # Synchronisiert die Reihenfolge mit dem Drag & Drop aus dem Admin-Frontend
        state.sort(key=lambda x: new_order.index(x["id"]) if x["id"] in new_order else 999)
        
    elif action == "add" and new_name:
        # Manuelles Hinzufügen durch den Admin (z.B. für Leute ohne Handy)
        state.append({"id": client_counter, "name": new_name, "active": False, "is_go": False})
        client_counter += 1
        
    # Nach jeder Aktion (außer ping) alle Clients updaten
    await manager.broadcast()
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Halte die Verbindung offen, bis der Client abbricht
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Aufräumen, wenn der Client die Seite schließt
        manager.disconnect(websocket)