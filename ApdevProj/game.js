document.getElementById("play-btn").addEventListener("click", function () {
    window.location.href = "User.html";
});

document.getElementById("credits-btn").addEventListener("click", function () {
    window.location.href = "Credits.html";
});

document.getElementById("exit-btn").addEventListener("click", function () {
    if (confirm("Are you sure you want to exit?")) {
        window.close();
    }
});