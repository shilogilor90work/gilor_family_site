document.addEventListener('DOMContentLoaded', () => {
    const widthInput = document.getElementById('widthInput');
    const heightInput = document.getElementById('heightInput');
    const generateBtn = document.getElementById('generateBtn');
    const rangeOutput = document.getElementById('rangeOutput');
    const gridOutput = document.getElementById('gridOutput');

    generateBtn.addEventListener('click', generateGrid);

    function generateGrid() {
        const width = parseInt(widthInput.value);
        const height = parseInt(heightInput.value);

        // Basic validation for numbers (HTML min attribute helps, but JS adds robustness)
        if (isNaN(width) || width < 1) {
            alert("Please enter a valid width (a number greater than 0).");
            return;
        }
        if (isNaN(height) || height < 1) {
            alert("Please enter a valid height (a number greater than 0).");
            return;
        }

        // Python equivalent of the for loop for the grid
        let gridText = '';
        for (let x = 1; x <= height; x++) {
            const spaces = ' * '.repeat(width);
            gridText += `${x} ${spaces}\n`;
        }
        gridOutput.textContent = gridText;
    }

    // Optional: Generate grid on page load with default values
    generateGrid();
});