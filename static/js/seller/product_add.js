let productId = null;
function getProductId() {
    const parts = window.location.pathname.split("/");
    const addIndex = parts.indexOf("add");
    if (addIndex !== -1 && parts[addIndex + 1]) {
        return parts[addIndex + 1];
    }
    return null;
}

async function loadCategories(){
    try{
        const categories = await ApiClient.get("products/api/categories/");
        const select = document.getElementById("category");
        const data = categories.results ? categories.results : categories;
        data.forEach(category => {
            select.innerHTML += `
                <option value="${category.id}">
                    ${category.name}
                </option>`;
        });
    }
    catch(error){
        console.error(error);
    }
}

// Form submit
function initProductForm() {
    const form = document.getElementById("productForm");
    console.log(form);
    if (!form) return;
    form.addEventListener("submit", async function(e){e.preventDefault();
        const formData = new FormData();
        formData.append("name", document.getElementById("name").value);
        formData.append("description", document.getElementById("description").value);
        formData.append("category", document.getElementById("category").value);
        formData.append("price", document.getElementById("price").value);
        formData.append("discount_price", document.getElementById("discount_price").value);
        formData.append("stock", document.getElementById("stock").value);
        formData.append("is_active", document.getElementById("is_active").checked);
        try {
            if(productId){
                await updateProduct(productId, formData);
                await uploadProductImage(productId);
                alert("Product updated successfully.");
            }
            else{
                const product = await createProduct(formData);
                await uploadProductImage(product.id);
                alert("Product added successfully.");
            }
            window.location.href="/seller/products/";
        }
        catch(error){
            console.error(error);
            alert("Something went wrong.");
        }
    });
}

// Create Product
async function createProduct(formData){
    return await ApiClient.upload("products/api/seller/products/",formData);
}

// Upload Product Image
async function uploadProductImage(productId) {
    const imageInput = document.getElementById("image");
    if (!imageInput) {
        console.log("Image input not found.");
        return;
    }
    if (!imageInput.files.length) {
        console.log("No image selected.");
        return;
    }
    const imageFile = imageInput.files[0];
    const imageFormData = new FormData();
    imageFormData.append("product",productId);
    imageFormData.append("image",imageFile);
    const result = await ApiClient.upload("products/api/product-images/",imageFormData);
    console.log("Uploaded image:", result);
    return result;
}

// Update Product
async function updateProduct(id, formData){
    return await ApiClient.upload(`products/api/seller/products/${id}/`,formData,"PATCH");
}

// Edit page load data
async function loadProduct(id){
    try{
        const product = await ApiClient.get(`products/api/seller/products/${id}/`);
        document.getElementById("name").value = product.name;
        document.getElementById("description").value = product.description;
        document.getElementById("category").value = product.category;
        document.getElementById("price").value = product.price;
        document.getElementById("discount_price").value = product.discount_price || "";
        document.getElementById("stock").value = product.stock;
        document.getElementById("is_active").checked = product.is_active;
    }
    catch(error){
        console.error(error);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    await loadCategories();
    productId = getProductId();
    if(productId){
        await loadProduct(productId);
    }
    initProductForm();
});