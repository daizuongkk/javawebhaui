# Dữ Liệu Phụ Kiện Chuẩn Hóa V2

## 📊 Tóm Tắt

Dữ liệu phụ kiện đã được sinh tự động và chuẩn hóa theo format v2, tương tự như dữ liệu điện thoại.

### 📈 Thống Kê Dữ Liệu

| Loại Dữ Liệu          | Số Lượng            |
| --------------------- | ------------------- |
| **Tổng Sản Phẩm**     | 24                  |
| **Hình Ảnh Sản Phẩm** | 72 (3 ảnh/sản phẩm) |
| **Review/Đánh Giá**   | 72                  |
| **Danh Mục**          | 6                   |

### 📂 Cấu Trúc Dữ Liệu

#### 1. Danh Mục Phụ Kiện

```
- Cáp, Sạc Điện Thoại iPhone, Android (5 sản phẩm)
  * Lightning Cable 2m - Apple
  * USB-C Fast Charger 65W - Belkin
  * USB-C Cable 3.1 2m - Anker
  * Super Fast Charger 45W - Samsung
  * GaN Charger 120W 4 Port - Baseus

- Dán Màn Hình Điện Thoại (3 sản phẩm)
  * Tempered Glass H+ Pro - Nillkin
  * Screen Protector Clear 3D - Tech21
  * Tempered Glass Premium - ESR

- Phụ Kiện Apple (4 sản phẩm)
  * AirPods Pro 2nd Gen
  * AirTag
  * Magic Mouse 2
  * Smart Keyboard Folio

- Pin Dự Phòng (3 sản phẩm)
  * PowerCore 26800mAh - Anker
  * Mi Power Bank 3 Pro 20000mAh - Xiaomi
  * 25000mAh Fast Charging - Samsung

- Sim 5G | 4G | 3G (3 sản phẩm)
  * Sim 4G Viettel MAX15
  * Sim 5G Mobifone MAX10
  * Sim 5G Vinaphone 4G60

- Thẻ Nhớ, USB (3 sản phẩm)
  * Ultra microSD 256GB - SanDisk
  * DataTraveler USB 3.0 64GB - Kingston
  * microSD Card Pro 128GB - Samsung

- Ốp Lưng Điện Thoại | Bao Da (3 sản phẩm)
  * Rugged Armor Case - Spigen
  * Defender Series Case - OtterBox
  * Silicone Case - Apple
```

## 📁 Các File Được Tạo

### 1. **normalized_accessories_v2.json**

- **Kích thước:** 42.48 KB
- **Nội dung:** Dữ liệu JSON đầy đủ (products, product_images, reviews)
- **Cấu trúc:**
  ```json
  {
    "products": [...],
    "product_images": [...],
    "reviews": [...]
  }
  ```

### 2. **normalized_accessories_products_v2.csv**

- **Kích thước:** 10.45 KB
- **Cột:** product_id, name, brand, category, price, promotion, description, detail
- **Số dòng:** 24 (sản phẩm)
- **Sử dụng:** Import vào bảng `products`

### 3. **normalized_accessories_product_images_v2.csv**

- **Kích thước:** 5.20 KB
- **Cột:** product_id, image_url
- **Số dòng:** 72 (3 ảnh/sản phẩm)
- **Sử dụng:** Import vào bảng `product_images`

### 4. **normalized_accessories_inventory_v2.csv**

- **Kích thước:** 0.96 KB
- **Cột:** product_id, quantity, warehouse, last_updated
- **Số dòng:** 24 (tồn kho)
- **Sử dụng:** Import vào bảng `inventory` hoặc `product_inventory`

### 5. **insert_accessories_normalized_v2.sql**

- **Nội dung:** SQL INSERT statements
- **Gồm:** INSERT products + INSERT product_images
- **Sử dụng:** Chạy trực tiếp trên database

## 🔧 Cách Sử Dụng

### Option 1: Import sử dụng SQL

```bash
# Chạy file SQL trực tiếp
mysql -u root -p database_name < insert_accessories_normalized_v2.sql
```

### Option 2: Import CSV vào Database

```bash
# Sử dụng MySQL LOAD DATA INFILE
LOAD DATA INFILE 'normalized_accessories_products_v2.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'normalized_accessories_product_images_v2.csv'
INTO TABLE product_images
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

### Option 3: Sử dụng Python/Node.js

```python
import json

with open('normalized_accessories_v2.json', 'r', encoding='utf-8') as f:
    accessories_data = json.load(f)

# Xử lý dữ liệu
products = accessories_data['products']
images = accessories_data['product_images']

for product in products:
    # Thêm vào database
    insert_product(product)
```

## 📋 Chi Tiết Cấu Trúc Dữ Liệu

### Products Schema

```json
{
  "name": "Lightning Cable 2m",
  "description": "Cáp Lightning chính hãng Apple...",
  "detail": "• Chiều dài: 2 mét\n• Loại kết nối: Lightning...",
  "summary": "Lightning Cable 2m - Cáp Lightning chính hãng...",
  "category": "CÁP,_SẠC_ĐIỆN_THOẠI_IPHONE,_AN",
  "price": 25.0,
  "brand": "Apple",
  "promotion": 10
}
```

### Product Images Schema

```json
{
  "product_id": 1,
  "image_url": "https://cdn.example.com/accessories/apple/lightning-cable-2m-1.jpg"
}
```

### Reviews Schema

```json
{
  "product_id": 1,
  "rating": 5,
  "comment": "Sản phẩm chất lượng tốt, đúng với mô tả...",
  "created_date": "2026-03-28T10:30:45.123456"
}
```

## 💡 Thông Tin Bổ Sung

### Giá Sản Phẩm

- **Giá thấp nhất:** $2.49 (Sim 5G Mobifone)
- **Giá cao nhất:** $299.99 (AirPods Pro 2nd Gen)
- **Giá trung bình:** ~$45 USD

### Mức Giảm Giá (Promotion)

- **Từ 0% đến 20%** tùy sản phẩm
- **Trung bình:** ~10%

### Thương Hiệu

Apple, Samsung, Xiaomi, Anker, Belkin, Baseus, SanDisk, Kingston, Viettel, Mobifone, Vinaphone, v.v.

## 🛠️ Sinh Tạo Dữ Liệu

Dữ liệu được sinh tự động sử dụng các script Python:

1. **generate_accessories_v2.py** - Sinh JSON
2. **generate_accessories_sql_v2.py** - Sinh SQL
3. **generate_accessories_csv_v2.py** - Sinh CSV

### Chạy lại để cập nhật dữ liệu:

```bash
python generate_accessories_v2.py
python generate_accessories_sql_v2.py
python generate_accessories_csv_v2.py
```

## ✅ Kiểm Tra Dữ Liệu

### Kiểm tra JSON

```bash
python -c "import json; data = json.load(open('normalized_accessories_v2.json')); print(f'Products: {len(data[\"products\"])}'); print(f'Images: {len(data[\"product_images\"])}')"
```

### Kiểm tra CSV

```bash
wc -l normalized_accessories_*.csv
```

## 📝 Ghi Chú

- Tất cả dữ liệu được sinh **tự động** và có thể tái tạo
- Dữ liệu được **chuẩn hóa** theo format v2
- Các URL hình ảnh là **mẫu** (placeholder) và có thể thay thế
- Các mô tả sản phẩm là **chính xác theo thực tế**
- Giá tiền được tính bằng **USD**

## 🎯 Lợi Ích

✅ Dữ liệu **đầy đủ** cho 24 sản phẩm  
✅ **Chuẩn hóa** theo format v2  
✅ Có **hình ảnh** (3 ảnh/sản phẩm)  
✅ Có **review/đánh giá**  
✅ Có **thông tin tồn kho**  
✅ Hỗ trợ nhiều **định dạng** (JSON, CSV, SQL)  
✅ Dễ **import** vào database  
✅ Dễ **tái tạo** lại dữ liệu

---

**Ngày tạo:** 2026-03-28  
**Phiên bản:** v2.0  
**Trạng thái:** ✅ Hoàn thành
