let password = "";
let hint = "";
let lives = 0;
let mode = "";

function startGame() {
  password = document.getElementById("password").value.trim();
  hint = document.getElementById("hint").value.trim();
  lives = parseInt(document.getElementById("lives").value);
  mode = document.getElementById("mode").value;

  if (!password || (mode !== "hard" && !hint) || lives < 1) {
    alert("Fill in all fields (hint not required for hard mode).");
    return;
  }

  document.getElementById("setup").classList.add("hidden");
  document.getElementById("pass-device").classList.remove("hidden");
}

function prepareGame() {
  setTimeout(() => {
    console.clear();
    setTimeout(() => {
      document.getElementById("pass-device").classList.add("hidden");
      document.getElementById("guessing").classList.remove("hidden");

      document.getElementById("hintDisplay").textContent =
        mode === "hard" ? "" : "Hint: " + hint;
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
    endGame("Out of lives. Game over.");
    return;
  }

  let message = `'${guess}' is not correct. ${lives} lives remaining.`;
  if (mode === "hard") {
    hardModeEffect();
  }

  feedback.textContent = message;
  document.getElementById("livesDisplay").textContent = `Lives left: ${lives}`;
  document.getElementById("guessInput").value = "";
}

function endGame(message) {
  document.getElementById("guessing").classList.add("hidden");
  document.getElementById("end").classList.remove("hidden");
  document.getElementById("endMessage").textContent = message;
}

function hardModeEffect() {
  const container = document.querySelector(".container");
  container.classList.add("blurred");
  setTimeout(() => {
    container.classList.remove("blurred");
  }, 800); // simulate screen distortion/delay
}
