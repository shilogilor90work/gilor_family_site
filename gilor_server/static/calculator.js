document.addEventListener('DOMContentLoaded', () => {
    const num1Input = document.getElementById('num1');
    const operatorInput = document.getElementById('operator');
    const num2Input = document.getElementById('num2');
    const calculateBtn = document.getElementById('calculate-btn');
    const resultDisplay = document.getElementById('result');
    const num1Error = document.getElementById('num1-error');
    const operatorError = document.getElementById('operator-error');
    const num2Error = document.getElementById('num2-error');

    calculateBtn.addEventListener('click', calculateResult);

    function isValidNumber(inputString) {
        return /^\d+$/.test(inputString);
    }

    function isValidOperator(op) {
        return ['/', '*', '+', '-', '^'].includes(op);
    }

    function calculateResult() {
        // Clear previous errors
        num1Error.textContent = '';
        operatorError.textContent = '';
        num2Error.textContent = '';
        resultDisplay.textContent = '';

        let num1Str = num1Input.value.trim();
        let operator = operatorInput.value.trim();
        let num2Str = num2Input.value.trim();

        let isValid = true;

        if (!isValidNumber(num1Str)) {
            num1Error.textContent = 'Must contain only digits.';
            isValid = false;
        }

        if (!isValidOperator(operator)) {
            operatorError.textContent = 'Must be one of /, *, +, -, ^.';
            isValid = false;
        }

        if (!isValidNumber(num2Str)) {
            num2Error.textContent = 'Must contain only digits.';
            isValid = false;
        }

        if (!isValid) {
            return; // Stop if there are validation errors
        }

        let num1 = parseInt(num1Str);
        let num2 = parseInt(num2Str);
        let result;

        switch (operator) {
            case '*':
                result = num1 * num2;
                break;
            case '/':
                if (num2 === 0) {
                    resultDisplay.textContent = 'Error: Division by zero';
                    return;
                }
                result = num1 / num2;
                break;
            case '+':
                result = num1 + num2;
                break;
            case '-':
                result = num1 - num2;
                break;
            case '^':
                result = Math.pow(num1, num2);
                break;
            default:
                result = "Invalid operation"; // Should not be reached due to validation
        }

        // Round to 3 decimal places for numbers, keep as is for "Invalid operation" or "Error"
        if (typeof result === 'number') {
            result = parseFloat(result.toFixed(3));
        }
        
        resultDisplay.textContent = `${num1} ${operator} ${num2} = ${result}`;
    }
});