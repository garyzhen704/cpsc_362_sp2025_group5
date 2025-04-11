document.addEventListener('DOMContentLoaded', () => {
    // Game elements
    const mazeElement = document.getElementById('maze');
    const levelElement = document.getElementById('level');
    const movesElement = document.getElementById('moves');
    const completionMessage = document.getElementById('completion-message');
    const completionMoves = document.getElementById('completion-moves');
    const nextLevelButton = document.getElementById('next-level');
    
    // Control buttons
    const upButton = document.getElementById('up');
    const downButton = document.getElementById('down');
    const leftButton = document.getElementById('left');
    const rightButton = document.getElementById('right');
    
    // Game state
    let maze = [];
    let playerPos = [0, 0];
    let endPos = [0, 0];
    let level = 1;
    let moves = 0;
    let completed = false;
    
    // Start a new game
    function startNewGame() {
        fetch('/maze/new-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            maze = data.maze;
            playerPos = data.player_pos;
            endPos = data.end_pos;
            level = data.level;
            moves = data.moves;
            completed = false;
            
            updateUI();
            renderMaze();
            completionMessage.style.display = 'none';
        })
        .catch(error => console.error('Error starting new game:', error));
    }
    
    // Move the player
    function movePlayer(direction) {
        if (completed) return;
        
        fetch('/maze/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ direction })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                playerPos = data.position;
                moves = data.moves;
                completed = data.completed;
                
                updateUI();
                renderMaze();
                
                if (completed) {
                    showCompletionMessage();
                }
            }
        })
        .catch(error => console.error(`Error moving ${direction}:`, error));
    }
    
    // Load next level
    function loadNextLevel() {
        fetch('/maze/next-level', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            maze = data.maze;
            playerPos = data.position;
            endPos = data.end_pos;
            level = data.level;
            moves = data.moves;
            completed = data.completed;
            
            updateUI();
            renderMaze();
            completionMessage.style.display = 'none';
        })
        .catch(error => console.error('Error loading next level:', error));
    }
    
    // Render the maze
    function renderMaze() {
        // Clear the maze
        mazeElement.innerHTML = '';
        
        // Render each cell
        for (let y = 0; y < maze.length; y++) {
            for (let x = 0; x < maze[y].length; x++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                
                if (maze[y][x] === 1) {
                    cell.classList.add('wall');
                } else {
                    cell.classList.add('path');
                }
                
                // Player position
                if (x === playerPos[0] && y === playerPos[1]) {
                    cell.classList.add('player');
                }
                
                // End position
                if (x === endPos[0] && y === endPos[1]) {
                    cell.classList.add('end');
                }
                
                mazeElement.appendChild(cell);
            }
        }
    }
    
    // Update UI elements
    function updateUI() {
        levelElement.textContent = `Level: ${level}`;
        movesElement.textContent = `Moves: ${moves}`;
    }
    
    // Show completion message
    function showCompletionMessage() {
        completionMoves.textContent = moves;
        completionMessage.style.display = 'block';
    }
    
    // Event listeners for controls
    upButton.addEventListener('click', () => movePlayer('up'));
    downButton.addEventListener('click', () => movePlayer('down'));
    leftButton.addEventListener('click', () => movePlayer('left'));
    rightButton.addEventListener('click', () => movePlayer('right'));
    nextLevelButton.addEventListener('click', loadNextLevel);
    
    // Keyboard controls
    document.addEventListener('keydown', (event) => {
        if (completed) return;
        
        switch (event.key) {
            case 'ArrowUp':
            case 'w':
                movePlayer('up');
                break;
            case 'ArrowDown':
            case 's':
                movePlayer('down');
                break;
            case 'ArrowLeft':
            case 'a':
                movePlayer('left');
                break;
            case 'ArrowRight':
            case 'd':
                movePlayer('right');
                break;
        }
    });
    
    // Start the game
    startNewGame();
});