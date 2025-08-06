const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.querySelector('.score');

let bird = {
  x: 50,
  y: 150,
  width: 30,
  height: 30,
  gravity: 0.6,
  lift: -10,
  velocity: 0
};

let pipes = [];
let frame = 0;
let score = 0;
let gameOver = false;
let user_name = document.querySelector('.user-name')?.textContent || 'Anonymous'; // Get the username from the HTML

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function sendGameRecordToAPI(Score, name) {


    fetch('/amitai/save_flappy_bird_score', { // Updated API endpoint URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            name: name,
            score: Score,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('API response:', data);
        if (data.status === 'success') {
            console.log('Game record successfully sent to API!');
            // Optionally, you might want to refresh the leaderboard here
            // if you implement an API for getting scores, or reload the page.
            // For now, it just saves.
        } else {
            console.error('Failed to send game record:', data.message);
        }
    })
    .catch(error => {
        console.error('Error sending game record to API:', error);
    });
}
async function delay(seconds) {
  return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

function drawBird() {
  ctx.fillStyle = 'yellow';
  ctx.fillRect(bird.x, bird.y, bird.width, bird.height);
}

function updateBird() {
  bird.velocity += bird.gravity;
  bird.y += bird.velocity;

  if (bird.y + bird.height >= canvas.height) {
    gameOver = true;
  }
  if (bird.y <= 0) {
    bird.y = 0;
    bird.velocity = 0;
  }
}

function drawPipes() {
  ctx.fillStyle = 'green';
  pipes.forEach(pipe => {
    ctx.fillRect(pipe.x, 0, pipe.width, pipe.top);
    ctx.fillRect(pipe.x, canvas.height - pipe.bottom, pipe.width, pipe.bottom);
  });
}

function updatePipes() {
  if (frame % 90 === 0) {
    let top = Math.floor(Math.random() * (canvas.height - 140)) + 20;
    let gap = 200; // Space between pipes!!!!
    let bottom = canvas.height - top - gap;
    pipes.push({ x: canvas.width, width: 40, top, bottom });
  }

  pipes.forEach(pipe => {
    pipe.x -= 2;

    // Collision check
    if (
      bird.x < pipe.x + pipe.width &&
      bird.x + bird.width > pipe.x &&
      (bird.y < pipe.top || bird.y + bird.height > canvas.height - pipe.bottom)
    ) {
      gameOver = true;
    }

    // Score update
    if (pipe.x + pipe.width === bird.x) {
      score++;
      scoreElement.textContent = 'Score: ' + score;
    }
  });

  pipes = pipes.filter(pipe => pipe.x + pipe.width > 0);
}
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawBird();
  drawPipes();
}
function highScore() {fetch('/amitai/get_flappy_bird_top_score', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    }})
    .then(response => response.json())
    .then(data => {
      console.log('High score:', data);
        if (data.score !== null) {
            console.log('High score:', data.score);
            ctx.fillStyle = '#fff';
            ctx.font = '20px sans-serif';
            ctx.fillText('High Score: ' + data.score, 10, 30);
        } else {
            console.error('Failed to fetch high score:', data.message);
        }
    });
}

function update() {
  if (gameOver) {
    ctx.fillStyle = 'rgba(0,0,0,0.5)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#fff';
    ctx.font = '24px sans-serif';
    ctx.fillText('Game Over', 100, canvas.height / 2);
    ctx.fillText('Score: ' + score, 115, canvas.height / 2 + 30);
    sendGameRecordToAPI(score, user_name);
    ctx.fillText('highscore:' + highScore(), 100, canvas.height / 2 + 60);
    return;
  }
  updateBird();
  updatePipes();
  draw();
  frame++;
  requestAnimationFrame(update);
}

window.addEventListener('keydown', () => {
  bird.velocity = bird.lift;
});
window.addEventListener('click', () => {
  bird.velocity = bird.lift;
});

delay(3);
update();

function resetGame() {
    bird.y = 150;
    bird.velocity = 0;
    pipes = [];
    frame = 0;
    score = 0;
    gameOver = false;
    scoreElement.textContent = 'Score: ' + score;
    delay(3);
    update();
}

document.querySelector('.reset-button').addEventListener('click', resetGame);
