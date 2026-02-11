async function openCase() {
    const img = document.getElementById("dropImg");
    img.classList.add("spin");

    setTimeout(async () => {
        const res = await fetch("/open/12345");
        const data = await res.json();

        img.src = data.img;
        document.getElementById("result").innerHTML =
            "🎉 You won: " + data.name;

        img.classList.remove("spin");
    }, 1000);
}
