# 💸 BudgetMate - Django Expenses Tracker

BudgetMate is a personal finance web application that helps users track their monthly expenses, set budgets, and visualize spending habits. Built using Django and Bootstrap, it offers a clean and intuitive interface for managing finances.

![screenshot](https://via.placeholder.com/900x400?text=Add+Screenshot+Here)

---

## 🔧 Features

✅ User authentication (register, login, logout)  
✅ Add, edit, and delete personal expenses  
✅ Set a monthly budget  
✅ Filter expenses by month  
✅ Category-wise expense summary chart (Chart.js)  
✅ Budget vs Spent progress indicator  
✅ Budget history table (month-to-month overview)  
✅ Export expenses to Excel (`.xlsx`)  
✅ Export budget history to CSV (`.csv`)  
✅ Bootstrap-based responsive UI

---

## 🖼 Sample Screenshots

> (You can add your own screenshots in `/static/screens/` and update these links)

- ![Dashboard](static/screens/dashboard.png)
- ![Add Expense](static/screens/add_expense.png)
- ![Budget History](static/screens/budget_history.png)

---

## 🚀 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** Bootstrap, HTML, Chart.js
- **Database:** SQLite (default, for local use)
- **Others:** OpenPyXL (for Excel export), CSV module (for budget export)

---

## 💡 Installation Guide

```bash
# 1. Clone the repository
git clone https://github.com/Juven65/django-budgetmate.git
cd django-budgetmate

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser (admin)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
