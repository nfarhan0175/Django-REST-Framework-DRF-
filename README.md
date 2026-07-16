# Django E-Commerce REST API Backend

A backend-only e-commerce REST API built using **Django** and **Django REST Framework**.
The project provides a complete backend system for an e-commerce platform, including authentication, product management, shopping cart, order processing, payment integration, and notification management.

The APIs are designed to be consumed by web or mobile frontend applications.



## Features

## Authentication & User Management

* Custom User Model implementation
* JWT-based authentication using SimpleJWT
* User registration and login
* Access and refresh token support
* Logout with token blacklisting
* Customer and Seller role management
* User profile management
* Protected API endpoints

---

## Product Management

* Category management
* Product CRUD operations
* Product image upload
* Product reviews
* Seller-only product management
* Customer read-only access
* Stock management
* Discount and final price calculation

---

## Shopping Cart

* Automatic cart creation for users
* Add products to cart
* Update product quantity
* Remove cart items
* Calculate subtotal and total cart price

---

## Address Management

* Multiple user addresses
* Default address support
* Address CRUD operations
* Order delivery address management

---

## Order Management

* Create orders from cart items
* Convert cart products into order items
* Automatic stock reduction after purchase
* Clear cart after successful order creation
* Order history management

Order workflow:

```
Cart
 |
 ↓
Create Order
 |
 ↓
Create Order Items
 |
 ↓
Update Product Stock
 |
 ↓
Clear Cart
```

---

## Payment Integration

* Payment model implementation
* SSLCommerz payment gateway integration
* Transaction ID generation
* Payment status tracking

Supported payment methods:

* Cash On Delivery
* SSLCommerz

Payment statuses:

* Pending
* Success
* Failed
* Cancelled
* Refunded

Payment workflow:

```
Order
 |
 ↓
Create Payment
 |
 ↓
SSLCommerz Gateway
 |
 ↓
Payment Callback
 |
 ↓
Update Payment Status
```

---

## Notification System

* User notification management
* Notification listing
* Mark notification as read
* Unread notification count

Notification types:

* Order
* Account
* System

---

# Technologies Used

* Python
* Django
* Django REST Framework
* JWT Authentication (SimpleJWT)
* SQLite Database
* Pillow
* django-environ
* SSLCommerz API
* Thunder Client (API Testing)
* Git & GitHub

---

# Project Structure

```
ecommerce/

├── accounts/
├── products/
├── carts/
├── orders/
├── payments/
├── notifications/
├── ecommerce/
├── templates/
├── media/
├── manage.py
└── requirement.txt
```

---

# Architecture

The project follows a modular Django application structure:

```
API Request

     ↓

Views / ViewSets

     ↓

Serializers

     ↓

Services & Business Logic

     ↓

Models

     ↓

Database
```

---

# Security Features

* JWT Authentication
* Role-based permissions
* Seller authorization
* Review ownership validation
* User-specific cart access
* User-specific order access
* User-specific notification access
* Payment ownership validation

---

# Database Design

An ERD diagram is included in the repository as a reference for the database design process.

The final implementation has been extended with additional modules such as:

* Address Management
* Notification System

---

# API Testing

All API endpoints were tested using:

**Thunder Client (VS Code Extension)**

---

# Future Improvements

Possible future enhancements:

* Swagger/OpenAPI documentation
* Search and filtering
* Pagination
* Wishlist system
* Coupon and discount system
* Inventory alerts
* Seller dashboard
* Unit testing
* Docker support
* PostgreSQL migration
