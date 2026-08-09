async function getCart(){
    try{
        const cart = await ApiClient.get("carts/api/cart/");
        displayCart(cart);
    }
    catch(error){
        console.log(error);
    }
}

function displayCart(cart){
     if (cart.cart_products.length === 0) {
        container.innerHTML = `
            <div class="text-center py-5">
                <h4>Your cart is empty</h4>
            </div>
        `;
        document.getElementById("cartTotal").innerHTML = "Total: ৳ 0";
        return;
    }
    const container = document.getElementById("cartItems");
    container.innerHTML = "";
    cart.cart_products.forEach(item => {
        container.innerHTML += `
            <div class="card mb-3">
                <div class="card-body d-flex justify-content-between align-items-center">
                    <div>
                        <h5>${item.product_name}</h5>
                        <p>Price : ৳ ${item.product_price}</p>
                        <div class="d-flex align-items-center gap-2">
                            <button class="btn btn-outline-secondary btn-sm"
                                onclick="updateQuantity(${item.id}, ${item.quantity-1})">-</button>
                            <span>${item.quantity}</span>
                            <button class="btn btn-outline-secondary btn-sm"
                                onclick="updateQuantity(${item.id}, ${item.quantity+1})">+</button>
                        </div>
                    </div>

                    <div class="text-end">
                        <h5>৳ ${item.subtotal}</h5>
                        <button
                            class="btn btn-danger btn-sm"
                            onclick="removeCartItem(${item.id})">
                            Remove
                        </button>
                    </div>
                </div>
            </div>
            `;
    });
    document.getElementById("cartTotal").innerHTML =
        `Total: ৳ ${cart.total_price}`;
}

async function removeCartItem(id){
    try{
        await ApiClient.delete(`carts/api/cart/item/${id}/remove/`);
        getCart();
    }
    catch(error){
        console.log(error);
    }
}
async function updateQuantity(id, quantity){
    if(quantity < 1){
        await removeCartItem(id);
        return;
    }
    try{
        await ApiClient.patch(
            `carts/api/cart/item/${id}/`,
            {
                quantity: quantity
            }
        );
        getCart();
    }
    catch(error){
        console.log(error);
        alert(error.error || "Failed to update quantity");
    }
}

// call function
document.addEventListener("DOMContentLoaded", function(){
    if(document.getElementById("cartItems")){
        getCart();
    }
});