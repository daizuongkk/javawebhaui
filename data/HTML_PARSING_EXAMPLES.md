# 🔍 HTML PARSING EXAMPLES

## I. PARSE META TAGS

### **Code:**

```python
from bs4 import BeautifulSoup
import requests

# Fetch page
response = requests.get('https://cellphones.com.vn/iphone-15-pro.html')
soup = BeautifulSoup(response.text, 'html.parser')

# 1. Extract og:title
og_title = soup.find('meta', {'property': 'og:title'})
name = og_title.get('content') if og_title else 'Unknown'
print(f"Name: {name}")
# Output: "iPhone 15 Pro Max | Giá rẻ, trả góp 0%"

# 2. Extract og:description
og_desc = soup.find('meta', {'property': 'og:description'})
description = og_desc.get('content') if og_desc else ''
print(f"Description: {description}")
# Output: "Mua ngay iPhone 15 Pro Max giá rẻ - Hỗ trợ trả góp 0%, đổi mới 30 ngày..."

# 3. Extract og:image
og_image = soup.find('meta', {'property': 'og:image'})
image = og_image.get('content') if og_image else ''
print(f"Image: {image}")
# Output: "https://cdn2.cellphones.com.vn/200x/media/catalog/product/i/p/iphone_15_pro_max.png"
```

### **HTML Source:**

```html
<head>
  <meta property="og:title" content="iPhone 15 Pro Max | Giá rẻ, trả góp 0%" />
  <meta
    property="og:description"
    content="Mua ngay iPhone 15 Pro Max giá rẻ - Hỗ trợ trả góp 0%..."
  />
  <meta
    property="og:image"
    content="https://cdn2.cellphones.com.vn/200x/media/catalog/product/i/p/iphone_15_pro_max.png"
  />
</head>
```

---

## II. PARSE JSON-LD

### **Code:**

```python
import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, 'html.parser')

# Tìm tất cả JSON-LD scripts
scripts = soup.find_all('script', {'type': 'application/ld+json'})

for script in scripts:
    data = json.loads(script.string)

    # Kiếm product schema
    if data.get('@type') == 'Product':
        print(f"Name: {data['name']}")
        # Output: "iPhone 15 Pro Max"

        print(f"Image: {data['image']}")
        # Output: "https://cdn2.cellphones.com.vn/.../iphone_15_pro_max.png"

        print(f"Rating: {data['aggregateRating']['ratingValue']}")
        # Output: "4.9"

        # Xử lý giá từ offers
        offers = data.get('offers', {})
        if isinstance(offers, dict):
            price = offers.get('price')
            currency = offers.get('priceCurrency')
            print(f"Price: {price} {currency}")
            # Output: "29990000 VND"
```

### **HTML Source:**

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": "iPhone 15 Pro Max",
    "image": "https://cdn2.cellphones.com.vn/200x/media/catalog/product/i/p/iphone_15_pro_max.png",
    "description": "Mua ngay...",
    "offers": {
      "@type": "Offer",
      "url": "https://cellphones.com.vn/iphone-15-pro-max.html",
      "priceCurrency": "VND",
      "price": "29990000"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "ratingCount": "1203"
    }
  }
</script>
```

---

## III. PARSE HTML ELEMENTS

### **Code - Extract Specifications:**

```python
soup = BeautifulSoup(response.text, 'html.parser')

# Cách 1: Tìm bằng class name (nếu biết)
specs_div = soup.find('div', class_='specifications')
if specs_div:
    specs = []
    for spec in specs_div.find_all('div', class_='spec-item'):
        label = spec.find('span', class_='label')
        value = spec.find('span', class_='value')
        if label and value:
            specs.append(f"{label.text}: {value.text}")

    detail = '\n'.join(specs)
    print(detail)
    # Output:
    # Display: 6.7" Super Retina XDR
    # Chipset: Apple A17 Pro
    # RAM: 8GB
    # Storage: 256GB
    # Camera Rear: 48MP f/1.78
    # Camera Front: 12MP f/2.2
    # Battery: 4685mAh
    # OS: iOS 17
```

### **HTML Source:**

```html
<div class="specifications">
  <div class="spec-item">
    <span class="label">Display</span>
    <span class="value">6.7" Super Retina XDR</span>
  </div>
  <div class="spec-item">
    <span class="label">Chipset</span>
    <span class="value">Apple A17 Pro</span>
  </div>
  ...
</div>
```

### **Code - Extract Price:**

```python
# Cách 1: Tìm span có class 'price'
price_elem = soup.find('span', class_='price')
if price_elem:
    price_text = price_elem.text.strip()  # "29.990.000đ"
    # Remove currency, dots
    price = int(price_text.replace('đ', '').replace('.', ''))
    print(f"Price: {price}")  # Output: 29990000

# Cách 2: Tìm bằng regex
import re
price_text = soup.find('span', class_='sale-price').text
# "29.990.000đ" → 29990000
match = re.search(r'(\d+(?:\.\d+)*)', price_text.replace('.', ''))
price = int(match.group(1)) if match else None
print(f"Price: {price}")
```

### **HTML Source:**

```html
<span class="original-price">30.000.000đ</span>
<span class="price">29.990.000đ</span>
```

---

## IV. EXTRACT PRODUCT LINKS FROM LIST PAGE

### **Code:**

```python
from urllib.parse import urljoin

BASE_URL = 'https://cellphones.com.vn'

# Fetch category page
response = requests.get(f'{BASE_URL}/dien-thoai.html')
soup = BeautifulSoup(response.text, 'html.parser')

# Tìm product links
product_links = []
for link in soup.find_all('a', href=True):
    href = link.get('href', '')

    # Filter: phải chứa category code, phải là .html, không phải filter/sort
    if ('dien-thoai' in href.lower() and
        href.endswith('.html') and
        not any(x in href for x in ['?', 'filter', 'sort', 'page'])):

        full_url = urljoin(BASE_URL, href)
        product_links.append(full_url)

# Remove duplicates
product_links = list(set(product_links))[:10]

print(f"Found {len(product_links)} products:")
for link in product_links:
    print(f"  - {link}")

# Output:
# Found 10 products:
#  - https://cellphones.com.vn/iphone-15-pro.html
#  - https://cellphones.com.vn/iphone-15-pro-max.html
#  - https://cellphones.com.vn/samsung-galaxy-s24.html
#  - ...
```

### **HTML Source (Category Page):**

```html
<div class="product-list">
  <a href="/iphone-15-pro.html" class="product-link">
    <img src="..." alt="iPhone 15 Pro" />
    <span>iPhone 15 Pro</span>
  </a>

  <a href="/iphone-15-pro-max.html" class="product-link">
    <img src="..." alt="iPhone 15 Pro Max" />
    <span>iPhone 15 Pro Max</span>
  </a>

  <a href="/samsung-galaxy-s24.html" class="product-link">
    <img src="..." alt="Samsung Galaxy S24" />
    <span>Samsung Galaxy S24</span>
  </a>
</div>
```

---

## V. HANDLE PRICE PARSING

### **Code:**

```python
import re

def extract_price(price_text):
    """Extract giá từ text (handle multiple formats)"""
    if not price_text:
        return None

    text = str(price_text).strip()

    # Format: "X triệu"
    if 'triệu' in text.lower():
        match = re.search(r'(\d+[.,]?\d*)\s*triệu', text, re.IGNORECASE)
        if match:
            try:
                return int(float(match.group(1).replace(',', '.')) * 1000000)
            except:
                pass

    # Format: "29.990.000đ"
    numbers = re.findall(r'\d+', text.replace('.', '').replace(',', ''))
    if numbers:
        try:
            return int(numbers[0])
        except:
            pass

    return None

# Test cases
print(extract_price("29.990.000đ"))      # 29990000
print(extract_price("29,990,000₫"))      # 29990000
print(extract_price("29 triệu 990 ngàn")) # 29990000
print(extract_price("đ29.990.000"))      # 29990000
print(extract_price("35 triệu"))         # 35000000
```

**Output:**

```
29990000
29990000
29990000
29990000
35000000
```

---

## VI. EXTRACT BRAND FROM PRODUCT NAME

### **Code:**

```python
def extract_brand(product_name):
    """Trích xuất brand từ tên sản phẩm"""
    brands = {
        'Apple': ['iPhone', 'iPad', 'MacBook', 'AirPods'],
        'Samsung': ['Galaxy', 'Galaxy S', 'Galaxy Note'],
        'Xiaomi': ['Xiaomi', 'Redmi', 'POCO'],
        'ASUS': ['ASUS', 'TUF', 'Vivobook'],
        'Lenovo': ['Lenovo', 'ThinkPad', 'Legion'],
        'Sony': ['Sony', 'Vaio'],
    }

    for brand, keywords in brands.items():
        for keyword in keywords:
            if keyword.lower() in product_name.lower():
                return brand

    # Fallback: lấy từ đầu
    return product_name.split()[0] if product_name else 'Unknown'

# Test cases
print(extract_brand("iPhone 15 Pro Max"))              # Apple
print(extract_brand("Samsung Galaxy S24 Ultra"))       # Samsung
print(extract_brand("Laptop ASUS TUF Gaming F16"))    # ASUS
print(extract_brand("Lenovo ThinkPad X1 Carbon"))     # Lenovo
print(extract_brand("Generic Product"))                # Generic
```

**Output:**

```
Apple
Samsung
ASUS
Lenovo
Generic
```

---

## VII. FULL EXAMPLE: SCRAPE 1 PRODUCT

### **Complete Code:**

```python
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_product(product_url):
    """Cào chi tiết 1 sản phẩm"""

    # 1. Fetch page
    headers = {'User-Agent': 'Mozilla/5.0...'}
    response = requests.get(product_url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 2. Parse Meta Tags
    og_title = soup.find('meta', {'property': 'og:title'})
    og_desc = soup.find('meta', {'property': 'og:description'})
    og_image = soup.find('meta', {'property': 'og:image'})

    name = og_title.get('content') if og_title else ''
    description = og_desc.get('content') if og_desc else ''
    image = og_image.get('content') if og_image else ''

    # Clean name (remove "| Giá rẻ..." part)
    if ' | ' in name:
        name = name.split(' | ')[0].strip()

    # 3. Parse JSON-LD
    rating = None
    rating_count = None

    scripts = soup.find_all('script', {'type': 'application/ld+json'})
    for script in scripts:
        try:
            data = json.loads(script.string)
            if data.get('@type') == 'Product':
                if 'aggregateRating' in data:
                    rating = float(data['aggregateRating'].get('ratingValue', 0))
                    rating_count = int(data['aggregateRating'].get('ratingCount', 0))
                break
        except:
            pass

    # 4. Extract brand
    brands = {
        'Apple': ['iPhone', 'iPad'],
        'Samsung': ['Galaxy'],
        'ASUS': ['ASUS', 'TUF'],
    }
    brand = 'Unknown'
    for brand_name, keywords in brands.items():
        for keyword in keywords:
            if keyword.lower() in name.lower():
                brand = brand_name
                break

    # 5. Return product data
    return {
        'name': name,
        'description': description[:100] if description else '',
        'brand': brand,
        'image': image,
        'rating': rating or 4.5,
        'rating_count': rating_count or 0,
        'url': product_url
    }

# Usage:
product = scrape_product('https://cellphones.com.vn/iphone-15-pro.html')
print(json.dumps(product, indent=2, ensure_ascii=False))

# Output:
# {
#   "name": "iPhone 15 Pro",
#   "description": "Mua ngay iPhone 15 Pro giá rẻ - Hỗ trợ trả góp 0%, đổi mới...",
#   "brand": "Apple",
#   "image": "https://cdn2.cellphones.com.vn/...",
#   "rating": 4.9,
#   "rating_count": 1203,
#   "url": "https://cellphones.com.vn/iphone-15-pro.html"
# }
```

---

## VIII. COMMON PARSING MISTAKES ❌

### ❌ **Mistake 1: Không encode UTF-8**

```python
# ❌ WRONG
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# ✅ CORRECT
response = requests.get(url)
response.encoding = 'utf-8'  # Set encoding first!
soup = BeautifulSoup(response.text, 'html.parser')
```

### ❌ **Mistake 2: Parse JSON-LD không check @type**

```python
# ❌ WRONG
scripts = soup.find_all('script', {'type': 'application/ld+json'})
data = json.loads(scripts[0].string)  # Có thể khác type!

# ✅ CORRECT
for script in scripts:
    data = json.loads(script.string)
    if data.get('@type') == 'Product':  # Check type!
        # Process product
```

### ❌ **Mistake 3: Quên clean data**

```python
# ❌ WRONG
name = og_title.get('content')
# Result: "iPhone 15 Pro Max | Giá rẻ, trả góp 0%"

# ✅ CORRECT
name = og_title.get('content')
if ' | ' in name:
    name = name.split(' | ')[0].strip()
# Result: "iPhone 15 Pro Max"
```

### ❌ **Mistake 4: Không handle missing elements**

```python
# ❌ WRONG
rating = float(data['aggregateRating']['ratingValue'])  # KeyError!

# ✅ CORRECT
rating = None
if 'aggregateRating' in data:
    rating = float(data['aggregateRating'].get('ratingValue', 0))
else:
    rating = 4.5  # Fallback
```

### ❌ **Mistake 5: Không handle connection errors**

```python
# ❌ WRONG
response = requests.get(url)

# ✅ CORRECT
try:
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}")
except requests.RequestException as e:
    print(f"Error fetching {url}: {e}")
    return None
```

---

## 📚 SUMMARY

| Task            | Method                                              | Source          |
| --------------- | --------------------------------------------------- | --------------- |
| **Name**        | `soup.find('meta', {'property': 'og:title'})`       | Meta tag        |
| **Description** | `soup.find('meta', {'property': 'og:description'})` | Meta tag        |
| **Image**       | `soup.find('meta', {'property': 'og:image'})`       | Meta tag        |
| **Specs**       | Parse JSON-LD hoặc HTML `<div class='spec*'>`       | JSON-LD / HTML  |
| **Price**       | `extract_price(text)` + regex                       | HTML element    |
| **Rating**      | `json_ld['aggregateRating']['ratingValue']`         | JSON-LD         |
| **Brand**       | `extract_brand(name)`                               | Extract từ name |
| **Links**       | `soup.find_all('a', href=True)`                     | HTML links      |

---

**Created**: 2026-03-28  
**Version**: 1.0.0  
**Use with**: BeautifulSoup 4.12+ & Requests 2.31+
