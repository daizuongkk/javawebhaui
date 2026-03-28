import json
import re

def generate_sql_insert():
    """Sinh SQL INSERT cho dữ liệu phụ kiện chuẩn hóa"""
    
    with open("normalized_accessories_v2.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    products = data["products"]
    product_images = data["product_images"]
    
    sql_content = """-- ===================== INSERT ACCESSORIES =====================
-- Generated: 2026-03-28
-- This file contains INSERT statements for accessories category

"""
    
    # INSERT PRODUCTS
    sql_content += "-- ===================== INSERT PRODUCTS =====================\n"
    sql_content += "INSERT INTO products (name, description, detail, summary, category, price, brand, promotion, created_date) VALUES\n"
    
    product_values = []
    for i, product in enumerate(products):
        # Escape single quotes for SQL
        name = product["name"].replace("'", "''")
        description = product["description"].replace("'", "''")
        detail = product["detail"].replace("'", "''")
        summary = product["summary"].replace("'", "''")
        category = product["category"].replace("'", "''")
        created_date = product["created_date"]
        
        value_str = f"('{name}', '{description}', '{detail}', '{summary}', '{category}', {product['price']}, '{product['brand']}', {product['promotion']}, '{created_date}')"
        product_values.append(value_str)
    
    sql_content += ",\n".join(product_values) + ";\n\n"
    
    # INSERT PRODUCT IMAGES
    sql_content += "-- ===================== INSERT PRODUCT IMAGES =====================\n"
    sql_content += "INSERT INTO product_images (product_id, image_url) VALUES\n"
    
    image_values = []
    for image in product_images:
        image_url = image["image_url"].replace("'", "''")
        value_str = f"({image['product_id']}, '{image_url}')"
        image_values.append(value_str)
    
    sql_content += ",\n".join(image_values) + ";\n"
    
    return sql_content

def save_sql_file():
    """Lưu SQL vào file"""
    sql_content = generate_sql_insert()
    
    with open("insert_accessories_normalized_v2.sql", "w", encoding="utf-8") as f:
        f.write(sql_content)
    
    print("✓ Generated insert_accessories_normalized_v2.sql")
    
    # Count statements
    insert_products = sql_content.count("INSERT INTO products")
    insert_images = sql_content.count("INSERT INTO product_images")
    
    print(f"  - INSERT statements: {insert_products + insert_images}")
    print(f"  - Products to insert: {insert_products * 1}")  # One INSERT for all products
    print(f"  - Product images to insert: {insert_images * 1}")
    
    # In preview
    lines = sql_content.split("\n")
    print("\n=== Preview (first 40 lines) ===")
    for line in lines[:40]:
        print(line)

if __name__ == "__main__":
    save_sql_file()
