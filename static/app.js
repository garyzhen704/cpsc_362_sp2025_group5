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
      document.getElementById('start-button').style.display= 'none';
      document.getElementById('bust_message').remove();
      

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
          //deck: getDeck(),
      })
  })
  .then(response => response.json())
  .then(data => {
    console.log("Received data from server:", data);
      // Update player hand
      updateHand('player', data.player_hand);
      //updateHand('deck', data.deck);

      // Update player value
      document.getElementById('player-value').innerText = `Player Value: ${data.player_value}`;

      // Check if the player has busted
      if (data.player_value > 21) {
          document.getElementById('start-button').style.display= 'inline-block';
          const pElement_m = document.createElement('p');
          pElement_m.innerText = "Bust!!";
          pElement_m.style.color = 'red';  // Change text color to red
          pElement_m.style.fontSize = '30px';  // Change font size to 20px
          pElement_m.style.backgroundColor = 'yellow';  // Set background color to yellow
          pElement_m.style.position = 'absolute';  // Set background color to yellow
          pElement_m.style.top= '55%';  // Set background color to yellow
          pElement_m.style.left = '45%';  // Set background color to yellow
          pElement_m.style.margin = '0';
          
          pElement_m.style.textAlign = 'center';  
          pElement_m.setAttribute('id', 'bust_message')
          const parentDiv = document.getElementById('table');
          parentDiv.insertBefore(pElement_m, document.getElementById('player'));
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
          //deck: getDeck(),
      })
  })
  .then(response => response.json())
  .then(data => {
      // Update dealer hand
      updateHand('dealer', data.dealer_hand);
      //document.getElementById('dealer-value').innerText = `Dealer Value: ${data.dealer_value}`;
      
      // Display result
      document.getElementById('start-button').style.display= 'inline-block';
      const pElement_m = document.createElement('p');
      pElement_m.innerText = `Game Over! ${data.result}`;
      pElement_m.style.color = 'red';  // Change text color to red
      pElement_m.style.fontSize = '30px';  // Change font size to 20px
      pElement_m.style.backgroundColor = 'yellow';  
      pElement_m.style.position = 'absolute';  
      pElement_m.style.top= '55%';  
      pElement_m.style.left = '35%'; 
      pElement_m.style.margin = '0';
      
      pElement_m.style.textAlign = 'center';  
      pElement_m.setAttribute('id', 'bust_message')
      const parentDiv = document.getElementById('table');
      parentDiv.insertBefore(pElement_m, document.getElementById('player'));
      //alert(`Game Over! ${data.result}`);
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

function disableButtons() {
  document.getElementById('hit-button').disabled = true;
  document.getElementById('stand-button').disabled = true;
}
