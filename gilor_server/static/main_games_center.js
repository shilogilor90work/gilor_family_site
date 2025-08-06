const gameGallery = document.getElementById('game-gallery');

const games = [
    {
        imageSrc: "https:placehold.co/400x250/FF5733/FFFFFF?text=Madlibs", // <--- ADD YOUR IMAGE URL HERE
        name: "Madlibs", // <--- ADD YOUR GAME NAME HERE
        gamePath: "/amitai/madlibs_game" // <--- ADD YOUR GAME PATH (URL) HERE
    },
    {
        imageSrc: "https://placehold.co/400x250/33FF57/000000?text=Two+Player+Password", // <--- ADD YOUR IMAGE URL HERE
        name: "Two Player Password", // <--- ADD YOUR GAME NAME HERE
        gamePath: "/amitai/two_player" // <--- ADD YOUR GAME PATH (URL) HERE
    },
    {
        imageSrc: "https://placehold.co/400x250/3357FF/FFFFFF?text=Snake", // <--- ADD YOUR IMAGE URL HERE
        name: "Snake", // <--- ADD YOUR GAME NAME HERE
        gamePath: "/amitai/snake" // <--- ADD YOUR GAME PATH (URL) HERE
    },
    {
        imageSrc: "https://placehold.co/400x250/335754/FFFFFF?text=Rectangle", // <--- ADD YOUR IMAGE URL HERE
        name: "Rectangle",
        gamePath: "/amitai/rectangle"
    },
    {
        imageSrc: "https://placehold.co/400x250/AAAAAA/000000?text=Countdown",
        name: "Countdown",
        gamePath: "/amitai/countdown"
    },
    {
        imageSrc: "https://placehold.co/400x250/FFAA33/FFFFFF?text=Calculator",
        name: "Calculator",
        gamePath: "/amitai/calculator"
    },
    {
        imageSrc: "https://placehold.co/400x250/33AAFF/FFFFFF?text=Tic Tac Toe",
        name: "Tic Tac Toe",
        gamePath: "/amitai/tic_tac_toe"
    },
    {
        imageSrc: "https://placehold.co/400x250/FF33AA/FFFFFF?text=Flappy Bird",
        name: "Flappy Bird",
        gamePath: "/amitai/flappy_bird"
    },
    {
        imageSrc: "https://placehold.co/400x250/FF33FF/FFFFFF?text=Hangman",
        name: "Hangman",
        gamePath: "/amitai/hangman"
    }
];


function searchGames() {
    // Get the search input value and convert it to lowercase for a case-insensitive search
    const searchInput = document.getElementById('search-bar').value.toLowerCase();
    const resultsList = document.getElementById('game-gallery');
    resultsList.innerHTML = ''; // Clear previous results
    if (searchInput.length < 1) {
        games.forEach(game => {
            const card = createGameCard(game);
            gameGallery.appendChild(card);
        });
    }// copy from here
    else if (searchInput === 'die'){
        resultsList.innerHTML = '<h1 class="text-2xl text-red-500 font-bold">You are a looser.</h1>';
    }// copy to here in order to add secret message
    else if (searchInput === 'roi') {
        resultsList.innerHTML = '<h1 class="text-2xl text-red-500 font-bold">die already</h1>';
    }
    else if (searchInput === 'amitai') {
        resultsList.innerHTML = '<h1 class="text-2xl text-red-500 font-bold">my leader</h1>';
    }
    else if (searchInput === 'mum') {
        resultsList.innerHTML = '<h1 class="text-2xl text-red-500 font-bold">I love you</h1>';
    }
    else if (searchInput === 'dado') {
        resultsList.innerHTML = '<h1 class="text-2xl text-red-500 font-bold">I love you</h1>';
    }
    else if (searchInput === 'belle') {
        resultsList.innerHTML = '<h1 class="text-2xl text-red-500 font-bold">the best sis ever!!!</h1>';
    }
    else if (searchInput === 'the game!!!!!!!!!!!!!!!!!!!!!!!!!!') {
        resultsList.innerHTML = '<h1 class="text-2xl text-red-500 font-bold">OH NOOOOOO!!! THEY FOUND OUT!!!</h1>';
    }
    else {
    // Get the results list element
        // Clear any previous results
        resultsList.innerHTML = '';
    
        // Filter the games array
        const filteredGames = games.filter(game => 
        game.name.toLowerCase().includes(searchInput)
        );
        filteredGames.forEach(game => {
            const card = createGameCard(game);
            gameGallery.appendChild(card);
        });
    }
}


// Function to create a single game card element
function createGameCard(game) {
    // Create the main container for the game card
    const gameCard = document.createElement('div');
    gameCard.className = 'game-card bg-gray-800 rounded-lg shadow-lg overflow-hidden';

    // Create the image element
    const img = document.createElement('img');
    img.src = game.imageSrc;
    img.alt = game.name;
    img.className = 'w-full h-48 object-cover rounded-t-lg'; // Tailwind classes for image styling

    // Create the game name overlay element
    const gameName = document.createElement('div');
    gameName.className = 'game-name'; // Custom CSS class for styling and hover effect
    gameName.textContent = game.name;

    // Append image and name to the game card
    gameCard.appendChild(img);
    gameCard.appendChild(gameName);

    // Add click event listener to redirect to the game path
    gameCard.addEventListener('click', () => {
        window.location.href = game.gamePath;
    });

    return gameCard;
}

document.addEventListener('DOMContentLoaded', () => {
    // Loop through the games array and add each game to the gallery
    games.forEach(game => {
        const card = createGameCard(game);
        gameGallery.appendChild(card);
    });
});