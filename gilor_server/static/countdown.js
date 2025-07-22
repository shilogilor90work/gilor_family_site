document.addEventListener('DOMContentLoaded', () => {
    const timeInput = document.getElementById('timeInput');
    const startBtn = document.getElementById('startBtn');
    const countdownDisplay = document.getElementById('countdownDisplay');
    const messageDisplay = document.getElementById('messageDisplay');
    const errorMessage = document.getElementById('error-message');

    let countdownInterval;

    startBtn.addEventListener('click', startCountdown);

    function startCountdown() {
        // Clear any previous countdown and messages
        clearInterval(countdownInterval);
        countdownDisplay.textContent = '';
        messageDisplay.textContent = '';
        errorMessage.textContent = '';
        startBtn.disabled = false; // Ensure button is enabled for new start

        let timeWait = timeInput.value.trim();

        // Validation: check if input contains only digits and is a positive number
        if (!/^\d+$/.test(timeWait) || parseInt(timeWait) <= 0) {
            errorMessage.textContent = 'Invalid input: Please enter a positive whole number.';
            return;
        }

        timeWait = parseInt(timeWait);
        startBtn.disabled = true; // Disable button during countdown

        countdownDisplay.textContent = timeWait; // Display initial number immediately

        countdownInterval = setInterval(() => {
            timeWait--;
            if (timeWait > 0) {
                countdownDisplay.textContent = timeWait;
            } else {
                clearInterval(countdownInterval);
                countdownDisplay.textContent = ''; // Clear number
                messageDisplay.textContent = 'GO!!!!!';
                startBtn.disabled = false; // Re-enable button
            }
        }, 1000); // 1000 milliseconds = 1 second
    }
});