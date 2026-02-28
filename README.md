👟 DripDeck – Django Sneaker E-Commerce Platform

<<<<<<< HEAD
DripDeck is a production-style sneaker e-commerce web application built using Django.
It includes secure authentication, product and order management, coupon system, Razorpay payment integration, and a complete admin dashboard.

This project focuses on real-world e-commerce workflows, backend architecture, and deployment practices.

🚀 Tech Stack

=======
DripDeck is a production-level sneaker e-commerce web application built using Django. It includes secure authentication, product management, coupon system, Razorpay payment integration, and a complete admin dashboard.

This project focuses on real-world e-commerce architecture and backend implementation.

🚀 Tech Stack
>>>>>>> 6ffea34 (Added README)
Backend

Python

Django

<<<<<<< HEAD
PostgreSQL (Production) / SQLite (Development)
=======
PostgreSQL (Production)

SQLite (Development)
>>>>>>> 6ffea34 (Added README)

Frontend

HTML

CSS

Bootstrap

JavaScript

AJAX

Authentication

<<<<<<< HEAD
Email & Password

OTP Verification

Google OAuth (social login)

Payment

Razorpay Integration (with signature verification)
=======
Email & Password Authentication

OTP Verification

Google OAuth

Payment

Razorpay (with backend signature verification)
>>>>>>> 6ffea34 (Added README)

Deployment

AWS EC2

Gunicorn

Nginx

📂 Project Structure
<<<<<<< HEAD
dripdeck/
│
├── accounts/        # User authentication & OTP
├── admindash/       # Admin dashboard logic
├── brand/           # Brand management
├── cart/            # Cart functionality
├── category/        # Category management
├── coupon/          # Coupon system
├── order/           # Orders & payments
├── product/         # Product management
├── userdash/        # User profile & dashboard
├── utils/           # Helper utilities
=======

dripdeck/
│
├── accounts/
├── admindash/
├── brand/
├── cart/
├── category/
├── coupon/
├── order/
├── product/
├── userdash/
├── utils/
>>>>>>> 6ffea34 (Added README)
│
├── templates/
├── static/
├── media/
│
├── manage.py
├── requirements.txt
└── db.sqlite3
<<<<<<< HEAD
✨ Key Features
User Features

User registration with OTP verification

Secure login/logout

Google authentication

Product listing with filters

Product detail page with image zoom

Add to cart / update quantity (AJAX-based)

Wishlist functionality

Coupon apply & remove
=======

✨ Features
👤 User Features

User registration with OTP verification

Secure login and logout

Google authentication

Product listing with filtering

Product detail page with image zoom

Add to cart with dynamic quantity update (AJAX)

Wishlist functionality

Apply and remove coupons
>>>>>>> 6ffea34 (Added README)

Razorpay online payment

Order tracking

Order cancellation with reason

Wallet refund handling

Advanced search

<<<<<<< HEAD
Admin Features
=======
🛠️ Admin Features
>>>>>>> 6ffea34 (Added README)

Admin authentication

User management (block/unblock)

<<<<<<< HEAD
Category & brand management

Product management (minimum 3 images)
=======
Category and brand management

Product management (minimum 3 images required)
>>>>>>> 6ffea34 (Added README)

Image cropping before upload

Coupon management

Offer module

Order management

<<<<<<< HEAD
Sales reports (PDF & Excel export)

💳 Payment Flow

Razorpay order is created from backend.

Amount converted to paise.

Razorpay returns payment response.

Signature verification is performed.

Order status updated after successful verification.

⚙️ Local Setup
1. Clone the Repository
git clone https://github.com/yourusername/dripdeck.git
cd dripdeck
2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
3. Install Dependencies
pip install -r requirements.txt
4. Environment Variables
=======
Sales report generation (PDF & Excel export)

💳 Payment Workflow

Backend creates Razorpay order

Amount converted to paise

Razorpay returns payment response

Signature verification is performed

Order status updated after successful verification

⚙️ Local Setup
1. Clone Repository
git clone https://github.com/yourusername/dripdeck.git
cd dripdeck

2. Create Virtual Environment

Windows:
python -m venv venv
venv\Scripts\activate
Mac/Linux:

python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables
>>>>>>> 6ffea34 (Added README)

Create a .env file:

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
<<<<<<< HEAD
5. Run Migrations
python manage.py migrate
6. Create Superuser
python manage.py createsuperuser
7. Run Server
=======
5. Apply Migrations
python manage.py migrate
6. Create Superuser
python manage.py createsuperuser
7. Run Development Server
>>>>>>> 6ffea34 (Added README)
python manage.py runserver
🔐 Security Practices

Environment-based SECRET_KEY handling

CSRF protection

Secure Razorpay signature verification

Server-side validation

Soft delete implementation

Proper authentication checks

📌 Learning Highlights

End-to-end Django e-commerce architecture

Payment gateway integration

AWS EC2 deployment

Nginx + Gunicorn configuration

<<<<<<< HEAD
Admin dashboard design

AJAX-based dynamic UI updates

=======
AJAX-based dynamic UI updates

Admin dashboard implementation

>>>>>>> 6ffea34 (Added README)
👨‍💻 Author

Amal P Thobias
Python Full Stack Developer
<<<<<<< HEAD
Kerala, India
=======
Kerala, India
>>>>>>> 6ffea34 (Added README)
