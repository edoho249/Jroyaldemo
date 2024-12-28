// // Function to load the cart and update the order details
function loadOrder() {
  const savedCart = JSON.parse(localStorage.getItem('cart'));  // Retrieve cart data from localStorage
  const orderItemsContainer = document.getElementById('order-items');
  const orderTotal = document.getElementById('order-total');
  const amountInput = document.getElementById('amount');

  if (savedCart && savedCart.length > 0) {
      let total = 0;
      
      // Loop through each cart item and display it in the order items section
      savedCart.forEach(item => {
          const orderItem = document.createElement('div');
          orderItem.classList.add('order-item');
          orderItem.innerHTML = `${item.name} - ₦${item.price.toFixed(2)} x ${item.quantity}`;
          orderItemsContainer.appendChild(orderItem);
          total += item.price * item.quantity;  // Calculate the total amount
      });

      // Display the total amount in the order summary and the amount input
      orderTotal.textContent = total.toFixed(2);  // Update the order total
      amountInput.value = total.toFixed(2);  // Set the total as the default value in the Amount input field
  } else {
      orderItemsContainer.innerHTML = 'Your cart is empty.';
      orderTotal.textContent = '0.00';
      amountInput.value = '0.00';
  }
}

// Load the cart and update the UI when the Order Page loads
window.addEventListener('load', loadOrder);

// Paystack payment function
const paymentForm = document.getElementById('paymentForm');
paymentForm.addEventListener("submit", payWithPaystack, false);

function payWithPaystack(e) {
e.preventDefault(); // Prevent form submission

const amount = document.getElementById("amount").value * 100; // Get the value from the input and convert to kobo (multiply by 100)
const email = document.getElementById("email-address").value; // Get the email address

let handler = PaystackPop.setup({
  key: 'pk_test_2ebd9a2eac85c29624d6dbe788916d71faaf62eb', // Replace with your public key
  email: email,
  amount: amount, // Amount in kobo
  currency: 'NGN', // Currency to be used
  ref: ''+Math.floor((Math.random() * 1000000000) + 1), // Generate a random reference number
  onClose: function(){
    alert('Payment window closed.');
  },
  callback: function(response){
    let message = 'Payment complete! Reference: ' + response.reference;
    alert(message);
  }
});

handler.openIframe(); // Open the Paystack iframe for payment
}
