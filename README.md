# First Blog

A simple blog application built with Django that allows users to create, edit, and view blog posts.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Author](#author)

---

## Introduction

This project is a basic blog built using the Django framework.  
Users can create, edit, and view blog posts.  
The goal of this project is to practice core Django concepts including models, views, and templates.

---

## Features

- Create, edit, and delete blog posts  
- Display posts in chronological order  
- Use HTML templates for rendering pages  
- View detailed content of each post

---

## Installation

1. Clone the repository:  
```bash
git clone https://github.com/Matinbarzegarbahrami/first-blog.git
```

2. Change directory to the project folder:
```bash
cd first-blog
```

3. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Apply database migrations:
```bash
python manage.py migrate
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage
Open your browser and navigate to http://localhost:8000 to see the list of blog posts.

To add or edit posts, use the Django admin interface:

Admin URL: http://localhost:8000/admin

You need to create a superuser with python manage.py createsuperuser to access this area.

## Project Structure
```bash
first-blog/
├── blog/              # Blog app folder
│   ├── migrations/    # Database migrations
│   ├── templates/     # HTML templates
│   ├── admin.py       # Admin configurations
│   ├── models.py      # Data models
│   ├── views.py       # Views
│   └── urls.py        # URL routing
├── firstblog/         # Project settings
├── manage.py          # Django project management script
└── requirements.txt   # Project dependencies
```
## Technologies
- Python 3.x
- Django 4.x
- SQLite (default database)

## Author
- Matin Barzegar bahrami
