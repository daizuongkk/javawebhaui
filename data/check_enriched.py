import json

data = json.load(open('phu_kien_enriched.json', 'r', encoding='utf-8'))
products = data['products']
images = data['product_images']

print('📊 THỐNG KÊ DỮ LIỆU:')
print(f'  Tổng sản phẩm: {len(products)}')
print(f'  Tổng hình ảnh: {len(images)}')

print()
print('💰 KIỂM SOÁT GIÁ CỦA 5 SẢN PHẨM ĐẦU:')
for i, p in enumerate(products[:5]):
    name = p['name'][:30] if p['name'] else 'N/A'
    price = p['price'] if p['price'] else 0
    old_price = p['old_price'] if p['old_price'] else 0
    discount = p['discount'] if p['discount'] else 0
    print(f'  {i+1}. {name:30} | Price: {price:,} | Old: {old_price:,} | Discount: {discount}%')

print()
print('📸 KIỂM SOÁT HỆ THỐNG IMAGE (từ product_id 32):')
product_ids = sorted(set(img['product_id'] for img in images))
print(f'  Product IDs có hình: {product_ids}')
for pid in product_ids:
    count = len([img for img in images if img['product_id'] == pid])
    print(f'  Product {pid}: {count} ảnh')

print()
print('✅ CREATED_AT SAMPLES:')
for i in [0, 9, 19, 29, 34]:
    if i < len(products):
        created = products[i].get('created_at', 'N/A')
        name = products[i].get('name', 'N/A')
        print(f'  Product {i+1} ({name[:25]}) -> {created}')

print()
print('==================')
print('✅ DỮ LIỆU ĐÃ SINH THÀNH CÔNG!')
print('📁 File: phu_kien_enriched.json')
print('==================')
