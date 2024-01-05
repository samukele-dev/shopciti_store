// cart.js

$(document).ready(function() {
    // Add to Cart button click event
    $('.add-to-cart').on('click', function(event) {
        event.preventDefault();

        // Get the product ID from the button's data attribute or other means
        var product_id = $(this).data('product-id');

        // Make an AJAX request to the add_to_cart view
        $.ajax({
            type: 'POST',
            url: '/add_to_cart/' + product_id + '/',
            data: {},
            dataType: 'json',
            success: function(response) {
                // Update the cart sidebar with the received data
                updateCartSidebar(response);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });

    // Function to update the cart sidebar
    function updateCartSidebar(data) {
        // Update cart items in the sidebar
        $('#cart-sidebar .cart-items').empty();
        $.each(data.cart_items, function(index, item) {
            $('#cart-sidebar .cart-items').append('<div class="cart-item">' +
                '<p>' + item.name + ' x' + item.quantity + '</p>' +
                '<p>Price: R' + item.price.toFixed(2) + '</p>' +
                '<a href="#">Remove</a>' +
                '</div>');
        });

        // Open the cart sidebar
        $('#cart-sidebar').removeClass('closed');
    }
});

// cart.js

// Function to get the CSRF token from the cookie
$(document).ready(function() {
    // Add to Cart form submission event
    $('#add-to-cart-form').on('submit', function(event) {
        event.preventDefault();

        // Get the product ID from the button's data attribute or other means
        var product_id = $('.add-to-cart').data('product-id');

        // Get the CSRF token directly from the form
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

        // Make an AJAX request to the add_to_cart view
        $.ajax({
            type: 'POST',
            url: '/add_to_cart/' + product_id + '/',
            data: {},
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                // Include the CSRF token in the request headers
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function(response) {
                // Update the cart sidebar with the received data
                updateCartSidebar(response);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });
});


$(document).ready(function() {
    // Add to Cart button click event
    $('.add-to-cart').on('click', function(event) {
        event.preventDefault();

        // Get the product ID from the button's data attribute or other means
        var product_id = $(this).data('product-id');

        // Get the CSRF token
        var csrftoken = getCookie('csrftoken');

        // Make an AJAX request to the add_to_cart view
        // Make an AJAX request to the add_to_cart view
        $.ajax({
            type: 'POST',
            url: '/add_to_cart/' + product_id + '/',
            data: {},
            dataType: 'json',
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(response) {
                // Update the cart sidebar with the received data
                updateCartSidebar(response);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });

    });

    // Function to update the cart sidebar
    function updateCartSidebar(data) {
        console.log('Response:', data);

        // Update cart items in the sidebar
        $('#cart-sidebar .cart-items').empty();
        $.each(data.cart_items, function(index, item) {
            $('#cart-sidebar .cart-items').append('<div class="cart-item">' +
                '<p>' + item.name + ' x' + item.quantity + '</p>' +
                '<p>Price: R' + item.price.toFixed(2) + '</p>' +
                '<a href="#">Remove</a>' +
                '</div>');
        });

        $('#cart-sidebar .cart-footer p').text('Total: R' + data.total_price); // Change 'response' to 'data'

        // Open the cart sidebar
        $('#cart-sidebar').removeClass('closed');
    }

});