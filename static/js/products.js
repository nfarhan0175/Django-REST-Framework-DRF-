/* =========================================
 product list relevant js file
========================================= */
async function loadCategories(){
    try{
        const categories = await ApiClient.get("products/api/categories/");
        const select = document.getElementById("categoryFilter");
        if(!select) return;
        categories.forEach(category=>{
            select.innerHTML += `
                <option value="${category.id}">
                    ${category.name}
                </option>
            `;
        });
    }
    catch(error){
        console.log("Category error:",error);
    }
}

// bring Product
async function getProducts() {
    try {
        const products = await ApiClient.get("products/api/products/");
        displayProducts(products);
    } catch (error) {
        console.error(error);
    }
}

// Display Products
function displayProducts(products) {
    const container = document.getElementById("productGrid");
    container.innerHTML = "";
    products.forEach(product => {
        container.innerHTML += createProductCard(product);
    });
}

// Product Card
function createProductCard(product){
    let image = "https://placehold.co/400x400?text=No+Image";
    if(product.images.length > 0){
        image = product.images[0].image;
    }
    let price = product.discount_price || product.price;
    let discountPrice = product.discount_price;
    // let price = product.discount_price ? product.discount_price : product.price;
    return `
    <div class="col-md-6 col-lg-4">
        <div class="card h-100">
            <img src="${image}" class="card-img-top" style="height:250px; object-fit:cover;">

            <div class="card-body">
                <h5 class="card-title">${product.name}</h5>

                ${
                    product.discount_price
                        ? `
                            <p class="mb-1 text-muted">
                                <del>৳ ${product.price}</del>
                            </p>
                            <p class="mb-2 text-danger fw-bold">
                                ৳ ${product.discount_price}
                            </p>
                        `
                        : `
                            <p class="mb-2 fw-bold">
                                ৳ ${product.price}
                            </p>
                        `
                }

                <a href="/products/product_detail/${product.id}/"
                class="btn btn-primary">
                    View Details
                </a>
            </div>
        </div>
    </div>
    `;
}

/* =========================================
 product detail relevant js file
========================================= */

// একটি Product আনা
async function getProduct(id) {
    try {
        const product = await ApiClient.get(`products/api/products/${id}/`);
        displayProduct(product);
    } catch (error) {
        console.error(error);
    }
}

// একটি Product Show করবে
function displayProduct(product){
    let image = "https://placehold.co/600x600";
    if(product.images.length){
        image = product.images[0].image;
    }
    document.getElementById("galleryMainImage").src = image;
    document.getElementById("detailName").textContent = product.name;
    document.getElementById("detailPrice").textContent = `৳ ${product.discount_price || product.price}`;
    document.getElementById("detailStock").textContent = product.stock > 0 ? "In Stock" : "Out of Stock";
    document.getElementById("detailDescription").textContent = product.description;
    document.getElementById("detailQuantity").value = 1;

    // একই category-এর product load
    if(product.category){
        getRelatedProducts(product.category, product.id);
    }
    document.getElementById("addToCartBtn").onclick = () => addToCart(product.id);
}

// Add To Cart
async function addToCart(productId){
    try{
        const quantity = parseInt(document.getElementById("detailQuantity").value);
        await ApiClient.post("carts/api/cart/add/",{
            product: productId,
            quantity: quantity 
        });
        alert("Product added to cart.");
    }
    catch(error){
        console.error(error);
        alert("Unable to add product.");
    }
}

// releted products
async function getRelatedProducts(categoryId, currentProductId){
    try{
        const products = await ApiClient.get(`products/api/products/?category=${categoryId}`);
        // বর্তমান product বাদ দাও
        const relatedProducts = products.filter(product => product.id !== currentProductId);
        displayRelatedProducts(relatedProducts);
    }catch(error){
        console.error(error);
    } 
}

function displayRelatedProducts(products){
    const container = document.getElementById("relatedGrid");
    if(!container) return;
    container.innerHTML = "";
    if(products.length === 0){
        container.innerHTML = `
            <div class="col-12">
                <p class="text-muted text-center">
                    No related products found.
                </p>
            </div>
        `;
        return;
    }
    products.slice(0, 4).forEach(product => {
        container.innerHTML += createProductCard(product);
    });
}

/* =========================================
   REVIEW SYSTEM
========================================= */
let selectedRating = 0;
async function loadReviews(productId){
    try{
        const response = await ApiClient.get(
            `products/api/reviews/?product=${productId}`
        );
        const reviewsList = document.getElementById("reviewsList");
        if(!reviewsList)
            return;     
        if(response.length === 0){
            reviewsList.innerHTML = `
                <p class="text-muted">
                    No reviews yet. Be the first to review!
                </p>
            `;
            return;
        }
        reviewsList.innerHTML = response.map(review=>{
            return `
            <div class="card mb-3 p-3 shadow-sm">
                <div class="d-flex justify-content-between">
                    <strong>
                        ${review.reviewer}
                    </strong>
                    <span class="text-warning">
                        ${
                            "★".repeat(review.rating)
                        }
                        ${
                            "☆".repeat(5-review.rating)
                        }
                    </span>
                </div>
                <p class="mt-2 mb-0">
                    ${review.comment}
                </p>
            </div>
            `;
        }).join("");
    }
    catch(error){
        console.log("Review load error:",error);
    }

}
 
function setupStarPicker(){
    const stars =document.querySelectorAll("#reviewStarPicker i");
    if(!stars.length)
        return;
    stars.forEach(star=>{
        star.addEventListener(
            "click",
            function(){selectedRating = parseInt(this.dataset.value);
                stars.forEach(s=>{
                    if(parseInt(s.dataset.value)<= selectedRating){
                        s.classList.add("active");
                    }
                    else{
                        s.classList.remove("active");
                    }
                });
            }
        );
    });
}

async function submitReview(event){
    event.preventDefault();
    const root = document.getElementById("productDetailRoot");
    const productId = root.dataset.productId;
    const comment =document.getElementById("reviewComment").value;
    if(selectedRating === 0){
        alert("Please select rating");
        return;
    }
    try{
        await ApiClient.post("products/api/reviews/",
            {
                product: productId,
                rating: selectedRating,
                comment: comment
            }
        );
        alert("Review submitted successfully");
        document.getElementById("reviewForm").reset();
        selectedRating = 0;
        document.querySelectorAll("#reviewStarPicker i")
        .forEach(star=>
            {
                star.classList.remove("active");
        });
        loadReviews(productId);
    }
    catch(error){
        console.log("Review submit error:",error);
        alert("Please login to submit review");
    }
}

/*=========================================
others common functions
========================================= */

// Quantity Stepper
function stepQuantity(value){
    const input = document.getElementById("detailQuantity");
    if(!input){
        return;
    }
    let quantity = parseInt(input.value) || 1;
    quantity += value;
    if(quantity < 1){
        quantity = 1;
    }
    input.value = quantity;
}

// Product List Filter + Search
async function fetchFilteredProducts(params = ""){
    try{
        const products = await ApiClient.get(`products/api/products/${params}`);
        displayProducts(products.results || products);
    }catch(error){
        console.log("Filter error:", error);
    }
}

function applyFilters(event){event.preventDefault();
    let params = [];

    const search = document.getElementById("filter-search").value;
    const ordering = document.getElementById("filter-ordering").value;
    const minPrice = document.getElementById("filter-min_price").value;
    const maxPrice = document.getElementById("filter-max_price").value;
    const category = document.getElementById("categoryFilter").value;

    if(search){ 
        params.push(`search=${encodeURIComponent(search)}`);
    }

    if(ordering){
        params.push(`ordering=${encodeURIComponent(ordering)}`);
    }

    if(minPrice){
        params.push(`min_price=${encodeURIComponent(minPrice)}`);
    }

    if(maxPrice){
        params.push(`max_price=${encodeURIComponent(maxPrice)}`);
    }

    if(category){
        params.push(`category=${encodeURIComponent(category)}`);
    }

    let query = params.length ? "?" + params.join("&") : "";
    fetchFilteredProducts(query);
}

function clearFilters(){
    document.getElementById("filtersForm").reset();
    fetchFilteredProducts("");
}

// call functions
document.addEventListener("DOMContentLoaded",function(){
    if(document.getElementById("productGrid")){
        getProducts();
        loadCategories();
        document.getElementById("filtersForm").addEventListener("submit", applyFilters);
        document.getElementById("clearFiltersBtn").addEventListener("click", clearFilters);
    }

    const detailRoot = document.getElementById("productDetailRoot");
    if(detailRoot){
        const productId = detailRoot.dataset.productId;
        getProduct(productId);
        loadReviews(productId);
        setupStarPicker();
        const reviewForm = document.getElementById("reviewForm");
        if(reviewForm)
            reviewForm.addEventListener("submit",submitReview);
    }  

    document.getElementById("filterForm").addEventListener("submit", applyFilters);
});