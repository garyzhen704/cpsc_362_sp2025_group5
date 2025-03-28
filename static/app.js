// Add event listener for place bet button
document.getElementById('place-bet-button').addEventListener('click', function() {
  const betAmount = parseInt(document.getElementById('bet-amount').value);
  
  // Disable the button to prevent multiple clicks
  document.getElementById('place-bet-button').disabled = true;
  
  fetch('/place_bet', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      bet_amount: betAmount
    })
  })
  .then(response => response.json())
  .then(data => {
    // Update UI to reflect bet placement
    document.getElementById('balance').innerText = `Balance: $${data.balance}`;
    document.getElementById('current-bet').innerText = `Current Bet: $${data.current_bet}`;
    
    // Enable start button only if bet was successfully placed
    if (data.success) {
      document.getElementById('start-button').disabled = false;
      // Keep the place bet button disabled until the game is over
    } else {
      alert('Not enough balance to place bet!');
      // Re-enable the button if the bet was unsuccessful
      document.getElementById('place-bet-button').disabled = false;
    }
  });
});

// Add event listener for cancel bet button
document.getElementById('cancel-bet-button').addEventListener('click', function() {
  fetch('/cancel_bet', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }
  })
  .then(response => response.json())
  .then(data => {
    // Update UI to reflect bet cancellation
    document.getElementById('balance').innerText = `Balance: $${data.balance}`;
    document.getElementById('current-bet').innerText = `Current Bet: $${data.current_bet}`;
    document.getElementById('start-button').disabled = true;
    document.getElementById('place-bet-button').disabled = false;
  });
});

// Add event listener for reset balance button
document.getElementById('reset-balance-button').addEventListener('click', function() {
  fetch('/reset_balance', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }
  })
  .then(response => response.json())
  .then(data => {
    // Update UI to reflect balance reset
    document.getElementById('balance').innerText = `Balance: $${data.balance}`;
    document.getElementById('current-bet').innerText = `Current Bet: $${data.current_bet}`;
    document.getElementById('place-bet-button').disabled = false;
  });
});

document.getElementById('start-button').addEventListener('click', function () {
  fetch('/start', {
      method: 'POST',
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('start-button').innerText = `New Game`
    
      // Update player and dealer hands
      updateHand('player', data.player_hand);
      updateHand('dealer', data.dealer_hand);

      // Enable buttons
      document.getElementById('hit-button').disabled = false;
      document.getElementById('stand-button').disabled = false;
      document.getElementById('player-value').innerText = `Player Value: ${data.player_value}`;
      
      // Enable double down button if player has enough balance
      if (data.can_double_down) {
        document.getElementById('double-button').disabled = false;
      }
      
      // Disable place bet button during game
      document.getElementById('place-bet-button').disabled = true;
      
      try {
        document.getElementById('bust_message').remove();
      } catch (e) {
        // Element might not exist yet
      }
  });
});

document.getElementById('hit-button').addEventListener('click', function () {
  fetch('/hit', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          player_hand: getPlayerHand(),
          dealer_hand: getDealerHand(),
      })
  })
  .then(response => response.json())
  .then(data => {
      // Update player hand
      updateHand('player', data.player_hand);

      // Update player value
      document.getElementById('player-value').innerText = `Player Value: ${data.player_value}`;
      
      // Disable double down button after hit
      document.getElementById('double-button').disabled = true;
      
      // Check if the player has busted
      if (data.player_value > 21) {
          // Update balance after loss
          document.getElementById('balance').innerText = `Balance: $${data.balance}`;
          document.getElementById('current-bet').innerText = `Current Bet: $${data.current_bet}`;
          
          const pElement_m = document.createElement('p');
          pElement_m.innerText = "Bust!! Dealer wins!";
          pElement_m.style.color = 'red';
          pElement_m.style.fontSize = '30px';
          pElement_m.style.backgroundColor = 'yellow';
          pElement_m.style.position = 'absolute';
          pElement_m.style.top = '50%';
          pElement_m.style.left = '50%';
          pElement_m.style.transform = 'translate(-50%, -50%)';
          pElement_m.style.margin = '0';
          pElement_m.style.padding = '10px 20px';
          pElement_m.style.borderRadius = '10px';
          pElement_m.style.textAlign = 'center';  
          pElement_m.setAttribute('id', 'bust_message')
          const parentDiv = document.getElementById('table');
          parentDiv.appendChild(pElement_m);
          disableButtons();
      }
  });
});

document.getElementById('stand-button').addEventListener('click', function () {
  fetch('/stand', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          player_hand: getPlayerHand(),
          dealer_hand: getDealerHand(),
      })
  })
  .then(response => response.json())
  .then(data => {
      // Update dealer hand
      updateHand('dealer', data.dealer_hand);
      
      // Update balance after payout
      document.getElementById('balance').innerText = `Balance: $${data.balance}`;
      document.getElementById('current-bet').innerText = `Current Bet: $${data.current_bet}`;
      
      // Display result
      document.getElementById('start-button').style.display= 'inline-block';
      const pElement_m = document.createElement('p');
      pElement_m.innerText = `Game Over! ${data.result}`;
      pElement_m.style.color = 'red';
      pElement_m.style.fontSize = '30px';
      pElement_m.style.backgroundColor = 'yellow';
      pElement_m.style.position = 'absolute';
      pElement_m.style.top = '50%';
      pElement_m.style.left = '50%';
      pElement_m.style.transform = 'translate(-50%, -50%)';
      pElement_m.style.margin = '0';
      pElement_m.style.padding = '10px 20px';
      pElement_m.style.borderRadius = '10px';
      pElement_m.style.textAlign = 'center';  
      pElement_m.setAttribute('id', 'bust_message')
      const parentDiv = document.getElementById('table');
      parentDiv.appendChild(pElement_m);
      
      disableButtons();
  });
});

function getPlayerHand() {
  return Array.from(document.querySelectorAll('#player .card')).map(cardElement => ({
    rank: cardElement.dataset.rank,
    suit: cardElement.dataset.suit,
    is_face_down: cardElement.dataset.isFaceDown === 'true', // Convert string to boolean
  }));
}

function getDealerHand() {
  return Array.from(document.querySelectorAll('#dealer .card')).map(cardElement => ({
    rank: cardElement.dataset.rank,
    suit: cardElement.dataset.suit,
    is_face_down: cardElement.dataset.isFaceDown === 'true', // Convert string to boolean
  }));
}

//function getDeck() {
  //return Array.from(document.querySelectorAll('.deck .card')).map(cardElement => cardElement.dataset.card);
//}

function updateHand(player, hand) {
  const handDiv = document.getElementById(player);
  handDiv.innerHTML = ''; // Clear existing hand
  hand.forEach(card => {
      const cardElement = document.createElement('div');
      cardElement.classList.add('card');
      cardElement.dataset.rank = card.rank;
      cardElement.dataset.suit = card.suit;
      cardElement.dataset.isFaceDown = card.is_face_down;
      const cardImage = document.createElement('img')
      cardImage.src = '/static/' + card.image;
      cardImage.alt = `${card.rank} of ${card.suit}`;
      cardElement.appendChild(cardImage);
      handDiv.appendChild(cardElement);
  });
}

// Add event listener for double down button
document.getElementById('double-button').addEventListener('click', function() {
  // Check if double down button is disabled
  if (this.disabled) {
    // Create message that double down is not allowed after hit
    const pElement_m = document.createElement('p');
    pElement_m.innerText = "Cannot double down after hit!";
    pElement_m.style.color = 'red';
    pElement_m.style.fontSize = '30px';
    pElement_m.style.backgroundColor = 'yellow';
    pElement_m.style.position = 'absolute';
    pElement_m.style.top = '50%';
    pElement_m.style.left = '50%';
    pElement_m.style.transform = 'translate(-50%, -50%)';
    pElement_m.style.margin = '0';
    pElement_m.style.padding = '10px 20px';
    pElement_m.style.borderRadius = '10px';
    pElement_m.style.textAlign = 'center';
    pElement_m.setAttribute('id', 'double_down_message');
    
    const parentDiv = document.getElementById('table');
    parentDiv.appendChild(pElement_m);
    
    // Remove message after 2 seconds
    setTimeout(function() {
      try {
        document.getElementById('double_down_message').remove();
      } catch (e) {
        // Element might not exist
      }
    }, 2000);
    
    return;
  }
  
  fetch('/double_down', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      player_hand: getPlayerHand(),
      dealer_hand: getDealerHand(),
    })
  })
  .then(response => response.json())
  .then(data => {
    // Update player hand
    updateHand('player', data.player_hand);
    
    // Update balance and bet
    document.getElementById('balance').innerText = `Balance: $${data.balance}`;
    document.getElementById('current-bet').innerText = `Current Bet: $${data.current_bet}`;
    
    // Update player value
    document.getElementById('player-value').innerText = `Player Value: ${data.player_value}`;
    
    // Double down automatically stands, so process dealer play and result
    updateHand('dealer', data.dealer_hand);
    
    // Display result
    const pElement_m = document.createElement('p');
    pElement_m.innerText = `Game Over! ${data.result}`;
    pElement_m.style.color = 'red';
    pElement_m.style.fontSize = '30px';
    pElement_m.style.backgroundColor = 'yellow';
    pElement_m.style.position = 'absolute';
    pElement_m.style.top = '50%';
    pElement_m.style.left = '50%';
    pElement_m.style.transform = 'translate(-50%, -50%)';
    pElement_m.style.margin = '0';
    pElement_m.style.padding = '10px 20px';
    pElement_m.style.borderRadius = '10px';
    pElement_m.style.textAlign = 'center';
    pElement_m.setAttribute('id', 'bust_message');
    
    const parentDiv = document.getElementById('table');
    parentDiv.appendChild(pElement_m);
    
    disableButtons();
  });
});

function disableButtons() {
  document.getElementById('hit-button').disabled = true;
  document.getElementById('stand-button').disabled = true;
  document.getElementById('double-button').disabled = true;
  document.getElementById('start-button').disabled = true;
  document.getElementById('place-bet-button').disabled = false;
}
