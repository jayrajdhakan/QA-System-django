# QA-System

This is a Django-based Automated Invoice Processing System built using
Python.

------------------------------------------------------------------------

## 🚀 Features

-   Django backend
-   REST API support (optional)
-   Environment variable support
-   Modular project structure
-   Easy deployment

------------------------------------------------------------------------

# 🛠️ Setup Guide

## 1️⃣ Clone the Repository

``` bash
git clone <your-repository-url>
cd <project-folder>
```

------------------------------------------------------------------------

## 2️⃣ Create Virtual Environment

### ▶ For Windows:

``` bash
python -m venv venv
venv\Scripts\activate
```

### ▶ For Mac/Linux:

``` bash
python3 -m venv venv
source venv/bin/activate
```

------------------------------------------------------------------------

## 3️⃣ Install Requirements

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 4️⃣ Start a Django Project

``` bash
django-admin startproject projectname .
```

OR

``` bash
python -m django startproject projectname
```

------------------------------------------------------------------------

## 5️⃣ Run Migrations

``` bash
python manage.py makemigrations
python manage.py migrate
```

------------------------------------------------------------------------

## 6️⃣ Create Superuser (Optional)

``` bash
python manage.py createsuperuser
```

------------------------------------------------------------------------

## 7️⃣ Run the Server

``` bash
python manage.py runserver
```

Then open:

http://127.0.0.1:8000/

------------------------------------------------------------------------

## 📂 Project Structure

    project/
    │
    ├── manage.py
    ├── requirements.txt
    ├── README.md
    ├── projectname/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    │
    └── app/

------------------------------------------------------------------------

