# 🥛 Milk-Connect

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![HTML](https://img.shields.io/badge/HTML%2FCSS%2FJS-F7DF1E?style=flat&logo=javascript&logoColor=black)

A full-stack web platform that **directly connects milk producers (farmers) with consumers**, eliminating middlemen, ensuring fair pricing, and making daily dairy delivery transparent and efficient.

---

## 🚀 The Problem It Solves

In India's dairy supply chain:
- Farmers get unfair prices due to middlemen
- Consumers have no visibility into milk quality or source
- No reliable way to find and verify local milk suppliers

**Milk-Connect digitizes this local supply chain** — farmers list their products, consumers find trusted suppliers nearby, and orders flow directly between them.

---

## 🎯 Key Features

### 👨‍🌾 Farmer Module
- Register and create a supplier profile
- List milk quantity, price, and availability
- Track incoming orders and earnings

### 🛒 Consumer Module
- Find trusted milkmen nearby
- Browse and compare products and prices
- Place one-time or recurring orders
- Track delivery status

### 🛠️ Admin Dashboard
- Manage users, listings, and orders
- Monitor platform activity

### 💳 Payments & Auth
- Secure user login and signup
- Integrated payment flow
- Cash on delivery option

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Django |
| Database | MySQL |

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repo
git clone https://github.com/vikaspal76/Milk-Connect.git
cd Milk-Connect

# 2. Create and activate virtual environment
python -m venv env
source env/bin/activate      # Mac/Linux
env\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure MySQL in settings.py, then run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 📁 Project Structure

```
Milk-Connect/
├── manage.py
├── requirements.txt
├── static/              # CSS, JS, images
├── templates/           # HTML templates
└── app/
    ├── models.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

---

## 🔮 Future Enhancements

- AI-based demand prediction for farmers
- Subscription-based milk delivery
- Mobile app (Android/iOS)
- IoT integration for milk quality monitoring

---

## 👨‍💻 Author

**Vikash Singh**  
B.Tech CSE (AI & ML) — Galgotias University  
[GitHub](https://github.com/vikaspal76)
