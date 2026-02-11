from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ----------------------------
# Временная база данных
# ----------------------------
users = {}

# ----------------------------
# NFT Telegram Gifts
# ----------------------------
gifts = [
    {
        "name": "Common Gift",
        "chance": 74,  # 74%
        "img": "https://cdn-icons-png.flaticon.com/512/1077/1077035.png"
    },
    {
        "name": "Rare Telegram Gift",
        "chance": 20,  # 20%
        "img": "https://cdn-icons-png.flaticon.com/512/3523/3523887.png"
    },
    {
        "name": "Epic Telegram Gift",
        "chance": 5,  # 5%
        "img": "https://cdn-icons-png.flaticon.com/512/616/616494.png"
    },
    {
        "name": "ULTRA NFT STAR",
        "chance": 1,  # 1% минимальный шанс
        "img": "https://cdn-icons-png.flaticon.com/512/616/616489.png"
    }
]

CASE_PRICE = 100


# ----------------------------
# Главная страница
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ----------------------------
# Открытие кейса
# ----------------------------
@app.get("/open/{user_id}")
async def open_case(user_id: int):

    # Создаём пользователя если его нет
    if user_id not in users:
        users[user_id] = {
            "balance": 500,
            "inventory": []
        }

    # Проверка баланса
    if users[user_id]["balance"] < CASE_PRICE:
        return {"error": "Not enough coins"}

    # Списываем деньги
    users[user_id]["balance"] -= CASE_PRICE

    # Выбор приза по шансам
    roll = random.randint(1, 100)
    current = 0
    won_gift = gifts[0]

    for gift in gifts:
        current += gift["chance"]
        if roll <= current:
            won_gift = gift
            break

    # Добавляем в инвентарь
    users[user_id]["inventory"].append(won_gift)

    return {
        "name": won_gift["name"],
        "img": won_gift["img"],
        "balance": users[user_id]["balance"]
    }


# ----------------------------
# Инвентарь
# ----------------------------
@app.get("/inventory/{user_id}")
async def get_inventory(user_id: int):
    if user_id not in users:
        return {"inventory": [], "balance": 0}

    return {
        "inventory": users[user_id]["inventory"],
        "balance": users[user_id]["balance"]
    }
