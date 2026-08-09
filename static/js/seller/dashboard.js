async function loadDashboard() {
    try {
        const productsResponse = await ApiClient.get("products/api/seller/products/");
        const ordersResponse = await ApiClient.get("orders/api/seller_orders/");

        // Handle normal array or paginated response
        const products = productsResponse.results || productsResponse;
        const orders = ordersResponse.results || ordersResponse;

        // Total Products
        document.getElementById("totalProducts").textContent = products.length;
        const pendingOrders = orders.filter(order => order.status === "pending");
        document.getElementById("pendingOrders").textContent = pendingOrders.length;
        const completedOrders = orders.filter(order => order.status === "delivered");
        document.getElementById("completedOrders").textContent = completedOrders.length;
        const totalRevenue = orders.reduce((total, order) => {
                return total + Number(order.seller_total || 0 );
            }, 0
        );
        document.getElementById("totalRevenue").textContent =`৳ ${totalRevenue.toFixed(2)}`;

        displayRecentOrders(orders);
        displayLowStockProducts(products);
    } catch (error) {
        console.log("Dashboard loading error:", error);
    }
}


// =====================================
// Recent Orders
// =====================================

function displayRecentOrders(orders) {
    const container = document.getElementById("recentOrdersList");
    if (!container) {
        return;
    }
    container.innerHTML = "";
    if (orders.length === 0) {
        container.innerHTML = `
            <tr>
                <td colspan="6"
                    class="text-center text-muted py-4">
                    No recent orders yet.
                </td>
            </tr>
        `;
        return;
    }
    // Latest orders first
    const recentOrders = [...orders]
        .sort(
            (a, b) =>
                new Date(b.created_at) -
                new Date(a.created_at)
        )
        .slice(0, 5);
    recentOrders.forEach(order => {
        container.innerHTML += `
            <tr>
                <td class="fw-semibold"> #${order.id} </td>
                <td>${order.customer_name || "Customer"}</td>
                <td>${new Date( order.created_at).toLocaleDateString()}</td>
                <td>৳ ${Number(order.seller_total || 0).toFixed(2)}</td>
                <td>${getStatusBadge(order.status )}</td>
                <td class="text-end">
                    <a href="/seller/orders/${order.id}/" class="btn btn-sm btn-outline-secondary">
                        <i class="bi bi-eye"></i>
                    </a>
                </td>
            </tr>
        `;
    });
}

// =====================================
// Status Badge
// =====================================
function getStatusBadge(status) {
    if (status === "pending") {
        return `
            <span class="badge text-bg-warning">
                Pending
            </span>
        `;
    }
    if (status === "processing") {
        return `
            <span class="badge text-bg-info">
                Processing
            </span>
        `;
    }
    if (status === "shipped") {
        return `
            <span class="badge text-bg-primary">
                Shipped
            </span>
        `;
    }
    if (status === "delivered") {
        return `
            <span class="badge text-bg-success">
                Delivered
            </span>
        `;
    }
    if (status === "cancelled") {
        return `
            <span class="badge text-bg-danger">
                Cancelled
            </span>
        `;
    }
    return `<span class="badge text-bg-secondary">${status} </span> `;
}

// =====================================
// Low Stock Products
// =====================================

function displayLowStockProducts(products) {
    const container = document.getElementById("lowStockProducts");
    if (!container) {
        return;
    }
    container.innerHTML = "";
    const lowStock = products
        .filter(product => product.stock <= 5)
        .sort((a, b) => a.stock - b.stock)
        .slice(0, 5);
    if (lowStock.length === 0) {
        container.innerHTML = `
            <tr>
                <td colspan="3"
                    class="text-center text-muted py-4">
                    All products are well stocked.
                </td>
            </tr>
        `;
        return;
    }

    lowStock.forEach(product => {
        let image = "https://placehold.co/40x40";
        if (product.images &&product.images.length > 0 ) {
            image = product.images[0].image;
        }
        container.innerHTML += `
            <tr>
                <td class="d-flex align-items-center gap-2">
                    <img
                        src="${image}"
                        alt="${product.name}"
                        class="rounded"
                        style="
                            width:36px;
                            height:36px;
                            object-fit:cover;
                        "
                    >
                    <span>${product.name}</span>
                </td>
                <td>
                    <span class="badge text-bg-danger">
                        ${product.stock} left
                    </span>
                </td>
                <td class="text-end">
                    <a href="/seller/products/add/${product.id}/"
                        class="btn btn-sm btn-outline-secondary">
                        <i class="bi bi-pencil"></i>
                    </a>
                </td>
            </tr>
        `;
    });
}


document.addEventListener("DOMContentLoaded", function () {
        loadDashboard();
    }
);
