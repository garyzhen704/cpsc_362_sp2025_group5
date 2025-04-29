//White box
function testPaddleAndBallCollision() {   
    console.log("Running testPaddleAndBallCollision..."); // Debugging log

    // Setup
    paddleX = canvas.width / 2 - paddleWidth / 2; // Center the paddle
    const ball = { x: paddleX + paddleWidth / 2, y: canvas.height - paddleHeight - ballRadius, dx: 4, dy: 4 };

    console.log("Paddle position:", paddleX, "Paddle width:", paddleWidth);
    console.log("Ball position before movement:", ball.x, ball.y);

    // Simulate ball movement
    ball.x += ball.dx;
    ball.y += ball.dy;

    console.log("Ball position after movement:", ball.x, ball.y);

    // Check collision with paddle
    if (
        ball.x > paddleX &&
        ball.x < paddleX + paddleWidth &&
        ball.y + ballRadius >= canvas.height - paddleHeight
    ) {
        ball.dy = -ball.dy; // Reverse ball direction
        console.log("Collision detected: Ball reversed direction.");
    } else {
        console.log("No collision detected.");
    }

    // Assertions
    if (ball.dy < 0) {
        console.log("Test Passed: Ball collided with paddle and reversed direction.");
    } else {
        console.error("Test Failed: Ball did not reverse direction after collision.");
    }

    if (ball.x > paddleX && ball.x < paddleX + paddleWidth) {
        console.log("Test Passed: Ball is within paddle bounds.");
    } else {
        console.error("Test Failed: Ball is not within paddle bounds.");
    }
}

//Black box
function testBrickCollision() {
    console.log("Running testBrickCollision..."); // Debugging log

    // Define brick dimensions (match values from brick_breaker.js)
    const brickWidth = 75;
    const brickHeight = 20;

    // Setup
    const testBrick = { x: 50, y: 50, status: 1 };
    const testBall = { x: 55, y: 55, dx: 4, dy: -4 };

    console.log("Before collision:", testBall.dy);

    // Simulate collision
    if (
        testBall.x > testBrick.x &&
        testBall.x < testBrick.x + brickWidth &&
        testBall.y > testBrick.y &&
        testBall.y < testBrick.y + brickHeight
    ) {
        testBrick.status = 0; // Mark brick as hit
        testBall.dy = -testBall.dy; // Reverse ball direction
    }

    console.log("After collision:", testBall.dy);

    // Assertions
    if (testBrick.status === 0) {
        console.log("Test Passed: Brick was hit and removed.");
    } else {
        console.error("Test Failed: Brick was not hit or removed.");
    }

    if (testBall.dy === 4) {
        console.log("Test Passed: Ball reversed direction after hitting the brick.");
    } else {
        console.error("Test Failed: Ball did not reverse direction after hitting the brick.");
    }
}

//Smoke
function testGameInitialization() {
    try {
        resizeCanvas(); // Ensure canvas is resized
        draw(); // Start the game loop
        console.log("Smoke Test Passed: Game initialized and running without errors.");
    } catch (error) {
        console.error("Smoke Test Failed: Game initialization error -", error);
    }
}

function testPowerUpCollection() {
    // Setup
    paddleX = canvas.width / 2 - paddleWidth / 2; // Center the paddle
    const powerUp = { x: paddleX + 10, y: canvas.height - paddleHeight - 1, type: "extraLife" };
    powerUps.push(powerUp);


    // Simulate power-up collection
    collectPowerUps();


    // Assertions
    console.assert(lives === 4, "Test Passed: Extra life power-up collected successfully.");
    console.assert(powerUps.length === 0, "Test Passed: Power-up removed after collection.");
}


window.onload = function () {
    testPaddleAndBallCollision();
    testBrickCollision();
    testGameInitialization();
    testPowerUpCollection();
};

// Add <script src="{{ url_for('static', filename='brick_breaker_test.js') }}"></script> to the HTML file to test