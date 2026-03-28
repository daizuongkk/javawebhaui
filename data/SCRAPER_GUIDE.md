# 🛍️ Cellphones.com.vn Scraper Suite

**Bộ công cụ crawl dữ liệu từ cellphones.com.vn**

## 📋 Nội dung

3 script khác nhau với đặc điểm riêng:

### 1. **scrape_cellphones.py** - Recommended ⭐
```bash
python scrape_cellphones.py
```
**Đặc điểm:**
- ✅ Universal scraper - Hỗ trợ cả API và HTML parsing
- ✅ Tự động fallback từ API sang HTML nếu API không có
- ✅ Delay thông minh để tránh rate limiting
- ✅ Export JSON và SQL cùng lúc
- ✅ Xử lý lỗi tốt với retry logic
- ✅ Logging chi tiết tiến độ

**Output:**
- `cellphones_data.json` - Dữ liệu đầy đủ theo cấu trúc JSON
- `cellphones_data.sql` - SQL insert statements

### 2. **cellphones_advanced_scraper.py** - Advanced
```bash
python cellphones_advanced_scraper.py
```
**Đặc điểm:**
- ✅ API-first approach
- ✅ Fallback HTML scraper tự động
- ✅ Lọc và xử lý dữ liệu nâng cao
- ✅ Được thiết kế cho production

### 3. **cellphones_scraper.py** - Original
```bash
python cellphones_scraper.py
```
**Đặc điểm:**
- ✅ Scraper đơn giản, dễ hiểu
- ✅ Hỗ trợ cơ bản HTML parsing
- ✅ Có thể dùng làm template

---

## ⚙️ Cài đặt

### 1.**Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

### 2. **Hoặc cài lẻ:**
```bash
pip install requests beautifulsoup4 lxml
```

---

## 🚀 Sử dụng

### **Cách 1: Hệ thống tự động** (RECOMMENDED)
```bash
python scrape_cellphones.py
```
- Tự động cố gắng dùng API
- Nếu API không có, tự động chuyển sang HTML parsing
- Export JSON + SQL tự động

### **Cách 2: Tuỳ chỉnh**
```bash
# Sửa các biến trong code
# - BASE_URL: Thay đổi base URL
# - CATEGORIES: Thêm/bớt category
# - delay: Điều chỉnh tốc độ crawl
python scrape_cellphones.py
```

### **Cách 3: Import như module**
```python
from scrape_cellphones import UniversalCellphonesScraper

scraper = UniversalCellphonesScraper(delay=1.0)
scraper.scrape_all()
scraper.export()
```

---

## 📊 Cấu trúc Output

### **JSON Format**
```json
{
  "metadata": {
    "source": "cellphones.com.vn",
    "scraped_at": "2026-03-28T...",
    "total_products": 50,
    "total_images": 55,
    "categories": [...]
  },
  "products": [
    {
      "id": 1,
      "name": "iPhone 17 Pro",
      "category": "Điện thoại",
      "price": 28000000,
      "old_price": 31000000,
      "discount": 10,
      "rating": 4.8,
      "rating_count": 250,
      "image": "https://...",
      "created_at": "2026-03-28T...",
      "updated_at": "2026-03-28T..."
    }
  ],
  "product_images": [...],
  "inventory": [...]
}
```

### **SQL Format**
```sql
INSERT INTO products (id, name, description, category, price, old_price, ...)
VALUES
  (1, 'iPhone 17 Pro', NULL, 'Điện thoại', 28000000, 31000000, ...),
  (2, 'Samsung Galaxy S26', NULL, 'Điện thoại', 25000000, 28000000, ...),
  ...
```

---

## 🎯 Categories hỗ trợ

- `dien-thoai` - Điện thoại
- `tablet` - Tablet
- `laptop` - Laptop
- `phu-kien` - Phụ kiện

Để thêm category mới, sửa `CATEGORIES` dict trong code.

---

## ⚙️ Tuỳ chỉnh

### **Điều chỉnh delay giữa requests**
```python
scraper = UniversalCellphonesScraper(delay=2.0)  # 2 giây
```

### **Giới hạn sản phẩm per category**
Sửa dòng `[:15]` trong hàm `scrape_category()`
```python
for idx, prod in enumerate(products[:50]):  # Limit 50 per category
```

### **Thêm header tùy chỉnh**
```python
scraper.session.headers.update({
    'Accept-Language': 'vi-VN,...',
    'Custom-Header': 'value'
})
```

---

## 🐛 Troubleshooting

### **403 Forbidden / 429 Too Many Requests**
```python
# Tăng delay
scraper = UniversalCellphonesScraper(delay=3.0)

# Hoặc dùng proxy
scraper.session.proxies = {
    'http': 'http://proxy:port',
    'https': 'https://proxy:port'
}
```

### **Không tìm thấy products**
- Kiểm tra CSS selector trong code
- Có thể cấu trúc HTML đã thay đổi
- Cập nhật regex patterns

### **Lỗi encoding**
```python
response.encoding = 'utf-8'  # Đã có trong code
```

---

## 📈 Performance Tips

1. **Điều chỉnh delay hợp lý**: Tránh quá nhanh (bị block) hay quá chậm (mất thời gian)
2. **Giới hạn sản phẩm per category** khi test
3. **Dùng threading** cho multiple categories (advanced)
4. **Cache responses** để tránh crawl lại

---

## 📁 File output

| File | Mô tả |
|------|-------|
| `cellphones_data.json` | Dữ liệu đầy đủ JSON |
| `cellphones_data.sql` | SQL insert statements |
| `cellphones_products.json` | (Advanced scraper) |
| `cellphones_products.sql` | (Advanced scraper) |

---

## 🔄 Workflow đề xuất

```
1. python scrape_cellphones.py          # Crawl dữ liệu
2. Review cellphones_data.json          # Kiểm tra dữ liệu
3. Sửa SQL nếu cần (thêm categories, etc)
4. Import cellphones_data.sql vào database
```

---

## 📝 Notes

- ⚠️ **Terms of Service**: Hãy kiểm tra robots.txt và ToS của cellphones.com.vn
- 🔒 **Rate Limit**: Script đã có delay hợp lý, nhưng có thể bị block nếu crawl quá nhanh
- 🌐 **Proxy Support**: Có thể thêm proxy nếu bị block
- 💾 **Data Persistence**: Dữ liệu được export ra JSON để có thể xử lý tiếp

---

## 🤝 Support

Nếu có vấn đề:
1. Kiểm tra logs (script in ra console)
2. Sửa CSS selector nếu HTML thay đổi
3. Tăng delay nếu bị rate limited
4. Check website structure trong browser dev tools

---

**Version**: 1.0  
**Last Updated**: 2026-03-28  
**Status**: ✅ Ready to use
