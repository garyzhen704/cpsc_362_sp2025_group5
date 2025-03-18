document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-button');
    const hitButton = document.getElementById('hit-button');
    const standButton = document.getElementById('stand-button');
    const playerHandDiv = document.getElementById('player-hand');
    const dealerHandDiv = document.getElementById('dealer-hand');
    const playerValueP = document.getElementById('player-value');
    const dealerValueP = document.getElementById('dealer-value');
    const resultP = document.getElementById('result');

    let deck, playerHand, dealerHand;

    // Update the UI with the current game state
    const updateUI = (playerHand, dealerHand, playerValue, dealerValue, result) => {
        playerHandDiv.innerHTML = playerHand.map(card => `<img src="/static/cards/${card.rank}-of-${card.suit}.png" 
            alt="${card.rank} of ${card.suit}" class="card-image">`).join('');
        dealerHandDiv.innerHTML = dealerHand.map(card => card === 'hidden' ? `<img src="/static/cards/back.png" 
            alt="Hidden Card" class="card-image">` : `<img src="/static/cards/${card.rank}-of-${card.suit}.png" 
            alt="${card.rank} of ${card.suit}" class="card-image">`).join('');
        playerValueP.textContent = `Value: ${playerValue || 0}`;
        dealerValueP.textContent = `Value: ${dealerValue || 0}`;
        resultP.textContent = result || '';
    };

    // Start button
    const startGame = async () => {
        const response = await fetch('/start', { method: 'POST' });
        const data = await response.json();
        deck = data.deck;
        playerHand = data.player_hand;
        dealerHand = [data.dealer_hand[0], 'hidden'];
        updateUI(playerHand, dealerHand, 0, 0);
        hitButton.disabled = false;
        standButton.disabled = false;
    };

    // Hit button
    const hit = async () => {
        const response = await fetch('/hit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ deck, player_hand: playerHand })
        });
        const data = await response.json();
        deck = data.deck;
        playerHand = data.player_hand;
        updateUI(playerHand, dealerHand, data.player_value, 0);
        if (data.player_value > 21) {
            resultP.textContent = 'Bust! You lose.';
            hitButton.disabled = true;
            standButton.disabled = true;
        }
    };

    const stand = async () => {
        // Remove 'hidden' card before sending data to the server
        const dealerHandToSend = dealerHand.filter(card => card !== 'hidden');
        const response = await fetch('/stand', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ deck, player_hand: playerHand, dealer_hand: dealerHandToSend })
        });
        const data = await response.json();
        dealerHand = data.dealer_hand;
        updateUI(playerHand, dealerHand, data.player_value, data.dealer_value, data.result);
        hitButton.disabled = true;
        standButton.disabled = true;

    };

    startButton.addEventListener('click', startGame);
    hitButton.addEventListener('click', hit);
    standButton.addEventListener('click', stand);
});