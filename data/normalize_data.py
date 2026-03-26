import json
import re
import csv
from datetime import datetime

# Read the raw data
with open('cellphones_full.json', 'r', encoding='utf-8') as f:
    raw_products = json.load(f)

# Function to extract brand from product name
def extract_brand(name):
    brands = {
        'iphone': 'Apple',
        'ipad': 'Apple',
        'samsung': 'Samsung',
        'galaxy': 'Samsung',
        'redmi': 'Xiaomi',
        'poco': 'Xiaomi',
        'oppo': 'OPPO',
        'vivo': 'Vivo',
        'realme': 'Realme',
        'honor': 'Honor',
        'google': 'Google',
        'pixel': 'Google',
        'nokia': 'Nokia',
        'oneplus': 'OnePlus',
        'asus': 'Asus',
        'motorola': 'Motorola',
        'moto': 'Motorola'
    }
    
    name_lower = name.lower()
    for key, brand in brands.items():
        if key in name_lower:
            return brand
    
    # Extract first word if no brand match
    first_word = name.split()[0]
    return first_word if first_word else 'Unknown'

# Function to parse price
def parse_price(price_str):
    if not price_str:
        return 0
    # Remove đ symbol and dots
    price_str = str(price_str).replace('đ', '').replace('.', '').replace('₫', '')
    try:
        return float(price_str.strip())
    except:
        return 0

# Function to calculate promotion
def calculate_promotion(current_price, old_price):
    if not old_price or current_price >= old_price:
        return 0
    discount = ((old_price - current_price) / old_price) * 100
    return int(round(discount))

# Prepare normalized data
products = []
product_images_data = []
reviews = []
inventory = []

for idx, item in enumerate(raw_products, 1):
    # Extract basic info
    name = item.get('name', '').strip()
    brand = extract_brand(name)
    
    current_price = parse_price(item.get('price', 0))
    old_price = parse_price(item.get('old_price', 0))
    promotion = calculate_promotion(current_price, old_price)
    
    # Build description from specifications
    specs = item.get('specifications', {})
    spec_text = '\n'.join([f"{k}: {v}" for k, v in specs.items()]) if specs else ""
    
    # Product summary
    summary = item.get('subtitle', '') or ""
    
    # Category extracted from specifications
    category = "Điện thoại"  # From the data, these are all phones
    
    product = {
        'id': idx,
        'name': name,
        'description': name,
        'detail': spec_text,
        'summary': summary[:255] if summary else "",
        'category': category,
        'price': current_price,
        'brand': brand,
        'promotion': promotion,
        'created_at': datetime.now().isoformat()
    }
    products.append(product)
    
    # Add images
    images = item.get('images', [])
    for img_idx, image_url in enumerate(images, 1):
        product_images_data.append({
            'id': len(product_images_data) + 1,
            'product_id': idx,
            'image_url': image_url
        })
    
    # Add inventory (assume 10 items for each product)
    inventory.append({
        'product_id': idx,
        'quantity': 10
    })
    
    # Add reviews if rating exists
    if item.get('rating'):
        try:
            rating_score = int(float(item.get('rating', 0)))
            if 1 <= rating_score <= 5:
                review = {
                    'id': len(reviews) + 1,
                    'user_id': 1,  # Placeholder - no user data in source
                    'product_id': idx,
                    'feedback': f"{name} - {item.get('rating_count', '')}",
                    'score': rating_score,
                    'created_at': datetime.now().isoformat()
                }
                reviews.append(review)
        except:
            pass

# Save products to CSV
print(f"Processing {len(products)} products...")

with open('normalized_products.csv', 'w', newline='', encoding='utf-8') as f:
    if products:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'description', 'detail', 'summary', 'category', 'price', 'brand', 'promotion', 'created_at'])
        writer.writeheader()
        writer.writerows(products)
print(f"✓ Saved {len(products)} products to normalized_products.csv")

# Save product images to CSV
with open('normalized_product_images.csv', 'w', newline='', encoding='utf-8') as f:
    if product_images_data:
        writer = csv.DictWriter(f, fieldnames=['id', 'product_id', 'image_url'])
        writer.writeheader()
        writer.writerows(product_images_data)
print(f"✓ Saved {len(product_images_data)} product images to normalized_product_images.csv")

# Save inventory to CSV
with open('normalized_inventory.csv', 'w', newline='', encoding='utf-8') as f:
    if inventory:
        writer = csv.DictWriter(f, fieldnames=['product_id', 'quantity'])
        writer.writeheader()
        writer.writerows(inventory)
print(f"✓ Saved {len(inventory)} inventory entries to normalized_inventory.csv")

# Save reviews to CSV
with open('normalized_reviews.csv', 'w', newline='', encoding='utf-8') as f:
    if reviews:
        writer = csv.DictWriter(f, fieldnames=['id', 'user_id', 'product_id', 'feedback', 'score', 'created_at'])
        writer.writeheader()
        writer.writerows(reviews)
print(f"✓ Saved {len(reviews)} reviews to normalized_reviews.csv")

# Save normalized JSON for reference
normalized_data = {
    'products': products,
    'product_images': product_images_data,
    'inventory': inventory,
    'reviews': reviews
}

with open('normalized_data.json', 'w', encoding='utf-8') as f:
    json.dump(normalized_data, f, ensure_ascii=False, indent=2)
print(f"✓ Saved normalized data to normalized_data.json")

print("\n=== Summary ===")
print(f"Products: {len(products)}")
print(f"Product Images: {len(product_images_data)}")
print(f"Inventory Entries: {len(inventory)}")
print(f"Reviews: {len(reviews)}")
