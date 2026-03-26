import json
import csv
from datetime import datetime

# Read normalized data v2
with open('normalized_data_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Helper function to escape SQL strings
def escape_sql(value):
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"

# Create SQL file
with open('insert_normalized_data_v2.sql', 'w', encoding='utf-8') as f:
    f.write("-- ===================== INSERT PRODUCTS =====================\n")
    f.write("-- Category Code: DIEN_THOAI (Điện thoại)\n")
    f.write("INSERT INTO products (name, description, detail, summary, category, price, brand, promotion) VALUES\n")
    
    products = data['products']
    for idx, product in enumerate(products):
        f.write(f"({escape_sql(product['name'])}, {escape_sql(product['description'])}, {escape_sql(product['detail'])}, {escape_sql(product['summary'])}, {escape_sql(product['category'])}, {product['price']}, {escape_sql(product['brand'])}, {product['promotion']})")
        
        if idx < len(products) - 1:
            f.write(",\n")
        else:
            f.write(";\n")
    
    f.write("\n-- ===================== INSERT PRODUCT IMAGES =====================\n")
    f.write("INSERT INTO product_images (product_id, image_url) VALUES\n")
    
    images = data['product_images']
    for idx, image in enumerate(images):
        f.write(f"({image['product_id']}, {escape_sql(image['image_url'])})")
        
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
    f.write("INSERT INTO reviews (user_id, product_id, feedback, score) VALUES\n")
    
    reviews = data['reviews']
    if reviews:
        for idx, review in enumerate(reviews):
            f.write(f"({review['user_id']}, {review['product_id']}, {escape_sql(review['feedback'])}, {review['score']})")
            
            if idx < len(reviews) - 1:
                f.write(",\n")
            else:
                f.write(";\n")

print("✓ Created insert_normalized_data_v2.sql")
print(f"\nSQL file includes:")
print(f"- {len(products)} product INSERT statements (without id, created_at)")
print(f"- {len(images)} product image INSERT statements")
print(f"- {len(inventory)} inventory INSERT statements")
print(f"- {len(reviews)} review INSERT statements")
print(f"\nCategory Code: DIEN_THOAI")
print(f"\nUsage: mysql -u user -p ecommerce < insert_normalized_data_v2.sql")
