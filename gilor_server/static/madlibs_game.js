const API_BASE_URL = 'http://127.0.0.1:8000/amitai';
const CREATE_DATA_ENDPOINT = `${API_BASE_URL}/create_finished_data`;
const GET_RANDOM_TEMPLATE = `${API_BASE_URL}/get_random_template`;


async function saveData(type, data) {
    console.log("starting function");
    try {
        const response = await fetch(CREATE_DATA_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data }),
        });
        console.log("started fetch");
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `API error: ${response.status}`);
        }
        console.log("end fetch");
        return await response.json();
    } catch (error) {
        console.error(`Error saving ${type}:`, error);
        displayMessage(`Error saving ${type}: ${error.message}`, 'error');
        throw error;
    }
}

// async function get_random_template(data, type) {
//     try {
//         console.log("starting get_random_template");
//         // Construct query string parameters
//         const queryParams = new URLSearchParams({ type, data: JSON.stringify(data) }).toString();
//         const url = `${GET_RANDOM_TEMPLATE}?${queryParams}`;

//         const response = await fetch(url, {
//             method: 'GET',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//         });

//         if (!response.ok) {
//             const errorData = await response.json();
//             console.log("end get_random_template");
//             throw new Error(errorData.message || `API error: ${response.status}`);
//         }
//         return await response.json();
//     } catch (error) {
//         console.error(`Error fetching random template for ${type}:`, error);
//         displayMessage(`Error fetching random template for ${type}: ${error.message}`, 'error');
//         throw error;
//     }
// }

async function get_random_template(type) { // Removed 'data' from parameters
    try {
        console.log("starting get_random_template");
        // Construct query string parameters with only 'type'
        const queryParams = new URLSearchParams({ type }).toString(); // Removed 'data'
        const url = `${GET_RANDOM_TEMPLATE}?${queryParams}`;

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        console.log(response);

        if (!response.ok) {
            const errorData = await response.json();
            console.log("end get_random_template");
            throw new Error(errorData.message || `API error: ${response.status}`);
        }
        console.log("done");
        return await response.json();
    } catch (error) {
        console.error(`Error fetching random template for ${type}:`, error);
        displayMessage(`Error fetching random template for ${type}: ${error.message}`, 'error');
        throw error;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const generateButton = document.getElementById('generateStory');
    const madLibsStoryOutput = document.getElementById('madLibsStory');

    generateButton.addEventListener('click', () => {
        
        const adj1 = document.getElementById('adj1').value;
        const noun1 = document.getElementById('noun1').value;
        const adj2 = document.getElementById('adj2').value;
        const verb1 = document.getElementById('verb1').value;
        const adj3 = document.getElementById('adj3').value;
        const adj4 = document.getElementById('adj4').value;

        if (adj1 && noun1 && adj2 && verb1 && adj3 && adj4) {
            const story = `Today I went to a ${adj1} zoo.
In an exhibit, I saw a ${noun1} tied to a tree.
The ${noun1} was very ${adj2},
${verb1} it was ${adj3}.
I would ${adj4} to go there again.`;


            madLibsStoryOutput.textContent = story;
            console.log("calling function");
            saveData("finished_story", {
                "paragraph_id": 1, 
                "user_name": "Amitai",
                "noun": [noun1],
                "adjective": [adj1, adj2, adj3, adj4],
                "verb": [verb1],
                "funny_word": [],
                "funny_name": []
            });
            console.log("called function");


        } else {
            const result= get_random_template("paragraph");
            console.log(result);
            madLibsStoryOutput.textContent = "Please fill in all the blanks to generate the story!";
        }
    });
});