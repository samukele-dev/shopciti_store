document.getElementById("add-to-cart").addEventListener("click", function(event) {
    // Perform AJAX request to add item to cart
    fetch("{% url 'add_to_cart' %}", {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                    product_id: 1
                }) // Adjust product_id as needed
        })
        .then(response => {
            // Check if response is successful
            if (!response.ok) {
                throw new Error("Failed to add item to cart");
            }
            return response.json();
        })
        .then(data => {
            // Update the cart count display
            document.getElementById("quantity_text").textContent = data.cart_item_count;

            // Prevent the default behavior of the link after AJAX request is completed
            event.preventDefault();
        })
        .catch(error => {
            console.error("Error:", error);
        });
});