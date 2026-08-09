async function register(){
    const password = document.getElementById("registerPassword").value;
    const confirmPassword = document.getElementById("registerPassword2").value;
    if(password !== confirmPassword){
        alert("Passwords do not match");
        return;
    }
    try{
        await ApiClient.post("accounts/api/register/",
            {
                username: document.getElementById("registerUsername").value,
                email: document.getElementById("registerEmail").value,
                password: document.getElementById("registerPassword").value,
                role: "customer"
            }
        );
        alert("Registration successful");
        window.location="/accounts/login/";
    }
    catch(error){
        // alert("Registration failed: " + error.response.data.detail);
        console.log(error);
    }
} 

async function login(){
    try{
        const response = await ApiClient.post(
                "accounts/api/token/",
                {
                    email: document.getElementById("email").value,
                    password: document.getElementById("password").value
                }
            );
        localStorage.setItem("access", response.access);
        localStorage.setItem("refresh", response.refresh);
        localStorage.setItem("role", response.role);
        localStorage.setItem("username", document.getElementById("email").value);
        alert("Login Successful");
        if(response.role === "seller"){
            window.location="/seller/dashboard/";
        }else{
            window.location="/home/";
        }
    }
    catch(error){
        console.log(error);
    }
}

async function logout() {
    try {
        await ApiClient.post("accounts/api/logout/", {
            refresh: localStorage.getItem("refresh")
        });
    } catch (error) {
        console.error(error);
    }
    localStorage.clear();
    window.location="/accounts/login/";
}


function updateNavbar() {
    const token = localStorage.getItem("access");
    const role = localStorage.getItem("role");

    const guestElements = document.querySelectorAll(".guest-only");
    const authElements = document.querySelectorAll(".auth-only");
    const customerElements = document.querySelectorAll(".customer-only");
    const sellerElements = document.querySelectorAll(".seller-only");

    if (token) {
        // Hide guest elements
        guestElements.forEach(el => {el.style.display = "none";});
        // Show authenticated elements
        authElements.forEach(el => {el.style.display = "";});

        // Show/hide based on role
        if (role === "seller") {
            customerElements.forEach(el => {el.style.display = "none";});
            sellerElements.forEach(el => {el.style.display = "";});
        } else {
            customerElements.forEach(el => {el.style.display = "";});
            sellerElements.forEach(el => {el.style.display = "none";});
        }
        // Username
        const username = localStorage.getItem("username");
        const navUsername = document.querySelectorAll(".navUsername");
        if (username) { 
            navUsername.forEach(el => { el.innerText = username; }); 
        }
    } else {
        guestElements.forEach(el => {el.style.display = "";});
        authElements.forEach(el => {el.style.display = "none";});
    }
}


// form submit
document.getElementById("loginForm")?.addEventListener("submit", async function (e) {
    e.preventDefault();
    await login();
});
document.getElementById("registerForm")?.addEventListener("submit", async function (e) {
    e.preventDefault();
    await register();
});
document.querySelectorAll(".logoutBtn")?.forEach(function(btn) {
    btn.addEventListener("click", async function (e) {
        e.preventDefault();
        await logout();
    });
});
document.addEventListener("DOMContentLoaded", updateNavbar);

