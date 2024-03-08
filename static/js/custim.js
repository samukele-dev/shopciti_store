// custom.js

document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to Add to Cart buttons
    var addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(function(button) {
        button.addEventListener('click', addToCart);
    });
});

function addToCart(event) {
    var productId = event.target.dataset.productId;
    var url = '/add-to-cart/';

    // AJAX request to add product to cart
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Get CSRF token
            },
            body: JSON.stringify({ 'product_id': productId })
        })
        .then(function(response) {
            if (response.ok) {
                // Product added successfully
                alert('Product added to cart!');
            } else {
                // Error adding product to cart
                alert('Failed to add product to cart.');
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
        });
}

// Function to get CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}