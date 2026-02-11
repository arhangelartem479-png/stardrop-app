let userId = 12345;

if (window.Telegram && Telegram.WebApp) {
    Telegram.WebApp.ready();
    Telegram.WebApp.expand();
    const user = Telegram.WebApp.initDataUnsafe.user;
    if (user) userId = user.id;
}

async function loadInventory() {
    const res = await fetch(`/inventory/${userId}`);
    const data = await res.json();

    document.getElementById("balance").innerText = data.balance;

    const inv = document.getElementById("inventory");
    inv.innerHTML = "";

    data.inventory.forEach(item => {
        inv.innerHTML += `
            <div class="inventory-item">
                <img src="${item.img}" width="60"><br>
                ${item.name}
            </div>
        `;
    });
}

async function openCase() {
    const img = document.getElementById("dropImg");
    img.classList.add("spin");

    setTimeout(async () => {
        const res = await fetch(`/open/${userId}`);
        const data = await res.json();

        if (data.error) {
            alert(data.error);
            img.classList.remove("spin");
            return;
        }

        img.src = data.img;
        img.classList.remove("spin");
        loadInventory();
    }, 1000);
}

async function demoCase() {
    const img = document.getElementById("dropImg");
    img.classList.add("spin");

    setTimeout(async () => {
        const res = await fetch(`/demo/${userId}`);
        const data = await res.json();

        img.src = data.img;
        img.classList.remove("spin");
    }, 1000);
}

loadInventory();
