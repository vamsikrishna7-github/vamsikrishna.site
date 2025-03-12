# Vamsi Krishna's Dynamic Portfolio

Welcome to my open-source portfolio project! This Django-based portfolio includes an admin panel, automatic email responses, reCAPTCHA spam protection, and a secure contact form. 🚀
## 🌐 Live Demo

![Image](https://github.com/user-attachments/assets/02498b93-7f79-41b8-977a-7dbe3511b7e7)
🌐 Visit: [www.vamsikrishna.site](https://vamsikrishna.site)

## Features

- 🌐 **Responsive Django Portfolio**
- 🔒 **Secure Admin Panel**
- 📩 **Auto-Email Responses for Contact Form**
- 🛡 **reCAPTCHA Spam Protection**
- 🔐 **Contact Form with Secure Admin Login**
- 🗄 **SQLite Database Support**
- ✨ **Customizable & Open Source**

---

## 🛠 Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Django (Python)
- **Database:** SQLite (Can be switched to MySQL)
- **Security:** reCAPTCHA, Django Admin Authentication
- **Version Control:** Git, GitHub

## Project Overview
This is a responsive Django portfolio with:
- ✅ Custom admin panel (`/admin/`)
- ✅ Auto-email responses on form submissions
- ✅ reCAPTCHA spam protection
- ✅ Secure admin login
- ✅ Dynamic contact form
- ✅ SQLite database

## 🚀 Installation Guide

Follow these steps to set up the project on your local machine.

### 1️⃣ Clone the Repository

```bash
    git https://github.com/vamsikrishna7-github/vamsikrishna.site.git
    cd vamsikrishna.in
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)

```bash
    python -m venv vamsi
    source vamsi/bin/activate  # For macOS/Linux
    vamsikrishna\Scripts\activate  # For Windows
```

### 3️⃣ Install Dependencies

```bash
    pip install -r requirements.txt
```

### 4️⃣ Set Up Database Migrations

```bash
    python manage.py migrate
```

### 5️⃣ Create a Superuser (For Admin Panel)

```bash
    python manage.py createsuperuser
```
### * Collect Static Files (for Deployment)

```bash
    python manage.py collectstatic
```
### 6️⃣ Run the Development Server

```bash
    python manage.py runserver
```

Then visit: `http://127.0.0.1:8000/`

## 🔑 reCAPTCHA Setup (For Production)

1. Register your site at [Google reCAPTCHA](https://www.google.com/recaptcha/admin/create).
2. Get your **Site Key** and **Secret Key**.
3. Update `settings.py`:

```python
    RECAPTCHA_PUBLIC_KEY = "your_real_site_key"
    RECAPTCHA_PRIVATE_KEY = "your_real_secret_key"
```
## Email Setup (Gmail SMTP)
To enable email notifications, add the following settings to `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```
⚠️ **Note:** Use an [App Password](https://myaccount.google.com/apppasswords) instead of your actual password for security.

## 📜 License

This project is open-source under the **MIT License**. Feel free to use and modify it!

## 🎯 Contributing

This project is open-source! Feel free to fork, modify, and contribute via pull requests. 💡

### 1. Fork the Repository

```bash
git clone https://github.com/vamsikrishna7-github/vamsikrishna.site.git
```

### 2. Create a New Branch

```bash
git checkout -b feature-branch
```

### 3. Make Your Changes & Commit

```bash
git add .
git commit -m "Added a new feature"
```

### 4. Push & Submit a Pull Request

```bash
git push origin feature-branch
```

---

## Troubleshooting 🛠
If you face any issues during installation or setup, feel free to contact me:                                                                                
📧 **Email:** contact@vamsikrishna.site 
🌐 **Portfolio:** [www.vamsikrishna.site](https://vamsikrishna.site/#contact)

Made with ❤️ by **Vamsi Krishna**

