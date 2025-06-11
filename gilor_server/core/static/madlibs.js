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
        } else {
            madLibsStoryOutput.textContent = "Please fill in all the blanks to generate the story!";
        }
    });
});