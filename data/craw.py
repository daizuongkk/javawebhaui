"""
CellphoneS → Database Scraper
Maps scraped data to your ecommerce schema:
  - products
  - product_images
  - inventory
  - reviews (structure only — không scrape được user_id thật)

Requirements:
    pip install requests beautifulsoup4 pandas

Usage:
    python cellphones_db_scraper.py
    python cellphones_db_scraper.py --category dien-thoai --pages 5
    python cellphones_db_scraper.py --category laptop --pages 3 --output sql
    python cellphones_db_scraper.py --category dien-thoai --pages 2 --output all
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import argparse
import re
import os
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────

BASE_URL = "https://cellphones.com.vn"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://cellphones.com.vn/",
}

CATEGORIES = {
    "dien-thoai":  "/mobile.html",
    "laptop":      "/laptop.html",
    "tablet":      "/tablet.html",
    "smartwatch":  "/smartwatch-thong-minh.html",
    "phu-kien":    "/phu-kien.html",
    "am-thanh":    "/am-thanh.html",
    "man-hinh":    "/man-hinh.html",
}

# Default inventory quantity when scraping (stock info usually needs login)
DEFAULT_INVENTORY_QTY = 50

# ─── Helpers ──────────────────────────────────────────────────────────────────

def clean_price(text: str) -> float | None:
    if not text:
        return None
    digits = re.sub(r"[^\d]", "", text)
    return float(digits) if digits else None


def escape_sql(s: str | None) -> str:
    if s is None:
        return "NULL"
    s = str(s).replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ").replace("\r", "")
    return f"'{s}'"


def get_page(url: str, retries: int = 3) -> BeautifulSoup | None:
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except requests.RequestException as e:
            print(f"  [!] Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)
    return None


# ─── Detail page scraper ──────────────────────────────────────────────────────

def scrape_detail(url: str) -> dict:
    """
    Scrapes a single product detail page.
    Returns data mapped to the DB schema fields.
    """
    soup = get_page(url)
    if not soup:
        return {}

    result = {}

    # ── description (maps to products.description, max 2000 chars) ──
    desc_el = (
        soup.select_one("div.product-description")
        or soup.select_one("[class*='short-description']")
        or soup.select_one("div.des-content")
    )
    if desc_el:
        result["description"] = desc_el.get_text(separator=" ", strip=True)[:2000]

    # ── detail (maps to products.detail, full HTML/text) ──
    detail_el = (
        soup.select_one("div.content-product-detail")
        or soup.select_one("[class*='product-detail-content']")
        or soup.select_one("div#product-description")
    )
    if detail_el:
        result["detail"] = detail_el.get_text(separator="\n", strip=True)

    # ── summary — first sentence of description or meta description ──
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        result["summary"] = meta_desc["content"][:255]

    # ── brand — from breadcrumb, meta, or spec table ──
    brand_el = (
        soup.select_one("span.product-brand")
        or soup.select_one("[class*='brand-name']")
        or soup.select_one("a[class*='brand']")
    )
    if brand_el:
        result["brand"] = brand_el.get_text(strip=True)[:255]

    # Try extracting brand from spec table if not found
    if not result.get("brand"):
        spec_rows = soup.select("table.product-info-table tr") or soup.select("[class*='specification'] tr")
        for row in spec_rows:
            cells = row.find_all(["td", "th"])
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True).lower()
                if "thương hiệu" in key or "hãng" in key or "brand" in key:
                    result["brand"] = cells[1].get_text(strip=True)[:255]
                    break

    # ── all product images (maps to product_images table) ──
    images = []
    # Main image
    main_img = (
        soup.select_one("img.product-main-img")
        or soup.select_one("div.product-image img")
        or soup.select_one("[class*='product-gallery'] img")
    )
    if main_img:
        src = main_img.get("src") or main_img.get("data-src")
        if src:
            images.append(src)

    # Thumbnail gallery
    for thumb in soup.select("div.product-thumbnail img, [class*='gallery-thumb'] img, ul.product-list-thumbnail img"):
        src = thumb.get("src") or thumb.get("data-src")
        if src and src not in images:
            images.append(src)

    result["images"] = images

    # ── reviews ──
    reviews = []
    for rev_el in soup.select("[class*='review-item'], [class*='comment-item']")[:20]:
        score_el = rev_el.select_one("[class*='rating'], [class*='star']")
        score_text = score_el.get_text(strip=True) if score_el else ""
        # Try to extract numeric score
        score_match = re.search(r"\d", score_text)
        score = int(score_match.group()) if score_match else None

        feedback_el = rev_el.select_one("[class*='content'], p, span.text")
        feedback = feedback_el.get_text(strip=True)[:2000] if feedback_el else None

        if feedback:
            reviews.append({"score": score, "feedback": feedback})

    result["reviews"] = reviews

    return result


# ─── Listing page scraper ─────────────────────────────────────────────────────

def scrape_listing_page(soup: BeautifulSoup, category_name: str) -> list[dict]:
    """Parse product cards from a category listing page."""
    products = []

    cards = (
        soup.select("div.product-info-container")
        or soup.select("li.product-item")
        or soup.select("div.cps-product-item")
        or soup.select("div[class*='product-item']")
    )

    if not cards:
        print("  [!] No product cards found — layout may have changed.")
        return products

    for card in cards:
        try:
            name_el = (
                card.select_one("h3")
                or card.select_one("p.product-name")
                or card.select_one("[class*='product-name']")
            )
            name = name_el.get_text(strip=True) if name_el else None
            if not name:
                continue

            link_el = card.select_one("a[href]")
            href = link_el["href"] if link_el else None
            url = (BASE_URL + href) if href and not href.startswith("http") else href

            price_el = (
                card.select_one("p.product-price")
                or card.select_one("[class*='product-price']")
                or card.select_one("span.price")
            )
            price_text = price_el.get_text(strip=True) if price_el else None
            price = clean_price(price_text)

            # Thumbnail (first image for product_images)
            img_el = card.select_one("img")
            thumb = img_el.get("src") or img_el.get("data-src") if img_el else None

            products.append({
                # ── products table ──
                "name": name[:255],
                "category": category_name,
                "price": price,
                "description": None,   # filled later from detail page
                "detail": None,
                "summary": None,
                "brand": None,
                # ── meta ──
                "url": url,
                "thumb": thumb,
                # ── related tables ──
                "images": [thumb] if thumb else [],
                "reviews": [],
            })
        except Exception as e:
            print(f"  [!] Card parse error: {e}")

    return products


# ─── Category crawler ─────────────────────────────────────────────────────────

def crawl_category(
    category_slug: str,
    max_pages: int = 3,
    fetch_details: bool = True,
    delay: float = 1.5,
) -> list[dict]:
    path = CATEGORIES.get(category_slug, f"/{category_slug}.html")
    all_products = []

    for page_num in range(1, max_pages + 1):
        url = BASE_URL + path + (f"?page={page_num}" if page_num > 1 else "")
        print(f"\n  📄 Page {page_num}: {url}")

        soup = get_page(url)
        if not soup:
            break

        products = scrape_listing_page(soup, category_slug)
        if not products:
            print("  [!] No products found, stopping.")
            break

        print(f"  ✔ Found {len(products)} products")

        if fetch_details:
            for i, p in enumerate(products):
                if p.get("url"):
                    print(f"    [{i+1}/{len(products)}] {p['name'][:60]}")
                    extra = scrape_detail(p["url"])
                    # Merge detail data
                    for k in ("description", "detail", "summary", "brand"):
                        if extra.get(k):
                            p[k] = extra[k]
                    if extra.get("images"):
                        # Merge images, avoid duplicates
                        existing = set(p["images"])
                        for img in extra["images"]:
                            if img not in existing:
                                p["images"].append(img)
                                existing.add(img)
                    if extra.get("reviews"):
                        p["reviews"] = extra["reviews"]
                    time.sleep(delay)

        all_products.extend(products)
        time.sleep(delay)

    return all_products


# ─── SQL Generator ────────────────────────────────────────────────────────────

def generate_sql(products: list[dict], start_id: int = 1) -> str:
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("-- ============================================================")
    lines.append(f"-- Generated by cellphones_db_scraper.py at {now}")
    lines.append(f"-- Total products: {len(products)}")
    lines.append("-- ============================================================\n")

    lines.append("SET NAMES utf8mb4;")
    lines.append("SET FOREIGN_KEY_CHECKS = 0;\n")

    # ── products ──────────────────────────────────────────────────────────────
    lines.append("-- ===================== products =====================")
    lines.append("INSERT INTO products (id, name, description, detail, summary, category, price, brand, created_at, updated_at)")
    lines.append("VALUES")

    product_rows = []
    for idx, p in enumerate(products):
        pid = start_id + idx
        p["_db_id"] = pid
        row = (
            f"  ({pid}, "
            f"{escape_sql(p.get('name'))}, "
            f"{escape_sql(p.get('description'))}, "
            f"{escape_sql(p.get('detail'))}, "
            f"{escape_sql(p.get('summary'))}, "
            f"{escape_sql(p.get('category'))}, "
            f"{p['price'] if p.get('price') else 'NULL'}, "
            f"{escape_sql(p.get('brand'))}, "
            f"'{now}', '{now}')"
        )
        product_rows.append(row)

    lines.append(",\n".join(product_rows) + ";")
    lines.append("")

    # ── product_images ────────────────────────────────────────────────────────
    lines.append("-- ===================== product_images =====================")
    img_rows = []
    img_id = 1
    for p in products:
        pid = p["_db_id"]
        for img_url in p.get("images", []):
            if img_url:
                img_rows.append(f"  ({img_id}, {pid}, {escape_sql(img_url)})")
                img_id += 1

    if img_rows:
        lines.append("INSERT INTO product_images (id, product_id, image_url)")
        lines.append("VALUES")
        lines.append(",\n".join(img_rows) + ";")
    else:
        lines.append("-- (no images found)")
    lines.append("")

    # ── inventory ─────────────────────────────────────────────────────────────
    lines.append("-- ===================== inventory =====================")
    inv_rows = []
    for p in products:
        pid = p["_db_id"]
        inv_rows.append(f"  ({pid}, {DEFAULT_INVENTORY_QTY}, '{now}')")

    lines.append("INSERT INTO inventory (product_id, quantity, updated_at)")
    lines.append("VALUES")
    lines.append(",\n".join(inv_rows) + ";")
    lines.append("")

    # ── reviews (sample, no real user_id) ────────────────────────────────────
    review_rows = []
    rev_id = 1
    # Use user_id = 1 as placeholder (admin/test user)
    for p in products:
        pid = p["_db_id"]
        for r in p.get("reviews", []):
            feedback = escape_sql(r.get("feedback"))
            score = r.get("score") if r.get("score") else "NULL"
            review_rows.append(
                f"  ({rev_id}, {feedback}, {score}, 1, {pid}, '{now}')"
            )
            rev_id += 1

    if review_rows:
        lines.append("-- ===================== reviews =====================")
        lines.append("-- NOTE: user_id = 1 is a placeholder. Update with real user IDs.")
        lines.append("INSERT INTO reviews (id, feedback, score, user_id, product_id, created_at)")
        lines.append("VALUES")
        lines.append(",\n".join(review_rows) + ";")
        lines.append("")

    lines.append("SET FOREIGN_KEY_CHECKS = 1;")
    return "\n".join(lines)


# ─── JSON/CSV Exporters ───────────────────────────────────────────────────────

def export_json(products: list[dict], path: str):
    # Remove internal _db_id
    clean = [{k: v for k, v in p.items() if k != "_db_id"} for p in products]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, indent=2)
    print(f"  ✅ JSON  → {path}")


def export_csv_products(products: list[dict], path: str):
    rows = []
    for p in products:
        rows.append({
            "id":          p.get("_db_id", ""),
            "name":        p.get("name", ""),
            "description": (p.get("description") or "")[:2000],
            "detail":      (p.get("detail") or "")[:500] + "..." if p.get("detail") and len(p.get("detail","")) > 500 else p.get("detail",""),
            "summary":     p.get("summary", ""),
            "category":    p.get("category", ""),
            "price":       p.get("price", ""),
            "brand":       p.get("brand", ""),
            "image_count": len(p.get("images", [])),
            "review_count": len(p.get("reviews", [])),
            "url":         p.get("url", ""),
        })
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  ✅ CSV   → {path}")


def export_csv_images(products: list[dict], path: str):
    rows = []
    for p in products:
        pid = p.get("_db_id", "")
        for img in p.get("images", []):
            rows.append({"product_id": pid, "image_url": img})
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  ✅ CSV   → {path}")


def export_csv_inventory(products: list[dict], path: str):
    rows = [
        {"product_id": p.get("_db_id", ""), "quantity": DEFAULT_INVENTORY_QTY}
        for p in products
    ]
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  ✅ CSV   → {path}")


def export_csv_reviews(products: list[dict], path: str):
    rows = []
    for p in products:
        pid = p.get("_db_id", "")
        for r in p.get("reviews", []):
            rows.append({
                "product_id": pid,
                "user_id":    1,    # placeholder
                "score":      r.get("score", ""),
                "feedback":   r.get("feedback", ""),
            })
    if rows:
        pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  ✅ CSV   → {path}")
    else:
        print(f"  ℹ️  No reviews scraped (reviews may require login on CellphoneS).")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Scrape CellphoneS and export data matching ecommerce DB schema"
    )
    parser.add_argument(
        "--category", default="dien-thoai",
        help=f"Category: {', '.join(CATEGORIES.keys())} (default: dien-thoai)"
    )
    parser.add_argument("--pages",   type=int,   default=3,     help="Pages to scrape (default: 3)")
    parser.add_argument("--delay",   type=float, default=1.5,   help="Delay between requests in seconds")
    parser.add_argument("--no-details", action="store_true",    help="Skip detail page scraping (faster, less data)")
    parser.add_argument(
        "--output", choices=["sql", "csv", "json", "all"], default="all",
        help="Output format (default: all)"
    )
    parser.add_argument("--start-id", type=int, default=1,      help="Starting product ID for SQL (default: 1)")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  CellphoneS → DB Scraper")
    print(f"  Category   : {args.category}")
    print(f"  Pages      : {args.pages}")
    print(f"  Details    : {'No' if args.no_details else 'Yes'}")
    print(f"  Output     : {args.output}")
    print(f"{'='*60}")

    products = crawl_category(
        args.category,
        max_pages=args.pages,
        fetch_details=not args.no_details,
        delay=args.delay,
    )

    if not products:
        print("\n[!] No products scraped. The site layout may have changed.")
        return

    # Assign DB IDs
    for i, p in enumerate(products):
        p["_db_id"] = args.start_id + i

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = args.category
    out = args.output

    print(f"\n{'='*60}")
    print(f"  Exporting {len(products)} products...")
    print(f"{'='*60}")

    if out in ("sql", "all"):
        sql = generate_sql(products, start_id=args.start_id)
        sql_path = f"cellphones_{slug}_{ts}.sql"
        with open(sql_path, "w", encoding="utf-8") as f:
            f.write(sql)
        print(f"  ✅ SQL   → {sql_path}")

    if out in ("json", "all"):
        export_json(products, f"cellphones_{slug}_{ts}.json")

    if out in ("csv", "all"):
        export_csv_products(products,  f"cellphones_{slug}_{ts}_products.csv")
        export_csv_images(products,    f"cellphones_{slug}_{ts}_product_images.csv")
        export_csv_inventory(products, f"cellphones_{slug}_{ts}_inventory.csv")
        export_csv_reviews(products,   f"cellphones_{slug}_{ts}_reviews.csv")

    print(f"\n{'='*60}")
    print(f"  ✅ Done! {len(products)} products exported.")
    print(f"{'='*60}\n")

    # Quick summary
    with_price    = sum(1 for p in products if p.get("price"))
    with_brand    = sum(1 for p in products if p.get("brand"))
    with_images   = sum(1 for p in products if p.get("images"))
    total_images  = sum(len(p.get("images", [])) for p in products)
    total_reviews = sum(len(p.get("reviews", [])) for p in products)

    print("  Summary:")
    print(f"    Products with price  : {with_price}/{len(products)}")
    print(f"    Products with brand  : {with_brand}/{len(products)}")
    print(f"    Products with images : {with_images}/{len(products)} ({total_images} total images)")
    print(f"    Reviews scraped      : {total_reviews}")


if __name__ == "__main__":
    main()