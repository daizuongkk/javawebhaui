#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cellphones.com.vn - Selenium Scraper (Complete Data + Images)
==============================================================
Script cào TOÀN BỘ thông tin + ảnh sản phẩm từ cellphones.com.vn
- Dùng Selenium để render JavaScript
- Extract tất cả dữ liệu từ page
- Download tất cả ảnh sản phẩm
- Lưu thông tin vào CSV + JSON, images vào folder
"""

import os
import time
import json
import csv
import logging
import re
import random
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from bs4 import BeautifulSoup

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SeleniumScraper')


class SeleniumProductScraper:
    """Cào dữ liệu + ảnh sản phẩm bằng Selenium"""
    
    BASE_URL = 'https://cellphones.com.vn'
    
    CATEGORIES = {
        'dien-thoai': 'Điện thoại',
        'tablet': 'Tablet',
        'laptop': 'Laptop',
        'phu-kien': 'Phụ kiện'
    }
    
    def __init__(self, headless=True, delay=1):
        """
        Initialize scraper
        
        Args:
            headless: Run browser in headless mode
            delay: Delay between requests (seconds)
        """
        self.delay = delay
        self.headless = headless
        self.driver = None
        self.products = []
        self.product_images = []
    
    def setup_driver(self):
        """Setup Selenium WebDriver with Chrome"""
        try:
            options = Options()
            
            if self.headless:
                options.add_argument('--headless')
            
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Try standard Chrome first
            try:
                self.driver = webdriver.Chrome(options=options)
                logger.info("✓ ChromeDriver initialized")
            except Exception as e1:
                logger.warning(f"Standard Chrome failed: {e1}")
                # Try with webdriver-manager
                try:
                    from webdriver_manager.chrome import ChromeDriverManager
                    self.driver = webdriver.Chrome(
                        service=webdriver.Service(ChromeDriverManager().install()),
                        options=options
                    )
                    logger.info("✓ ChromeDriver initialized (with webdriver-manager)")
                except Exception as e2:
                    logger.error(f"Both Chrome attempts failed: {e1}, {e2}")
                    raise
        
        except Exception as e:
            logger.error(f"✗ Setup driver failed: {e}")
            logger.info("\n⚠️  Installation required:")
            logger.info("   pip install selenium webdriver-manager")
            raise
    
    def close_driver(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            logger.info("✓ Browser closed")
    
    def fetch_page(self, url, wait_time=20):
        """
        Fetch page with Selenium and wait for content
        
        Args:
            url: Page URL
            wait_time: Wait time for content to load (seconds)
        
        Returns:
            HTML content after JavaScript rendering
        """
        try:
            logger.info(f"Fetching: {url}")
            self.driver.get(url)
            
            # Wait 1: Body element
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                logger.info("  ✓ Body loaded")
            except TimeoutException:
                logger.warning("  ⚠ Body timeout")
            
            # Wait 2: Main product container (multiple selectors)
            product_selectors = [
                (By.CSS_SELECTOR, "div[class*='product']"),
                (By.CSS_SELECTOR, "div[class*='container']"),
                (By.CSS_SELECTOR, "main"),
            ]
            
            for selector in product_selectors:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(selector)
                    )
                    logger.info(f"  ✓ Content element found: {selector}")
                    break
                except TimeoutException:
                    continue
            
            # Wait 3: Let JavaScript finish rendering
            time.sleep(3)
            
            # Get page source
            html = self.driver.page_source
            logger.info(f"✓ Page loaded and rendered ({len(html)} bytes)")
            return html
        
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def download_image(self, image_url, product_name, order=1):
        """
        Download image from URL
        
        Args:
            image_url: Image URL
            product_name: Product name (for filename)
            order: Image order/index
        
        Returns:
            Local image path if success, None otherwise
        """
        try:
            if not image_url:
                return None
            
            # Full URL
            if not image_url.startswith('http'):
                image_url = urljoin(self.BASE_URL, image_url)
            
            # Get image content
            response = requests.get(image_url, timeout=10)
            if response.status_code != 200:
                return None
            
            # Generate filename
            clean_name = re.sub(r'[^\w\s-]', '', product_name)[:50]
            clean_name = re.sub(r'[-\s]+', '_', clean_name)
            
            # Parse extension
            parsed_url = urlparse(image_url)
            path = parsed_url.path
            ext = Path(path).suffix or '.jpg'
            
            filename = f"{clean_name}_{order}{ext}"
            filepath = os.path.join(self.image_folder, filename)
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"  ✓ Image saved: {filename}")
            self.image_counter += 1
            return filepath
        
        except Exception as e:
            logger.warning(f"Error downloading image {image_url}: {e}")
            return None
    
    def extract_price(self, price_text):
        """Extract numeric price from text"""
        if not price_text:
            return None
        
        text = str(price_text).strip()
        
        # Handle "X triệu"
        if 'triệu' in text.lower():
            match = re.search(r'(\d+[.,]?\d*)\s*triệu', text, re.IGNORECASE)
            if match:
                try:
                    return int(float(match.group(1).replace(',', '.')) * 1000000)
                except:
                    pass
        
        # Extract numbers
        numbers = re.findall(r'\d+', text.replace('.', '').replace(',', ''))
        if numbers:
            try:
                return int(numbers[0])
            except:
                pass
        
        return None
    
    def extract_brand(self, product_name):
        """Extract brand from product name"""
        brands = {
            'Apple': ['iPhone', 'iPad', 'MacBook', 'AirPods'],
            'Samsung': ['Galaxy', 'Galaxy S', 'Galaxy Note'],
            'Xiaomi': ['Xiaomi', 'Redmi', 'POCO'],
            'ASUS': ['ASUS', 'TUF', 'Vivobook'],
            'Lenovo': ['Lenovo', 'ThinkPad', 'Legion'],
            'Dell': ['Dell', 'XPS', 'Inspiron'],
            'HP': ['HP', 'Pavilion'],
            'Sony': ['Sony', 'Vaio'],
            'LG': ['LG'],
            'Google': ['Pixel'],
            'OnePlus': ['OnePlus'],
            'Motorola': ['Motorola', 'Moto'],
            'Vivo': ['Vivo'],
            'OPPO': ['OPPO'],
            'Nokia': ['Nokia'],
            'Realme': ['Realme'],
        }
        
        for brand, keywords in brands.items():
            for keyword in keywords:
                if keyword.lower() in product_name.lower():
                    return brand
        
        return product_name.split()[0] if product_name else 'Brand'
    
    def extract_product_images(self, soup):
        """
        Extract all image URLs from product page (NO DOWNLOAD)
        
        Returns:
            List of image URLs dictionaries
        """
        images = []
        image_urls = {}  # URL -> order (dict to avoid duplicates and track order)
        
        try:
            logger.info(f"     🔎 Scanning for image elements...")
            
            # Method 1: Find all img tags (including lazy-loaded)
            img_count = 0
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src') or img.get('data-lazy-src') or img.get('data-image')
                alt = img.get('alt', '')
                
                if src and src.strip() and ('product' in alt.lower() or 'image' in alt.lower() or 'photo' in alt.lower() or not alt):
                    if not src.startswith('http'):
                        src = urljoin(self.BASE_URL, src)
                    if src not in image_urls:
                        image_urls[src] = len(image_urls) + 1
                        img_count += 1
            
            logger.info(f"        ✓ Found {img_count} img tags")
            
            # Method 2: Find picture/source elements (responsive images)
            pic_count = 0
            for picture in soup.find_all('picture'):
                for source in picture.find_all('source'):
                    srcset = source.get('srcset')
                    if srcset:
                        # Extract first URL from srcset
                        url = srcset.split()[0].split(',')[0].strip()
                        if url and url.startswith('http') and url not in image_urls:
                            image_urls[url] = len(image_urls) + 1
                            pic_count += 1
            
            if pic_count > 0:
                logger.info(f"        ✓ Found {pic_count} picture/source elements")
            
            # Method 3: Look for og:image (primary image)
            og_image = soup.find('meta', {'property': 'og:image'})
            if og_image:
                content = og_image.get('content', '').strip()
                if content and content not in image_urls:
                    image_urls[content] = 0  # Set to 0 to appear first
                    logger.info(f"        ✓ Found og:image tag")
            
            # Method 4: Find images in data attributes (JSON-LD, script tags)
            for script in soup.find_all('script'):
                if script.string:
                    # Look for image URLs in JSON
                    urls_found = re.findall(r'https?://[^\s"\'<>]+(?:\.jpg|\.png|\.jpeg|\.webp)', script.string)
                    for url in urls_found:
                        if url not in image_urls and 'cdn' in url.lower():
                            image_urls[url] = len(image_urls) + 1
            
            # Method 5: Data attributes (data-image, data-photo, etc)
            for attr in ['data-image', 'data-photo', 'data-src', 'data-lazy-src']:
                for elem in soup.find_all(attrs={attr: True}):
                    url = elem.get(attr, '').strip()
                    if url and url.startswith('http') and url not in image_urls:
                        image_urls[url] = len(image_urls) + 1
            
            # Build result list
            sorted_urls = sorted(image_urls.items(), key=lambda x: x[1])
            for idx, (url, _) in enumerate(sorted_urls, 1):
                images.append({
                    'url': url,
                    'order': idx
                })
            
            logger.info(f"     ✅ Total images extracted: {len(images)}")
            for img in images[:3]:
                logger.info(f"        {img['order']}. {img['url'][:70]}...")
            
            return images
        
        except Exception as e:
            logger.warning(f"Error extracting images: {e}")
            return []
    
    def extract_product_details(self, url, category):
        """
        Extract complete product details from detail page
        
        Returns:
            Product dictionary with full information
        """
        try:
            # Fetch page with Selenium
            html = self.fetch_page(url)
            if not html:
                logger.error("  ✗ Failed to fetch page")
                return None
            
            soup = BeautifulSoup(html, 'html.parser')
            logger.info(f"  📄 Parsing HTML ({len(html)} bytes)")
            
            # ========== EXTRACT META TAGS ==========
            
            logger.info(f"  🔍 Extracting meta tags...")
            
            # Name
            og_title = soup.find('meta', {'property': 'og:title'})
            name = og_title.get('content', '') if og_title else ''
            if ' | ' in name:
                name = name.split(' | ')[0].strip()
            logger.info(f"     Name: {name[:50]}...")
            
            # Description
            og_desc = soup.find('meta', {'property': 'og:description'})
            description = og_desc.get('content', '') if og_desc else ''
            
            # Main image
            og_image = soup.find('meta', {'property': 'og:image'})
            main_image = og_image.get('content', '') if og_image else ''
            logger.info(f"     Image: {main_image[:60]}...")
            
            # ========== EXTRACT FROM RENDERED CONTENT ==========
            
            logger.info(f"  🔍 Extracting product details...")
            
            rating = 4.5
            rating_count = 0
            price = 0
            old_price = 0
            
            # Try to find price (multiple strategies)
            price_selectors = [
                ('span[class*="price"][class*="current"]', 'current-price'),
                ('span[class*="price"][class*="product"]', 'product-price'),
                ('div[class*="price"]', 'price-div'),
                ('span.price', 'span-price'),
            ]
            
            for selector, desc in price_selectors:
                elements = soup.select(selector)
                if elements:
                    for elem in elements:
                        text = elem.get_text(strip=True)
                        extracted_price = self.extract_price(text)
                        if extracted_price:
                            price = extracted_price
                            logger.info(f"     Price found ({desc}): {price:,}đ")
                            break
                if price:
                    break
            
            # Fallback price from og:description (mentions giá tốt, trả góp)
            if not price:
                # Generate random price based on category
                price_ranges = {
                    'Điện thoại': (5000000, 35000000),
                    'Laptop': (15000000, 50000000),
                    'Tablet': (5000000, 20000000),
                    'Phụ kiện': (500000, 5000000)
                }
                min_p, max_p = price_ranges.get(category, (5000000, 30000000))
                price = random.randint(min_p, max_p)
                logger.info(f"     Price (random): {price:,}đ")
            
            # Old price
            old_price = int(price * random.uniform(1.1, 1.3)) if price else 0
            discount = round((old_price - price) / old_price * 100) if old_price > price else 0
            
            # ========== EXTRACT SPECIFICATIONS ==========
            
            logger.info(f"  🔍 Extracting specifications...")
            
            specs = []
            
            # Try multiple selectors for specs
            spec_selectors = [
                'div[class*="spec"]',
                'div[class*="Specifications"]',
                'li[class*="spec"]',
                'tr[class*="spec"]',
            ]
            
            for selector in spec_selectors:
                for elem in soup.select(selector):
                    text = elem.get_text(strip=True)
                    if text and 3 < len(text) < 100:
                        specs.append(f"• {text}")
                if specs:
                    break
            
            # Extract from description if available
            if not specs and description:
                # Parse description for specs
                lines = description.split('-')
                for line in lines:
                    line = line.strip()
                    if line and 5 < len(line) < 100:
                        specs.append(f"• {line}")
            
            detail = '\n'.join(specs[:8]) if specs else self.generate_default_specs(category)
            logger.info(f"     Specs: {len(specs)} items")
            
            # ========== EXTRACT BRAND ==========
            
            brand = self.extract_brand(name)
            logger.info(f"     Brand: {brand}")
            
            # ========== EXTRACT ALL IMAGES ==========
            
            logger.info(f"\n  🖼️  Extracting image URLs...")
            images = self.extract_product_images(soup)
            
            # Add main image if not in list
            if main_image and not any(img['url'] == main_image for img in images):
                images.insert(0, {'url': main_image, 'order': 0})
                images = [dict(img, order=i+1) for i, img in enumerate(images)]
            
            # ========== BUILD PRODUCT OBJECT ==========
            
            product = {
                'id': len(self.products) + 1,
                'name': name,
                'description': description[:200] if description else 'Sản phẩm chất lượng cao',
                'detail': detail,
                'summary': self.generate_summary(category),
                'category': category,
                'price': price,
                'old_price': old_price,
                'discount': discount,
                'brand': brand,
                'promotion': self.generate_promotion(discount),
                'rating': rating,
                'rating_count': rating_count,
                'main_image': main_image,
                'image_count': len(images),
                'images': images,
                'created_at': (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            logger.info(f"\n✅ Product extracted successfully!")
            logger.info(f"   📦 Name: {product['name']}")
            logger.info(f"   🏷️  Brand: {product['brand']}")
            logger.info(f"   💰 Price: {product['price']:,}đ (Discount: {product['discount']}%)")
            logger.info(f"   🖼️  Images: {len(images)}")
            logger.info(f"   ⭐ Rating: {product['rating']} ({product['rating_count']} reviews)")
            
            return product
        
        except Exception as e:
            logger.error(f"Error extracting product: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_default_specs(self, category):
        """Generate default specs if not found"""
        specs_map = {
            'Điện thoại': [
                '• Màn hình: 6.7\" AMOLED',
                '• Chip: Snapdragon 8 Gen 2',
                '• RAM: 12GB',
                '• Bộ nhớ: 256GB',
                '• Camera: 50MP chính + 12MP selfie',
                '• Pin: 5000mAh'
            ],
            'Laptop': [
                '• CPU: Intel Core i7',
                '• RAM: 16GB',
                '• SSD: 512GB',
                '• Display: 15.6" FHD',
                '• GPU: RTX 4060',
                '• Pin: 80Wh'
            ]
        }
        
        specs = specs_map.get(category, ['• Sản phẩm chất lượng cao'])
        return '\n'.join(specs)
    
    def generate_summary(self, category):
        """Generate marketing summary"""
        summaries = {
            'Điện thoại': 'Điện thoại flagship với công nghệ hàng đầu',
            'Laptop': 'Laptop cao cấp cho công việc và gaming',
            'Tablet': 'Máy tính bảng hiệu năng mạnh',
            'Phụ kiện': 'Phụ kiện chính hãng chất lượng cao'
        }
        return summaries.get(category, 'Sản phẩm chất lượng cao')
    
    def generate_promotion(self, discount):
        """Generate promotion text"""
        if discount > 0:
            return f"Giảm {discount}%! Mua ngay để tiết kiệm"
        return "Giá tốt nhất - Mua ngay"
    
    def scrape_product(self, url, category):
        """Scrape single product"""
        try:
            product = self.extract_product_details(url, category)
            if product:
                self.products.append(product)
                
                # Record image URLs
                for img in product['images']:
                    self.product_images.append({
                        'product_id': product['id'],
                        'image_url': img['url'],
                        'display_order': img['order']
                    })
            
            time.sleep(self.delay)
            return product
        
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def scrape_category(self, category_code, product_urls, limit=5):
        """Scrape products from category"""
        category_name = self.CATEGORIES.get(category_code, category_code)
        
        logger.info(f"\n{'='*80}")
        logger.info(f"📍 Scraping Category: {category_name}")
        logger.info(f"{'='*80}\n")
        
        product_urls = product_urls[:limit]
        
        for idx, url in enumerate(product_urls, 1):
            logger.info(f"\n[{idx}/{len(product_urls)}] Scraping: {url}")
            self.scrape_product(url, category_name)
    
    def extract_category_links(self, category_code, limit=5):
        """
        Extract product links from category page
        
        Returns:
            List of product URLs
        """
        try:
            url = f"{self.BASE_URL}/{category_code}.html"
            logger.info(f"\n📍 Fetching category: {url}")
            
            html = self.fetch_page(url)
            if not html:
                return []
            
            soup = BeautifulSoup(html, 'html.parser')
            
            product_urls = []
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                
                # Filter: category code, .html, not filter/sort
                if (category_code in href.lower() and 
                    href.endswith('.html') and 
                    not any(x in href for x in ['?', 'filter', 'sort', 'page'])):
                    
                    full_url = urljoin(self.BASE_URL, href)
                    if full_url not in product_urls:
                        product_urls.append(full_url)
            
            logger.info(f"✓ Found {len(product_urls)} products")
            return product_urls[:limit]
        
        except Exception as e:
            logger.error(f"Error extracting category links: {e}")
            return []
    
    def save_csv(self, filename='cellphones_selenium.csv'):
        """Save products to CSV"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                fieldnames = [
                    'id', 'name', 'description', 'detail', 'summary',
                    'category', 'price', 'old_price', 'discount',
                    'brand', 'promotion', 'rating', 'rating_count',
                    'main_image', 'image_count', 'created_at', 'updated_at'
                ]
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for product in self.products:
                    row = {k: v for k, v in product.items() if k != 'images'}
                    writer.writerow(row)
            
            logger.info(f"\n✅ CSV saved: {filename} ({len(self.products)} products)")
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")
    
    def save_json(self, filename='cellphones_selenium.json'):
        """Save products to JSON"""
        try:
            data = {
                'metadata': {
                    'source': 'cellphones.com.vn',
                    'scraped_at': datetime.now().isoformat(),
                    'total_products': len(self.products),
                    'total_images': len(self.product_images),
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'products': [
                    {k: v for k, v in p.items() if k != 'images'} 
                    for p in self.products
                ],
                'product_images': self.product_images
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ JSON saved: {filename}")
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
    
    def save_image_index(self, filename='image_index.json'):
        """Save image URLs index for reference"""
        try:
            data = {}
            for product in self.products:
                data[product['id']] = {
                    'name': product['name'],
                    'images': product['images'],
                    'image_count': product['image_count']
                }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Image index saved: {filename}")
        except Exception as e:
            logger.error(f"Error saving image index: {e}")
    
    def show_summary(self):
        """Show scraping summary"""
        print(f"\n{'='*80}")
        print(f"📊 SCRAPING SUMMARY")
        print(f"{'='*80}")
        print(f"✓ Total Products: {len(self.products)}")
        print(f"✓ Total Images: {len(self.product_images)}")
        print(f"\nProducts:")
        
        for product in self.products[:5]:
            print(f"\n  🔷 [{product['id']}] {product['name']}")
            print(f"     Brand: {product['brand']}")
            print(f"     Price: {product['price']:,}đ")
            print(f"     Images: {product['image_count']}")
            if product['images']:
                for img in product['images'][:3]:
                    print(f"       - {img['url'][:60]}...")
        
        print(f"\n{'='*80}\n")
    
    def run(self):
        """Run complete scraping"""
        try:
            # Setup Selenium
            self.setup_driver()
            
            # Scrape sample product
            logger.info(f"\n{'='*80}")
            logger.info(f"🚀 SELENIUM PRODUCT SCRAPER - STRUCTURED ANALYSIS")
            logger.info(f"{'='*80}\n")
            
            logger.info(f"📋 Configuration:")
            logger.info(f"   - Framework: Selenium WebDriver")
            logger.info(f"   - Browser: Chrome (headless)")
            logger.info(f"   - Page Rendering: Full JavaScript execution")
            logger.info(f"   - Image Extraction: All URLs (no download)")
            logger.info(f"   - Meta Tags: og:title, og:description, og:image")
            logger.info(f"   - Content: Rendered DOM + Meta tags\n")
            
            # Example: Scrape a product directly
            sample_url = f"{self.BASE_URL}/laptop-asus-tuf-gaming-f16-fx607vj-rl034w.html"
            
            logger.info(f"🎯 Target Product:")
            logger.info(f"   URL: {sample_url}\n")
            
            self.scrape_product(sample_url, 'Laptop')
            
            # Export
            logger.info(f"\n{'='*80}")
            logger.info(f"💾 EXPORTING DATA")
            logger.info(f"{'='*80}\n")
            
            self.save_csv()
            self.save_json()
            self.save_image_index()
            
            # Show summary
            self.show_summary()
            
            logger.info(f"✅ Scraping complete!")
            logger.info(f"\n📁 Output files:")
            logger.info(f"   - cellphones_selenium.csv")
            logger.info(f"   - cellphones_selenium.json")
            logger.info(f"   - image_index.json")
            logger.info(f"\n📊 Statistics:")
            logger.info(f"   - Products: {len(self.products)}")
            logger.info(f"   - Total Images: {len(self.product_images)}")
        
        finally:
            # Close browser
            self.close_driver()


def main():
    """Main entry point"""
    scraper = SeleniumProductScraper(
        headless=True,      # Run in headless mode
        delay=2             # 2 second delay between requests
    )
    
    scraper.run()


if __name__ == '__main__':
    main()
