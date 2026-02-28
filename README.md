👟 DripDeck – Django Sneaker E-Commerce Platform

DripDeck is a production-style sneaker e-commerce web application built using Django.
It includes secure authentication, product and order management, coupon system, Razorpay payment integration, and a complete admin dashboard.

This project focuses on real-world e-commerce workflows, backend architecture, and deployment practices.

🚀 Tech Stack

Backend

Python

Django

PostgreSQL (Production) / SQLite (Development)

Frontend

HTML

CSS

Bootstrap

JavaScript

AJAX

Authentication

Email & Password

OTP Verification

Google OAuth (social login)

Payment

Razorpay Integration (with signature verification)

Deployment

AWS EC2

Gunicorn

Nginx

📂 Project Structure
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
│
├── templates/
├── static/
├── media/
│
├── manage.py
├── requirements.txt
└── db.sqlite3
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

Razorpay online payment

Order tracking

Order cancellation with reason

Wallet refund handling

Advanced search

Admin Features

Admin authentication

User management (block/unblock)

Category & brand management

Product management (minimum 3 images)

Image cropping before upload

Coupon management

Offer module

Order management

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

Create a .env file:

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
5. Run Migrations
python manage.py migrate
6. Create Superuser
python manage.py createsuperuser
7. Run Server
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

Admin dashboard design

AJAX-based dynamic UI updates

👨‍💻 Author

Amal P Thobias
Python Full Stack Developer
Kerala, India
