// board

let board;
let boardWidth = 360;
let boardHeight = 640;
let context;

// bird
// width/height ratio = 408/228 = 17/12
let birdWidth = 34;
let birdHeight = 24;
let birdX = boardWidth/8;
let birdY = boardHeight/2;
// let birdImg;
let birdImgs = [];
let birdImgsIndex = 0;

let bird = {
    x : birdX,
    y : birdY,
    width : birdWidth,
    height : birdHeight
}

// Pipes
// width/height ratio = 384/3072 = 1/8 
let pipeArray = [];
let pipeWidth = 64; 
let pipeHeight = 512;
let pipeX = boardWidth;
let pipeY = 0;

let topPipeImg;
let bottomPipeImg;

// Game Physics
let velocityX = -2; // pipes moving left
let velocityY = 0; // bird jump speed
let gravity = 0.2; 

let gameOver = false;
let score = 0;

let wingSound = new Audio("./sfx_wing.wav");
let hitSound = new Audio("./sfx_hit.wav")

window.onload = function(){
    board = document.getElementById("board");
    board.height = boardHeight;
    board.Width = boardWidth;
    context = board.getContext("2d");

    // context.fillStyle = "green";
    // context.fillRect(bird.x, bird.y, bird.width, bird.height);

    // load images
    // birdImg = new Image();
    // birdImg.src = "./flappybird.png";
    // birdImg.onload = function() {
    //     context.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height)
    // }

    // animations
    for (let i = 0; i < 4; i++){
        let birdImg = new Image();
        birdImg.src = `./flappybird${i}.png`;
        birdImgs.push(birdImg);
    }

    topPipeImg = new Image();
    topPipeImg.src = "./toppipe.png";

    bottomPipeImg = new Image();
    bottomPipeImg.src = "./bottompipe.png";


    requestAnimationFrame(update);
    setInterval(placePipes, 1500); // every 1.5 seconds
    setInterval(animateBird, 100);
    document.addEventListener("keydown", moveBird);
}

function update(){
    requestAnimationFrame(update);
    if(gameOver){
        return;
    }
    context.clearRect(0, 0, board.width, board.height);

    //bird
    velocityY += gravity;
    // bird.y += velocityY;
    bird.y = Math.max(bird.y + velocityY, 0); // apply gravity to current bird.y or limit the bird.y to top of the canvas
    // context.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);
    context.drawImage(birdImgs[birdImgsIndex], bird.x, bird.y, bird.width, bird.height);
    // birdImgsIndex++;
    // birdImgsIndex %= birdImgs.length;

    if(bird.y > board.height){
        gameOver = true;
    }

    //pipes
    for(let i = 0; i < pipeArray.length; i++){
        let pipe = pipeArray[i];
        pipe.x += velocityX;
        context.drawImage(pipe.img, pipe.x, pipe.y, pipe.width, pipe.height);

        if(!pipe.passed && bird.x > pipe.x + pipe.width){
            score += 0.5; // because there are two pipes
            pipe.passed = true;
        }

        if(detectCollision(bird, pipe)){
            hitSound.play();
            gameOver = true;
        }
    }

    // clear pipes (for memory issues)
    while(pipeArray.length > 0 && pipeArray[0].x < -pipeWidth){
        pipeArray.shift(); // removes first element from the array
    }

    // score
    context.fillStyle = "White";
    context.font = "45px sans-serif";
    context.fillText(score, 5, 45);

    if(gameOver){
        context.fillText("GAME OVER", 5, 90);
    }

}

function animateBird(){
    birdImgsIndex++;
    birdImgsIndex %= birdImgs.length;
}

function placePipes(){

    if (gameOver){
        return;
    }

    let randomPipeY = pipeY - pipeHeight/4 - Math.random()*(pipeHeight/2);
    let openingSpace = board.height/4;

    let topPipe = {
        img : topPipeImg,
        x : pipeX,
        y : randomPipeY,
        width : pipeWidth,
        height : pipeHeight,
        passed : false
    }

    pipeArray.push(topPipe);

    let bottomPipe = {
        img : bottomPipeImg,
        x : pipeX,
        y : randomPipeY + pipeHeight + openingSpace,
        width : pipeWidth,
        height : pipeHeight,
        passed : false
    }

    pipeArray.push(bottomPipe)
}

function moveBird(e) {
    if(e.code == "Space" || e.code == "ArrowUp" || e.code == "KeyX"){
        // jump
        wingSound.play();
        velocityY = -6;
    }

    //reset game
    if(gameOver){
        bird.y = birdY;
        pipeArray = [];
        score = 0;
        gameOver = false;
    }
}

function detectCollision(a,b){
    return a.x < b.x + b.width &&
            a.x + a.width > b.x &&
            a.y < b.y + b.height &&
            a.y + a.height > b.y;
    }