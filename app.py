from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# ─── Load environment variables from .env ────────────────────────────────────
load_dotenv()

app = Flask(__name__)
CORS(app)

# ─── Supabase Client ──────────────────────────────────────────────────────────
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

ALLOWED_CATEGORIES = ["Electronics", "Furniture", "Clothing", "Books", "Food", "Other"]


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return jsonify({"message": "Product Store API is running!", "version": "2.0 (Supabase)"})


# GET /products – Return all products
@app.route("/products", methods=["GET"])
def get_products():
    try:
        response = supabase.table("products").select("*").order("id").execute()
        return jsonify({"success": True, "count": len(response.data), "products": response.data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# GET /products/<id> – Return a single product
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        response = supabase.table("products").select("*").eq("id", product_id).execute()
        if not response.data:
            return jsonify({"success": False, "error": "Product not found"}), 404
        return jsonify({"success": True, "product": response.data[0]}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# POST /products – Create a new product
@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Request body must be valid JSON"}), 400

    # ── Validation ────────────────────────────────────────────────────────────
    errors = {}

    name = str(data.get("name", "")).strip()
    if not name:
        errors["name"] = "Name is required"
    elif len(name) < 2:
        errors["name"] = "Name must be at least 2 characters"
    elif len(name) > 100:
        errors["name"] = "Name must be under 100 characters"

    try:
        price = float(data.get("price", -1))
        if price < 0:
            errors["price"] = "Price must be a non-negative number"
    except (TypeError, ValueError):
        errors["price"] = "Price must be a valid number"

    category = str(data.get("category", "")).strip()
    if not category:
        errors["category"] = "Category is required"
    elif category not in ALLOWED_CATEGORIES:
        errors["category"] = f"Category must be one of: {', '.join(ALLOWED_CATEGORIES)}"

    description = str(data.get("description", "")).strip()
    if len(description) > 500:
        errors["description"] = "Description must be under 500 characters"

    try:
        stock = int(data.get("stock", 0))
        if stock < 0:
            errors["stock"] = "Stock cannot be negative"
    except (TypeError, ValueError):
        errors["stock"] = "Stock must be a whole number"

    image_url = str(data.get("image_url", "")).strip()
    if image_url and not (image_url.startswith("http://") or image_url.startswith("https://")):
        errors["image_url"] = "Image URL must start with http:// or https://"

    if errors:
        return jsonify({"success": False, "errors": errors}), 422

    # ── Insert into Supabase ──────────────────────────────────────────────────
    try:
        new_product = {
            "name": name,
            "price": round(price, 2),
            "category": category,
            "description": description,
            "stock": stock,
            "image_url": image_url,
        }
        response = supabase.table("products").insert(new_product).execute()
        return jsonify({"success": True, "message": "Product created successfully", "product": response.data[0]}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# PUT /products/<id> – Update a product
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Request body must be valid JSON"}), 400

    errors = {}
    updates = {}

    if "name" in data:
        name = str(data["name"]).strip()
        if len(name) < 2:
            errors["name"] = "Name must be at least 2 characters"
        else:
            updates["name"] = name

    if "price" in data:
        try:
            price = float(data["price"])
            if price < 0:
                errors["price"] = "Price must be non-negative"
            else:
                updates["price"] = round(price, 2)
        except (TypeError, ValueError):
            errors["price"] = "Price must be a valid number"

    if "category" in data:
        category = str(data["category"]).strip()
        if category not in ALLOWED_CATEGORIES:
            errors["category"] = f"Category must be one of: {', '.join(ALLOWED_CATEGORIES)}"
        else:
            updates["category"] = category

    if "description" in data:
        description = str(data["description"]).strip()
        if len(description) > 500:
            errors["description"] = "Description must be under 500 characters"
        else:
            updates["description"] = description

    if "stock" in data:
        try:
            stock = int(data["stock"])
            if stock < 0:
                errors["stock"] = "Stock cannot be negative"
            else:
                updates["stock"] = stock
        except (TypeError, ValueError):
            errors["stock"] = "Stock must be a whole number"

    if "image_url" in data:
        image_url = str(data["image_url"]).strip()
        if image_url and not (image_url.startswith("http://") or image_url.startswith("https://")):
            errors["image_url"] = "Image URL must start with http:// or https://"
        else:
            updates["image_url"] = image_url

    if errors:
        return jsonify({"success": False, "errors": errors}), 422

    try:
        response = supabase.table("products").update(updates).eq("id", product_id).execute()
        if not response.data:
            return jsonify({"success": False, "error": "Product not found"}), 404
        return jsonify({"success": True, "message": "Product updated successfully", "product": response.data[0]}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# DELETE /products/<id> – Delete a product
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        response = supabase.table("products").delete().eq("id", product_id).execute()
        if not response.data:
            return jsonify({"success": False, "error": "Product not found"}), 404
        return jsonify({"success": True, "message": "Product deleted successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# GET /search?q=query – Search products
@app.route("/search", methods=["GET"])
def search_products():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"success": False, "error": "Query parameter 'q' is required"}), 400
    try:
        response = supabase.table("products").select("*").ilike("name", f"%{query}%").execute()
        return jsonify({"success": True, "count": len(response.data), "products": response.data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5001)
