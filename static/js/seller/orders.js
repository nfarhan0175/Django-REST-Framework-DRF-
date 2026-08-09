async function getSellerOrders() {
    try {
        const orders = await ApiClient.get("orders/api/seller_orders/");
        displaySellerOrders(orders);
    } catch (error) {
        console.log("Seller orders error:", error);
        const container = document.getElementById("sellerOrdersList");
         container.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4">
                    Failed to load orders
                </td>
            </tr>
        `;
    }
}


function displaySellerOrders(orders) {
    const container = document.getElementById("sellerOrdersList");
    container.innerHTML = "";
    if (orders.length === 0) {
        container.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-5">
                    No orders found
                </td>
            </tr>
        `;
        return;
    }
    orders.forEach(order => {
        order.items.forEach(item => {
            container.innerHTML += `
                <tr>
                    <td>#${order.id}</td>
                    <td>${order.customer_name}</td>
                    <td>${item.product_name}</td>
                    <td>${new Date(order.created_at).toLocaleDateString()}</td>
                    <td>${item.quantity}</td>
                    <td>৳ ${item.subtotal}</td>
                    <td>${order.payment_method}</td>
                    <td><span class="badge bg-warning">${order.status}</span></td>
                    <td>
                    <button class="btn btn-sm btn-outline-secondary" onclick="" aria-label="Edit product">
                        Done <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteProduct(${order.id})" aria-label="Delete product">
                        Cancel <i class="bi bi-trash"></i>
                    </button>
                </td>
                </tr>
            `;
        });
    });
}

document.addEventListener("DOMContentLoaded", function () {
        if (document.getElementById("sellerOrdersList")) {
            getSellerOrders();
        }
    }
);