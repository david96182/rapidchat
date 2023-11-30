# RapidChat

<p align="center">   <img width="220" height="200" src="rapidchat/static/images/logo.png" alt="RapidChat logo"/> </p>

![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter) ![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)

## Introduction

RapidChat is a feature-rich real-time web application that enables users to engage in real-time chat conversations, receive notifications, and manage their accounts seamlessly. This readme provides an overview of the project, including its features, setup instructions, usage guidelines, and deployment options.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Features

- User Registration and Sign In: Users can create accounts and sign in to the application.
- Email Verification: Users receive email verification messages to verify their email addresses.
- Multiple Emails per User: Users can associate multiple email addresses with their accounts.
- Password Reset: Users can reset their passwords if they forget them.
- Real-time Chat: Users can engage in real-time chat with other users.
- Real-time Notifications: Users receive real-time notifications.

## Project Description

RapidChat is designed to provide a seamless and interactive communication experience for users. With its real-time chat functionality, users can connect with others and exchange messages instantly. The application also offers features such as email verification, password reset, and multiple email support to enhance user account management.

## Setup

### Prerequisites

- Python 3.6+
- Django 4+
- Channels 2.4+
- Redis 5+
- Postgres

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/david96182/rapidchat.git
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements/local.txt
   ```

4. Rename the `.env.example` file:

   ```bash
   mv .env.example .env
   ```

5. Update the `.env` file:
   Open the `.env` file and update the settings according to your environment. This includes database configuration, secret key, email settings, and any other necessary variables.

6. Run the migrations:

   ```bash
   python manage.py migrate
   ```

7. Run the server:

   ```bash
   uvicorn config.asgi:application --host 0.0.0.0 --reload --reload-include '*.html'
   ```

### Configuration

The project uses Django's built-in settings management. You can modify the settings in the `config/settings` folder.

## Usage

### User Registration and Sign In

- To create a normal user account, go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a superuser account, use this command:

```
python manage.py createsuperuser
```

### Real-time Chat

The real-time chat feature is implemented using Django Channels. The chat messages are handled through consumers, which are responsible for receiving and sending messages in real-time.

### Real-time Notifications

The real-time notifications feature is also implemented using Django Channels. The notifications are handled through consumers, which are responsible for receiving and sending notifications in real-time.

## Tests

To run the tests, check your test coverage, and generate an HTML coverage report:

```
coverage run -m pytest
coverage html
open htmlcov/index.html
```

## Deployment

The project can be deployed using Docker. See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html). Additionally, you can explore alternative deployment options such as deploying to cloud platforms like AWS, Heroku, or others.

## Contributing

Contributions are welcome. Please feel free to submit a pull request.

## Troubleshooting

guide for possible solutions or seekfurther assistance in the project's issue tracker..
