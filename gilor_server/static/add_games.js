
const CREATE_GAME_ENDPOINT = `amitai/create_game`;

async function createGame(gameData) {
    try {
        const response = await fetch(CREATE_GAME_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(gameData),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `API error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error creating game:', error);
        displayMessage(`Error creating game: ${error.message}`, 'error');
        throw error;
    }
}

const game_name = document.getElementById('gameName');
const game_link = document.getElementById('gameLink');
const game_image = document.getElementById('gameImage');

addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission

    const gameData = {
        game_name: game_name,
        game_link: game_link,
        game_image: game_image,
    };

    try {
        const createdGame = await createGame(gameData);
        displayMessage(`Game created successfully: ${createdGame.name}`, 'success');
    } catch (error) {
        displayMessage(`Error creating game: ${error.message}`, 'error');
    }
}
);