# Django Issue Tracker

A minimal issue tracking web application built with Django 5.2 LTS. Used as the sample app for the [How to Deploy a Django Web Application with Uncloud](https://labs.iximiuz.com/tutorials/uncloud-deploy-django-app-7a378bc3) tutorial on iximiuz Labs.

## Features

- Full CRUD operations for issues
- Status tracking (Open, In Progress, Done)
- Priority levels (Low, Medium, High)
- Comment system
- Django admin interface
- SQLite database with Docker volume persistence

## Tech Stack

- Python 3.14
- Django 5.2 LTS
- Gunicorn 23
- SQLite

## Local Development

```sh
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit http://localhost:8000/

## Deployment with Uncloud

```sh
cd ~/app
uc deploy
```

See the [tutorial](https://labs.iximiuz.com/tutorials/uncloud-deploy-django-app-7a378bc3) for a full walkthrough.
