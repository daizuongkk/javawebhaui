# 📊 Phân Tích Cấu Trúc Website Cellphones.com.vn

## I. CẤU TRÚC WEBSITE

### 1. **Technology Stack**

```
Frontend:  Nuxt.js (Server-Side Rendering)
Backend:   Node.js / Express
Database:  Magento / Custom CMS
Data Formats: HTML, JSON-LD, Meta Tags
```

### 2. **URL Structure**

```
Homepage:        https://cellphones.com.vn/
Category:        https://cellphones.com.vn/{category}.html
                 - dien-thoai.html (Điện thoại)
                 - tablet.html (Tablet)
                 - laptop.html (Laptop)
                 - phu-kien.html (Phụ kiện)

Product Detail:  https://cellphones.com.vn/{slug}.html
                 Ví dụ: laptop-asus-tuf-gaming-f16-fx607vj-rl034w.html
```

---

## II. DATA EXTRACTION POINTS

### 📍 **Trang Danh Sách (Category Page)**

```html
href= "https://cellphones.com.vn/laptop-asus-tuf-gaming-f16-fx607vj-rl034w.html"
└─ Chứa link đến detail page (cần parse để lấy URL)
```

**Cách lấy:**

```python
# Tìm links tới products
for link in soup.find_all('a', href=True):
    href = link.get('href', '')
    if category_code in href and href.endswith('.html'):
        product_urls.append(urljoin(BASE_URL, href))
```

---

### 📍 **Trang Chi Tiết Sản Phẩm (Product Detail)**

#### **A. Meta Tags** (Dễ extract + có sẵn HTML)

```html
<!-- Title -->
<title>Laptop ASUS TUF Gaming F16 FX607VJ-RL034W | Giá rẻ, trả góp 0%</title>

<!-- Open Graph Tags -->
<meta
  property="og:title"
  content="Laptop ASUS TUF Gaming F16 FX607VJ-RL034W | Giá rẻ, trả góp 0%"
/>
<meta
  property="og:description"
  content="Mua ngay Laptop ASUS TUF Gaming F16 FX607VJ-RL034W giá rẻ - Hỗ trợ trả góp 0%, đổi mới 30 ngày..."
/>
<meta
  property="og:image"
  content="https://cdn2.cellphones.com.vn/200x/media/catalog/product/..."
/>
<meta
  property="og:url"
  content="https://cellphones.com.vn/laptop-asus-tuf-gaming-f16-fx607vj-rl034w.html"
/>

<!-- Keywords -->
<meta name="keywords" content="Laptop ASUS TUF Gaming F16 FX607VJ-RL034W" />
<meta name="description" content="..." />
```

**Extract:**

```python
og_title = soup.find('meta', {'property': 'og:title'})
name = og_title.get('content') if og_title else ''

og_desc = soup.find('meta', {'property': 'og:description'})
description = og_desc.get('content') if og_desc else ''

og_image = soup.find('meta', {'property': 'og:image'})
image = og_image.get('content') if og_image else ''
```

---

#### **B. JSON-LD Schema.org** (Cấu trúc dữ liệu)

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": "Laptop ASUS TUF Gaming F16 FX607VJ-RL034W",
    "image": "https://cdn2.cellphones.com.vn/200x/media/catalog/product/...",
    "description": "Mua ngay Laptop ASUS TUF Gaming F16 FX607VJ-RL034W giá rẻ...",
    "offers": {
      "@type": "Offer",
      "url": "https://cellphones.com.vn/laptop-asus-tuf-gaming-f16-fx607vj-rl034w.html",
      "priceCurrency": "VND",
      "price": "29990000",
      "pricePriceCurrency": "30000000",
      ...
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.8",
      "ratingCount": "523"
    }
  }
</script>
```

**Extract:**

```python
scripts = soup.find_all('script', {'type': 'application/ld+json'})
for script in scripts:
    data = json.loads(script.string)
    if data.get('@type') == 'Product':
        return data  # Có tất cả dữ liệu cục bộ
```

---

#### **C. HTML Structure**

```html
<!-- Product Name -->
<h1 class="product-title">Laptop ASUS TUF Gaming F16 FX607VJ-RL034W</h1>

<!-- Price Elements -->
<span class="price">29.990.000đ</span>
<span class="original-price">30.000.000đ</span>

<!-- Specifications (thường nằm trong tabs) -->
<div class="specs">
  <div class="spec-item">
    <span class="label">Bộ xử lý</span>
    <span class="value">Intel Core i9-13980HX</span>
  </div>
  ...
</div>

<!-- Description/Content -->
<div class="description">
  <h2>Đặc tính chính</h2>
  <ul>
    <li>Hiệu năng cao...</li>
    <li>Màn hình 4K...</li>
  </ul>
</div>

<!-- Reviews/Ratings -->
<div class="reviews">
  <span class="rating">4.8</span>
  <span class="count">523 đánh giá</span>
</div>
```

**Extract:**

```python
# Price
price_elem = soup.find('span', class_='price')
price = extract_price(price_elem.text if price_elem else '')

# Specs - iterate through spec items
specs = []
for spec in soup.find_all('div', class_='spec-item'):
    label = spec.find('span', class_='label').text
    value = spec.find('span', class_='value').text
    specs.append(f"{label}: {value}")
```

---

## III. DỮ LIỆU CẦN EXTRACT

| Field            | Source                   | Priority  | Fallback               |
| ---------------- | ------------------------ | --------- | ---------------------- |
| **name**         | og:title / JSON-LD       | 🔴 High   | <title>                |
| **description**  | og:description           | 🔴 High   | Meta description       |
| **detail**       | HTML specs section       | 🟡 Medium | Generate từ spec items |
| **summary**      | Meta description snippet | 🟡 Medium | Tạo từ category        |
| **brand**        | Extract từ name          | 🟡 Medium | Hardcode list          |
| **category**     | URL path / breadcrumb    | 🔴 High   | Infer từ path          |
| **price**        | JSON-LD offers.price     | 🔴 High   | HTML price element     |
| **old_price**    | JSON-LD / HTML           | 🟡 Medium | Calculate × 1.2        |
| **discount**     | (old - new) / old × 100  | 🟡 Medium | Extract từ badge       |
| **promotion**    | Meta / breadcrumb        | 🟡 Medium | Generate text          |
| **image**        | og:image / JSON-LD       | 🟡 Medium | First product image    |
| **rating**       | JSON-LD aggregateRating  | 🟡 Medium | Random 3.5-5.0         |
| **rating_count** | JSON-LD aggregate Rating | 🟡 Medium | Random 50-2000         |

---

## IV. FLOW CÀO DỮ LIỆU

```
┌─────────────────────────────────────┐
│  GET Category Page (dien-thoai.html) │
└──────────────┬──────────────────────┘
               │ Parse product links
               ▼
┌─────────────────────────────────────┐
│  Extract URLs từ <a href=...>       │
│  (loop qua các sản phẩm)            │
└──────────────┬──────────────────────┘
               │ limit = X products
               ▼
┌─────────────────────────────────────┐
│  GET Product Detail Page             │
│  (laptop-asus-tuf-gaming-...html)   │
└──────────────┬──────────────────────┘
               │
         ┌─────┴──────┐
         │            │
         ▼            ▼
   ┌───────────┐  ┌─────────────┐
   │ Meta Tags │  │ JSON-LD     │
   │ (title,   │  │ (Product    │
   │ og:*)     │  │  schema)    │
   └─────┬─────┘  └────────┬────┘
         │                  │
         └────────┬─────────┘
                  │ Parse + Extract
                  ▼
         ┌─────────────────────┐
         │ Product Object      │
         │ ✓ name              │
         │ ✓ description       │
         │ ✓ detail            │
         │ ✓ price             │
         │ ✓ brand             │
         │ ✓ promotion         │
         └─────────┬───────────┘
                   │ Delay 1-2s (politeness)
                   ▼
        ┌──────────────────────┐
        │ Loop next product    │
        │ (hoặc next category) │
        └──────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Save to CSV / JSON   │
        │ ✓ cellphones_..csv   │
        │ ✓ cellphones_..json  │
        └──────────────────────┘
```

---

## V. BEST PRACTICES

### ✅ **DO:**

- ✅ Thêm delays (1-2 giây) giữa requests (politeness)
- ✅ Set proper User-Agent (tránh bị block)
- ✅ Parse JSON-LD trước (có cấu trúc rõ ràng)
- ✅ Fallback khi thiếu dữ liệu
- ✅ Log chi tiết (debugging)
- ✅ Handle exceptions (timeout, 404, etc.)
- ✅ Respect robots.txt

### ❌ **DON'T:**

- ❌ Không hammer server (delay quá ngắn)
- ❌ Không change User-Agent liên tục
- ❌ Không parse failed pages
- ❌ Không lưu password/auth info
- ❌ Không violate Terms of Service

---

## VI. EXAMPLE DATA OUTPUT

### CSV Format:

```csv
id,name,description,detail,summary,category,price,old_price,discount,brand,promotion,rating,rating_count,image,created_at
1,"Laptop ASUS TUF Gaming F16 FX607VJ-RL034W","Mua ngay Laptop ASUS TUF Gaming...","• Bộ xử lý: Intel Core i9-13980HX\n• RAM: 32GB...","Laptop cao cấp cho công việc và gaming...","Laptop",29990000,30000000,0,"ASUS","Giảm 5% - Hàng có sẵn",4.8,523,"https://cdn2.cellphones.com.vn/...",2026-03-28T10:30:00
```

### JSON Format:

```json
{
  "metadata": {
    "source": "cellphones.com.vn",
    "scraped_at": "2026-03-28T10:30:00",
    "total_products": 12
  },
  "products": [
    {
      "id": 1,
      "name": "Laptop ASUS TUF Gaming F16 FX607VJ-RL034W",
      "description": "Mua ngay Laptop ASUS TUF Gaming...",
      "detail": "• Bộ xử lý: Intel Core i9-13980HX\n• RAM: 32GB...",
      "category": "Laptop",
      "price": 29990000,
      "old_price": 30000000,
      "discount": 0,
      "brand": "ASUS",
      "promotion": "Giảm 5% - Hàng có sẵn",
      "image": "https://cdn2.cellphones.com.vn/..."
    }
  ]
}
```

---

## VII. TROUBLESHOOTING

| Issue           | Cause                  | Solution                   |
| --------------- | ---------------------- | -------------------------- |
| 404 Not Found   | Product không tồn tại  | Bỏ qua, log warning        |
| Timeout         | Server chậm/block      | Retry 3x, tăng delay       |
| Empty data      | CSS selectors sai      | Parse JSON-LD thay vì HTML |
| Blocked (403)   | IP banned              | Dùng proxy, giảm rate      |
| Meta tags thiếu | JavaScript render      | Dùng Selenium/Playwright   |
| Giá missing     | Không có price element | Generate random fallback   |

---

## VIII. ADVANCED TIPS

### 1. **Parallel Scraping** (cẩn thận!)

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:  # Max 3 threads
    futures = [executor.submit(scrape, url) for url in urls]
    results = [f.result() for f in futures]
```

### 2. **Rotating Proxies** (nếu bị block)

```python
proxies = [
    'http://proxy1.com:8080',
    'http://proxy2.com:8080',
]
proxy = random.choice(proxies)
response = session.get(url, proxies={'http': proxy})
```

### 3. **Session Persistence**

```python
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0...'})
# Tái sử dụng session (connection pooling)
for url in urls:
    response = session.get(url)  # Nhanh hơn New request()
```

### 4. **Smart Retry Logic**

```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
```
