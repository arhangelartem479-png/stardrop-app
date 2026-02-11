from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

users = {}

CASE_PRICE = 100

gifts = [
    {"name": "Common Gift", "chance": 70, "img": "https://cdn-icons-png.flaticon.com/512/1077/1077035.png"},
    {"name": "Rare Telegram Gift", "chance": 20, "img": "https://cdn-icons-png.flaticon.com/512/3523/3523887.png"},
    {"name": "Epic Gift", "chance": 9, "img": "https://cdn-icons-png.flaticon.com/512/616/616494.png"},
    {"name": "ULTRA NFT STAR", "chance": 1, "img": "https://cdn-icons-png.flaticon.com/512/616/616489.png"}
]

demo_gifts = [
    {"name": "Common Gift", "chance": 40, "img": "https://cdn-icons-png.flaticon.com/512/1077/1077035.png"},
    {"name": "Rare Telegram Gift", "chance": 35, "img": "https://cdn-icons-png.flaticon.com/512/3523/3523887.png"},
    {"name": "Epic Gift", "chance": 20, "img": "https://cdn-icons-png.flaticon.com/512/616/616494.png"},
    {"name": "ULTRA NFT STAR", "chance": 5, "img": "https://cdn-icons-png.flaticon.com/512/616/616489.png"}
]


def roll_drop(drop_list):
    roll = random.randint(1, 100)
    current = 0
    for gift in drop_list:
        current += gift["chance"]
        if roll <= current:
            return gift


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/open/{user_id}")
async def open_case(user_id: int):
    if user_id not in users:
        users[user_id] = {"balance": 500, "inventory": []}

    if users[user_id]["balance"] < CASE_PRICE:
        return {"error": "Not enough coins"}

    users[user_id]["balance"] -= CASE_PRICE

    won = roll_drop(gifts)
    users[user_id]["inventory"].append(won)

    return {
        "name": won["name"],
        "img": won["img"],
        "balance": users[user_id]["balance"]
    }


@app.get("/demo/{user_id}")
async def demo_case(user_id: int):
    won = roll_drop(demo_gifts)
    return {
        "name": won["name"],
        "img": won["img"]
    }


@app.get("/inventory/{user_id}")
async def inventory(user_id: int):
    if user_id not in users:
        return {"inventory": [], "balance": 0}

    return users[user_id]
