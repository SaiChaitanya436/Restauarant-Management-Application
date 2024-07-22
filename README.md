# Restauarant-Management-Application
This is a Restaurant Management Application built using Python-Django.


https://github.com/user-attachments/assets/e2f07e91-ffbb-4f89-8a1f-3a175250dfc3



## Features

- User authentication (Sign up, Log in, Log out)
- Role-based access control (Admin, Customer)
- Menu management (Add, Update, Delete menu items)
- Order management (Create, View, Update, Delete orders)
- Customer management (Add, View, Update customer details)
- Generate and download order history as CSV
- RESTful API for managing menu items, orders, and customers


## Technologies Used

- Django
- Django REST Framework
- PostgreSQL
- HTML, CSS


## Prerequisites

- Python 3.x
- PostgreSQL
- Django


## Installation


1. Create and activate a virtual environment:

    ```
    python -m venv venv
    venv\Scripts\activate
    ```

2. Install the dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Set up the PostgreSQL database:

    - Create a database named restaurant_manage
    - Update the `DATABASES` setting in `settings.py` with your database credentials.

4. Apply the migrations:

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Make the groups:

    ```
    python manage.py create_user_groups
    ```

6. Create a superuser:

    ```
    python manage.py createsuperuser
    ```

7. Run the development server:

    ```
    python manage.py runserver
    ```

8. Access the application:

    - Visit `http://127.0.0.1:8000` to view the application.
    - Visit `http://127.0.0.1:8000/admin` to access the Django admin interface.

## Project Structure

Restaurant/
├── account/
│   ├── management/
│   │    └── commands/
│   │         ├── __init__.py
│   │         └── create_user_groups.py
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── menu/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── order/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/
│   ├── RestaurantApp/css
│   │    └── add_item.css
│        ├── base.css
│        ├── delete_menu_item.css
│        └── login.css
│        └── menu.css
	 └── order_history.css
	 ├── place_order.css
│        ├── signup.css
│        └── update_menu_item.css
├── templates/
│   ├── account/
│   │    ├── login.html
│   │    └── signup.html
│   ├── menu/
│   │    └── menu.html
|   |    |__ add_item.html
|   |    |__ delete_menu_item.html
|   |    |__ update_menu_item.html
│   ├── order/
│   │    ├── cart.html
│   │    └── order_history.html
│   └── Restaurant/
│        ├── base.html
│        ├── index.html
├── manage.py
└── requirements.txt


## User Roles

- Customer Service: Can view customers, menu items and orders and manage customers
- Manager: Can view and manage customers, menu items and orders


## Authentication

- Users can sign up and log in.
- Upon signing up, users are automatically added to the selected group (role).


## Menu Management

- Add, update, and delete menu items.
- View a list of all menu items.


## Order Management

- Create new orders.
- View, update, and delete existing orders.
- Download order history as a CSV file.


## Customer Management

- Add and update customer details.
- View a list of all customers.


## REST API

The project also provides a RESTful API for managing menu items, orders, and customers. The API is secured with token-based authentication.


## Endpoints

### Menu Items:

- GET /api/menu/ - List all menu items
- POST /api/menu/ - Create a new menu item
- GET /api/menu/<id>/ - Retrieve a menu item
- PUT /api/menu/<id>/ - Update a menu item
- DELETE /api/menu/<id>/ - Delete a menu item

### Orders:

- GET /api/orders/ - List all orders
- POST /api/orders/ - Create a new order
- GET /api/orders/<id>/ - Retrieve an order
- PUT /api/orders/<id>/ - Update an order
- DELETE /api/orders/<id>/ - Delete an order


## Authentication

To access the API, you need to obtain an authentication token. Use the following endpoint to obtain a token:

- POST /api-token-auth/ - Obtain an authentication token
