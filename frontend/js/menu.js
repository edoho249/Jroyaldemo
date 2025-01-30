function filterCategory(category) {
  const allItems = document.querySelectorAll(".boxx");

  // If 'All' is selected, show all items
  if (category === "all") {
    allItems.forEach((item) => {
      item.style.display = "block";
    });
  } else {
    // Hide items that do not match the selected category
    allItems.forEach((item) => {
      const itemCategory = item.getAttribute("data-category");
      if (itemCategory === category) {
        item.style.display = "block"; // Show item
      } else {
        item.style.display = "none"; // Hide item
      }
    });
  }
}

// Global cart array to hold the items
let cart = [];

// Function to add item to the cart
function addToCart(event) {
  const button = event.target;
  const name = button.getAttribute("data-name");
  const price = parseFloat(button.getAttribute("data-price"));

  // Check if the item is already in the cart
  const existingItemIndex = cart.findIndex((item) => item.name === name);

  if (existingItemIndex !== -1) {
    // If item already exists, increase the quantity
    cart[existingItemIndex].quantity++;
  } else {
    // If item does not exist, add it to the cart with quantity 1
    cart.push({
      name: name,
      price: price,
      quantity: 1,
    });
  }

  // Show success message
  showSuccessMessage();

  // Update the cart UI
  updateCartUI();
}

// Function to update the cart UI (show cart items and total)
function updateCartUI() {
  const cartContainer = document.getElementById("cart-items");
  const cartCount = document.querySelector(".cart-count");
  const cartTotal = document.getElementById("cart-total");

  // Clear previous cart content
  cartContainer.innerHTML = "";

  let total = 0;
  cart.forEach((item) => {
    // Create an item element for each cart item
    const cartItem = document.createElement("div");
    cartItem.classList.add("cart-item");
    cartItem.innerHTML = `${item.name} - ₦${item.price.toFixed(2)} x ${
      item.quantity
    }`;
    cartContainer.appendChild(cartItem);
    total += item.price * item.quantity;
  });

  // Display total cart price
  cartTotal.textContent = `Total: ₦${total.toFixed(2)}`;

  // Update cart item count
  cartCount.textContent = `(${cart.length})`;

  // Optionally save the cart in localStorage
  saveCart();
}

// Function to initialize cart from localStorage (optional)
function loadCart() {
  const savedCart = JSON.parse(localStorage.getItem("cart"));
  if (savedCart) {
    cart = savedCart;
    updateCartUI();
  }
}

// Function to save cart to localStorage (optional)
function saveCart() {
  localStorage.setItem("cart", JSON.stringify(cart));
}

// Function to clear the cart
function clearCart() {
  cart = [];
  updateCartUI();
}

// Function to show success message
function showSuccessMessage() {
  const successMessage = document.getElementById("success-message");
  successMessage.style.display = "block";

  // Hide the message after 2 seconds
  setTimeout(() => {
    successMessage.style.display = "none";
  }, 2000);
}

// Function to open the cart sidebar
function openCart() {
  const cartContainer = document.getElementById("cart-container");
  cartContainer.style.display = "block";
}

// Function to close the cart sidebar
function closeCart() {
  const cartContainer = document.getElementById("cart-container");
  cartContainer.style.display = "none";
}

// Event listener to handle "Add to Cart" button clicks
document.querySelectorAll(".add-to-cart-btn").forEach((button) => {
  button.addEventListener("click", addToCart);
});

// Event listener for the cart icon to open the cart
document.getElementById("cart-icon").addEventListener("click", openCart);

// Load the cart on page load
window.addEventListener("load", loadCart);

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
