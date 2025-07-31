let password = "";
let hint = "";
let lives = 0;

function startGame() {
  password = document.getElementById("password").value.trim();
  hint = document.getElementById("hint").value.trim();
  lives = parseInt(document.getElementById("lives").value);

  if (!password || lives < 1) {
    alert("Fill in all fields.");
    return;
  }
  console.log(password)
  document.getElementById("setup").classList.add("hidden");
  document.getElementById("pass-device").classList.remove("hidden");
}

function prepareGame() {
  setTimeout(() => {
    console.log(password);
    setTimeout(() => {
      document.getElementById("pass-device").classList.add("hidden");
      document.getElementById("guessing").classList.remove("hidden");
      document.getElementById("hintDisplay").textContent = `Hint: ${hint}`;
      document.getElementById("livesDisplay").textContent = `Lives left: ${lives}`;
    }, 500);
  }, 500);
}

function checkGuess() {
  const guess = document.getElementById("guessInput").value.trim();
  const feedback = document.getElementById("feedback");

  if (guess.toLowerCase() === password.toLowerCase()) {
    endGame("You may enter!");
    return;
  }

  lives--;

  if (lives <= 0) {
    endGame("Out of lives. Game over.The password was: " + password);
    return;
  }

  let message = `'${guess}' is not correct. ${lives} lives remaining.`;

  feedback.textContent = message;
  document.getElementById("livesDisplay").textContent = `Lives left: ${lives}`;
  document.getElementById("guessInput").value = "";
}

function endGame(message) {
  document.getElementById("guessing").classList.add("hidden");
  document.getElementById("end").classList.remove("hidden");
  document.getElementById("endMessage").textContent = message;
}

function resetGame() {
  document.getElementById("end").classList.add("hidden");
  document.getElementById("setup").classList.remove("hidden");
  document.getElementById("password").value = "";
  document.getElementById("hint").value = "";
  document.getElementById("lives").value = "3";
  password = "";
  hint = "";
  lives = 0;
  document.getElementById("feedback").textContent = "";
}
