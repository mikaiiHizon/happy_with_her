// Function to switch to Page 2
function goToPage2() {
    document.getElementById('page1').style.display = 'none';
    document.getElementById('page2').style.display = 'block';
}

// Function to generate the grateful message
function generateMessage() {
    const message = "These past 5 months have been the best of my life. I'm so grateful for every moment with you. You're my everything, Mika. ❤️";
    document.getElementById('generatedMessage').innerText = message;
}

// Function for "I Love You" button
function iLoveYou() {
    alert("I love you so much, Mika! You mean the world to me! 💖");
}