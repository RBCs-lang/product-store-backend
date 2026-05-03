# 🛒 Product Store — Backend

A RESTful API built with **Flask** and **Supabase (PostgreSQL)** for managing a product inventory.

> 🔗 Backend Repo: https://github.com/RBCs-lang/product-store-Backend

---

## 👥 Team
| Name | Role |
|------|------|
|Biswajit Moharana| Backend Development |
|Subh Sharma| Frontend Development |

---

## 🛠️ Tech Stack
- **Python** — Programming language
- **Flask** — Web framework for building APIs
- **Supabase** — Cloud PostgreSQL database
- **Flask-CORS** — Allows frontend to communicate with backend
- **python-dotenv** — Loads secret keys from `.env` file

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/product-store-backend.git
cd product-store-backend
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file
Create a file called `.env` in the root folder and add your Supabase credentials:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_secret_key
```
> ⚠️ Never share or push this file to GitHub.

### 4. Set up the Supabase database
Create a table called `products` in your Supabase project with these columns:

| Column | Type |
|--------|------|
| id | int8 (primary key) |
| name | text |
| price | float8 |
| category | text |
| description | text |
| stock | int4 |
| image_url | text |

### 5. Run the server
```bash
python app.py
```
Server runs at: **http://localhost:5001**

---

## ⚠️ Important — You Must Run This Every Time

> The Flask server is a **local server** and does not stay running on its own.

**Every time you want to use the app, you must:**
1. Open a terminal in the backend folder
2. Run `python app.py`
3. Keep the terminal **open** — closing it stops the server

```
✅ Server is running when you see:
 * Running on http://127.0.0.1:5001
 * Debug mode: on

❌ If terminal is closed = frontend will show "Could not connect to backend"
```

> 💡 Think of it like a restaurant — the kitchen (backend) must be open before customers (frontend) can place orders.

---

## 📡 API Endpoints

### Get all products
```
GET /products
```
**Response:**
```json
{
  "success": true,
  "count": 3,
  "products": [...]
}
```

---

### Get a single product
```
GET /products/<id>
```
**Response:**
```json
{
  "success": true,
  "product": { "id": 1, "name": "Mechanical Keyboard", ... }
}
```

---

### Create a new product
```
POST /products
Content-Type: application/json
```
**Request Body:**
```json
{
  "name": "Wireless Mouse",
  "price": 1499,
  "category": "Electronics",
  "description": "Ergonomic design, 2.4GHz wireless.",
  "stock": 30,
  "image_url": "https://example.com/image.jpg"
}
```
**Allowed categories:** Electronics, Furniture, Clothing, Books, Food, Other

**Response:**
```json
{
  "success": true,
  "message": "Product created successfully",
  "product": { "id": 4, "name": "Wireless Mouse", ... }
}
```

---

### Update a product
```
PUT /products/<id>
Content-Type: application/json
```
**Request Body:** (send only fields you want to update)
```json
{
  "price": 1299,
  "stock": 25
}
```

---

### Delete a product
```
DELETE /products/<id>
```
**Response:**
```json
{
  "success": true,
  "message": "Product deleted successfully"
}
```

---

### Search products
```
GET /search?q=keyboard
```
**Response:**
```json
{
  "success": true,
  "count": 1,
  "products": [...]
}
```

---

## ✅ Data Validation
The API validates all incoming data and returns field-specific errors:
- `name` — Required, 2–100 characters
- `price` — Required, non-negative number
- `category` — Required, must be one of the allowed values
- `description` — Optional, max 500 characters
- `stock` — Optional, non-negative whole number
- `image_url` — Optional, must start with http:// or https://

**Validation error response (422):**
```json
{
  "success": false,
  "errors": {
    "name": "Name is required",
    "price": "Price must be a non-negative number"
  }
}
```

---

## 📁 Project Structure
```
product-store-backend/
├── app.py            ← Flask app with all API routes
├── requirements.txt  ← Python dependencies
├── .gitignore        ← Excludes .env from GitHub
├── .env              ← Secret keys (not on GitHub)
└── README.md         ← This file
```

---

## 🔒 Security
- API keys are stored in `.env` and never pushed to GitHub
- `.gitignore` ensures `.env` is always excluded
- CORS is configured to allow frontend communication
