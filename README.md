# Marketplace FastAPI Project

This is a FastAPI-based marketplace project designed to provide an online marketplace with features like user registration, authentication, product management, and role-based access control, all powered by **Tortoise ORM** for database management.

## Features

- **User Registration and Login** with JWT tokens
- **Product Management** (CRUD operations for products)
- **Role-Based Access Control** to differentiate between admin and regular users
- **PostgreSQL Support** via Tortoise ORM
- **Secure Authentication** with password hashing and JWT-based token generation
- **API Documentation** auto-generated using FastAPI's built-in documentation at `/docs`
- **Docker Support** for easy setup with containers

## Requirements

- Python 3.9+
- FastAPI
- Tortoise ORM
- PostgreSQL
- Docker (Optional, but recommended for local development)

## Setup Instructions

### 1. Clone the Repository

Start by cloning this repository to your local machine:

```bash
git clone https://github.com/yourusername/marketplace.git
cd marketplace
