import json
import random
from datetime import datetime

# Load dữ liệu hiện tại
with open('phu_kien_enriched.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['products']
product_images = data['product_images']

# Chuẩn hoá sang cấu trúc SQL
normalized_products = []
normalized_images = []
normalized_inventory = []

for idx, product in enumerate(products, 1):
    # Lấy brand từ detail_name
    detail_name = product.get('detail_name', '')
    brand = 'Generic'
    if 'apple' in detail_name.lower():
        brand = 'Apple'
    elif 'samsung' in detail_name.lower():
        brand = 'Samsung'
    elif 'xiaomi' in detail_name.lower():
        brand = 'Xiaomi'
    elif 'oppo' in detail_name.lower():
        brand = 'OPPO'
    elif 'baseus' in detail_name.lower():
        brand = 'Baseus'
    elif 'anker' in detail_name.lower():
        brand = 'Anker'
    elif 'ugreen' in detail_name.lower():
        brand = 'UGreen'
    
    created_at = product.get('created_at', datetime.now().isoformat())
    
    # Tạo normalized product
    normalized_product = {
        'id': idx,
        'name': product.get('name', f'Phụ kiện {idx}'),
        'description': product.get('description_html', '').strip('<div></div>').replace('<h3>', '').replace('</h3>', ''),
        'detail': product.get('detail_name', ''),
        'summary': f"{product.get('name', f'Phụ kiện {idx}')} - Giá {product.get('price', 0):,}đ, Giảm {product.get('discount', 0)}%",
        'category': 'phu-kien',
        'price': product.get('price', 0),
        'brand': brand,
        'created_at': created_at,
        'updated_at': datetime.now().isoformat()
    }
    normalized_products.append(normalized_product)
    
    # Thêm inventory
    normalized_inventory.append({
        'product_id': idx,
        'quantity': random.randint(10, 100),
        'updated_at': datetime.now().isoformat()
    })

# Xử lý product_images - map lại product_id từ product_id 32 trở đi
for img in product_images:
    new_img = {
        'product_id': img['product_id'],
        'image_url': img['image_url']
    }
    normalized_images.append(new_img)

# Lưu cấu trúc normalized
output = {
    'products': normalized_products,
    'product_images': normalized_images,
    'inventory': normalized_inventory
}

with open('phu_kien_normalized.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✅ DỮ LIỆU ĐÃ CHUẨN HÓA THÀNH CÔNG!")
print()
print("📊 CẤU TRÚC DỮ LIỆU:")
print(f"  - Products: {len(normalized_products)}")
print(f"  - Product Images: {len(normalized_images)}")
print(f"  - Inventory: {len(normalized_inventory)}")
print()
print("📋 SAMPLE PRODUCT (id=1):")
print(json.dumps(normalized_products[0], ensure_ascii=False, indent=2))
print()
print("📸 SAMPLE IMAGE:")
if normalized_images:
    print(json.dumps(normalized_images[:2], ensure_ascii=False, indent=2))
print()
print("📦 SAMPLE INVENTORY:")
print(json.dumps(normalized_inventory[0], ensure_ascii=False, indent=2))
print()
print("📁 Output: phu_kien_normalized.json")
