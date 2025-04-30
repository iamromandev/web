# 🧑‍💻 Personal Portfolio Website

A **web platform for showcasing personal projects and skills**, built using **Django**.

---

## 🚀 Features

- Clean, responsive design
- Project and blog section
- Admin dashboard for easy content management
- SEO-friendly metadata
- Modular Django app structure

---

## 🛠 Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript (templated)
- **Deployment**: cPanel, Docker (optional)
- **CI/CD**: GitHub Actions

---

## 📦 Getting Started

### Prerequisites

- Python 3.10+
- pip or Poetry
- (Optional) Docker

### Install and Run Locally

```bash
# Clone the repo
git clone https://github.com/iamromandev/web.git
cd web

# (Option 1) Install dependencies
pip install -r requirements.txt

# (Option 2) Using Poetry
poetry install

# Run migrations and start server
python manage.py migrate
python manage.py runserver
