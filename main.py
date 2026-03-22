import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Header, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Config laden
CONFIG_FILE = "config.json"
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"title": "Redeliste", "admin_password": "admin"}

config = load_config()
state: List[Dict] = []
client_counter = 1

# WebSocket Manager für Echtzeit-Updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast()

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self):
        for connection in self.active_connections:
            await connection.send_json({"list": state})

manager = ConnectionManager()

# --- Routen (Frontend) ---
@app.get("/")
async def get_public(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": config["title"]})

@app.get("/admin")
async def get_admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, "title": config["title"]})

# --- API (Logik) ---
class JoinRequest(BaseModel):
    name: str

class LeaveRequest(BaseModel):
    id: int

@app.post("/api/join")
async def join_list(req: JoinRequest):
    global client_counter
    new_id = client_counter
    state.append({"id": new_id, "name": req.name, "active": False})
    client_counter += 1
    await manager.broadcast()
    return {"status": "ok", "id": new_id} # Hier geben wir die ID ans Handy zurück

@app.post("/api/leave")
async def leave_list(req: LeaveRequest):
    global state
    state = [p for p in state if p["id"] != req.id]
    await manager.broadcast()
    return {"status": "ok"}

@app.post("/api/admin/action")
async def admin_action(action: str, target_id: int = None, new_order: List[int] = None, new_name: str = None, x_admin_token: str = Header(None)):
    global state, client_counter
    if x_admin_token != config["admin_password"]:
        raise HTTPException(status_code=401, detail="Falsches Passwort")

    if action == "activate":
        for p in state:
            p["active"] = (p["id"] == target_id)
    elif action == "remove":
        state = [p for p in state if p["id"] != target_id]
    elif action == "reorder" and new_order:
        state.sort(key=lambda x: new_order.index(x["id"]) if x["id"] in new_order else 999)
    elif action == "add" and new_name:
        state.append({"id": client_counter, "name": new_name, "active": False})
        client_counter += 1
        
    await manager.broadcast()
    return {"status": "ok"}

# --- WebSockets ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
