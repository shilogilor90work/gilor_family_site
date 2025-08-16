
const get_games_endpoint = `get_game_info`;

async function fetchGames() {
    try {
        const response = await fetch(get_games_endpoint, {
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
        return Array.isArray(data) ? data : (data.games || []);
    } catch (error) {
        console.error(`Error fetching games:`, error);
        displayMessage(`Error fetching games: ${error.message}`, 'error');
        throw error;
    }
}



const gameGallery = document.getElementById('game-gallery');


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
        game.game_name.toLowerCase().includes(searchInput)
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
    img.src = game.game_image; // Fallback image if not available
    img.alt = game.game_name; // Fallback alt text if game_name is not available
    img.className = 'w-full h-48 object-cover rounded-t-lg'; // Tailwind classes for image styling

    // Create the game name overlay element
    const gameName = document.createElement('div');
    gameName.className = 'game-name'; // Custom CSS class for styling and hover effect
    gameName.textContent = game.game_name;

    // Append image and name to the game card
    gameCard.appendChild(img);
    gameCard.appendChild(gameName);

    // Add click event listener to redirect to the game path
    gameCard.addEventListener('click', () => {
        window.location.href = game.game_link; // Use game_link if available, otherwise fallback to gamePath
    });

    return gameCard;
}

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const games = await fetchGames(); // ✅ wait for fetch to finish
        games.forEach(game => {
            const card = createGameCard(game);
            gameGallery.appendChild(card);
        });
    } catch (error) {
        console.error("Could not load games:", error);
    }
});
