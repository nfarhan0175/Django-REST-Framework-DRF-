async function loadCheckoutCart(){
    try{
        const cart = await ApiClient.get("carts/api/cart/");
        displayCheckoutSummary(cart);
    }
    catch(error){
        console.log(error);
    }
}

function displayCheckoutSummary(cart){
    const list = document.getElementById("checkoutSummaryList");
    const total = document.getElementById("checkoutTotals");
    list.innerHTML = "";
    if(cart.cart_products.length === 0){
        list.innerHTML = `
            <p>Your cart is empty.</p>
        `;
        total.innerHTML = "";
        return;
    }
    cart.cart_products.forEach(item=>{
        list.innerHTML += `
            <div class="d-flex justify-content-between mb-2">
                <span>${item.product_name} × ${item.quantity}</span>
                <span> ৳ ${item.subtotal} </span>
            </div>
        `;
    });
    total.innerHTML = `
        <hr>
        <h5>Total: ৳ ${cart.total_price}</h5>
    `;
}

async function createAddress(){
    const data = {
        full_name: document.getElementById("checkoutFullName").value,
        phone: document.getElementById("checkoutPhone").value,
        city: document.getElementById("checkoutCity").value,
        area: document.getElementById("checkoutArea").value,
        street: document.getElementById("checkoutAddress").value,
        postal_code: document.getElementById("checkoutPostalCode").value
    };
    const response = await ApiClient.post("carts/api/addresses/",data);
    return response.id;
}

async function placeOrder(addressId, paymentMethod){
    try{
        const response = await ApiClient.post(
            "orders/api/create/",
            {
                address: addressId,
                payment_method: paymentMethod
            }
        );
        if(paymentMethod === "COD"){
            alert("Order placed successfully");
            window.location.href = "/orders/order/";
        }
        if(paymentMethod === "SSLCOMMERZ"){
            // payment.js call
            startPayment(response.id);
        }
    }
    catch(error){
        console.log(error);
        alert(error.error || "Order creation failed");
    }
}

document.getElementById("checkoutForm")?.addEventListener("submit",async function(e){
    e.preventDefault();
    try{
        const paymentMethod = document.querySelector('input[name="paymentMethod"]:checked').value;
        let paymentType = paymentMethod;
        if(paymentMethod === "ONLINE"){
            paymentType = "SSLCOMMERZ";
        }
        const addressId = await createAddress();
        await placeOrder(addressId, paymentType);
    }
    catch(error){
       console.log(error);
    }
});

document.addEventListener("DOMContentLoaded",function(){loadCheckoutCart();});