const API_BASE_URL = 'http://127.0.0.1:8000/amitai';
const CREATE_DATA_ENDPOINT = `${API_BASE_URL}/create_finished_data`;
const GET_RANDOM_TEMPLATE = `${API_BASE_URL}/get_random_template`;
const SAVE_STORY_API_ENDPOINT = `${API_BASE_URL}/create_finished_data`; 


let currentTemplate = null; // To store the fetched template

// Function to display messages (e.g., errors)
function displayMessage(message, type) {
    const messageContainer = document.createElement('div');
    messageContainer.textContent = message;
    messageContainer.className = `message ${type}`; // Add styling for 'error' messages
    document.body.prepend(messageContainer);
    setTimeout(() => messageContainer.remove(), 5000); // Remove after 5 seconds
}


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


async function get_random_template(type) { // Removed 'data' from parameters
    try {
        // Construct query string parameters with only 'type'
        const queryParams = new URLSearchParams({ type }).toString(); // Removed 'data'
        const url = `${GET_RANDOM_TEMPLATE}?${queryParams}`;

        response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.log("end get_random_template");
            throw new Error(errorData.message || `API error: ${response.status}`);
        }
        json_data = await response.json();
        return json_data;
    } catch (error) {
        console.error(`Error fetching random template for ${type}:`, error);
        displayMessage(`Error fetching random template for ${type}: ${error.message}`, 'error');
        throw error;
    }
}


// document.addEventListener('DOMContentLoaded', () => {
//     const generateButton = document.getElementById('generateStory');
//     const madLibsStoryOutput = document.getElementById('madLibsStory');

//     generateButton.addEventListener('click', async () => {
        
//         const adj1 = document.getElementById('adj1').value;
//         const noun1 = document.getElementById('noun1').value;
//         const adj2 = document.getElementById('adj2').value;
//         const verb1 = document.getElementById('verb1').value;
//         const adj3 = document.getElementById('adj3').value;
//         const adj4 = document.getElementById('adj4').value;

//         if (adj1 && noun1 && adj2 && verb1 && adj3 && adj4) {
//             const story = `Today I went to a ${adj1} zoo.
// In an exhibit, I saw a ${noun1} tied to a tree.
// The ${noun1} was very ${adj2},
// ${verb1} it was ${adj3}.
// I would ${adj4} to go there again.`;


//             madLibsStoryOutput.textContent = story;
//             console.log("calling function");
//             saveData("finished_story", {
//                 "paragraph_id": 1, 
//                 "user_name": "Amitai",
//                 "noun": [noun1],
//                 "adjective": [adj1, adj2, adj3, adj4],
//                 "verb": [verb1],
//                 "funny_word": [],
//                 "funny_name": []
//             });
//             console.log("called function");


//         } else {
//             result = await get_random_template("paragraph");
//             console.log(result);
//             madLibsStoryOutput.textContent = "Please fill in all the blanks to generate the story!";
//         }
//     });
// });


// Function to generate input fields based on template
function generateInputFields(template) {
    const inputSection = document.getElementById('inputSection');
    inputSection.innerHTML = ''; // Clear existing inputs

    const placeholders = {}; // To count occurrences of each placeholder type

    // Regex to find placeholders like [noun], [verb], [adjective]
    const regex = /\[(noun|verb|adjective|funny_name|funny_word)\]/g;
    let match;

    while ((match = regex.exec(template.paragraph)) !== null) {
        const placeholderType = match[1]; // e.g., 'noun', 'verb'
        placeholders[placeholderType] = (placeholders[placeholderType] || 0) + 1;
    }

    // Create input fields for each placeholder
    for (const type in placeholders) {
        for (let i = 1; i <= placeholders[type]; i++) {
            const label = document.createElement('label');
            label.setAttribute('for', `${type}${i}`);

            let promptText = '';
            switch (type) {
                case 'noun':
                    promptText = 'Enter a noun (person, place, or thing):';
                    break;
                case 'verb':
                    promptText = "Enter a verb (an action word, often ending with 'ing' if specified in the template):";
                    break;
                case 'adjective':
                    promptText = 'Enter an adjective (a descriptive word):';
                    break;
                case 'funny_name':
                    promptText = 'Enter a funny name:';
                    break;
                case 'funny_word':
                    promptText = 'Enter a funny word:';
                    break;
                default:
                    promptText = `Enter a ${type}:`;
            }
            label.textContent = `${promptText}`;

            const input = document.createElement('input');
            input.setAttribute('type', 'text');
            input.setAttribute('id', `${type}${i}`);
            input.setAttribute('data-type', type); // Store the type for easier retrieval later

            inputSection.appendChild(label);
            inputSection.appendChild(input);
        }
    }
}


// Function to generate the story
// function generateStory() {
//     if (!currentTemplate) {
//         displayMessage('No template loaded. Please refresh the page.', 'error');
//         return;
//     }

//     let story = currentTemplate.paragraph;
//     const inputs = document.querySelectorAll('#inputSection input');
//     const replacements = {};

//     inputs.forEach(input => {
//         const type = input.getAttribute('data-type');
//         const id = input.id;
//         replacements[id] = input.value || `[${type}]`; // Use placeholder if input is empty
//     });

//     // Replace placeholders in the story
//     const regex = /\[(noun|verb|adjective|funny_name|funny_word)\]/g;
//     let inputCounter = { noun: 0, verb: 0, adjective: 0, funny_name: 0, funny_word: 0 };

//     story = story.replace(regex, (match, p1) => {
//         inputCounter[p1]++;
//         const replacementId = `${p1}${inputCounter[p1]}`;
        
//         return replacements[replacementId] || match; // Use the collected replacement or original placeholder
//     });

//     document.getElementById('madLibsStory').textContent = story;
// }



// Function to generate the story
async function generateStory() { // Made async to await saveStoryToAPI
    if (!currentTemplate) {
        displayMessage('No template loaded. Please refresh the page or get a new template.', 'error');
        return;
    }

    let story = currentTemplate.paragraph;
    const inputs = document.querySelectorAll('#inputSection input');
    const replacements = {};
    const collectedWords = {
        noun: [],
        adjective: [],
        verb: [],
        funny_word: [],
        funny_name: []
    };

    inputs.forEach(input => {
        const type = input.getAttribute('data-type');
        const id = input.id;
        const value = input.value.trim(); // Trim whitespace

        replacements[id] = value || `[${type}]`; // Use placeholder if input is empty

        // Collect words into their respective arrays for API
        if (collectedWords.hasOwnProperty(type)) {
            collectedWords[type].push(value);
        }
    });

    // Replace placeholders in the story
    const regex = /\[(noun|verb|adjective|funny_name|funny_word)\]/g;
    let inputCounter = { noun: 0, verb: 0, adjective: 0, funny_name: 0, funny_word: 0 };

    story = story.replace(regex, (match, p1) => {
        inputCounter[p1]++;
        const replacementId = `${p1}${inputCounter[p1]}`;
        return replacements[replacementId] || match; // Use the collected replacement or original placeholder
    });

    document.getElementById('madLibsStory').textContent = story;

    // NEW: Prepare data for saving
    const userName = document.getElementById('user_Name')?.value.trim() || 'Anonymous'; // Get user name, default to Anonymous
    const storyData = {
        paragraph_id: currentTemplate.id,
        user_name: userName,
        noun: collectedWords.noun,
        adjective: collectedWords.adjective,
        verb: collectedWords.verb,
        funny_word: collectedWords.funny_word,
        funny_name: collectedWords.funny_name,
        generated_story_text: story // You might want to save the final story text as well
    };
    console.log("Generated Story Data:", storyData); // Log the data to be saved
    // NEW: Save the story to the API
    await saveStoryToAPI(storyData); // Call the new function
}



// Event listener for the Generate Story button
document.getElementById('generateStory').addEventListener('click', generateStory);

// On page load, fetch a random template and generate inputs
// document.addEventListener('DOMContentLoaded', async () => {
//     try {
//         // You might want to pass a 'type' if your API supports filtering templates
//         // For now, assuming a general random template is fetched
//         currentTemplate = await get_random_template('general');
//         if (currentTemplate && currentTemplate.paragraph) {
//             generateInputFields(currentTemplate);
//         } else {
//             displayMessage('Failed to load a valid Mad Libs template.', 'error');
//         }
//     } catch (error) {
//         console.error('Error on page load:', error);
//         displayMessage('Could not load Mad Libs template on startup. Please try again later.', 'error');
//     }
// });

// Function to handle loading a new template (for button click)
async function loadNewTemplate() {
    try {
        const template = await get_random_template('general'); // Fetch a new template
        if (template && template.paragraph) {
            currentTemplate = template; // Update the currentTemplate
            generateInputFields(currentTemplate); // Regenerate inputs based on new template
            document.getElementById('madLibsStory').textContent = ''; // Clear previous story
        } else {
            displayMessage('Failed to load a new valid Mad Libs template.', 'error');
        }
    } catch (error) {
        console.error('Error loading new template:', error);
        displayMessage('Could not load a new Mad Libs template. Please try again.', 'error');
    }
}

// Event listener for the New Template button
document.getElementById('newTemplateButton').addEventListener('click', loadNewTemplate);


// On page load, fetch a random template and generate inputs
document.addEventListener('DOMContentLoaded', async () => {
    await loadNewTemplate(); // Use the new function for initial load too
});


// NEW FUNCTION: Save the generated story data to the API
async function saveStoryToAPI(storyData) {
    try {
        const response = await fetch(SAVE_STORY_API_ENDPOINT, { // <--- CUSTOMIZE SAVE_STORY_API_ENDPOINT
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // <--- CUSTOMIZE: If you need CSRF token for Django, add it here.
                // 'X-CSRFToken': getCookie('csrftoken'), // Example: If using Django with CSRF
            },
            body: JSON.stringify({ data: storyData }), // Your API expects data nested under 'data'
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `API error: ${response.status}`);
        }

        const result = await response.json();
        console.log('Story saved successfully:', result);
        displayMessage('Story saved successfully!', 'success');
    } catch (error) {
        console.error('Error saving story:', error);
        displayMessage(`Error saving story: ${error.message}`, 'error');
    }
}
