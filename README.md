# ☕ Coffee Value Chain Management System (KCVMS)

A **Django-based platform** that digitizes and manages the entire coffee value chain — from farmer registration to processing, export, and traceability.
Built for **Kikonelo Coffee** by **Hamwe EA**, the system ensures transparency, efficiency, and accountability across all coffee operations.

---

## 🌍 Overview

CCVMS streamlines data flow between farmers, collection centers, processors, and exporters.
It provides real-time visibility into coffee production, quality, and payments, helping cooperatives and value chain actors make data-driven decisions.

---

## 🚀 Core Features

### 🌱 Farmer & Farm Management

* Farmer registration and profiling
* Farm geo-tagging using GPS coordinates
* Crop and production tracking
* Certification and training records

### 🏠 Collection & Aggregation

* Cherry and parchment collection
* Digital weighing and receipts
* Farmer payment tracking (mobile money compatible)
* Quality grading and batch creation

### 🏭 Processing & Warehousing

* Wet and dry mill process tracking
* Inventory management by lot and grade
* Moisture and quality testing

### 📦 Marketing & Export

* Buyer and contract management
* Export documentation (ICO, phytosanitary, invoices)
* Lot traceability from farm to shipment

### 📊 Analytics & Reports

* Farmer and yield performance reports
* Quality grading statistics
* Payment summaries and export metrics

---

## ⚙️ Tech Stack

| Layer              | Technology                       |
| ------------------ | -------------------------------- |
| **Backend**        | Django 5 / Django REST Framework |
| **Frontend**       | HTML5, Bootstrap 5, jQuery       |
| **Database**       | PostgreSQL                       |
| **Authentication** | JWT (JSON Web Token)             |
| **Environment**    | Python 3.12                      |
| **Deployment**     | Docker / Gunicorn / Nginx        |

---

## 🧩 System Architecture

```
┌────────────────────────────┐
│  Field App (Optional)      │
│  → Collects farmer data    │
└──────────────┬─────────────┘
               │ REST API
┌──────────────▼─────────────┐
│      Django Backend API    │
│  (DRF + PostgreSQL DB)     │
└──────────────┬─────────────┘
               │
┌──────────────▼─────────────┐
│   Web Dashboard (Admin)    │
└────────────────────────────┘
```

---

## 🛠️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/kikonelo-coffee-vcms.git
cd kikonelo-coffee-vcms
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=kcvms
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True
```

### 5️⃣ Run Migrations

```bash
python manage.py migrate
```

### 6️⃣ Create a Superuser

```bash
python manage.py createsuperuser
```

### 7️⃣ Start the Server

```bash
python manage.py runserver
```

Then open:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧱 Project Structure

```
kcvms/
├── core/                # Core settings, URLs, and utilities
├── farmers/             # Farmer and farm management app
├── collection/          # Coffee collection module
├── processing/          # Coffee processing and inventory module
├── sales/               # Sales and export management
├── reports/             # Dashboards and analytics
├── templates/           # HTML templates
├── static/              # CSS, JS, and images
└── manage.py
```

---

## 🧰 Docker Setup (Optional)

If you prefer running the project in Docker:

```bash
docker-compose up --build
```

Then access:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🔒 Authentication & Security

* JWT-based authentication (DRF SimpleJWT)
* Role-based access control (Admin, Field Officer, Processor, Exporter)
* HTTPS-ready configuration
* Secure environment variables with `.env`

---

## 📊 Reporting & Analytics

* Daily/weekly farmer collections
* Payment summaries per cooperative
* Quality and moisture analysis reports
* Export summary by destination

---

## 🤝 Contributing

Contributions are welcome! Please follow the standard Git workflow:

```bash
git checkout -b feature/my-feature
git commit -m "Added new feature"
git push origin feature/my-feature
```

Open a pull request and describe your change.

---

## 🧑‍💻 Author & Maintainer

**Developed by:** HAMWE EA
**Lead Developer:** TECH
📧 Email: [tech@hamwe.org](mailto:tech@hamwe.org)
🌍 Location: Kampala, Uganda

---

## 📄 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---

