import json
import csv

def generate_csv_files():
    """Sinh các file CSV cho dữ liệu phụ kiện chuẩn hóa"""
    
    with open("normalized_accessories_v2.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    products = data["products"]
    product_images = data["product_images"]
    
    # File 1: Products CSV
    with open("normalized_accessories_products_v2.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["product_id", "name", "brand", "category", "price", "promotion", "created_date", "description", "detail"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for idx, product in enumerate(products, 1):
            writer.writerow({
                "product_id": idx,
                "name": product["name"],
                "brand": product["brand"],
                "category": product["category"],
                "price": product["price"],
                "promotion": product["promotion"],
                "created_date": product["created_date"],
                "description": product["description"],
                "detail": product["detail"]
            })
    
    print("✓ Generated normalized_accessories_products_v2.csv")
    print(f"  - Total rows: {len(products)}")
    
    # File 2: Product Images CSV
    with open("normalized_accessories_product_images_v2.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["product_id", "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for image in product_images:
            writer.writerow({
                "product_id": image["product_id"],
                "image_url": image["image_url"]
            })
    
    print("✓ Generated normalized_accessories_product_images_v2.csv")
    print(f"  - Total rows: {len(product_images)}")
    
    # File 3: Inventory CSV (mô phỏng)
    with open("normalized_accessories_inventory_v2.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["product_id", "quantity", "warehouse", "last_updated"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for idx in range(1, len(products) + 1):
            import random
            from datetime import datetime
            writer.writerow({
                "product_id": idx,
                "quantity": random.randint(10, 100),
                "warehouse": "HCM" if idx % 2 == 0 else "HA NOI",
                "last_updated": datetime.now().isoformat()
            })
    
    print("✓ Generated normalized_accessories_inventory_v2.csv")
    print(f"  - Total rows: {len(products)}")
    
    # Print preview
    print("\n=== Preview normalized_accessories_products_v2.csv (first 5 rows) ===")
    with open("normalized_accessories_products_v2.csv", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i < 6:
                print(line.rstrip())

if __name__ == "__main__":
    generate_csv_files()
