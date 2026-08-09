const API_URL = "/accounts/api/profile/";
const token = localStorage.getItem("access");

// ---------------------- Elements ----------------------
const profileForm = document.getElementById("profileForm");

const editBtn = document.getElementById("editProfileBtn");
const cancelBtn = document.getElementById("cancelEditBtn");
const saveWrap = document.getElementById("saveButtonWrap");

const avatar = document.getElementById("profileAvatar");
const displayName = document.getElementById("profileDisplayName");

const username = document.getElementById("profileUsername");
const email = document.getElementById("profileEmail");
const firstName = document.getElementById("profileFirstName");
const lastName = document.getElementById("profileLastName");
const phone = document.getElementById("profilePhone");

// HTML change করলে এগুলো কাজ করবে
const city = document.getElementById("profileCity");
const state = document.getElementById("profileState");
const country = document.getElementById("profileCountry");

const picture = document.getElementById("profilePicture");

// -----------------------------------------------------

if (!token) {
    window.location.href = "/accounts/login/";
}

// enable / disable inputs
function toggleEdit(enable) {
    firstName.disabled = !enable;
    lastName.disabled = !enable;
    phone.disabled = !enable;

    if (city) city.disabled = !enable;
    if (state) state.disabled = !enable;
    if (country) country.disabled = !enable;

    if (picture)
        picture.classList.toggle("d-none", !enable);

    saveWrap.classList.toggle("d-none", !enable);
    editBtn.classList.toggle("d-none", enable);
}


// load profile
async function loadProfile() {
    try {
        const response = await fetch(API_URL, {
            headers: {Authorization: `Bearer ${token}`}
        });
        if (!response.ok) {
            throw new Error("Failed to load profile");
        }
        const data = await response.json();
        username.value = data.username;
        email.value = data.email;
        firstName.value = data.first_name || "";
        lastName.value = data.last_name || "";
        phone.value = data.phone || "";

        if (city) city.value = data.city || "";
        if (state) state.value = data.state || "";
        if (country) country.value = data.country || "";

        // sidebar name
        displayName.textContent =
            `${data.first_name || ""} ${data.last_name || ""}`.trim()
            || data.username;

        // avatar
        if (data.profile_picture) {
            avatar.innerHTML = `
                <img
                    src="${data.profile_picture}"
                    class="w-100 h-100 rounded-circle"
                    style="object-fit:cover;">
            `;
        } else {
            avatar.innerHTML = data.username.charAt(0).toUpperCase();
        }
    }
    catch (err) {
        console.error(err);
        alert("Unable to load profile.");
    }
}

loadProfile();

// edit button
editBtn.addEventListener("click", () => {
    toggleEdit(true);
});

// cancel
cancelBtn.addEventListener("click", () => {
    toggleEdit(false);
    loadProfile();
});

// save profile
profileForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const formData = new FormData();
        formData.append("first_name", firstName.value);
        formData.append("last_name", lastName.value);
        formData.append("phone", phone.value);
        if (city)
            formData.append("city", city.value);
        if (state)
            formData.append("state", state.value);
        if (country)
            formData.append("country", country.value);
        if (picture && picture.files.length > 0) {
            formData.append(
                "profile_picture",
                picture.files[0]
            );
        }
        const response = await fetch(API_URL, {
            method: "PATCH",
            headers: {
                Authorization: `Bearer ${token}`
            },
            body: formData
        });
        if (!response.ok) {
            throw new Error("Update failed");
        }
        const data = await response.json();
        alert("Profile updated successfully.");
        toggleEdit(false);
        loadProfile();
    }
    catch (err) {
        console.error(err);
        alert("Failed to update profile.");
    }
});