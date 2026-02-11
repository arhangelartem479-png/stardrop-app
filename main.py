from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
import sqlite3
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DB = "database.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 1000
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS inventory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

NFT_ITEMS = [
    {"name": "Telegram Diamond NFT", "chance": 0.5, "img": "https://i.imgur.com/8Km9tLL.png"},
    {"name": "Telegram Gold NFT", "chance": 2, "img": "https://i.imgur.com/qIufhof.png"},
    {"name": "Telegram Silver NFT", "chance": 10, "img": "https://i.imgur.com/MK3eW3A.png"},
    {"name": "Common Gift", "chance": 87.5, "img": "https://i.imgur.com/Z6X9KXv.png"},
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/open/{user_id}")
def open_case(user_id: int):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
    c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    balance = c.fetchone()[0]

    if balance < 100:
        return {"error": "Not enough balance"}

    c.execute("UPDATE users SET balance=balance-100 WHERE user_id=?", (user_id,))

    names = [i["name"] for i in NFT_ITEMS]
    weights = [i["chance"] for i in NFT_ITEMS]
    drop = random.choices(NFT_ITEMS, weights=weights)[0]

    c.execute("INSERT INTO inventory(user_id,item) VALUES(?,?)", (user_id, drop["name"]))

    conn.commit()
    conn.close()

    return drop

@app.get("/inventory/{user_id}")
def get_inventory(user_id: int):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT item FROM inventory WHERE user_id=?", (user_id,))
    items = c.fetchall()
    conn.close()
    return {"items": items}
