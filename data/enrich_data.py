import json
import random
from datetime import datetime, timedelta

# Dữ liệu hình ảnh mẫu cho các loại phụ kiện
ACCESSORY_IMAGES = {
    'apple': [
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/a/i/airpods_pro_2.png',
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/a/i/airpods_max.jpg',
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/m/a/magsafe_charger.png',
    ],
    'sạc': [
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/s/a/sac_nhanh_65w.png',
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/s/a/sac_baseus.jpg',
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/s/a/sac_anker.jpg',
    ],
    'pin': [
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/p/i/pin_10000mah.png',
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/p/i/pin_20000mah.jpg',
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/p/i/pin_magsafe.png',
    ],
    'cáp': [
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/c/a/cap_lightning.png',
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/c/a/cap_usbc.jpg',
        'https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/c/a/cap_micro_usb.png',
    ],
}

def get_price_range(detail_name):
    """Xác định khoảng giá dựa trên loại phụ kiện"""
    detail_name_lower = detail_name.lower()
    
    if 'airpods' in detail_name_lower or 'max' in detail_name_lower:
        return (1000000, 9000000)
    elif 'tai nghe' in detail_name_lower or 'headphone' in detail_name_lower:
        return (200000, 3000000)
    elif 'sạc' in detail_name_lower or 'charger' in detail_name_lower:
        return (100000, 800000)
    elif 'pin' in detail_name_lower or 'power bank' in detail_name_lower:
        return (200000, 2000000)
    elif 'cáp' in detail_name_lower or 'cable' in detail_name_lower:
        return (50000, 500000)
    elif 'ốp' in detail_name_lower or 'case' in detail_name_lower:
        return (50000, 600000)
    elif 'kính cháy' in detail_name_lower or 'screen protector' in detail_name_lower:
        return (20000, 300000)
    else:
        return (100000, 2000000)

def get_images_for_product(detail_name, product_id):
    """Lấy hình ảnh phù hợp với loại sản phẩm"""
    detail_name_lower = detail_name.lower()
    
    # Chọn danh sách ảnh dựa trên keyword
    selected_images = ACCESSORY_IMAGES['sạc']  # mặc định
    
    if 'apple' in detail_name_lower:
        selected_images = ACCESSORY_IMAGES['apple']
    elif any(kw in detail_name_lower for kw in ['sạc', 'charger']):
        selected_images = ACCESSORY_IMAGES['sạc']
    elif any(kw in detail_name_lower for kw in ['pin', 'power bank']):
        selected_images = ACCESSORY_IMAGES['pin']
    elif 'cáp' in detail_name_lower or 'cable' in detail_name_lower:
        selected_images = ACCESSORY_IMAGES['cáp']
    
    # Lấy 3-5 ảnh random
    num_images = random.randint(3, 5)
    images = random.sample(selected_images, min(num_images, len(selected_images)))
    
    return images

def enrich_data():
    """Đọc file, sinh dữ liệu còn thiếu, và lưu"""
    with open('phu_kien_new.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Biến để lưu thông tin product_images
    product_images = []
    product_id = 1
    
    # Random date range (6 tháng gần đây)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    for product in data:
        # Sinh name từ detail_name nếu name bị null
        if product['name'] is None:
            product['name'] = product.get('detail_name', f'Phụ kiện {product_id}')
        
        detail_name = product['name']
        
        # Sinh giá tương thích với loại sản phẩm
        if product['price'] is None:
            price_range = get_price_range(detail_name)
            price = random.randint(price_range[0] // 10000, price_range[1] // 10000) * 10000
            product['price'] = price
        else:
            price = product['price']
        
        # Sinh old_price lớn hơn price (10-30% hơn)
        if product['old_price'] is None:
            increase_percent = random.randint(10, 30)
            product['old_price'] = int(price * (1 + increase_percent / 100))
        else:
            old_price = product['old_price']
        
        # Tính discount
        if product['discount'] is None:
            discount = round((product['old_price'] - product['price']) / product['old_price'] * 100)
            product['discount'] = discount
        
        # Sinh rating
        if product['rating'] is None:
            product['rating'] = round(random.uniform(3.5, 5.0), 1)
        
        # Sinh rating_count
        if product['rating_count'] is None:
            product['rating_count'] = random.randint(10, 2000)
        
        # Sinh created_at
        random_days = random.randint(0, 180)
        created_at = (start_date + timedelta(days=random_days)).isoformat()
        product['created_at'] = created_at
        
        # Sinh specification đơn giản
        if not product.get('specifications'):
            specs = {}
            if any(kw in detail_name.lower() for kw in ['pin', 'power bank']):
                specs['Dung lượng'] = f'{random.choice([10000, 20000, 25000])} mAh'
                specs['Công suất'] = f'{random.choice([18, 20, 22, 25])} W'
            elif any(kw in detail_name.lower() for kw in ['sạc', 'charger']):
                specs['Công suất'] = f'{random.choice([20, 30, 45, 65, 100])} W'
                specs['Loại đầu'] = random.choice(['USB-C', 'Lightning', 'Micro USB'])
            elif 'cáp' in detail_name.lower():
                specs['Độ dài'] = f'{random.choice([1, 1.5, 2])} m'
                specs['Loại'] = random.choice(['USB-C to USB-C', 'Lightning', 'Micro USB'])
            
            product['specifications'] = specs
        
        # Sinh description_html
        if product['description_html'] is None:
            product['description_html'] = f"""
            <div>
                <h3>{detail_name}</h3>
                <p>Sản phẩm chính hãng, bảo hành chính thức.</p>
                <p>Giá cực tốt. Mua ngay để nhận ưu đãi đặc biệt.</p>
            </div>
            """
        
        # Tạo product_images bắt đầu từ product_id 32
        if product_id >= 32:
            images = get_images_for_product(detail_name, product_id)
            for img_url in images:
                product_images.append({
                    'product_id': product_id,
                    'image_url': img_url,
                    'alt_text': f'{detail_name} - Hình {len([p for p in product_images if p["product_id"] == product_id]) + 1}',
                    'display_order': len([p for p in product_images if p["product_id"] == product_id]) + 1
                })
        
        product_id += 1
    
    # Lưu dữ liệu enriched
    output_data = {
        'products': data,
        'product_images': product_images
    }
    
    with open('phu_kien_enriched.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dữ liệu đã được sinh thành công!")
    print(f"   - Tổng sản phẩm: {len(data)}")
    print(f"   - Tổng ảnh (từ product_id 32): {len(product_images)}")
    print(f"   - File output: phu_kien_enriched.json")
    
    # Hiển thị mẫu dữ liệu
    print("\n📊 Mẫu dữ liệu product (id=1):")
    print(json.dumps(data[0], ensure_ascii=False, indent=2)[:500] + "...")
    
    print("\n📸 Mẫu dữ liệu product_images:")
    if product_images:
        print(json.dumps(product_images[:2], ensure_ascii=False, indent=2))

if __name__ == '__main__':
    enrich_data()
