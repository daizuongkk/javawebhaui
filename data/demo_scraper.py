#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DEMO SCRIPT - Cellphones Scraper Quick Start
============================================
Chạy script này để thấy scraper hoạt động như thế nào
"""

from scrape_cellphones import UniversalCellphonesScraper
import json
from datetime import datetime

def demo_basic():
    """Demo cơ bản - Scrape 1 category"""
    print("\n" + "="*70)
    print("🎯 DEMO #1: Quick scrape (1 category only)")
    print("="*70 + "\n")
    
    scraper = UniversalCellphonesScraper(delay=0.3)
    scraper.scrape_category('dien-thoai')  # Only smartphones
    
    print(f"\n✅ Scraped {len(scraper.products)} products")
    print(f"   Images: {len(scraper.images)}")
    print(f"   Inventory: {len(scraper.inventory)}")
    
    if scraper.products:
        print("\n📱 Sample products:")
        for p in scraper.products[:3]:
            print(f"   - {p['name'][:40]}")
            print(f"     💰 {p['price']:,} VND (was {p['old_price']:,})")
            print(f"     ⭐ {p['rating']}/5 ({p['rating_count']} reviews)\n")

def demo_full():
    """Demo đầy đủ - Scrape tất cả categories"""
    print("\n" + "="*70)
    print("🎯 DEMO #2: Full scrape (all categories)")
    print("="*70 + "\n")
    
    print("⏳ This will take ~30-60 seconds...\n")
    
    scraper = UniversalCellphonesScraper(delay=0.5)
    scraper.scrape_all()
    scraper.export()
    
    print("\n✅ Export completed!")
    print(f"   📊 Total: {len(scraper.products)} products")
    print(f"   📁 Check: cellphones_data.json and cellphones_data.sql")

def demo_custom():
    """Demo custom - Scrape with custom settings"""
    print("\n" + "="*70)
    print("🎯 DEMO #3: Custom configuration")
    print("="*70 + "\n")
    
    # Create scraper with custom delay
    scraper = UniversalCellphonesScraper(delay=1.0)
    
    # Modify categories
    scraper.CATEGORIES['smartwatch'] = {'name': 'Smartwatch', 'path': 'smartwatch'}
    
    # Scrape only selected categories
    print("Scraping: Smartphone + Laptop + Accessories\n")
    scraper.scrape_category('dien-thoai')
    scraper.scrape_category('laptop')
    scraper.scrape_category('phu-kien')
    
    print(f"\n✅ Custom scrape completed!")
    print(f"   Products: {len(scraper.products)}")
    
    # Show price statistics
    if scraper.products:
        prices = [p['price'] for p in scraper.products]
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        print(f"\n💰 Price Statistics:")
        print(f"   Min: {min_price:,} VND")
        print(f"   Avg: {avg_price:,.0f} VND")
        print(f"   Max: {max_price:,} VND")

def demo_analysis():
    """Demo analysis - Phân tích dữ liệu đã scrape"""
    print("\n" + "="*70)
    print("🎯 DEMO #4: Data Analysis")
    print("="*70 + "\n")
    
    # Load dữ liệu từ file nếu có
    try:
        with open('cellphones_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products = data['products']
        images = data['product_images']
        
        print(f"📊 Data Analysis for {len(products)} products:\n")
        
        # By category
        categories = {}
        for p in products:
            cat = p['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("Categories distribution:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"   {cat:20} : {count:3} products")
        
        # Price analysis
        prices = [p['price'] for p in products]
        print(f"\n💰 Price range:")
        print(f"   Min: {min(prices):>15,} VND")
        print(f"   Avg: {sum(prices)/len(prices):>15,.0f} VND")
        print(f"   Max: {max(prices):>15,} VND")
        
        # Discount analysis
        discounts = [p['discount'] for p in products]
        print(f"\n🎁 Discount:")
        print(f"   Average: {sum(discounts)/len(discounts):.1f}%")
        print(f"   Range: {min(discounts)}% - {max(discounts)}%")
        
        # Rating analysis
        ratings = [p['rating'] for p in products]
        print(f"\n⭐ Rating:")
        print(f"   Average: {sum(ratings)/len(ratings):.2f}/5")
        print(f"   Range: {min(ratings)} - {max(ratings)}")
        
        # Images analysis
        print(f"\n📸 Images:")
        print(f"   Total: {len(images)}")
        print(f"   Avg per product: {len(images)/len(products):.1f}")
        
    except FileNotFoundError:
        print("⚠️ cellphones_data.json not found")
        print("   Run demo_full() or scrape_cellphones.py first")

def show_menu():
    """Show interactive menu"""
    print("\n" + "="*70)
    print("🛍️  CELLPHONES SCRAPER - DEMO MENU")
    print("="*70)
    print("\nChoose a demo to run:\n")
    print("  1. Quick Demo      - Scrape 1 category (Smartphones)")
    print("  2. Full Demo       - Scrape all categories")
    print("  3. Custom Demo     - Custom scraping settings")
    print("  4. Analysis Demo   - Analyze scraped data")
    print("  0. Exit")
    print("\n" + "="*70)
    
    choice = input("\nEnter your choice (0-4): ").strip()
    
    demos = {
        '1': ('Quick Demo', demo_basic),
        '2': ('Full Demo', demo_full),
        '3': ('Custom Demo', demo_custom),
        '4': ('Analysis Demo', demo_analysis),
    }
    
    if choice in demos:
        title, func = demos[choice]
        print(f"\n▶️  Running {title}...")
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("\n💡 Make sure you have:")
            print("   - requests library: pip install requests")
            print("   - beautifulsoup4: pip install beautifulsoup4")
    elif choice == '0':
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice. Try again.")

if __name__ == '__main__':
    # Optional: Run demo directly without menu
    # Uncomment one of the following:
    
    # demo_basic()
    # demo_full()
    # demo_custom()
    # demo_analysis()
    
    # Or show interactive menu
    show_menu()
