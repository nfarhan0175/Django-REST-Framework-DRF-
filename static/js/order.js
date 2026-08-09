async function getOrders(){
    try{
        const orders = await ApiClient.get("orders/api/orderlist/");
        displayOrders(orders);
    }
    catch(error){
        console.log(error);
    }
}

function displayOrders(orders){

    const container = document.getElementById("ordersList");

    container.innerHTML = "";

    if(orders.length === 0){
        container.innerHTML = `
            <div class="text-center py-5">
                <h4>No orders found</h4>
            </div>
        `;
        return;
    }

    orders.forEach(order=>{
        container.innerHTML += `
        <div class="card mb-3">
            <div class="card-body">
                <h5>Order #${order.id}</h5>
                <p>
                    Status:
                    <span class="badge bg-warning">
                        ${order.status}
                    </span>
                </p>
                <p>Total: ৳ ${order.total_price}</p>
                <p>
                    Date:
                    ${new Date(order.created_at).toLocaleDateString()}
                </p>
                <hr>
                <h6>Products:</h6>
                ${order.items.map(item=>`
                    <div>
                        ${item.product_name}
                        × ${item.quantity}
                        = ৳ ${item.subtotal}
                    </div>
                `).join("")}
            </div>
        </div>
        `;
    });
}


document.addEventListener("DOMContentLoaded",function(){
    if(document.getElementById("ordersList")){
        getOrders();
    }
});