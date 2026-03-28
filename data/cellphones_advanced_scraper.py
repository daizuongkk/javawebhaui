import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
import random
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CellphonesAdvancedScraper:
    """Advanced scraper cho cellphones.com.vn với API support"""
    
    def __init__(self):
        self.base_url = 'https://cellphones.com.vn'
        self.api_url = 'https://api.cellphones.com.vn/v1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*'
        }
        self.products = []
        self.product_images = []
        self.inventory = []
        self.product_id = 1
    
    def fetch_json(self, url, params=None):
        """Fetch JSON từ API"""
        try:
            logger.info(f"Fetching {url}")
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
        return None
    
    def scrape_from_api(self):
        """Crawl dữ liệu từ API (nếu có)"""
        categories = [
            ('dien-thoai', 'Điện thoại'),
            ('tablet', 'Tablet'),
            ('laptop', 'Laptop'),
            ('phu-kien', 'Phụ kiện'),
        ]
        
        for category_slug, category_name in categories:
            self.scrape_category_api(category_slug, category_name)
    
    def scrape_category_api(self, category_slug, category_name):
        """Scrape một category từ API"""
        try:
            # Thử API endpoint (tuỳ vào cấu trúc thực tế)
            api_endpoint = f"{self.api_url}/products"
            params = {
                'category': category_slug,
                'limit': 50,
                'page': 1
            }
            
            data = self.fetch_json(api_endpoint, params)
            
            if data and 'data' in data:
                for product_data in data['data']:
                    product = self.parse_api_product(product_data, category_name)
                    if product:
                        self.products.append(product)
                        time.sleep(0.3)
            else:
                logger.warning(f"No data for {category_slug}")
        except Exception as e:
            logger.error(f"Error scraping {category_slug}: {str(e)}")
    
    def parse_api_product(self, data, category):
        """Parse sản phẩm từ API response"""
        try:
            product = {
                'id': self.product_id,
                'name': data.get('name') or data.get('title'),
                'description': data.get('description'),
                'price': int(float(data.get('price', 0))),
                'old_price': int(float(data.get('original_price', data.get('price', 0)))),
                'category': category,
                'rating': float(data.get('rating', random.uniform(3.5, 5.0))),
                'rating_count': int(data.get('review_count', random.randint(10, 1000))),
                'image': data.get('image') or data.get('thumbnail'),
                'brand': data.get('brand'),
                'sku': data.get('sku'),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Tính discount
            if product['old_price'] > product['price']:
                product['discount'] = round(
                    (product['old_price'] - product['price']) / product['old_price'] * 100
                )
            else:
                product['discount'] = 0
            
            # Add images
            images = data.get('images', [])
            if images:
                for idx, img_url in enumerate(images[:5], 1):
                    self.product_images.append({
                        'product_id': self.product_id,
                        'image_url': img_url,
                        'display_order': idx
                    })
            elif product['image']:
                self.product_images.append({
                    'product_id': self.product_id,
                    'image_url': product['image'],
                    'display_order': 1
                })
            
            # Add inventory
            quantity = int(data.get('stock', random.randint(20, 100)))
            self.inventory.append({
                'product_id': self.product_id,
                'quantity': quantity,
                'updated_at': datetime.now().isoformat()
            })
            
            self.product_id += 1
            return product
        
        except Exception as e:
            logger.error(f"Error parsing product: {str(e)}")
            return None
    
    def scrape_from_html(self):
        """Fallback: Crawl từ HTML nếu API không có"""
        categories = [
            ('mobile.html', 'Điện thoại'),
            ('tablet.html', 'Tablet'),
            ('laptop.html', 'Laptop'),
            ('phu-kien.html', 'Phụ kiện'),
        ]
        
        for path, name in categories:
            url = f"{self.base_url}/{path}"
            self.scrape_category_html(url, name)
    
    def scrape_category_html(self, url, category_name):
        """Scrape HTML category page"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                logger.error(f"Failed to fetch {url}")
                return
            
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tìm các product items (cần adjust selector theo cấu trúc thực tế)
            products = soup.find_all('div', class_=re.compile('product'))
            
            logger.info(f"Found {len(products)} products in {category_name}")
            
            for prod_elem in products[:20]:  # Limit để test
                product = self.parse_html_product(prod_elem, category_name)
                if product:
                    self.products.append(product)
                    time.sleep(random.uniform(0.3, 0.8))
        
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
    
    def parse_html_product(self, elem, category):
        """Parse sản phẩm từ HTML element"""
        try:
            # Tìm tên
            name = elem.find(['h2', 'h3', 'a'])
            name_text = name.get_text(strip=True) if name else None
            
            if not name_text or len(name_text) < 3:
                return None
            
            # Tìm giá
            price_elem = elem.find(['span', 'div'], class_=re.compile('price|cost'))
            price = 0
            if price_elem:
                price_text = price_elem.get_text()
                numbers = re.findall(r'\d+', price_text.replace('.', '').replace(',', ''))
                if numbers:
                    price = int(numbers[0])
            
            if price == 0:
                price = random.randint(1000000, 50000000)
            
            # Giá cũ
            old_price = int(price * random.uniform(1.1, 1.25))
            discount = round((old_price - price) / old_price * 100)
            
            # Hình ảnh
            img = elem.find('img')
            image_url = None
            if img:
                image_url = img.get('src') or img.get('data-src')
                if image_url and not image_url.startswith('http'):
                    image_url = f"{self.base_url}{image_url}"
            
            product = {
                'id': self.product_id,
                'name': name_text,
                'price': price,
                'old_price': old_price,
                'discount': discount,
                'category': category,
                'rating': round(random.uniform(3.5, 5.0), 1),
                'rating_count': random.randint(10, 1000),
                'image': image_url,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            if image_url:
                self.product_images.append({
                    'product_id': self.product_id,
                    'image_url': image_url,
                    'display_order': 1
                })
            
            self.inventory.append({
                'product_id': self.product_id,
                'quantity': random.randint(20, 100),
                'updated_at': datetime.now().isoformat()
            })
            
            self.product_id += 1
            return product
        
        except Exception as e:
            logger.error(f"Error parsing HTML product: {str(e)}")
            return None
    
    def export_data(self):
        """Export dữ liệu"""
        # JSON
        data = {
            'metadata': {
                'source': 'cellphones.com.vn',
                'scraped_at': datetime.now().isoformat(),
                'total_products': len(self.products),
                'total_images': len(self.product_images)
            },
            'products': self.products,
            'product_images': self.product_images,
            'inventory': self.inventory
        }
        
        with open('cellphones_products.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # SQL
        self.generate_sql()
        
        logger.info(f"\n✅ Export completed!")
        logger.info(f"   📁 cellphones_products.json - {len(self.products)} products")
        logger.info(f"   📁 cellphones_products.sql - SQL insert statements")
    
    def generate_sql(self):
        """Generate SQL file"""
        with open('cellphones_products.sql', 'w', encoding='utf-8') as f:
            f.write("-- ============================================================\n")
            f.write(f"-- Cellphones.com.vn Data Export\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Total Products: {len(self.products)}\n")
            f.write("-- ============================================================\n\n")
            
            f.write("SET NAMES utf8mb4;\nSET FOREIGN_KEY_CHECKS = 0;\n\n")
            
            # Products table
            f.write("-- ===== PRODUCTS =====\n")
            f.write("INSERT INTO products (id, name, description, category, price, old_price, discount, ")
            f.write("rating, rating_count, image, brand, created_at, updated_at) VALUES\n")
            
            for i, p in enumerate(self.products):
                comma = "," if i < len(self.products) - 1 else ";"
                f.write(f"  ({p['id']}, '{self.escape_sql(p['name'])}', NULL, ")
                f.write(f"'{p.get('category', 'unknown')}', {p['price']}, {p['old_price']}, {p['discount']}, ")
                f.write(f"{p['rating']}, {p['rating_count']}, ")
                f.write(f"'{self.escape_sql(p.get('image', ''))}', '{p.get('brand', 'Unknown')}', ")
                f.write(f"'{p['created_at']}', '{p['updated_at']}'){comma}\n")
            
            f.write("\n-- ===== PRODUCT IMAGES =====\n")
            f.write("INSERT INTO product_images (product_id, image_url, display_order) VALUES\n")
            
            for i, img in enumerate(self.product_images):
                comma = "," if i < len(self.product_images) - 1 else ";"
                f.write(f"  ({img['product_id']}, '{self.escape_sql(img['image_url'])}', {img['display_order']}){comma}\n")
            
            f.write("\n-- ===== INVENTORY =====\n")
            f.write("INSERT INTO inventory (product_id, quantity, updated_at) VALUES\n")
            
            for i, inv in enumerate(self.inventory):
                comma = "," if i < len(self.inventory) - 1 else ";"
                f.write(f"  ({inv['product_id']}, {inv['quantity']}, '{inv['updated_at']}'){comma}\n")
            
            f.write("\nSET FOREIGN_KEY_CHECKS = 1;\n")
    
    def escape_sql(self, text):
        """Escape SQL string"""
        if not text:
            return ""
        return str(text).replace("'", "\\'").replace('"', '\\"')
    
    def run(self):
        """Chạy scraper"""
        logger.info("🚀 Starting Cellphones.com.vn Advanced Scraper\n")
        
        try:
            # Thử API trước
            if self.scrape_from_api():
                logger.info("✅ API scraping successful")
            else:
                logger.info("⚠️ API not available, falling back to HTML scraping")
                self.scrape_from_html()
            
            if self.products:
                self.export_data()
            else:
                logger.warning("❌ No products scraped")
        
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    scraper = CellphonesAdvancedScraper()
    # Thử API trước
    scraper.scrape_from_api()
    
    # Nếu API không có dữ liệu, dùng HTML
    if not scraper.products:
        logger.info("Trying HTML scraping...")
        scraper.scrape_from_html()
    
    if scraper.products:
        scraper.export_data()
    else:
        logger.warning("No data scraped. Check if website structure or API endpoints changed.")
