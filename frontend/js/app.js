// List of words to cycle through
const words = [
  "Welcome to J-Royal",
  "Satisfy your Cravings",
  "...with excellence",
  "And don't forget...",
  "WE SERVE YOU!",
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
function showPopup() {
  document.getElementById("popup").style.display = "block";
}

function closePopup() {
  document.getElementById("popup").style.display = "none";
}

const carouselTrack = document.querySelector(".carousel-track");
const prevButton = document.querySelector(".prev-btn");
const nextButton = document.querySelector(".next-btn");
const images = document.querySelectorAll(".carousel-track img");

let currentIndex = 0;

// Get the width of the carousel container
function getContainerWidth() {
  return carouselTrack.offsetWidth;
}

function updateCarouselPosition() {
  const containerWidth = getContainerWidth();
  const moveDistance = containerWidth / 4; // Move 1/4th of the container width
  const translateX = -(currentIndex * moveDistance);
  carouselTrack.style.transition = "transform 0.5s ease-in-out";
  carouselTrack.style.transform = `translateX(${translateX}px)`;
}

// Reset to the first image after a specified delay
function resetToFirstImage(delay) {
  setTimeout(() => {
    currentIndex = 0;
    updateCarouselPosition();
  }, delay);
}

// Detect screen size and set the reset delay
function setResetDelay() {
  const isSmallDevice = window.innerWidth <= 768; // Define small devices as <= 768px
  const delay = isSmallDevice ? 20000 : 12000; // 20 seconds for small devices, 12 seconds for larger ones
  resetToFirstImage(delay);
}

// Move to the previous image
prevButton.addEventListener("click", () => {
  currentIndex--;
  if (currentIndex < 0) {
    currentIndex = images.length - 4; // Stop at the first image
  }
  updateCarouselPosition();
});

// Move to the next image
nextButton.addEventListener("click", () => {
  currentIndex++;
  if (currentIndex > images.length - 4) {
    currentIndex = 0; // Wrap back to the start
  }
  updateCarouselPosition();
});

// Auto-slide every 3 seconds
let autoSlideInterval = setInterval(() => {
  currentIndex++;
  if (currentIndex > images.length - 4) {
    currentIndex = 0; // Wrap back to the start
  }
  updateCarouselPosition();
}, 3000);

// Pause auto-slide on hover
carouselTrack.addEventListener("mouseenter", () =>
  clearInterval(autoSlideInterval)
);

// Resume auto-slide on mouse leave
carouselTrack.addEventListener("mouseleave", () => {
  autoSlideInterval = setInterval(() => {
    currentIndex++;
    if (currentIndex > images.length - 4) {
      currentIndex = 0;
    }
    updateCarouselPosition();
  }, 3000);
});

// Apply the reset delay on load
setResetDelay();

// Reapply the reset delay on window resize
window.addEventListener("resize", setResetDelay);

// Get the elements
const messageOverlay = document.getElementById("messageOverlay");
const closeMessage = document.getElementById("closeMessage");

// Show the popup after 5 seconds
setTimeout(() => {
  messageOverlay.style.display = "flex";
}, 5000);

// Close the popup when the close button is clicked
closeMessage.addEventListener("click", () => {
  messageOverlay.style.display = "none";
});
