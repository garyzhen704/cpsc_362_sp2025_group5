document.addEventListener("DOMContentLoaded", function () {
  const titleElement = document.querySelector(".site-header h1");
  const titleText = titleElement.textContent;
  titleElement.textContent = ""; // Clear the text initially

  let i = 0;
  const speed = 100; // Speed of typing (in milliseconds)

  function typeWriter() {
    if (i < titleText.length) {
      titleElement.textContent += titleText.charAt(i);
      i++;
      setTimeout(typeWriter, speed);
    }
  }

  typeWriter(); // Start the typing effect
});

window.addEventListener('focus', function() {
  document.body.style.cursor = 'url("/images/cursor.cur") 0 0, auto';
});

// Listen for when the window loses focus (e.g., user clicks outside)
window.addEventListener('blur', function() {
  document.body.style.cursor = 'auto'; // Reset to default when focus is lost
});
