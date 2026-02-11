let userId = 12345; // fallback для браузера

// Если открыто внутри Telegram
if (window.Telegram && Telegram.WebApp) {
    Telegram.WebApp.ready();
    Telegram.WebApp.expand();

    const user = Telegram.WebApp.initDataUnsafe.user;

    if (user && user.id) {
        userId = user.id;
    }
}

async function openCase() {
    const img = document.getElementById("dropImg");
    img.classList.add("spin");

    setTimeout(async () => {

        const res = await fetch(`/open/${userId}`);
        const data = await res.json();

        if (data.error) {
            document.getElementById("result").innerHTML = "❌ " + data.error;
            img.classList.remove("spin");
            return;
        }

        img.src = data.img;

        document.getElementById("result").innerHTML =
            "🎉 You won: " + data.name;

        img.classList.remove("spin");

    }, 1200);
}
