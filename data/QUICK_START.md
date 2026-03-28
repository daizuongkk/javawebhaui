# 🚀 QUICK START - Smart Scraper

## 📋 Cấu Trúc Dự Án

```
d:\code\Project\Web\web\data\
├── smart_scraper.py                    # 🌟 Script chính cào dữ liệu
├── WEB_STRUCTURE_ANALYSIS.md           # 📊 Phân tích cấu trúc website
├── QUICK_START.md                      # 📖 File này
├── cellphones_products.csv             # 📤 Output: CSV data
├── cellphones_products.json            # 📤 Output: JSON data
├── product.html                        # 📄 Sample HTML (category page)
├── details.html                        # 📄 Sample HTML (detail page)
└── ...
```

---

## 🎯 MỤC ĐÍCH

**Script `smart_scraper.py` sẽ:**

1. ✅ **Parse Meta Tags** từ HTML
   - `og:title` → Tên sản phẩm
   - `og:description` → Mô tả sản phẩm
   - `og:image` → Hình ảnh

2. ✅ **Parse JSON-LD** (Schema.org)
   - Cấu trúc dữ liệu có sẵn
   - Thông tin giá, rating, review

3. ✅ **Tạo dữ liệu bổ sung**
   - **Detail**: Specs kỹ thuật (tự generate theo category)
   - **Summary**: Tóm tắt tiếp thị
   - **Promotion**: Text khuyến mãi
   - **Brand**: Trích xuất từ tên sản phẩm

4. ✅ **Export thành CSV/JSON**
   - Format: `name, description, detail, summary, category, price, brand, promotion`
   - Giống `normalized_products_v2.csv`

---

## 🔧 CÀI ĐẶT

### 1️⃣ **Cài Đặt Dependencies**

```bash
pip install requests beautifulsoup4 lxml

# Hoặc tất cả:
pip install -r requirements.txt
```

**requirements.txt:**

```
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
```

### 2️⃣ **Chạy Script**

```bash
cd d:\code\Project\Web\web\data

# Cào dữ liệu (sẽ cào ~12 sản phẩm: 4 category × 3 products)
python smart_scraper.py

# Output:
# ✅ cellphones_products.csv (12 products)
# ✅ cellphones_products.json (12 products + metadata)
```

---

## 📊 OUTPUT MẪU

### CSV (`cellphones_products.csv`)

```csv
id,name,description,detail,summary,category,price,old_price,discount,brand,promotion,rating,rating_count,image,created_at
1,"Laptop ASUS TUF Gaming F16 FX607VJ-RL034W","Mua ngay giá rẻ...","• Chip: Intel Core i7\n• RAM: 16GB\n• SSD: 512GB","Laptop cao cấp cho công việc...","Laptop",29990000,30000000,0,"ASUS","Giảm 5%...",4.8,523,"https://cdn2.cellphones.com.vn/...",2026-03-28T10:30:00
2,"iPhone 15 Pro Max","Điện thoại flagship Apple...","• Display: 6.7\"\n• Chip: A17 Pro\n• Camera: 48MP","Điện thoại cao cấp nhất...","Điện thoại",32000000,35000000,8,"Apple","Flash sale: Giảm 8%",4.9,1203,"https://...",2026-03-28T10:31:00
```

### JSON (`cellphones_products.json`)

```json
{
  "metadata": {
    "source": "cellphones.com.vn",
    "scraped_at": "2026-03-28T10:35:00.123456",
    "total_products": 12,
    "total_images": 12
  },
  "products": [
    {
      "id": 1,
      "name": "Laptop ASUS TUF Gaming F16 FX607VJ-RL034W",
      "description": "Mua ngay giá rẻ - Hỗ trợ trả góp 0%...",
      "detail": "• Chip: Intel Core i7-13700H\n• RAM: 16GB\n• SSD: 512GB\n• Display: 15.6\" FHD",
      "summary": "Laptop cao cấp cho công việc và gaming...",
      "category": "Laptop",
      "price": 29990000,
      "old_price": 30000000,
      "discount": 0,
      "brand": "ASUS",
      "promotion": "Giảm 5% - Hàng có sẵn",
      "rating": 4.8,
      "rating_count": 523,
      "image": "https://cdn2.cellphones.com.vn/200x/media/catalog/product/...",
      "created_at": "2026-03-28T10:30:00.000000",
      "updated_at": "2026-03-28T10:30:00.123456"
    },
    ...
  ],
  "product_images": [
    {
      "product_id": 1,
      "image_url": "https://cdn2.cellphones.com.vn/...",
      "display_order": 1
    },
    ...
  ]
}
```

---

## 🎮 TUỲ CHỈNH SCRIPT

### 1. **Thay Đổi Số Lượng Sản Phẩm**

```python
# Line ~455
for category_code in scraper.CATEGORIES.keys():
    scraper.scrape_category(category_code, limit=5)  # ← Thay 5 thành số bạn muốn
```

### 2. **Thay Đổi Delay (politeness)**

```python
# Line ~438
scraper = SmartCellphonesScraper(delay=2)  # ← 2 giây delay giữa requests
```

### 3. **Chỉ Cào Một Category**

```python
scraper = SmartCellphonesScraper(delay=1)
scraper.scrape_category('dien-thoai', limit=10)  # Chỉ điện thoại
scraper.save_csv('smartphones.csv')
scraper.save_json('smartphones.json')
```

### 4. **Thay Đổi Output Filenames**

```python
# Line ~471
scraper.save_csv('my_products.csv')
scraper.save_json('my_products.json')
```

---

## 🔍 CÁCH HOẠT ĐỘNG CHI TIẾT

### **Step 1: Fetch Category Page**

```python
# GET https://cellphones.com.vn/dien-thoai.html
response = self.fetch_page("https://cellphones.com.vn/dien-thoai.html")
soup = BeautifulSoup(response.text, 'html.parser')
```

### **Step 2: Extract Product Links**

```python
# Tìm tất cả <a href="..."> có chứa category code
for link in soup.find_all('a', href=True):
    href = link.get('href', '')
    if 'dien-thoai' in href and href.endswith('.html'):
        product_links.append(href)

# ↓ Kết quả:
# ['https://cellphones.com.vn/iphone-15-pro.html',
#  'https://cellphones.com.vn/samsung-galaxy-s24.html',
#  ...]
```

### **Step 3: Fetch Product Detail Page**

```python
# GET https://cellphones.com.vn/iphone-15-pro.html
response = self.fetch_page("https://cellphones.com.vn/iphone-15-pro.html")
soup = BeautifulSoup(response.text, 'html.parser')
```

### **Step 4: Parse Meta Tags**

```python
# <meta property="og:title" content="iPhone 15 Pro | Giá tốt nhất">
og_title = soup.find('meta', {'property': 'og:title'})
name = og_title.get('content') if og_title else 'Unknown'
# Result: "iPhone 15 Pro"
```

### **Step 5: Parse JSON-LD**

```python
# <script type="application/ld+json">{"@type": "Product", ...}</script>
scripts = soup.find_all('script', {'type': 'application/ld+json'})
for script in scripts:
    json_ld = json.loads(script.string)
    if json_ld.get('@type') == 'Product':
        # Có: name, description, image, price, rating, v.v.
        return json_ld
```

### **Step 6: Xử Lý/Tạo Dữ Liệu Bổ Sung**

```python
brand = self._extract_brand(name)
# "iPhone 15 Pro" → "Apple"

detail = self._generate_detail_specs(category, name)
# Tạo: "• Display: 6.7\"\n• Chip: A17 Pro\n..."

summary = self._generate_summary(category)
# Tạo: "Điện thoại flagship với công nghệ hàng đầu..."

promotion = self._generate_promotion(discount)
# Tạo: "🔥 Giảm 15%..."
```

### **Step 7: Tạo Product Object**

```python
product = {
    'id': 1,
    'name': 'iPhone 15 Pro',
    'description': 'Mua ngay...',
    'detail': '• Display: 6.7"\n...',
    'summary': 'Điện thoại flagship...',
    'category': 'Điện thoại',
    'price': 29990000,
    'old_price': 30000000,
    'discount': 0,
    'brand': 'Apple',
    'promotion': 'Giảm 15%...',
    'rating': 4.9,
    'rating_count': 1203,
    'image': 'https://...'
}
```

### **Step 8: Lưu Output**

```python
# Lưu CSV
with open('cellphones_products.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=[...])
    writer.writeheader()
    writer.writerows(products)  # ← Tất cả products vào CSV

# Lưu JSON
with open('cellphones_products.json', 'w') as f:
    json.dump({'products': products, 'metadata': {...}}, f)
```

---

## 🛠️ TROUBLESHOOTING

### ❌ **Error: ModuleNotFoundError: No module named 'requests'**

```bash
pip install requests beautifulsoup4 lxml
```

### ❌ **Error: Connection timeout**

**Nguyên nhân**: Server chậm hoặc trang khó connect  
**Giải pháp**:

- Tăng delay: `SmartCellphonesScraper(delay=3)`
- Retry: Script đã có retry 3 lần built-in

### ❌ **Error: No products found**

**Nguyên nhân**: HTML structure thay đổi hoặc CSS selectors sai  
**Giải pháp**:

- Mở `details.html` + `product.html` để kiểm tra cấu trúc
- Update selectors trong script

### ❌ **Empty description/price**

**Nguyên nhân**: Meta tags hoặc JSON-LD thiếu dữ liệu  
**Giải pháp**: Script tự generate fallback (detail, summary, price random)

### ✅ **Mọi thứ chạy nhưng không có dữ liệu?**

1. Kiểm tra logs để thấy chi tiết
2. Mở file output CSV/JSON để kiểm tra
3. Verify internet connection

---

## 📈 SCALE UP

### **Cào Nhiều Trang**

```python
# Cào 10 sản phẩm/category × 4 category = 40 products
scraper = SmartCellphonesScraper(delay=1.5)
for category in scraper.CATEGORIES:
    scraper.scrape_category(category, limit=10)
scraper.save_csv('large_dataset.csv')
```

### **Cào Nhiều Category Trong Loop**

```python
all_categories = ['dien-thoai', 'tablet', 'laptop', 'phu-kien']
for cat in all_categories:
    scraper.scrape_category(cat, limit=20)
```

### **Đẩy Lên Database**

```python
import sqlite3

conn = sqlite3.connect('cellphones.db')
for product in scraper.products:
    conn.execute('''INSERT INTO products
        (name, description, detail, summary, category, price, brand)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (product['name'], product['description'], ...))
conn.commit()
```

---

## 📚 THAM KHẢO

- Cấu trúc website: [WEB_STRUCTURE_ANALYSIS.md](WEB_STRUCTURE_ANALYSIS.md)
- HTML Samples: `product.html`, `details.html`
- BeautifulSoup Docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Schema.org: https://schema.org/Product

---

## 💡 TIPS

1. **Sử dụng JSON-LD ưu tiên** - đã có cấu trúc, không phụ thuộc CSS selectors
2. **Thêm delays** - tránh bị block (1-2 giây là tốt)
3. **Log chi tiết** - giúp debug khi có vấn đề
4. **Fallback data** - script tự generate nếu thiếu
5. **Test với sample HTML** - trước khi scale

---

**Viết bởi**: Smart Scraper  
**Ngày**: 2026-03-28  
**Version**: 1.0.0
