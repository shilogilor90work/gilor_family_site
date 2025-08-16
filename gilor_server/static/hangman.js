const API_BASE_URL = 'amitai';
const create_word_endpoint = `${API_BASE_URL}/create_hangman_word`;
const get_word_endpoint = `${API_BASE_URL}/get_hangman_word`;
const get_all_words_endpoint = `${API_BASE_URL}/get_hangman_words`;

async function saveWord(word) {
    try {
        const response = await fetch(create_word_endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ word }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `API error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Error saving word:`, error);
        displayMessage(`Error saving word: ${error.message}`, 'error');
        throw error;
    }
}

async function getAllWords() {
    try {
        const response = await fetch(get_all_words_endpoint, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `API error: ${response.status}`);
        }
        const data = await response.json();
        return data.words || [];
    } catch (error) {
        console.error(`Error fetching all words:`, error);
        displayMessage(`Error fetching all words: ${error.message}`, 'error');
        throw error;
    }
}

async function getWord() {
    try {
        const response = await fetch(get_word_endpoint, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `API error: ${response.status}`);
        }
        const data = await response.json();
        return data.word || '';
    }
    catch (error) {
        console.error(`Error fetching word:`, error);
        displayMessage(`Error fetching word: ${error.message}`, 'error');
        throw error;
    }
}

// Game variables
let selectedWord = '';
let guessedLetters = [];
let wrongGuesses = 0;
const maxWrongGuesses = 6; // Number of body parts for the hangman

// DOM elements - Game Section
const wordDisplay = document.getElementById('word-display');
const hangmanDrawing = document.getElementById('hangman-drawing');
const guessedLettersDisplay = document.getElementById('guessed-letters');
const keyboardContainer = document.getElementById('keyboard-container');
const messageDisplay = document.getElementById('message');
const newGameButton = document.getElementById('new-game-button');

// DOM elements - Future Input Section
const futureInput = document.getElementById('future-input');
const storeInputButton = document.getElementById('store-input-button');
const futureInputValueDisplay = document.getElementById('future-input-value');
let futureVariable = ''; // This variable will store the input value

// Hangman drawing stages (simplified gallows with a bit more detail)
const hangmanStages = [
    `
   +---+
   |   |
       |
       |
       |
       |
=========\n`, // 0 wrong guesses - Empty gallows
    `
   +---+
   |   |
   O   |
       |
       |
       |
=========\n`, // 1 wrong guess - Head
    `
   +---+
   |   |
   O   |
   |   |
       |
       |
=========\n`, // 2 wrong guesses - Body
    `
   +---+
   |   |
   O   |
  /|   |
       |
       |
=========\n`, // 3 wrong guesses - Left Arm
    `
   +---+
   |   |
   O   |
  /|\\  |
       |
       |
=========\n`, // 4 wrong guesses - Right Arm
    `
   +---+
   |   |
   O   |
  /|\\  |
  /    |
       |
=========\n`, // 5 wrong guesses - Left Leg
    `
   +---+
   |   |
   O   |
  /|\\  |
  / \\  |
       |
=========\n` // 6 wrong guesses - Right Leg - Game Over
];

// --- Game Functions ---

/**
 * Initializes a new game.
 * Resets game state, selects a new random word, and updates the display.
 */
async function initGame() {
    // Fetch a new word from the API
    selectedWord = await getWord();
    console.log(selectedWord);
    guessedLetters = [];
    wrongGuesses = 0;
    messageDisplay.textContent = '';
    messageDisplay.className = 'message'; // Reset message class

    // Re-enable all keyboard buttons
    const buttons = keyboardContainer.querySelectorAll('.letter-button');
    buttons.forEach(button => {
        button.disabled = false;
    });

    updateDisplay();
}

/**
 * Creates and appends the letter buttons to the keyboard container.
 */
function createKeyboard() {
    keyboardContainer.innerHTML = ''; // Clear existing buttons
    for (let i = 0; i < 26; i++) {
        const letter = String.fromCharCode(65 + i); // ASCII A-Z
        const button = document.createElement('button');
        button.textContent = letter;
        button.classList.add('letter-button');
        button.addEventListener('click', () => handleGuess(letter, button));
        keyboardContainer.appendChild(button);
    }
}

/**
 * Updates the word display with underscores for unguessed letters.
 */
function updateWordDisplay() {
    let display = '';
    for (const letter of selectedWord) {
        if (guessedLetters.includes(letter)) {
            display += letter + ' ';
        } else {
            display += '_ ';
        }
    }
    wordDisplay.textContent = display.trim();
}

/**
 * Updates the hangman drawing based on wrong guesses.
 */
function updateHangmanDrawing() {
    hangmanDrawing.textContent = hangmanStages[wrongGuesses];
}

/**
 * Updates the list of guessed letters.
 */
function updateGuessedLettersDisplay() {
    guessedLettersDisplay.textContent = `Guessed Letters: ${guessedLetters.length > 0 ? guessedLetters.join(', ') : 'None'}`;
}

/**
 * Updates all game display elements.
 */
function updateDisplay() {
    updateWordDisplay();
    updateHangmanDrawing();
    updateGuessedLettersDisplay();
}

/**
 * Handles a letter guess from the user via button click.
 * @param {string} guess - The letter guessed by the user.
 * @param {HTMLButtonElement} button - The button element that was clicked.
 */
function handleGuess(guess, button) {
    // Ensure the guessed letter is uppercase for consistent comparison
    guess = guess.toLowerCase();
    if (button.disabled) {
        return; // Do nothing if button is already disabled
    }

    button.disabled = true; // Disable the button after it's clicked

    if (guessedLetters.includes(guess)) {
        // This case should ideally not happen if buttons are disabled correctly
        messageDisplay.textContent = `You already guessed "${guess}".`;
        messageDisplay.className = 'message text-yellow-500';
        return;
    }

    guessedLetters.push(guess);
    updateGuessedLettersDisplay();

    if (selectedWord.includes(guess)) {
        messageDisplay.textContent = `Good guess! "${guess}" is in the word.`;
        messageDisplay.className = 'message text-green-500';
        updateWordDisplay();
    } else {
        wrongGuesses++;
        messageDisplay.textContent = `Sorry, "${guess}" is not in the word.`;
        messageDisplay.className = 'message text-red-500';
        updateHangmanDrawing();
    }

    checkGameStatus();
}

/**
 * Checks if the game has ended (win or lose).
 */
function checkGameStatus() {
    const currentWordState = wordDisplay.textContent.replace(/ /g, ''); // Remove spaces for comparison
    if (currentWordState === selectedWord) {
        messageDisplay.textContent = `Congratulations! You guessed the word: ${selectedWord}`;
        messageDisplay.classList.add('win');
        endGame(true);
    } else if (wrongGuesses >= maxWrongGuesses) {
        messageDisplay.textContent = `Game Over! The word was: ${selectedWord}`;
        messageDisplay.classList.add('lose');
        endGame(false);
    }
}

/**
 * Ends the current game session.
 * @param {boolean} won - True if the player won, false otherwise.
 */
function endGame(won) {
    // Disable all keyboard buttons
    const buttons = keyboardContainer.querySelectorAll('.letter-button');
    buttons.forEach(button => {
        button.disabled = true;
    });
}

// --- Future Input Section Logic ---
storeInputButton.addEventListener('click', () => {
    futureVariable = futureInput.value; // Store the input value in futureVariable
    saveWord(futureVariable) // Save the word to the API
    futureInputValueDisplay.textContent = futureVariable; // Display the stored value
});

futureInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        storeInputButton.click(); // Trigger button click on Enter key
    }
});

// --- Event Listeners ---
newGameButton.addEventListener('click', initGame);

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    createKeyboard(); // Create keyboard buttons once
    initGame(); // Initialize game state to start a new game
});
