



const carouselTrack = document.querySelector('.carousel-track');
const prevButton = document.querySelector('.prev-btn');
const nextButton = document.querySelector('.next-btn');
const images = document.querySelectorAll('.carousel-track img');

let currentIndex = 0;

function updateCarouselPosition() {
  const translateX = -(currentIndex * (100 / 4)); // Move one image's width (1/4 of the container)
  carouselTrack.style.transform = `translateX(${translateX}%)`;
}

// Move to the previous image
prevButton.addEventListener('click', () => {
  currentIndex--;
  if (currentIndex < 0) {
    currentIndex = images.length - 4; // Stop at the first image
  }
  updateCarouselPosition();
});

// Move to the next image
nextButton.addEventListener('click', () => {
  currentIndex++;
  if (currentIndex > images.length - 4) {
    currentIndex = 0; // Wrap back to the start
  }
  updateCarouselPosition();
});

// Auto-slide every 3 seconds
let autoSlideInterval = setInterval(() => {
  nextButton.click(); // Trigger the next button click
}, 3000);

// Pause auto-slide on hover
carouselTrack.addEventListener('mouseenter', () => clearInterval(autoSlideInterval));

// Resume auto-slide on mouse leave
carouselTrack.addEventListener('mouseleave', () => {
  autoSlideInterval = setInterval(() => {
    nextButton.click();
  }, 3000);
});