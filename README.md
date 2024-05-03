# Vendor-Management-System - Installation Guide

## Pre-Installation Instructions

Before cloning the repository, ensure you have PostgreSQL and PgAdmin installed on your system.

1. **Database Setup:**
   - Create a `.env` file in the root directory of the project.
   - Add the following PostgreSQL database details to the `.env` file:
     ```
     POSTGRES_DB=VENDORDB
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD='your_postgres_password'
     POSTGRES_HOST=localhost
     ```

2. **PgAdmin Setup:**
   - Open PgAdmin and set a password for your PgAdmin account.
   - Right-click on `Servers` and select `Register` > `Server`.
   - Name the server as `VENDOR`.
   - Under `Connections`, enter the hostname and PostgreSQL password, then save.
   - Right-click on `VENDOR`, create a new database named `VENDORDB`.

## Installation Instructions

1. **Setup Virtual Environment:**
   - Install virtualenv if not already installed:
     ```
     pip install virtualenv
     ```
   - Create a virtual environment:
     ```
     virtualenv <envname>
     ```
     or
     ```
     python -m virtualenv <nameOfEnv>
     ```
   - Activate the virtual environment:
     ```
     .\<envname>\Scripts\Activate.ps1
     ```

2. **Clone the Repository:**
   - Clone this repository to your local system.

   - You can use a Git client or the Git CLI to clone the repository. For example, in VSCode, you can use the Git Pull Requests extension.

   - For more help on cloning, refer to: [Cloning a Repository](https://youtu.be/_ynMa2XlRgk)


3. **Install Requirements:**
   - After cloning the repository, navigate to the project directory.
   - Run the following command to install the required dependencies:
     ```
     pip install -r requirements.txt
     ```

4. **Set Up the Django Project:**
   - Once the requirements are installed, you need to set up the Django project.
   - First, navigate to the project directory containing the `manage.py` file.
   - Before applying migrations, run the following command to create migration files based on the changes you've made to the models:
     ```
     python manage.py makemigrations
     ```
     This command analyzes your models and creates migration files in the `migrations` directory for any changes detected.

   - After creating migration files, apply migrations to create the necessary database tables:
     ```
     python manage.py migrate
     ```
     This command executes the migration files and creates or updates the database schema according to the changes defined in the migration files.

   - Next, create a superuser account to access the Django admin interface and manage the application:
     ```
     python manage.py createsuperuser
     ```
     Follow the prompts to enter a username, email address, and password for the superuser account.

    - To run the tests in the `tests` folder, use the following command:

    - You can also run individual tests for specific modules:
    - For vendor-related tests: `python manage.py test vendorapp.test_vendor`
    - For purchase order-related tests: `python manage.py test vendorapp.test_purchase_order`
    - For performance metrics tests: `python manage.py test vendorapp.test_performance_metrics`

   - Finally, start the development server by running the following command:
     ```
     python manage.py runserver
     ```
     This command launches the Django development server, allowing you to access the application locally in your web browser at `http://localhost:8000/`.

   - You can now access the Django admin interface at `http://localhost:8000/admin/` and log in using the superuser credentials created earlier.

    - You can also run individual tests for specific modules:
    - For vendor-related tests: `python manage.py test vendorapp.test_vendor`
    - For purchase order-related tests: `python manage.py test vendorapp.test_purchase_order`
    - For performance metrics tests: `python manage.py test vendorapp.test_performance_metrics`

    - Finally, start the development server by running the following command:

# Vendor API Endpoints Documentation

This document provides an overview of the API endpoints related to managing vendors within the system.

## 1. Create a New Vendor

- **URL:** `/api/vendors/`
- **Method:** POST
- **Description:** Create a new vendor.
- **Request Body:** Details of the vendor to be created.
- **Response:** Status code 201 (Created) along with the details of the newly created vendor.

## 2. List All Vendors

- **URL:** `/api/vendors/`
- **Method:** GET
- **Description:** Retrieve a list of all vendors.
- **Response:** A list of all vendors along with their details.

## 3. Retrieve a Specific Vendor

- **URL:** `/api/vendors/{vendor_id}/`
- **Method:** GET
- **Description:** Retrieve the details of a specific vendor identified by the `vendor_id`.
- **Response:** Details of the vendor identified by the provided `vendor_id`.

## 4. Update a Vendor

- **URL:** `/api/vendors/{vendor_id}/`
- **Method:** PUT
- **Description:** Update the details of a specific vendor identified by the `vendor_id`.
- **Request Body:** Updated details of the vendor.
- **Response:** Status code 200 (OK) along with the updated details of the vendor.

## 5. Delete a Vendor

- **URL:** `/api/vendors/{vendor_id}/`
- **Method:** DELETE
- **Description:** Delete a specific vendor identified by the `vendor_id`.
- **Response:** Status code 204 (No Content) with no response body.

These endpoints allow users to perform CRUD (Create, Read, Update, Delete) operations on vendor data within the system.

# Purchase Order API Endpoints Documentation

This document provides an overview of the API endpoints related to managing purchase orders within the system.

## 1. Create a Purchase Order

- **URL:** `/api/purchase_orders/`
- **Method:** POST
- **Description:** Create a new purchase order.
- **Request Body:** Details of the purchase order to be created.
- **Response:** Status code 201 (Created) along with the details of the newly created purchase order.

## 2. List All Purchase Orders

- **URL:** `/api/purchase_orders/`
- **Method:** GET
- **Description:** Retrieve a list of all purchase orders with an option to filter by vendor.
- **Response:** A list of all purchase orders along with their details.

## 3. Retrieve Details of a Specific Purchase Order

- **URL:** `/api/purchase_orders/{po_id}/`
- **Method:** GET
- **Description:** Retrieve the details of a specific purchase order identified by the `po_id`.
- **Response:** Details of the purchase order identified by the provided `po_id`.

## 4. Update a Purchase Order

- **URL:** `/api/purchase_orders/{po_id}/`
- **Method:** PUT
- **Description:** Update the details of a specific purchase order identified by the `po_id`.
- **Request Body:** Updated details of the purchase order.
- **Response:** Status code 200 (OK) along with the updated details of the purchase order.

## 5. Delete a Purchase Order

- **URL:** `/api/purchase_orders/{po_id}/`
- **Method:** DELETE
- **Description:** Delete a specific purchase order identified by the `po_id`.
- **Response:** Status code 204 (No Content) with no response body.

These endpoints allow users to perform CRUD (Create, Read, Update, Delete) operations on purchase orders within the system.

# Vendor Performance API Endpoint Documentation

This document provides details about the API endpoint used to retrieve a vendor's performance metrics.

## Retrieve a Vendor's Performance Metrics

- **URL:** `/api/vendors/{vendor_id}/performance/`
- **Method:** GET
- **Description:** Retrieve a specific vendor's performance metrics identified by the `vendor_id`.
- **Response:** 
  - Status code 200 (OK) along with the performance metrics data of the vendor.(g on_time_delivery_rate, quality_rating_avg,
    average_response_time, and fulfillment_rate.)
  - Status code 404 (Not Found) if the vendor with the provided `vendor_id` does not exist.

This endpoint allows users to retrieve the performance metrics of a specific vendor by providing the `vendor_id`.

# Acknowledgment Endpoint Documentation

This document provides details about the API endpoint used for acknowledging purchase orders.

## Acknowledge Purchase Order

- **URL:** `/api/purchase_orders/{po_id}/acknowledge/`
- **Method:** POST
- **Description:** Allows vendors to acknowledge purchase orders by updating the acknowledgment date and triggering the recalculation of average response time.
- **Request Body:**
  - `acknowledgment_date`: The date when the purchase order is acknowledged. Must be in ISO 8601 format (e.g., "YYYY-MM-DDTHH:MM:SS").
- **Response:** 
  - Status code 200 (OK) along with the updated purchase order data if the request is successful.
  - Status code 404 (Not Found) if the purchase order with the provided `po_id` does not exist.
  - Status code 400 (Bad Request) if there are validation errors in the request body.

This endpoint allows vendors to acknowledge purchase orders, ensuring that the acknowledgment date is not in the past. Upon acknowledgment, the acknowledgment date is updated, and the average response time is recalculated.
