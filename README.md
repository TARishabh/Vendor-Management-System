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

   - Finally, start the development server by running the following command:
     ```
     python manage.py runserver
     ```
     This command launches the Django development server, allowing you to access the application locally in your web browser at `http://localhost:8000/`.

   - You can now access the Django admin interface at `http://localhost:8000/admin/` and log in using the superuser credentials created earlier.

