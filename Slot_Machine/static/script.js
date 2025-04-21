document.addEventListener("DOMContentLoaded", function () {
  const balanceDisplay = document.getElementById("balanceDisplay");
  const betDisplay = document.getElementById("betDisplay");
  const payoutDisplay = document.getElementById("payoutDisplay");
  balanceDisplay.parentNode.insertBefore(payoutDisplay, balanceDisplay.nextSibling);

  const betButtons = document.querySelectorAll(".bet-button");
  const upButton = document.getElementById("upButton");
  const downButton = document.getElementById("downButton");
  const spinButton = document.getElementById("spinButton");
  const reels = [document.getElementById("reel1"), document.getElementById("reel2"), document.getElementById("reel3"), document.getElementById("reel4"), document.getElementById("reel5")];

  const gif = document.getElementById('edm-gif');
  const gifSrc = gif.dataset.gifSrc;
  const staticFrame = gif.dataset.staticFrame;
  const pauseButton = document.getElementById('pause');

  let isPaused = false;

  function toggleGif() {
    if (isPaused) {
      gif.src = gifSrc;
      pauseButton.innerHTML = "⏸️";
    } else {
      gif.src = staticFrame;
      pauseButton.innerHTML = "▶️";
    }
    isPaused = !isPaused; // Toggle the state
  }

  pauseButton.addEventListener("click", toggleGif);

  function playGif() {
    gif.src = gifSrc;
  }
  let balance = parseInt("{{ balance }}", 10) || 1000;
  let currentBet = parseInt("{{ current_bet }}", 10) || 0;

  function updateValues(newBalance, newBet) {
    balance = newBalance;
    currentBet = newBet;
    balanceDisplay.textContent = `Credit: $${balance}`;
    betDisplay.textContent = `Bet: $${currentBet}`;
  }

  function subtractBet(subtractBetBalance) {
    balance = subtractBetBalance;
    balanceDisplay.textContent = `Credit: $${balance}`;

  }

  const denominations = [1, 5, 21, 85, 200];
  let currentBetMultiplier = 0;

  function updateBetButtons() {
    betButtons.forEach(button => {
      const baseBet = parseFloat(button.dataset.bet, 10);
      button.textContent = `$${baseBet * denominations[currentBetMultiplier]}`;
    });
  }

  // Handle the up button (increase the multiplier by 2)
  upButton.addEventListener("click", function () {
    if (currentBetMultiplier < denominations.length - 1) {
      currentBetMultiplier++;
    }
    updateBetButtons();
  });

  // Handle the down button (decrease the multiplier by 2)
  downButton.addEventListener("click", function () {
    if (currentBetMultiplier > 0) {
      currentBetMultiplier--;
    }
    updateBetButtons();
  });

  // Handle bet button click
  betButtons.forEach(button => {
    button.addEventListener("click", async function () {
      const betAmount = parseFloat(this.dataset.bet, 10) * denominations[currentBetMultiplier];

      const response = await fetch("/place_bet", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bet_amount: betAmount })
      });

      const data = await response.json();
      if (data.success) {
        updateValues(data.balance, data.current_bet);
      } else {
        alert("Bet placement failed. Check your balance.");
      }
    });

    // Initial update of bet buttons on page load
    updateBetButtons();
  });

  function spinReel(reel, finalSymbols, duration = 3000) {
    const reelInner = reel.querySelector(".reel-inner");
    reelInner.innerHTML = ""; // Clear existing symbols

    // Create an array of spinning symbols (extend for a longer effect)
    let spinningSymbols = [];
    const possibleSymbols = ["🍒", "🍋", "🍉", "🍊", "🍓", "🔔", "💎", "🌟", "🎲"]; // Add more variety
    for (let i = 0; i < 30; i++) { // Adjust for a longer spin
      spinningSymbols.push(possibleSymbols[Math.floor(Math.random() * possibleSymbols.length)]);
    }

    // Add final symbols at the end to land on them
    spinningSymbols.unshift(...finalSymbols);

    // Populate the reel with spinning symbols
    spinningSymbols.forEach(symbol => {
      const slotItem = document.createElement("div");
      slotItem.classList.add("slot-item");
      slotItem.textContent = symbol;
      reelInner.appendChild(slotItem);
    });

    // Set initial position above the view
    reelInner.style.transition = "none";
    reelInner.style.top = `-${reelInner.scrollHeight}px`;

    // Animate spin (smooth transition over `duration` milliseconds)
    setTimeout(() => {
      reelInner.style.transition = `top ${duration / 1000}s cubic-bezier(0.25, 1, 0.5, 1)`;
      reelInner.style.top = "0px"; // Start the animation to the top
    }, 50);
  }


  // Trigger spins with delays
  spinButton.addEventListener("click", async function () {
    if (currentBet === 0) {
      alert("You must place a bet before spinning!");
      return;
    }

    const spinAudio = document.getElementById("spinAudio");
    spinAudio.volume = spinVolumeSlider.value;
    spinAudio.currentTime = 4.90;
    spinAudio.play();

    setTimeout(() => {
      spinAudio.pause();
    }, 7000);

    subtractBet(balance - currentBet);
    spinButton.disabled = true;

    const response = await fetch("/spin", { method: "POST" });
    const data = await response.json();

    reels.forEach((reel, index) => {
      setTimeout(() => {
        spinReel(reel, data.result[index], 3000 + index * 1000); // Longer spin with staggered delays
      }, index * 250);
    });

    // Update balance & payout after all reels stop
    setTimeout(() => {
      payoutDisplay.textContent = `Win: $${data.payout}`;

      updateValues(data.balance, currentBet);
      spinButton.disabled = false;
    }, 7000); // Wait for last reel to stop
  });

  const audio = document.getElementById('backgroundAudio');
  const volumeSlider = document.getElementById('volumeSlider');
  const effectsAudio = document.getElementById('spinAudio')
  const spinVolumeSlider = document.getElementById('spinVolumeSlider');

  // Set initial volumes
  audio.volume = volumeSlider.value;
  effectsAudio.volume = spinVolumeSlider.value;

  // Volume controls
  volumeSlider.addEventListener('input', () => {
    audio.volume = volumeSlider.value;
  });

  spinVolumeSlider.addEventListener('input', () => {
    effectsAudio.volume = spinVolumeSlider.value;
  });

  // First user interaction to enable autoplay
  document.body.addEventListener('click', function () {
    audio.muted = false;
    audio.play().catch(error => {
      console.log("Playback failed:", error);
    });
  }, { once: true });

  const settingsButton = document.getElementById('settings');
  const volumeControl = document.querySelector('.volume-control');

  // Toggle volume control visibility on settings button click
  settingsButton.addEventListener('click', (event) => {
    event.stopPropagation(); // Prevent event from bubbling to the window
    volumeControl.style.display = (volumeControl.style.display === 'block') ? 'none' : 'block';
  });

  // Prevent click inside volume control from closing it
  volumeControl.addEventListener('click', (event) => {
    event.stopPropagation();
  });

  // Hide volume control when clicking outside
  window.addEventListener('click', () => {
    volumeControl.style.display = 'none';
  });

  const pages = document.querySelectorAll('.rules-page');
  const nextButton = document.getElementById('nextPage');
  const prevButton = document.getElementById('prevPage');
  const closeButton = document.querySelector('.close-button');
  const infoPopup = document.getElementById('info');
  const infoButton = document.getElementById('infoButton');

  let currentPage = 0;

  function showPage(index) {
    pages.forEach((page, i) => {
      page.style.display = i === index ? 'block' : 'none';
    });

    // Disable buttons at bounds
    prevButton.disabled = index === 0;
    nextButton.disabled = index === pages.length - 1;
  }

  nextButton.addEventListener('click', () => {
    if (currentPage < pages.length - 1) {
      currentPage++;
      showPage(currentPage);
    }
  });

  prevButton.addEventListener('click', () => {
    if (currentPage > 0) {
      currentPage--;
      showPage(currentPage);
    }
  });

  closeButton.addEventListener('click', () => {
    infoPopup.style.display = 'none';
  });

  infoButton.addEventListener('click', () => {
    currentPage = 0;
    infoPopup.style.display = 'block';
    showPage(currentPage); // Refresh correct page when opening
  });

  window.addEventListener('click', (event) => {
    if (event.target === infoPopup) {
      infoPopup.style.display = 'none';
    }
  });

  // Show first page initially
  showPage(currentPage);
});

