const API_BASE_URL = "/";
const AUTH_TOKEN_KEY = "access";

const ApiClient = {
    getHeaders() {
        const headers = {"Content-Type": "application/json"};
        const token = localStorage.getItem(AUTH_TOKEN_KEY);
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }
        return headers;
    },

    async get(url) {
        const response = await fetch(API_BASE_URL + url, {
            headers: this.getHeaders()
        });
        console.log("API URL:", API_BASE_URL + url);
        console.log("STATUS:", response.status);
        const data = await response.json();
        console.log("RESPONSE:", data);
        if (!response.ok) {
            throw new Error("API Error");
        }
        return data//await response.json();
    },

    async post(url, data) {
        console.log("API URL:", API_BASE_URL + url);
        const response = await fetch(API_BASE_URL + url, {
            method: "POST",
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!response.ok) {
            console.log(result);
            throw result;
        }
        return result;
    },

    async put(url, data) {
        const response = await fetch(API_BASE_URL + url, {
            method: "PUT",
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error("API Error");
        }
        return await response.json();
    },
    async patch(url, data) {
        const response = await fetch(API_BASE_URL + url, {
            method: "PATCH",
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error("API Error");
        }
        return await response.json();
    },
    async delete(url) {
        const response = await fetch(API_BASE_URL + url, {
            method: "DELETE",
            headers: this.getHeaders()
        });
        if (!response.ok) {
            throw new Error("API Error");
        }
        return true;
    },
    async upload(url, formData, method = "POST") {
        const token = localStorage.getItem(AUTH_TOKEN_KEY);
        const response = await fetch(
            API_BASE_URL + url,
            {
                method: method,
                headers: {Authorization: `Bearer ${token}`},
                body: formData
            }
        );
        const result = await response.json();
        if (!response.ok) {
            console.log("UPLOAD ERROR:", result);
            throw result;
        }
        return result;
    }
};