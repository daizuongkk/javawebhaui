import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
import random
import time
from urllib.parse import urljoin, urlparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CellphonesScraper:
    def __init__(self):
        self.base_url = 'https://cellphones.com.vn'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.products = []
        self.product_images = []
        self.inventory = []
        self.categories = {}
        self.product_id_counter = 1
        
    def fetch_page(self, url):
        """Fetch HTML từ URL"""
        try:
            logger.info(f"Fetching {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response.text
            else:
                logger.error(f"Failed to fetch {url}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def extract_price(self, text):
        """Extract giá từ text"""
        if not text:
            return None
        # Loại bỏ whitespace và text không liên quan
        text = text.strip()
        # Tìm số tiền
        match = re.search(r'(\d{1,3}(?:[.,]\d{3})*)\s*(?:đ|VND|triệu)?', text.replace('.', '').replace(',', ''))
        if match:
            price_str = match.group(1).replace(',', '')
            try:
                # Nếu là triệu
                if 'triệu' in text.lower():
                    return int(float(price_str) * 1000000)
                return int(price_str)
            except:
                return None
        return None
    
    def extract_category(self, url):
        """Extract category từ URL"""
        path = urlparse(url).path
        parts = path.strip('/').split('/')
        if parts:
            return parts[0]
        return 'unknown'
    
    def scrape_product_list(self, category_url, category_name):
        """Crawl danh sách sản phẩm từ category"""
        html = self.fetch_page(category_url)
        if not html:
            return
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Tìm các product item (tuỳ vào cấu trúc trang)
        products = soup.find_all('div', class_='product-item')
        
        if not products:
            # Thử cách khác
            products = soup.find_all('a', class_='product')
        
        logger.info(f"Found {len(products)} products in {category_name}")
        
        for product in products[:10]:  # Limit 10 sản phẩm/category để test
            try:
                product_data = self.extract_product_info(product, category_name)
                if product_data:
                    self.products.append(product_data)
                    time.sleep(random.uniform(0.5, 1.5))  # Delay để tránh block
            except Exception as e:
                logger.error(f"Error extracting product: {str(e)}")
    
    def extract_product_info(self, product_elem, category):
        """Extract thông tin sản phẩm từ element"""
        try:
            # Tìm tên sản phẩm
            name_elem = product_elem.find('h2') or product_elem.find('a')
            name = name_elem.get_text(strip=True) if name_elem else None
            
            # Tìm giá
            price_elem = product_elem.find('span', class_='price') or \
                        product_elem.find('span', class_='current-price')
            price = None
            if price_elem:
                price = self.extract_price(price_elem.get_text())
            
            # Tìm giá cũ
            old_price_elem = product_elem.find('span', class_='old-price') or \
                            product_elem.find('span', class_='original-price')
            old_price = None
            if old_price_elem:
                old_price = self.extract_price(old_price_elem.get_text())
            
            # Nếu không có old_price, tạo random
            if old_price is None and price:
                old_price = int(price * random.uniform(1.1, 1.3))
            
            # Tính discount
            discount = None
            if price and old_price:
                discount = round((old_price - price) / old_price * 100)
            
            # Tìm hình ảnh
            img_elem = product_elem.find('img')
            image_url = None
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src')
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(self.base_url, image_url)
            
            # Tìm link sản phẩm
            link_elem = product_elem.find('a', href=True)
            product_url = None
            if link_elem:
                product_url = link_elem.get('href')
                if not product_url.startswith('http'):
                    product_url = urljoin(self.base_url, product_url)
            
            # Tìm description/summary
            desc_elem = product_elem.find('p', class_='description') or \
                       product_elem.find('div', class_='summary')
            description = desc_elem.get_text(strip=True) if desc_elem else None
            
            # Tìm rating
            rating_elem = product_elem.find('span', class_='rating') or \
                         product_elem.find('div', class_='star')
            rating = None
            if rating_elem:
                try:
                    rating = float(rating_elem.get_text(strip=True).split('/')[0])
                except:
                    rating = random.uniform(3.5, 5.0)
            else:
                rating = random.uniform(3.5, 5.0)
            
            rating_count = random.randint(10, 1000)
            
            if name and price:
                product_data = {
                    'id': self.product_id_counter,
                    'name': name,
                    'description': description,
                    'price': price,
                    'old_price': old_price,
                    'discount': discount,
                    'rating': round(rating, 1),
                    'rating_count': rating_count,
                    'category': category,
                    'url': product_url,
                    'image': image_url,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                
                # Add product image
                if image_url:
                    self.product_images.append({
                        'product_id': self.product_id_counter,
                        'image_url': image_url,
                        'display_order': 1
                    })
                
                # Add inventory
                self.inventory.append({
                    'product_id': self.product_id_counter,
                    'quantity': random.randint(20, 100),
                    'updated_at': datetime.now().isoformat()
                })
                
                self.product_id_counter += 1
                return product_data
        except Exception as e:
            logger.error(f"Error in extract_product_info: {str(e)}")
        
        return None
    
    def scrape_categories(self):
        """Crawl category pages"""
        categories_to_scrape = [
            ('mobile.html', 'Điện thoại'),
            ('laptop.html', 'Laptop'),
            ('tablet.html', 'Tablet'),
            ('phu-kien.html', 'Phụ kiện'),
        ]
        
        for path, name in categories_to_scrape:
            url = f"{self.base_url}/{path}"
            self.scrape_product_list(url, name)
    
    def export_json(self, filename='scraped_products.json'):
        """Export dữ liệu ra JSON"""
        data = {
            'metadata': {
                'total_products': len(self.products),
                'total_images': len(self.product_images),
                'scraped_at': datetime.now().isoformat(),
                'source': 'cellphones.com.vn'
            },
            'products': self.products,
            'product_images': self.product_images,
            'inventory': self.inventory
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Data exported to {filename}")
    
    def export_sql(self, filename='cellphones_scraped.sql'):
        """Export dữ liệu ra SQL"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("-- ============================================================\n")
            f.write(f"-- Cellphones.com.vn Scraped Data\n")
            f.write(f"-- Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Total products: {len(self.products)}\n")
            f.write("-- ============================================================\n\n")
            
            f.write("SET NAMES utf8mb4;\n")
            f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
            
            # Products
            f.write("-- ===================== products =====================\n")
            f.write("INSERT INTO products (id, name, description, summary, category, price, "
                   "old_price, discount, rating, rating_count, image_url, created_at, updated_at)\n")
            f.write("VALUES\n")
            
            product_lines = []
            for p in self.products:
                old_price = p.get('old_price') or p['price']
                discount = p.get('discount') or 0
                rating = p.get('rating') or 3.5
                rating_count = p.get('rating_count') or 0
                image = p.get('image') or 'NULL'
                
                line = (f"  ({p['id']}, {self.sql_string(p['name'])}, {self.sql_string(p.get('description'))}, "
                       f"{self.sql_string(p.get('description'))}, {self.sql_string(p.get('category'))}, "
                       f"{p['price']}, {old_price}, {discount}, {rating}, {rating_count}, "
                       f"{self.sql_string(image)}, "
                       f"'{p['created_at']}', '{p['updated_at']}')")
                product_lines.append(line)
            
            f.write(",\n".join(product_lines))
            f.write(";\n\n")
            
            # Product Images
            f.write("-- ===================== product_images =====================\n")
            f.write("INSERT INTO product_images (product_id, image_url, display_order)\n")
            f.write("VALUES\n")
            
            img_lines = []
            for img in self.product_images:
                line = f"  ({img['product_id']}, {self.sql_string(img['image_url'])}, {img.get('display_order', 1)})"
                img_lines.append(line)
            
            if img_lines:
                f.write(",\n".join(img_lines))
                f.write(";\n\n")
            
            # Inventory
            f.write("-- ===================== inventory =====================\n")
            f.write("INSERT INTO inventory (product_id, quantity, updated_at)\n")
            f.write("VALUES\n")
            
            inv_lines = []
            for inv in self.inventory:
                line = f"  ({inv['product_id']}, {inv['quantity']}, '{inv['updated_at']}')"
                inv_lines.append(line)
            
            if inv_lines:
                f.write(",\n".join(inv_lines))
                f.write(";\n\n")
            
            f.write("SET FOREIGN_KEY_CHECKS = 1;\n")
        
        logger.info(f"SQL exported to {filename}")
    
    def sql_string(self, value):
        """Convert value to SQL string"""
        if value is None:
            return "NULL"
        if isinstance(value, str):
            escaped = value.replace("'", "\\'")
            return f"'{escaped}'"
        return str(value)
    
    def run(self):
        """Chạy scraper"""
        logger.info("Starting Cellphones.com.vn scraper...")
        try:
            self.scrape_categories()
            
            # Export dữ liệu
            self.export_json('cellphones_scraped.json')
            self.export_sql('cellphones_scraped.sql')
            
            logger.info(f"\n✅ Scraping completed!")
            logger.info(f"   - Total products: {len(self.products)}")
            logger.info(f"   - Total images: {len(self.product_images)}")
            logger.info(f"   - Total inventory: {len(self.inventory)}")
            
        except Exception as e:
            logger.error(f"Error in scraper: {str(e)}")

if __name__ == '__main__':
    scraper = CellphonesScraper()
    scraper.run()
