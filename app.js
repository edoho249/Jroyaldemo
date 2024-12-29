


// List of words to cycle through
const words = ["Welcome to J-Royal", "Satisfy your Cravings", "...with excellence", "And don't forget..."
  ,"WE SERVE YOU!"
];
let currentWordIndex = 0; // Index to track the current word in the array
let currentText = ""; // Variable to store the current text being typed
let isDeleting = false; // Flag to track whether we're typing or deleting
let speed = 100; // Speed of typing/deleting
const typingTextElement = document.getElementById("typing-text"); // Element where text will appear

// Function to create the typing and deleting effect
function typeEffect() {
  const currentWord = words[currentWordIndex]; // Get the current word to type

  if (isDeleting) {
      // If we are deleting, remove one character at a time
      currentText = currentWord.substring(0, currentText.length - 1);
      typingTextElement.textContent = currentText;

      if (currentText === "") {
          isDeleting = false;
          currentWordIndex = (currentWordIndex + 1) % words.length; // Move to next word
      }
  } else {
      // If we are typing, add one character at a time
      currentText = currentWord.substring(0, currentText.length + 1);
      typingTextElement.textContent = currentText;

      if (currentText === currentWord) {
          isDeleting = true;
          setTimeout(typeEffect, 1000); // Pause before deleting
          return;
      }
  }

  setTimeout(typeEffect, speed);
}

// Start the typing effect
typeEffect();



// POP UP WHATSAPP
function showPopup(){

document.getElementById('popup').style.display = 'block';}

function closePopup(){

document.getElementById('popup').style.display = 'none';
}