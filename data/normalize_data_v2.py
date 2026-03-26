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
    
    first_word = name.split()[0]
    return first_word if first_word else 'Unknown'

# Function to parse price (VND to USD)
def parse_price(price_str):
    if not price_str:
        return 0
    price_str = str(price_str).replace('đ', '').replace('.', '').replace('₫', '')
    try:
        vnd_price = float(price_str.strip())
        # Convert VND to USD (1 USD = 25000 VND)
        usd_price = round(vnd_price / 25000, 2)
        return usd_price
    except:
        return 0

# Function to calculate promotion
def calculate_promotion(current_price, old_price):
    if not old_price or current_price >= old_price:
        return 0
    discount = ((old_price - current_price) / old_price) * 100
    return int(round(discount))

# Function to create rich description from specs
def create_rich_description(name, specs):
    """Create a more descriptive text from specifications"""
    description_parts = [name]
    
    # Add key specs to description
    key_specs = ['Camera sau', 'Camera trước', 'Chipset', 'Bộ nhớ trong', 'Dung lượng RAM', 'Hệ điều hành']
    for spec in key_specs:
        if spec in specs:
            description_parts.append(f"{spec}: {specs[spec]}")
    
    return " | ".join(description_parts)

# Function to create detailed summary
def create_detailed_summary(name, specs, price_usd):
    """Create a comprehensive product summary sentence"""
    summary_parts = []
    
    # Extract key info from specs
    screen_size = specs.get('Kích thước màn hình', '')
    camera_main = specs.get('Camera sau', '')
    ram = specs.get('Dung lượng RAM', '')
    storage = specs.get('Bộ nhớ trong', '')
    chipset = specs.get('Chipset', '')
    os = specs.get('Hệ điều hành', '')
    battery = specs.get('Pin', '')
    
    # Extract numbers from camera string
    main_camera_mp = ''
    if camera_main:
        import re
        match = re.search(r'(\d+)MP', camera_main)
        if match:
            main_camera_mp = match.group(1) + 'MP'
    
    # Build summary sentence
    summary_text = name
    
    if ram and storage:
        summary_text += f" - {ram} RAM, {storage} bộ nhớ"
    
    if main_camera_mp:
        summary_text += f", camera {main_camera_mp}"
    
    if screen_size:
        summary_text += f", màn hình {screen_size}"
    
    if price_usd > 0:
        summary_text += f" - Giá ${price_usd:.2f}"
    
    return summary_text[:255]

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
    
    # Build detailed specifications
    specs = item.get('specifications', {})
    spec_text = '\n'.join([f"• {k}: {v}" for k, v in specs.items()]) if specs else ""
    
    # Create rich summary and description
    summary = create_detailed_summary(name, specs, current_price)
    description = create_rich_description(name, specs)
    
    # Category with CODE format
    category = "DIEN_THOAI"  # All are phones
    
    product = {
        'name': name,
        'description': description[:255],
        'detail': spec_text[:2000] if spec_text else name,
        'summary': summary[:255],
        'category': category,
        'price': current_price,
        'brand': brand,
        'promotion': promotion
    }
    products.append(product)
    
    # Add images
    images = item.get('images', [])
    for img_idx, image_url in enumerate(images, 1):
        product_images_data.append({
            'product_id': idx,
            'image_url': image_url
        })
    
    # Add inventory (quantity = 10 for each product)
    inventory.append({
        'product_id': idx,
        'quantity': 10
    })
    
    # Add reviews if rating exists
    if item.get('rating'):
        try:
            rating_score = int(float(item.get('rating', 0)))
            if 1 <= rating_score <= 5:
                # Extract count from format like "(43 đánh giá)"
                rating_count_str = str(item.get('rating_count', ''))
                feedback = f"Đánh giá: {rating_count_str.replace('(', '').replace(')', '')} - {name}"
                
                review = {
                    'user_id': 1,
                    'product_id': idx,
                    'feedback': feedback[:2000],
                    'score': rating_score
                }
                reviews.append(review)
        except:
            pass

# Save products to CSV (without id and created_at)
print(f"Processing {len(products)} products...")

with open('normalized_products_v2.csv', 'w', newline='', encoding='utf-8') as f:
    if products:
        writer = csv.DictWriter(f, fieldnames=['name', 'description', 'detail', 'summary', 'category', 'price', 'brand', 'promotion'])
        writer.writeheader()
        writer.writerows(products)
print(f"✓ Saved {len(products)} products to normalized_products_v2.csv")

# Save product images to CSV
with open('normalized_product_images_v2.csv', 'w', newline='', encoding='utf-8') as f:
    if product_images_data:
        writer = csv.DictWriter(f, fieldnames=['product_id', 'image_url'])
        writer.writeheader()
        writer.writerows(product_images_data)
print(f"✓ Saved {len(product_images_data)} product images to normalized_product_images_v2.csv")

# Save inventory to CSV
with open('normalized_inventory_v2.csv', 'w', newline='', encoding='utf-8') as f:
    if inventory:
        writer = csv.DictWriter(f, fieldnames=['product_id', 'quantity'])
        writer.writeheader()
        writer.writerows(inventory)
print(f"✓ Saved {len(inventory)} inventory entries to normalized_inventory_v2.csv")

# Save reviews to CSV
with open('normalized_reviews_v2.csv', 'w', newline='', encoding='utf-8') as f:
    if reviews:
        writer = csv.DictWriter(f, fieldnames=['user_id', 'product_id', 'feedback', 'score'])
        writer.writeheader()
        writer.writerows(reviews)
print(f"✓ Saved {len(reviews)} reviews to normalized_reviews_v2.csv")

# Save normalized JSON for reference
normalized_data = {
    'products': products,
    'product_images': product_images_data,
    'inventory': inventory,
    'reviews': reviews
}

with open('normalized_data_v2.json', 'w', encoding='utf-8') as f:
    json.dump(normalized_data, f, ensure_ascii=False, indent=2)
print(f"✓ Saved normalized data to normalized_data_v2.json")

print("\n=== Summary ===")
print(f"Products: {len(products)}")
print(f"Product Images: {len(product_images_data)}")
print(f"Inventory Entries: {len(inventory)}")
print(f"Reviews: {len(reviews)}")
print(f"\nCategory Code Used: DIEN_THOAI")
print(f"Fields: name, description, detail, summary, category, price, brand, promotion")
print(f"(id and created_at excluded - they are auto-generated)")
