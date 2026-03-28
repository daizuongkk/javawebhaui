# 📚 Cellphones Scraper - Technical Specification

## Overview

**Universal Cellphones Scraper** là một bộ công cụ Python hoàn chỉnh để crawl dữ liệu từ cellphones.com.vn

**Các tính năng:**

- ✅ Hỗ trợ API scraping (tự động) + HTML fallback
- ✅ Xử lý lỗi tự động + retry logic
- ✅ Export JSON, SQL, CSV
- ✅ Product images tracking
- ✅ Inventory management
- ✅ Rate limiting thông minh

---

## Files và Mô tả

### Core Scripts

| File                             | Dòng | Mục đích          | Khuyến nghị     |
| -------------------------------- | ---- | ----------------- | --------------- |
| `scrape_cellphones.py`           | ~450 | Universal scraper | ⭐⭐⭐ USE THIS |
| `cellphones_scraper.py`          | ~400 | Basic scraper     | ⭐ Template     |
| `cellphones_advanced_scraper.py` | ~420 | Advanced scraper  | ⭐⭐ Production |
| `demo_scraper.py`                | ~280 | Demo & examples   | ⭐⭐ Learning   |
| `requirements.txt`               | 3    | Dependencies      | Must install    |

### Documentation

| File               | Mô tả             |
| ------------------ | ----------------- |
| `SCRAPER_GUIDE.md` | Quick start guide |
| `API_REFERENCE.md` | This file         |

---

## Class Reference

### `UniversalCellphonesScraper`

Main class trong `scrape_cellphones.py`

#### Constructor

```python
scraper = UniversalCellphonesScraper(delay=0.5)
```

**Parameters:**

- `delay` (float): Độ trễ giữa requests (giây). Default: 0.5. Khuyến nghị: 0.5-2.0

**Attributes:**

```python
.products : list          # Danh sách sản phẩm scraped
.images : list            # Hình ảnh sản phẩm
.inventory : list         # Dữ liệu kho hàng
.product_counter : int    # ID counter hiện tại
```

#### Methods

##### `scrape_all()`

Scrape tất cả categories

```python
scraper.scrape_all()
```

##### `scrape_category(category_key)`

Scrape một category cụ thể

```python
scraper.scrape_category('dien-thoai')
scraper.scrape_category('laptop')
```

**Available categories:**

- `dien-thoai` - Điện thoại
- `tablet` - Tablet
- `laptop` - Laptop
- `phu-kien` - Phụ kiện

##### `save_json(filename='cellphones_data.json')`

Export dữ liệu sang JSON

```python
scraper.save_json('my_products.json')
```

##### `save_sql(filename='cellphones_data.sql')`

Export dữ liệu sang SQL

```python
scraper.save_sql('import.sql')
```

##### `export(json_file='cellphones_data.json', sql_file='cellphones_data.sql')`

Export cả JSON và SQL cùng lúc

```python
scraper.export()
```

---

## Data Structures

### Product Object

```python
{
    'id': 1,                          # Product ID (auto-incremented)
    'name': 'iPhone 17 Pro',          # Product name
    'category': 'Điện thoại',         # Category
    'price': 28000000,                # Current price (VND)
    'old_price': 31000000,            # Original price (VND)
    'discount': 10,                   # Discount percentage
    'rating': 4.8,                    # Rating (0-5)
    'rating_count': 250,              # Number of reviews
    'image': 'https://...',           # Main image URL
    'description': None,              # Product description
    'created_at': '2026-03-28T...',   # Creation timestamp
    'updated_at': '2026-03-28T...'    # Update timestamp
}
```

### ProductImage Object

```python
{
    'product_id': 1,                  # Reference to product
    'image_url': 'https://...',       # Image URL
    'display_order': 1                # Display order (1-based)
}
```

### Inventory Object

```python
{
    'product_id': 1,                  # Reference to product
    'quantity': 50,                   # Available quantity
    'updated_at': '2026-03-28T...'    # Update timestamp
}
```

### Export Format

```python
{
    'metadata': {
        'source': 'cellphones.com.vn',
        'scraped_at': '2026-03-28T...',
        'total_products': 50,
        'total_images': 55,
        'categories': [...]
    },
    'products': [...],                # List of products
    'product_images': [...],          # List of images
    'inventory': [...]                # List of inventory
}
```

---

## Usage Examples

### Example 1: Basic Usage

```python
from scrape_cellphones import UniversalCellphonesScraper

# Create scraper
scraper = UniversalCellphonesScraper(delay=1.0)

# Scrape data
scraper.scrape_all()

# Export
scraper.export()
```

### Example 2: Selective Scraping

```python
scraper = UniversalCellphonesScraper()

# Only scrape specific categories
scraper.scrape_category('dien-thoai')
scraper.scrape_category('laptop')

# Export
scraper.save_json('smartphones_laptops.json')
```

### Example 3: Custom Processing

```python
scraper = UniversalCellphonesScraper(delay=0.3)
scraper.scrape_all()

# Process data
for product in scraper.products:
    if product['discount'] >= 10:
        print(f"{product['name']} - {product['discount']}% off")

# Save only
scraper.save_sql('high_discount_products.sql')
```

### Example 4: Data Analysis

```python
import json

scraper = UniversalCellphonesScraper()
scraper.scrape_category('dien-thoai')
scraper.save_json()

# Load and analyze
with open('cellphones_data.json') as f:
    data = json.load(f)

# Average price
avg_price = sum(p['price'] for p in data['products']) / len(data['products'])
print(f"Average price: {avg_price:,.0f} VND")

# High rated products
high_rated = [p for p in data['products'] if p['rating'] >= 4.5]
print(f"High rated: {len(high_rated)} products")
```

---

## SQL Schema

Generated SQL statements follow this schema:

### products table

```sql
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    price INT,
    old_price INT,
    discount INT,
    rating FLOAT,
    rating_count INT,
    image VARCHAR(500),
    created_at DATETIME,
    updated_at DATETIME
);
```

### product_images table

```sql
CREATE TABLE product_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    image_url VARCHAR(500),
    display_order INT,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### inventory table

```sql
CREATE TABLE inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT,
    updated_at DATETIME,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

---

## Configuration

### Available Settings

| Setting                | Type  | Default | Range  | Notes                            |
| ---------------------- | ----- | ------- | ------ | -------------------------------- |
| `delay`                | float | 0.5     | 0.1-10 | Delay between requests (seconds) |
| `timeout`              | int   | 10      | 5-60   | Request timeout (seconds)        |
| `max_products_per_cat` | int   | 15      | 1-100  | Products per category            |

### Modify Settings

```python
# Change delay
scraper = UniversalCellphonesScraper(delay=2.0)

# Modify timeout
scraper.session.timeout = 15

# Change max products
# (Edit code: for idx, prod in enumerate(products[:50]) )
```

---

## Error Handling

Script có built-in error handling:

```python
# HTTP errors
try:
    response = scraper.fetch(url)
    if response is None:
        logger.error("Failed to fetch")
except requests.RequestException as e:
    logger.error(f"Network error: {e}")

# Parse errors
try:
    product = scraper._parse_product(elem, category)
except Exception as e:
    logger.warning(f"Parse error: {e}")
```

### Common Issues

| Issue                   | Solution                                          |
| ----------------------- | ------------------------------------------------- |
| `403 Forbidden`         | Tăng delay hoặc sử dụng proxy                     |
| `429 Too Many Requests` | Tăng delay lên 2-3 giây                           |
| `Connection timeout`    | Tăng timeout lên 20-30 giây                       |
| `No products found`     | Kiểm tra CSS selectors, cấu trúc HTML có thay đổi |

---

## Performance

### Benchmarks

| Scenario              | Time  | Products | Notes      |
| --------------------- | ----- | -------- | ---------- |
| 1 category (15 items) | ~15s  | 15       | delay=0.5s |
| All categories        | ~60s  | 60       | delay=0.5s |
| High volume           | ~5min | 300      | delay=0.2s |

### Optimization Tips

1. **Reduce delay** (nhưng cẩn thận với rate limiting)

   ```python
   scraper = UniversalCellphonesScraper(delay=0.2)
   ```

2. **Limit categories**

   ```python
   scraper.scrape_category('dien-thoai')  # Chỉ 1 category
   ```

3. **Use threading** (advanced)
   ```python
   from concurrent.futures import ThreadPoolExecutor
   with ThreadPoolExecutor(max_workers=3) as executor:
       executor.map(scraper.scrape_category, [...])
   ```

---

## API Reference

### Network Methods

#### `fetch(url, timeout=10)`

Fetch raw HTML/JSON from URL with retry logic

```python
response = scraper.fetch('https://cellphones.com.vn/dien-thoai.html')
if response:
    print(response.text)
```

### Parsing Methods

#### `parse_price(price_text)`

Extract numeric price from text

```python
price = scraper.parse_price("28,000,000 VND")  # Returns: 28000000
price = scraper.parse_price("28 triệu")       # Returns: 28000000
```

#### `_parse_product(element, category)`

Parse single product from HTML element

```python
product = scraper._parse_product(html_elem, 'Điện thoại')
```

### Export Methods

#### `save_json(filename)`

Save products to JSON file

```python
scraper.save_json('products.json')
```

#### `save_sql(filename)`

Save products to SQL file

```python
scraper.save_sql('import.sql')
```

---

## Troubleshooting Guide

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
scraper = UniversalCellphonesScraper()
```

### Inspect Scraped Data

```python
print(f"Products: {len(scraper.products)}")
print(f"Images: {len(scraper.images)}")
print(f"Inventory: {len(scraper.inventory)}")

# First product
if scraper.products:
    print(json.dumps(scraper.products[0], indent=2))
```

### Check Network

```python
response = scraper.fetch('https://cellphones.com.vn')
print(f"Status: {response.status_code if response else 'Failed'}")
```

---

## Version History

| Version | Date       | Changes         |
| ------- | ---------- | --------------- |
| 1.0     | 2026-03-28 | Initial release |

---

## Support & Issues

- 📖 Check `SCRAPER_GUIDE.md` for quick start
- 🐛 Review error messages in console
- 🔧 Inspect website structure in browser DevTools
- 🌐 Update CSS selectors if website structure changes

---

**Last Updated**: 2026-03-28  
**Status**: ✅ Production Ready
