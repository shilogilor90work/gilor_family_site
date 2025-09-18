const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Canvas dimensions
canvas.width = 800;
canvas.height = 500;

// Game constants
const paddleWidth = 10;
const paddleHeight = 100;
const ballRadius = 7;
const winningScore = 5;
let ballSpeedX = 5;
let ballSpeedY = 5;
let gameRunning = true;

// Player objects
const player1 = {
    x: 10,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    color: 'white',
    score: 0
};

const player2 = {
    x: canvas.width - paddleWidth - 10,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    color: 'white',
    score: 0
};

// Ball object
const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: ballRadius,
    color: 'white',
    speed: 5, // Base speed, will be modified by ballSpeedX/Y
    dx: 1, // Direction on X axis
    dy: 1  // Direction on Y axis
};

// Movement
const paddleSpeed = 10;
let player1MoveUp = false;
let player1MoveDown = false;
let player2MoveUp = false;
let player2MoveDown = false;

// Event listeners for keyboard input
document.addEventListener('keydown', (e) => {
    if (e.key === 'w' || e.key === 'W') player1MoveUp = true;
    if (e.key === 's' || e.key === 'S') player1MoveDown = true;
    if (e.key === 'ArrowUp') player2MoveUp = true;
    if (e.key === 'ArrowDown') player2MoveDown = true;
});

document.addEventListener('keyup', (e) => {
    if (e.key === 'w' || e.key === 'W') player1MoveUp = false;
    if (e.key === 's' || e.key === 'S') player1MoveDown = false;
    if (e.key === 'ArrowUp') player2MoveUp = false;
    if (e.key === 'ArrowDown') player2MoveDown = false;
});

// Function to draw a rectangle (paddle)
function drawRect(x, y, w, h, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, w, h);
}

// Function to draw a circle (ball)
function drawCircle(x, y, r, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2, false);
    ctx.closePath();
    ctx.fill();
}

// Function to draw the score
function drawScore(text, x, y) {
    ctx.fillStyle = 'white';
    ctx.font = '45px Arial';
    ctx.fillText(text, x, y);
}

// Function to reset the ball's position and direction
function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.speed = 5; // Reset speed
    ball.dx = -ball.dx; // Reverse direction
    ball.dy = (Math.random() > 0.5 ? 1 : -1); // Randomize Y direction
}

// Function to update game state
function update() {
    if (!gameRunning) return;

    // Move paddles
    if (player1MoveUp && player1.y > 0) {
        player1.y -= paddleSpeed;
    }
    if (player1MoveDown && player1.y < canvas.height - paddleHeight) {
        player1.y += paddleSpeed;
    }
    if (player2MoveUp && player2.y > 0) {
        player2.y -= paddleSpeed;
    }
    if (player2MoveDown && player2.y < canvas.height - paddleHeight) {
        player2.y += paddleSpeed;
    }

    // Move ball
    ball.x += ball.dx * ball.speed;
    ball.y += ball.dy * ball.speed;

    // Ball collision with top/bottom walls
    if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) {
        ball.dy = -ball.dy;
    }

    // Ball collision with paddles
    // Player 1 paddle
    if (ball.x - ball.radius < player1.x + player1.width &&
        ball.y > player1.y && ball.y < player1.y + player1.height &&
        ball.x > player1.x) { // Ensure ball is moving towards player 1
        ball.dx = 1;
        ball.speed += 0.2; // Increase speed slightly
    }

    // Player 2 paddle
    if (ball.x + ball.radius > player2.x &&
        ball.y > player2.y && ball.y < player2.y + player2.height &&
        ball.x < player2.x + player2.width) { // Ensure ball is moving towards player 2
        ball.dx = -1;
        ball.speed += 0.2; // Increase speed slightly
    }

    // Ball goes out of bounds (scoring)
    if (ball.x - ball.radius > canvas.width) {
        player1.score++;
        resetBall();
        if (player1.score >= winningScore) {
            alert("Left Player Wins!");
            gameRunning = false;
        }
    } else if (ball.x + ball.radius < 0) {
        player2.score++;
        resetBall();
        if (player2.score >= winningScore) {
            alert("Right Player Wins!");
            gameRunning = false;
        }
    }
}

// Function to render the game
function render() {
    // Clear canvas
    drawRect(0, 0, canvas.width, canvas.height, '#000');

    // Draw paddles
    drawRect(player1.x, player1.y, player1.width, player1.height, player1.color);
    drawRect(player2.x, player2.y, player2.width, player2.height, player2.color);

    // Draw ball
    drawCircle(ball.x, ball.y, ball.radius, ball.color);

    // Draw scores
    drawScore(player1.score, canvas.width / 4, 40);
    drawScore(player2.score, 3 * canvas.width / 4, 40);

    // Draw center line (optional)
    ctx.strokeStyle = 'white';
    ctx.beginPath();
    ctx.setLineDash([10, 10]); // Dashed line
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
    ctx.setLineDash([]); // Reset line dash
}

// Game loop
function gameLoop() {
    update();
    render();
    if (gameRunning) {
        requestAnimationFrame(gameLoop);
    }
}

function gamestart() {
    player1.score = 0;
    player2.score = 0;
    gameRunning = false;
    gameRunning = true;
    gameLoop();
}

// Start the game
document.querySelector('#startButton').addEventListener('click', gamestart);
