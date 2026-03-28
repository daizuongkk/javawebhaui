"""
CellphoneS Accessories Scraper
================================
Dựa theo cấu trúc HTML thực tế của CellphoneS (từ source tham khảo).
Cào danh sách phụ kiện, vào từng trang chi tiết, sinh SQL INSERT
khớp với schema: products, product_images, inventory, reviews, users.

Cài thư viện:
    pip install selenium webdriver-manager beautifulsoup4 lxml

Chạy:
    python cellphones_scraper.py

Output:
    cellphones_data.json   -- raw data để debug
    cellphones_data.sql    -- import thẳng vào MySQL
"""

import json
import logging
import re
import time
import random
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# ──────────────────────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler(),
    ]
)
log = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────
BASE_URL = "https://cellphones.com.vn"

# Slug của các category phụ kiện trên CellphoneS
ACCESSORY_CATEGORIES = [
    "op-lung-dien-thoai",
    "kinh-cuong-luc",
    "sac-du-phong",
    "cap-sac",
    "tai-nghe",
    "op-lung-may-tinh-bang",
    "bao-da",
    "gia-do-dien-thoai",
]

CATEGORY_NAMES = {
    "op-lung-dien-thoai":    "Op lung dien thoai",
    "kinh-cuong-luc":        "Kinh cuong luc",
    "sac-du-phong":          "Sac du phong",
    "cap-sac":               "Cap sac",
    "tai-nghe":              "Tai nghe",
    "op-lung-may-tinh-bang": "Op lung may tinh bang",
    "bao-da":                "Bao da",
    "gia-do-dien-thoai":     "Gia do dien thoai",
}

MAX_PRODUCTS_PER_CATEGORY = 20   # giới hạn sp/category, tăng nếu muốn nhiều hơn
SHOW_MORE_WAIT  = 3   # giây chờ sau click "Xem thêm"
PAGE_LOAD_WAIT  = 8   # giây chờ trang detail load
DETAIL_DELAY    = (2, 4)  # random delay giữa các request detail

START_PRODUCT_ID = 1  # ID bắt đầu (đổi nếu DB đã có data)


# ──────────────────────────────────────────────────────────────
# DRIVER
# ──────────────────────────────────────────────────────────────
def build_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--window-size=1440,900")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service, options=opts)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"},
    )
    return driver


# ──────────────────────────────────────────────────────────────
# HELPER
# ──────────────────────────────────────────────────────────────
def parse_price(text: str) -> float:
    """'32.990.000 ₫'  →  32990000.0  (giống source tham khảo)"""
    if not text:
        return 0.0
    cleaned = str(text).translate({ord(c): None for c in " .₫\xa0,"})
    return float(cleaned) if cleaned.isdigit() else 0.0


def _q(s) -> str:
    """Escape string cho SQL INSERT."""
    if s is None:
        return "NULL"
    escaped = (str(s)
               .replace("\\", "\\\\")
               .replace("'", "\\'")
               .replace("\n", " ")
               .replace("\r", "")
               .strip())
    return f"'{escaped}'"


# ──────────────────────────────────────────────────────────────
# CRAWL CATEGORY PAGE  →  danh sách sản phẩm thô
# ──────────────────────────────────────────────────────────────
def crawl_category(driver: webdriver.Chrome, slug: str) -> list[dict]:
    """
    Mở trang category, click "Xem thêm" cho đến hết,
    rồi parse tất cả .item-product (class thực tế từ source tham khảo).
    Trả về list dict: {id, name, link, img_src, old_price, special_price}
    """
    url = f"{BASE_URL}/{slug}.html"
    log.info("  GET category: %s", url)
    driver.get(url)
    time.sleep(PAGE_LOAD_WAIT)

    # ── Click "Xem thêm / btn-load-more" cho đến khi ẩn ────────
    # (y hệt source tham khảo, chỉ đổi JS click thành .click() thật)
    try:
        while True:
            btn = driver.find_element(
                By.CSS_SELECTOR,
                "a.btn-show-more.btn-load-more, button.btn-show-more, .btn-show-more"
            )
            style = btn.get_attribute("style") or ""
            if "display: none" in style or "display:none" in style:
                break
            driver.execute_script("arguments[0].click();", btn)
            log.info("    → click 'Xem them'")
            time.sleep(SHOW_MORE_WAIT)
    except NoSuchElementException:
        log.info("    (Khong co nut Xem them)")
    except Exception as e:
        log.warning("    show-more exception: %s", e)

    # ── Parse HTML ──────────────────────────────────────────────
    soup = BeautifulSoup(driver.page_source, "lxml")

    # CellphoneS dùng class "item-product" cho mỗi thẻ sản phẩm
    # (đúng theo source tham khảo)
    items_raw = soup.find_all("div", class_="item-product")
    log.info("  → Tìm được %d .item-product", len(items_raw))

    products = []
    seen_ids: set[str] = set()

    for item in items_raw[:MAX_PRODUCTS_PER_CATEGORY]:
        try:
            _id = item.get("id", "")
            if not _id or _id in seen_ids:
                continue
            seen_ids.add(_id)

            # name & link  (class từ source tham khảo)
            name_tag = (
                item.find("div", class_="item-product__box-name") or
                item.find("div", class_="product-info")
            )
            a_name = name_tag.find("a") if name_tag else None
            name   = a_name.get_text(strip=True) if a_name else None
            if not name:
                continue

            # link detail
            img_box = (
                item.find("div", class_="item-product__box-img") or
                item.find("div", class_="product-img")
            )
            link = None
            img_src = None
            if img_box:
                a_img   = img_box.find("a")
                link    = a_img.get("href") if a_img else None
                img_tag = img_box.find("img")
                img_src = (img_tag.get("data-src") or img_tag.get("src")) if img_tag else None

            if link and not link.startswith("http"):
                link = BASE_URL + link

            # giá  (class từ source tham khảo)
            price_box = (
                item.find("div", class_="item-product__box-price") or
                item.find("div", class_="product-price")
            )
            old_price     = None
            special_price = None
            if price_box:
                old_el = price_box.find("p", class_="old-price")
                spe_el = price_box.find("p", class_="special-price")
                if old_el:
                    old_price = parse_price(old_el.get_text())
                if spe_el and "Dang ky" not in spe_el.get_text():
                    special_price = parse_price(spe_el.get_text())

            products.append({
                "id":            _id,
                "name":          name,
                "link":          link,
                "img_src":       img_src,
                "old_price":     old_price,
                "special_price": special_price,
            })

        except Exception as e:
            log.warning("    parse item lỗi: %s", e)

    return products


# ──────────────────────────────────────────────────────────────
# CRAWL DETAIL PAGE  →  bổ sung thông tin chi tiết
# ──────────────────────────────────────────────────────────────
def crawl_detail(driver: webdriver.Chrome, product: dict, category: str) -> dict:
    """
    Vào trang chi tiết sản phẩm, lấy:
    - blog_content (div.blog-content)  → field `detail`
    - thông số kỹ thuật (#tskt)        → field `description`
    - ảnh gallery                      → image_urls[]
    - rating, review_count
    - brand
    Trả về dict đã enriched.
    """
    link = product.get("link")
    if not link:
        return _enrich_basic(product, category)

    try:
        driver.get(link)
        WebDriverWait(driver, PAGE_LOAD_WAIT).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        time.sleep(2)
    except TimeoutException:
        log.warning("    Timeout: %s", link)
        return _enrich_basic(product, category)

    soup = BeautifulSoup(driver.page_source, "lxml")

    # ── blog-content  →  detail ───────────────────────────────
    # (y hệt source tham khảo: div.blog-content)
    detail = ""
    div_blog = soup.find("div", class_="blog-content")
    if div_blog:
        detail = div_blog.get_text(" ", strip=True)[:5000]

    # ── thông số kỹ thuật (#tskt)  →  description ────────────
    # (y hệt source tham khảo: detail_soup.select("#tskt tr"))
    specs = []
    for tr in soup.select("#tskt tr"):
        ths = tr.select("th")
        if len(ths) < 2:
            continue
        title = ths[0].get_text(strip=True)
        value = ths[1].get_text(strip=True)
        if "dang cap nhat" in title.lower() or "đang cập nhật" in title.lower():
            break
        if title and value:
            specs.append(f"{title}: {value}")
    description = " | ".join(specs)[:2000] if specs else ""

    # ── summary (meta description) ────────────────────────────
    summary = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        summary = (meta.get("content") or "")[:255]

    # ── brand ─────────────────────────────────────────────────
    brand = None
    brand_el = soup.select_one(".product-brand img, .brand-name, a.brand-link")
    if brand_el:
        brand = brand_el.get("alt") or brand_el.get_text(strip=True)
    if not brand:
        # fallback: từ đầu tiên trong tên sản phẩm
        brand = (product.get("name") or "").split()[0]

    # ── gallery images ─────────────────────────────────────────
    # Ưu tiên slider ảnh, sau đó ảnh thumbnail
    images: list[str] = []
    for sel in [
        ".product-image-gallery img",
        ".slick-slide img",
        ".product__media-gallery img",
        ".product-photos img",
    ]:
        for img in soup.select(sel):
            src = img.get("data-src") or img.get("src") or ""
            if src.startswith("http") and src not in images:
                images.append(src)
        if images:
            break
    # fallback: ảnh đã có từ category page
    if not images and product.get("img_src"):
        images = [product["img_src"]]

    # ── rating ────────────────────────────────────────────────
    rating = None
    review_count = 0
    for sel in [".average", ".rating-average", ".product-rating span"]:
        el = soup.select_one(sel)
        if el:
            try:
                v = float(re.sub(r"[^\d.]", "", el.get_text()))
                rating = v * 20 if v <= 5 else v  # /5 → /100
            except ValueError:
                pass
            break
    for sel in [".count-review", ".review-count", "[class*='count-review']"]:
        el = soup.select_one(sel)
        if el:
            nums = re.findall(r"\d+", el.get_text())
            review_count = int(nums[0]) if nums else 0
            break

    return {
        **product,
        "category":     category,
        "brand":        brand,
        "description":  description,
        "detail":       detail,
        "summary":      summary,
        "image_urls":   images,
        "rating":       rating,
        "review_count": review_count,
        # giá cuối cùng: special_price nếu có, không thì old_price
        "price":        product.get("special_price") or product.get("old_price") or 0.0,
        "promotion":    _calc_promo(product.get("old_price"), product.get("special_price")),
    }


def _enrich_basic(product: dict, category: str) -> dict:
    """Khi không vào được trang detail, dùng data từ category page."""
    imgs = [product["img_src"]] if product.get("img_src") else []
    return {
        **product,
        "category":     category,
        "brand":        (product.get("name") or "").split()[0],
        "description":  "",
        "detail":       "",
        "summary":      "",
        "image_urls":   imgs,
        "rating":       None,
        "review_count": 0,
        "price":        product.get("special_price") or product.get("old_price") or 0.0,
        "promotion":    _calc_promo(product.get("old_price"), product.get("special_price")),
    }


def _calc_promo(old, special) -> int:
    if old and special and old > special > 0:
        return round((old - special) / old * 100)
    return 0


# ──────────────────────────────────────────────────────────────
# MAIN LOOP
# ──────────────────────────────────────────────────────────────
def scrape_all() -> list[dict]:
    driver = build_driver()
    all_products: list[dict] = []
    seen_ids: set[str] = set()

    try:
        for slug in ACCESSORY_CATEGORIES:
            cat_name = CATEGORY_NAMES[slug]
            log.info("=" * 55)
            log.info("CATEGORY: %s", cat_name)
            log.info("=" * 55)

            raw_list = crawl_category(driver, slug)

            for i, raw in enumerate(raw_list, 1):
                pid = raw.get("id", "")
                if pid in seen_ids:
                    continue
                seen_ids.add(pid)

                log.info("  [%d/%d] %s", i, len(raw_list), raw.get("name", "")[:60])

                enriched = crawl_detail(driver, raw, cat_name)
                all_products.append(enriched)

                log.info("    price=%.0f  promo=%d%%  imgs=%d  specs=%d chars",
                         enriched["price"],
                         enriched["promotion"],
                         len(enriched["image_urls"]),
                         len(enriched["description"]))

                time.sleep(random.uniform(*DETAIL_DELAY))

    finally:
        driver.quit()

    log.info("TONG: %d san pham", len(all_products))
    return all_products


# ──────────────────────────────────────────────────────────────
# SQL GENERATOR
# ──────────────────────────────────────────────────────────────
FAKE_USERS = [
    ("nguyen_tuan", "Tuan"),  ("tran_linh", "Linh"),   ("le_minh", "Minh"),
    ("pham_thu", "Thu"),      ("hoang_nam", "Nam"),     ("bui_huong", "Huong"),
    ("do_quang", "Quang"),    ("ngo_bich", "Bich"),     ("duong_long", "Long"),
    ("vu_an", "An"),
]

REVIEW_TEXTS = [
    "San pham dung mo ta, giao hang nhanh.",
    "Chat luong tot, dung on dinh.",
    "Hang dep, dong goi can than.",
    "Rat hai long, se ung ho tiep.",
    "Tot cho tam gia, recommend.",
    "Giao hang nhanh, san pham chinh hang.",
    "Mau sac dep, vua tay.",
    "Dung duoc roi moi review, on.",
    "Gia hop ly, chat luong dat yeu cau.",
    "Hang chuan shop, khong that vong.",
]


def build_sql(products: list[dict]) -> str:
    lines: list[str] = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines += [
        "-- ============================================================",
        f"-- CellphoneS Accessories  |  Generated: {now}",
        f"-- Products: {len(products)}",
        "-- ============================================================",
        "SET NAMES utf8mb4;",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "",
    ]

    # ── users ──────────────────────────────────────────────────
    lines.append("-- ===== USERS =====")
    for uid, (uname, fname) in enumerate(FAKE_USERS, start=1):
        lines.append(
            f"INSERT IGNORE INTO users "
            f"(id, username, email, password, first_name, role, status, email_verified) "
            f"VALUES ({uid}, '{uname}', '{uname}@gmail.com', "
            f"'$2b$12$hashed_placeholder', '{fname}', 'CUSTOMER', 'ACTIVE', TRUE);"
        )
    lines.append("")

    # ── products ───────────────────────────────────────────────
    lines.append("-- ===== PRODUCTS =====")
    for pid, p in enumerate(products, start=START_PRODUCT_ID):
        lines.append(
            f"INSERT INTO products "
            f"(id, name, description, detail, summary, category, price, brand, promotion) "
            f"VALUES ("
            f"{pid}, "
            f"{_q(p.get('name'))}, "
            f"{_q(p.get('description', '')[:2000])}, "
            f"{_q(p.get('detail', '')[:5000])}, "
            f"{_q(p.get('summary', '')[:255])}, "
            f"{_q(p.get('category'))}, "
            f"{p.get('price', 0):.2f}, "
            f"{_q(p.get('brand'))}, "
            f"{int(p.get('promotion') or 0)});"
        )
    lines.append("")

    # ── product_images ─────────────────────────────────────────
    lines.append("-- ===== PRODUCT IMAGES =====")
    img_id = 1
    for pid, p in enumerate(products, start=START_PRODUCT_ID):
        for url in (p.get("image_urls") or []):
            if url:
                lines.append(
                    f"INSERT INTO product_images (id, product_id, image_url) "
                    f"VALUES ({img_id}, {pid}, {_q(url)});"
                )
                img_id += 1
    lines.append("")

    # ── inventory ──────────────────────────────────────────────
    lines.append("-- ===== INVENTORY =====")
    for pid in range(START_PRODUCT_ID, START_PRODUCT_ID + len(products)):
        qty = random.randint(10, 300)
        lines.append(f"INSERT INTO inventory (product_id, quantity) VALUES ({pid}, {qty});")
    lines.append("")

    # ── reviews ────────────────────────────────────────────────
    lines.append("-- ===== REVIEWS =====")
    review_id = 1
    for pid, p in enumerate(products, start=START_PRODUCT_ID):
        count = min(int(p.get("review_count") or 0), 5)
        if count == 0:
            count = random.randint(1, 3)
        rating_raw = p.get("rating")  # 0–100
        for _ in range(count):
            if rating_raw is not None:
                base  = max(1, min(5, round(float(rating_raw) / 20)))
                score = max(1, min(5, base + random.randint(-1, 1)))
            else:
                score = random.randint(3, 5)
            uid  = random.randint(1, len(FAKE_USERS))
            text = _q(random.choice(REVIEW_TEXTS))
            lines.append(
                f"INSERT INTO reviews (id, feedback, score, user_id, product_id) "
                f"VALUES ({review_id}, {text}, {score}, {uid}, {pid});"
            )
            review_id += 1

    lines += [
        "",
        "SET FOREIGN_KEY_CHECKS = 1;",
        f"\n-- Done: {len(products)} products | {img_id-1} images | {review_id-1} reviews",
    ]
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log.info("Bat dau cao CellphoneS phu kien...")

    products = scrape_all()

    if not products:
        log.error("Khong cao duoc san pham nao.")
        raise SystemExit(1)

    # Lưu JSON
    with open("cellphones_data.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
    log.info("JSON -> cellphones_data.json  (%d items)", len(products))

    # Sinh SQL
    sql = build_sql(products)
    with open("cellphones_data.sql", "w", encoding="utf-8") as f:
        f.write(sql)
    log.info("SQL  -> cellphones_data.sql")

    log.info("Xong! Import: mysql -u root -p ecommerce < cellphones_data.sql")