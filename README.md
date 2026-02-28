# 👟 DripDeck — Django Sneaker E-Commerce Platform

DripDeck is a production-level sneaker e-commerce web application built using Django. It includes secure authentication, product management, coupon system, Razorpay payment integration, and a complete admin dashboard. This project focuses on real-world e-commerce architecture and backend implementation.

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| Frontend | HTML, CSS, Bootstrap, JavaScript, AJAX |
| Database | PostgreSQL (Production) / SQLite (Development) |
| Authentication | Email & Password, OTP Verification, Google OAuth |
| Payment | Razorpay (with backend signature verification) |
| Deployment | AWS EC2, Gunicorn, Nginx |

---

## 📂 Project Structure

```
dripdeck/
│
├── accounts/       # User authentication & OTP
├── admindash/      # Admin dashboard logic
├── brand/          # Brand management
├── cart/           # Cart functionality
├── category/       # Category management
├── coupon/         # Coupon system
├── order/          # Orders & payments
├── product/        # Product management
├── userdash/       # User profile & dashboard
├── utils/          # Helper utilities
│
├── templates/
├── static/
├── media/
│
├── manage.py
├── requirements.txt
└── db.sqlite3
```

---

## ✨ Features

### 👤 User Features

- User registration with OTP verification
- Secure login and logout
- Google OAuth social login
- Product listing with filters and advanced search
- Product detail page with image zoom
- Add to cart with dynamic quantity update (AJAX)
- Wishlist functionality
- Apply and remove coupons
- Razorpay online payment
- Order tracking and cancellation with reason
- Wallet refund handling

### 🛠️ Admin Features

- Admin authentication
- User management (block/unblock)
- Category and brand management
- Product management (minimum 3 images required)
- Image cropping before upload
- Coupon management
- Offer module
- Order management
- Sales report generation (PDF & Excel export)

---

## 💳 Payment Workflow

1. Backend creates Razorpay order
2. Amount is converted to paise
3. Razorpay returns payment response to frontend
4. Backend performs signature verification
5. Order status is updated after successful verification

---

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/dripdeck.git
cd dripdeck
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root folder:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Open browser at `http://127.0.0.1:8000`

---

## 🔐 Security Practices

- Environment-based SECRET_KEY handling
- CSRF protection on all forms
- Secure Razorpay signature verification
- Server-side validation on all inputs
- Soft delete implementation
- Proper authentication checks on all views

---

## 📌 Key Learnings

- End-to-end Django e-commerce architecture
- Payment gateway integration with Razorpay
- AWS EC2 deployment with Nginx and Gunicorn
- AJAX-based dynamic UI updates
- Admin dashboard design and implementation

---

## 👨‍💻 Author

**Amal P Thobias**
Python Full Stack Developer
Kerala, India