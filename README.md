# 🏨 Hotel Booking Platform API

A secure and database-driven **Hotel Booking REST API** built using **Python, FastAPI, MySQL, SQLAlchemy, JWT Authentication, Pydantic, and bcrypt**.

This project implements the backend functionality required for a basic hotel booking platform. Users can create accounts, authenticate using JWT, create and manage their own room listings, search and filter rooms, check room availability for specific dates, and create bookings.

The application also includes **booking conflict detection**, which prevents a room from being booked when an existing confirmed booking overlaps with the requested check-in and check-out dates.

---

## 📌 Overview

The Hotel Booking Platform API is designed as a RESTful backend application using FastAPI.

The application provides functionality for three main resources:

- **Users**
- **Rooms**
- **Bookings**

Users can register and log in securely. After authentication, they receive a JWT access token that can be used to access protected endpoints.

Authenticated users can create hotel room listings and are allowed to update or delete only the rooms they own.

Users can search for rooms using different filters such as:

- Location
- Room type
- Capacity
- Check-in date
- Check-out date

When dates are provided, the API checks existing confirmed bookings and excludes rooms that are already booked during the requested period.

Users can also create bookings for available rooms. Before creating a booking, the API checks whether the requested dates overlap with an existing confirmed booking.

---

# 🎯 Project Objectives

The main objectives of this project are:

- Build a REST API using FastAPI
- Implement user registration and login
- Implement JWT-based authentication
- Secure passwords using bcrypt hashing
- Connect FastAPI with MySQL
- Use SQLAlchemy ORM for database operations
- Implement CRUD operations for rooms
- Implement user ownership and authorization
- Implement room search and filtering
- Implement date-based room availability
- Implement room booking
- Prevent overlapping room bookings
- Validate request data using Pydantic
- Handle API errors using appropriate HTTP status codes
- Use environment variables for configuration
- Test and document APIs using Swagger/OpenAPI

---
# Folder Structure

hotel-booking-api/
│
├── .gitignore
├── main.py
├── auth.py
├── database.py
├── models.py
├── schemas.py
└── README.md

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Backend programming language |
| **FastAPI** | REST API framework |
| **Uvicorn** | ASGI server |
| **MySQL** | Relational database |
| **SQLAlchemy** | ORM for database operations |
| **Pydantic** | Request and response validation |
| **JWT** | Authentication |
| **python-jose** | JWT encoding and decoding |
| **Passlib** | Password hashing framework |
| **bcrypt** | Password hashing algorithm |
| **python-dotenv** | Environment variable management |
| **OAuth2PasswordBearer** | Bearer token authentication |
| **Swagger UI** | Interactive API documentation |

---

# 🏗️ Application Architecture

The application follows a REST API architecture.

```text
                     Client
                       │
                       ▼
                ┌──────────────┐
                │   FastAPI    │
                │   REST API   │
                └───────┬──────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
       Users          Rooms        Bookings
          │             │             │
          └─────────────┼─────────────┘
                        │
                        ▼
                   SQLAlchemy
                        │
                        ▼
                     MySQL
🧠 Key Backend Concepts Learned

This project provided practical experience with:

Python backend development
FastAPI
REST API design
Dependency injection
SQLAlchemy
MySQL
Database relationships
CRUD operations
JWT authentication
OAuth2 bearer authentication
Password hashing
bcrypt
Pydantic
Request validation
Response models
Query parameters
Search and filtering
Date validation
Booking business logic
Booking conflict detection
Ownership-based authorization
HTTP status codes
Environment variables
Swagger/OpenAPI

⭐ Project Highlights
🔐 Secure Authentication

Implemented JWT-based authentication with token expiration.

🔑 Password Protection

Implemented bcrypt password hashing and verification.

🗄️ MySQL Integration

Connected FastAPI with MySQL using SQLAlchemy and PyMySQL.

🏨 Room CRUD

Implemented room creation, retrieval, updating, and deletion.

👤 Ownership Authorization

Users can update and delete only their own room listings.

🔎 Room Search

Implemented search and filtering using location, room type, capacity, and booking dates.

📅 Availability Checking

The search API can exclude rooms that are already booked for the requested dates.

🚫 Booking Conflict Prevention

Implemented date-overlap validation to prevent double booking.

📋 User Booking History

Users can retrieve their own bookings.

✅ Input Validation

Used Pydantic to validate user, room, and booking data.

📚 What I Learned

Through this project, I learned how different backend components work together to create a real-world API.

I learned how to:

Build REST APIs using FastAPI
Create database models using SQLAlchemy
Connect Python applications to MySQL
Create and manage database sessions
Use Pydantic for data validation
Hash and verify passwords using bcrypt
Generate and validate JWT tokens
Protect API endpoints using dependencies
Implement user authorization
Restrict resources based on ownership
Build CRUD functionality
Implement search and filtering
Handle date-based availability
Detect overlapping bookings
Return meaningful HTTP errors
Manage application configuration using .env
Test APIs through Swagger UI

👩‍💻 Author

Harshini S

B.Tech Information Technology
