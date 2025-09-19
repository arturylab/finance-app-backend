# Finance App Backend

## Description

This is the backend API for a personal finance application built with Django and Django Rest Framework. It provides a robust set of endpoints to manage users, financial accounts, transactions, categories, and transfers. It features JWT-based authentication for secure access.

The application is designed to automatically update account balances in response to transactions and transfers, ensuring data integrity.

## Live Demo

You can view a live demo of the application here:
[https://finance-app.arturylab.dev/](https://finance-app.arturylab.dev/)

## Frontend

You can view a live frontend repositorie here:
[https://github.com/arturylab/finance-app-frontend](https://github.com/arturylab/finance-app-frontend)

-----

## Features

  * **JWT Authentication:** Secure user registration and token-based authentication (access and refresh tokens).
  * **CRUD Operations:** Full Create, Read, Update, and Delete functionality for all financial models.
  * **User Management:** Endpoints for user registration and profile management.
  * **Financial Models:** Includes Accounts, Categories (Income/Expense), Transactions, and Transfers between accounts.
  * **Automatic Balance Updates:** Account balances are automatically adjusted when transactions or transfers are created, updated, or deleted, thanks to Django signals.
  * **Default Categories:** New users are automatically provided with a default set of income and expense categories to get started quickly.
  * **Filtering and Searching:** API endpoints support searching and filtering for easier data retrieval.

-----

## API Endpoints

The base URL for all endpoints is `/api/`.

### Authentication

| Method | Endpoint                    | Description                  |
| :----- | :-------------------------- | :--------------------------- |
| `POST` | `/register/`                | Register a new user.         |
| `POST` | `/auth/token/`              | Obtain JWT access and refresh tokens. |
| `POST` | `/auth/token/refresh/`      | Refresh an access token.     |

### Users

| Method  | Endpoint               | Description                  |
| :------ | :--------------------- | :--------------------------- |
| `GET`   | `/users/me/`           | Get the current user's profile. |
| `PATCH` | `/users/me/profile/`   | Update the current user's profile. |

### Accounts

| Method      | Endpoint               | Description                  |
| :---------- | :--------------------- | :--------------------------- |
| `GET`       | `/accounts/`           | List all of a user's accounts. |
| `POST`      | `/accounts/`           | Create a new account.        |
| `GET`       | `/accounts/{id}/`      | Retrieve a specific account. |
| `PUT/PATCH` | `/accounts/{id}/`      | Update a specific account.   |
| `DELETE`    | `/accounts/{id}/`      | Delete a specific account.   |

### Categories

| Method      | Endpoint               | Description                   |
| :---------- | :--------------------- | :---------------------------- |
| `GET`       | `/categories/`         | List all of a user's categories. |
| `POST`      | `/categories/`         | Create a new category.        |
| `GET`       | `/categories/{id}/`    | Retrieve a specific category. |
| `PUT/PATCH` | `/categories/{id}/`    | Update a specific category.   |
| `DELETE`    | `/categories/{id}/`    | Delete a specific category.   |

### Transactions

| Method      | Endpoint                 | Description                      |
| :---------- | :----------------------- | :------------------------------- |
| `GET`       | `/transactions/`         | List all of a user's transactions. |
| `POST`      | `/transactions/`         | Create a new transaction.        |
| `GET`       | `/transactions/{id}/`    | Retrieve a specific transaction. |
| `PUT/PATCH` | `/transactions/{id}/`    | Update a specific transaction.   |
| `DELETE`    | `/transactions/{id}/`    | Delete a specific transaction.   |

### Transfers

| Method      | Endpoint              | Description                   |
| :---------- | :-------------------- | :---------------------------- |
| `GET`       | `/transfers/`         | List all of a user's transfers. |
| `POST`      | `/transfers/`         | Create a new transfer.        |
| `GET`       | `/transfers/{id}/`    | Retrieve a specific transfer. |
| `PUT/PATCH` | `/transfers/{id}/`    | Update a specific transfer.   |
| `DELETE`    | `/transfers/{id}/`    | Delete a specific transfer.   |

-----

## Getting Started

### Prerequisites

  * Python (v3.9 or later)
  * pip (Python package installer)
  * A virtual environment tool (e.g., `venv`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/arturylab/finance-app-backend.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd finance-app-backend
    ```
3.  **Create and activate a virtual environment:**
    ```bash
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Create a `.env` file** in the root directory and add the following environment variables:
    ```env
    SECRET_KEY='your-secret-key-here'
    DEBUG=True
    ```
6.  **Run the database migrations:**
    ```bash
    python manage.py migrate
    ```

### Running the Application

1.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
2.  The API will be available at `http://127.0.0.1:8000/`.

-----

## Technologies Used

  * **Django:** A high-level Python web framework.
  * **Django Rest Framework:** A powerful and flexible toolkit for building Web APIs.
  * **Simple JWT:** A JSON Web Token authentication plugin for DRF.
  * **django-cors-headers:** A Django app for handling Cross-Origin Resource Sharing (CORS).
  * **django-filter:** A reusable Django application for allowing users to filter querysets dynamically.
  * **Python-dotenv:** Reads key-value pairs from a `.env` file and can set them as environment variables.