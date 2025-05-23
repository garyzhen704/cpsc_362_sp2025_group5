// Canvas Setup
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeCanvas, false);
resizeCanvas();

// Game Variables
let ballRadius = 10;
let balls = [{ x: canvas.width / 2, y: canvas.height - 30, dx: 4, dy: -4 }];
const maxBallSpeed = 15;

let paddleHeight = 15;
let paddleWidth = 150;
let paddleX = (canvas.width - paddleWidth) / 2;
let paddleSpeed = 12;

let rightPressed = false;
let leftPressed = false;

let brickRowCount = 10;
let brickColumnCount = Math.floor((canvas.width + 10) / (75 + 10));
let brickWidth = 75;
let brickHeight = 20;
let brickPadding = 10;
let brickOffsetTop = 55;
let brickOffsetLeft = 10;

let bricks = [];
for (let c = 0; c < brickColumnCount; c++) {
    bricks[c] = [];
    for (let r = 0; r < brickRowCount; r++) {
        bricks[c][r] = { x: 0, y: 0, status: 1 };
    }
}

let score = 0;
let lives = 3;

let powerUps = [];
const powerUpTypes = ["paddleWidth", "extraBall", "extraLife", "tripleBall"];
const powerUpWidth = 20;
const powerUpHeight = 20;
const powerUpFallSpeed = 2;

// Event Handlers
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

function keyDownHandler(e) {
    if (e.key == "Right" || e.key == "ArrowRight") {
        rightPressed = true;
    } else if (e.key == "Left" || e.key == "ArrowLeft") {
        leftPressed = true;
    }
}

function keyUpHandler(e) {
    if (e.key == "Right" || e.key == "ArrowRight") {
        rightPressed = false;
    } else if (e.key == "Left" || e.key == "ArrowLeft") {
        leftPressed = false;
    }
}

// Utility Functions
function drawRounded(x, y, width, height, radius) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.arcTo(x + width, y, x + width, y + radius, radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.arcTo(x + width, y + height, x + width - radius, y + height, radius);
    ctx.lineTo(x + radius, y + height);
    ctx.arcTo(x, y + height, x, y + height - radius, radius);
    ctx.lineTo(x, y + radius);
    ctx.arcTo(x, y, x + radius, y, radius);
    ctx.closePath();
}

// Drawing Functions
function drawPaddle() {
    let gradient = ctx.createLinearGradient(
        paddleX,
        canvas.height - paddleHeight,
        paddleX + paddleWidth,
        canvas.height
    );
    gradient.addColorStop(0, "white");

    drawRounded(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight, 7);
    ctx.fillStyle = gradient;
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = "white";
    ctx.stroke();
}

function drawBall(ball) {
    let gradient = ctx.createRadialGradient(
        ball.x,
        ball.y,
        5,
        ball.x,
        ball.y,
        ballRadius
    );
    gradient.addColorStop(0, "red");
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = gradient;
    ctx.fill();
    ctx.closePath();
}

function drawBricks() {
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            if (bricks[c][r].status == 1) {
                let brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
                let brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;

                let gradient = ctx.createLinearGradient(brickX, brickY, brickX + brickWidth, brickY + brickHeight);
                gradient.addColorStop(0, "blue");
                gradient.addColorStop(1, "lightblue");

                drawRounded(brickX, brickY, brickWidth, brickHeight, 5);
                ctx.fillStyle = gradient;
                ctx.fill();
                ctx.lineWidth = 2;
                ctx.strokeStyle = "white";
                ctx.stroke();
            }
        }
    }
}

function drawPowerUps() {
    powerUps.forEach((power, index) => {
        ctx.font = "20px Arial";
        ctx.fillStyle = power.type === "extraLife" ? "pink" : power.type === "extraBall" ? "blue" : power.type === "paddleWidth" ? "green" : "orange";
        ctx.fillText(power.type === "extraLife" ? "💖" : power.type === "extraBall" ? "🪩" : power.type === "paddleWidth" ? "↔️" : "X3", power.x, power.y);

        power.y += powerUpFallSpeed;

        if (power.y > canvas.height) {
            powerUps.splice(index, 1);
        }
    });
}

function drawScore() {
    ctx.font = "30px Arial";
    ctx.fillStyle = "white";
    ctx.fillText("Score: " + score, 15, 40);
}

function drawLives() {
    ctx.font = "30px Arial";
    ctx.fillStyle = "white";
    ctx.fillText("Lives: " + lives, canvas.width - 150, 40);
}

// Collision Detection
function collisionDetection() {
    for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
            let b = bricks[c][r];
            if (b.status == 1) {
                if (
                    balls.some(ball => ball.x > b.x && ball.x < b.x + brickWidth && ball.y > b.y && ball.y < b.y + brickHeight)
                ) {
                    balls.forEach(ball => {
                        if (ball.x + ballRadius > b.x &&
                            ball.x - ballRadius < b.x + brickWidth &&
                            ball.y + ballRadius > b.y &&
                            ball.y - ballRadius < b.y + brickHeight) {
                            ball.dy = -ball.dy;
                            b.status = 0;
                            score++;

                            // Randomly spawn a power-up when a brick is hit
                            if (Math.random() < 0.08) {
                                spawnPowerUp(b.x + brickWidth / 2, b.y + brickHeight);
                            }

                            const allBricksCleared = bricks.every(column => column.every(brick => brick.status === 0));
                            if (allBricksCleared) {
                                setTimeout(() => {
                                    alert("YOU WIN, CONGRATULATIONS!");
                                    resetBricks(); // Reset bricks for the next level
                                }, 100);
                            }
                        }
                    });
                }
            }
        }
    }
}

// Function to reset bricks
function resetBricks() {
    bricks = [];
    for (let c = 0; c < brickColumnCount; c++) {
        bricks[c] = [];
        for (let r = 0; r < brickRowCount; r++) {
            bricks[c][r] = { x: 0, y: 0, status: 1 }; // Reset all bricks to active
        }
    }
    gameStarted = false; // Pause the game until the player clicks
    balls = [{ x: canvas.width / 2, y: canvas.height - 30, dx: 0, dy: 0 }]; // Reset ball position
    paddleX = (canvas.width - paddleWidth) / 2; // Reset paddle position
}

function spawnPowerUp(x, y) { 
    const type = powerUpTypes[Math.floor(Math.random() * powerUpTypes.length)];
    powerUps.push({x: x, y: y, type: type});
}

function collectPowerUps() {
    powerUps.forEach((power, index) => {
        if (
            power.x > paddleX &&
            power.x < paddleX + paddleWidth &&
            power.y > canvas.height - paddleHeight &&
            power.y < canvas.height
        ) {
            if (power.type === "extraLife") {
                lives++;
                score += 5;
            } else if (power.type === "extraBall") {
                balls.push({ x: balls[0].x, y: balls[0].y, dx: 4, dy: -4 });
                score += 5;
            } else if (power.type === "paddleWidth") {
                paddleWidth += 50;
                score += 5;
                setTimeout(() => {
                    paddleWidth -= 20;
                }, 5000);
            } else if (power.type === "tripleBall") {
                balls.push({ x: balls[0].x, y: balls[0].y, dx: 4, dy: -4 });
                balls.push({ x: balls[0].x, y: balls[0].y, dx: -4, dy: -4 });
                score += 5;
            }
            powerUps.splice(index, 1);
        }
    });
}


// Add a gameStarted flag
let gameStarted = false;

let lastFrameTime = performance.now(); 

// Main Game Loop
function draw() {
    const currentFrameTime = performance.now();
    const deltaTime = (currentFrameTime - lastFrameTime) / 16.67; // Convert to seconds (assuming 60 FPS)
    lastFrameTime = currentFrameTime;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    balls.forEach(drawBall);
    drawPaddle();
    drawBricks();
    drawScore();
    drawLives();
    collisionDetection();
    drawPowerUps();
    collectPowerUps();

    if (!gameStarted) {
        // Position the ball on the paddle
        balls[0].x = paddleX + paddleWidth / 2;
        balls[0].y = canvas.height - paddleHeight - ballRadius;
    } else {
        // Update ball positions
        balls.forEach((ball, ballIndex) => {
            
            ball.x += ball.dx * deltaTime;
            ball.y += ball.dy * deltaTime;

            // Check for wall collisions
            if (ball.x + ball.dx > canvas.width - ballRadius || ball.x + ball.dx < ballRadius) {
                ball.dx = -ball.dx;
            }

            if (ball.y + ball.dy < ballRadius) {
                ball.dy = -ball.dy;
            } else if (ball.y + ball.dy > canvas.height - ballRadius) {
                // Check for collision with paddle
                if (
                    ball.x > paddleX &&
                    ball.x < paddleX + paddleWidth &&
                    ball.y + ballRadius >= canvas.height - paddleHeight
                ) {
                    let hitPosition = ball.x - (paddleX + paddleWidth / 2);
                    let hitAngle = (hitPosition / (paddleWidth / 2)) * (Math.PI / 3);

                    // Adjust ball direction based on hit position
                    ball.dx = 8 * Math.sin(hitAngle);
                    ball.dy = -Math.abs(8 * Math.cos(hitAngle));

                    // Limit ball speed
                    const speed = Math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy);
                    if (speed > maxBallSpeed) {
                        ball.dx = (ball.dx / speed) * maxBallSpeed;
                        ball.dy = (ball.dy / speed) * maxBallSpeed;
                    }
                } else {
                    balls.splice(ballIndex, 1);
                    if (balls.length === 0) {
                        lives--;
                        if (lives === 0) {
                            alert("GAME OVER");
                            document.location.reload();
                        } else {
                            // Reset ball and paddle position
                            balls = [{ x: canvas.width / 2, y: canvas.height - 30, dx: 0, dy: 0 }];
                            paddleX = (canvas.width - paddleWidth) / 2;
                            gameStarted = false; // Wait for player to click
                        }
                    }
                }
            }
        });
    }

    // Paddle movement
    if (rightPressed && paddleX < canvas.width - paddleWidth) {
        paddleX += paddleSpeed * deltaTime;
    } else if (leftPressed && paddleX > 0) {
        paddleX -= paddleSpeed * deltaTime;
    }

    requestAnimationFrame(draw);
}

// Add an event listener to start the game on click
canvas.addEventListener("click", () => {
    if (!gameStarted) {
        gameStarted = true;
        balls[0].dx = (Math.random() < 0.5 ? -1 : 1) * 4; // Randomize initial horizontal direction
        balls[0].dy = -8; // Set initial vertical direction
    }
});

draw();