async function loadProducts() {
    const tbody = document.getElementById("productTableBody");
    if (!tbody) return;
    const query = document.getElementById("searchInput")?.value || "";
    tbody.innerHTML = `
        <tr>
            <td colspan="8" class="text-center text-muted py-4">
                <span class="spinner-border spinner-border-sm me-2"></span>
                Loading products...
            </td>
        </tr>
    `;
    try {
        let url = "products/api/seller/products/";
        if (query) { url += `?search=${encodeURIComponent(query)}`; }
        // console.log("Search URL:", url);
        const data = await ApiClient.get(url);
        const products = data.results ? data.results : data;
        renderProducts(products);
    } catch (error) {
        console.error(error);
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center text-danger py-4">
                    Failed to load products.
                </td>
            </tr>
        `;
    }
}

function renderProducts(products) {
    const tbody = document.getElementById("productTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";
    if (!products || products.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center">
                    No Products Found
                </td>
            </tr>
        `;
        return;
    }
    products.forEach(product => {
        tbody.innerHTML += `
            <tr>
                <td>${product.id}</td>
                <td>
                    ${
                        product.images && product.images.length > 0
                        ? `<img src="${product.images[0].image}" width="60" height="60">`
                        : "-"
                    }
                </td>
                <td>${product.name}</td>
                <td>${product.category_name || "-"}</td>
                <td>৳${product.price}</td>
                <td>৳${product.discount_price}</td>
                <td>${product.stock}</td>
                <td>
                    ${  product.stock>0
                            ? '<span class="badge bg-success">Available</span>'
                            : '<span class="badge bg-danger">Out of Stock</span>'}
                </td>
                <td>
                    <button class="btn btn-sm btn-outline-secondary" 
                        onclick="editProduct(${product.id})" aria-label="Edit product">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" 
                        onclick="deleteProduct(${product.id})" aria-label="Delete product">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    });
}

// Delete / Edit                                                           
async function deleteProduct(id) {
    const confirmed = confirm("Delete this product?");
    if (!confirmed) return;
    try {
        await ApiClient.delete(`products/api/seller/products/${id}/`);
        loadProducts();
    } catch (error) {
        console.error(error);
        alert("Delete failed.");
    }
}

function editProduct(id) {
    window.location.href = `/seller/products/add/${id}/`;
}

// Search form                                                            
function initSearchForm() { 
    const form = document.querySelector("#productSearchForm"); 
    const input = document.getElementById("searchInput"); 
    if (!form || !input) return; 
    form.addEventListener("submit", (e) => { e.preventDefault(); 
        loadProducts(); 
    }); 
}

document.addEventListener("DOMContentLoaded", () => {
  initSearchForm();
  loadProducts();
});