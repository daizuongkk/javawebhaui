import json
import csv
from datetime import datetime

# Read normalized data
with open('normalized_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Helper function to escape SQL strings
def escape_sql(value):
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"

# Create SQL file
with open('insert_normalized_data.sql', 'w', encoding='utf-8') as f:
    f.write("-- ===================== INSERT PRODUCTS =====================\n")
    f.write("INSERT INTO products (id, name, description, detail, summary, category, price, brand, promotion, created_at, updated_at) VALUES\n")
    
    products = data['products']
    for idx, product in enumerate(products):
        f.write(f"({product['id']}, {escape_sql(product['name'])}, {escape_sql(product['description'])}, {escape_sql(product['detail'][:2000] if product['detail'] else '')}, {escape_sql(product['summary'])}, {escape_sql(product['category'])}, {product['price']}, {escape_sql(product['brand'])}, {product['promotion']}, NOW(), NOW())")
        
        if idx < len(products) - 1:
            f.write(",\n")
        else:
            f.write(";\n")
    
    f.write("\n-- ===================== INSERT PRODUCT IMAGES =====================\n")
    f.write("INSERT INTO product_images (id, product_id, image_url) VALUES\n")
    
    images = data['product_images']
    for idx, image in enumerate(images):
        f.write(f"({image['id']}, {image['product_id']}, {escape_sql(image['image_url'])})")
        
        if idx < len(images) - 1:
            f.write(",\n")
        else:
            f.write(";\n")
    
    f.write("\n-- ===================== INSERT INVENTORY =====================\n")
    f.write("INSERT INTO inventory (product_id, quantity) VALUES\n")
    
    inventory = data['inventory']
    for idx, item in enumerate(inventory):
        f.write(f"({item['product_id']}, {item['quantity']})")
        
        if idx < len(inventory) - 1:
            f.write(",\n")
        else:
            f.write(";\n")
    
    f.write("\n-- ===================== INSERT REVIEWS =====================\n")
    f.write("INSERT INTO reviews (id, user_id, product_id, feedback, score, created_at) VALUES\n")
    
    reviews = data['reviews']
    if reviews:
        for idx, review in enumerate(reviews):
            f.write(f"({review['id']}, {review['user_id']}, {review['product_id']}, {escape_sql(review['feedback'])}, {review['score']}, NOW())")
            
            if idx < len(reviews) - 1:
                f.write(",\n")
            else:
                f.write(";\n")

print("✓ Created insert_normalized_data.sql")
print(f"\nSQL file includes:")
print(f"- {len(products)} product INSERT statements")
print(f"- {len(images)} product image INSERT statements")
print(f"- {len(inventory)} inventory INSERT statements")
print(f"- {len(reviews)} review INSERT statements")
print("\nYou can now run: mysql -u user -p ecommerce < insert_normalized_data.sql")
