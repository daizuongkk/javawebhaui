import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

BASE = "https://cellphones.com.vn"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


# =========================
# PARSER
# =========================
def get_soup(html):
    try:
        return BeautifulSoup(html, "lxml")
    except:
        return BeautifulSoup(html, "html.parser")


# =========================
# 1. LẤY LIST PRODUCT (UI MỚI)
# =========================
def get_products_from_list(page=1):
    url = f"{BASE}/phu-kien.html?page={page}"
    print(f"📄 Crawl list: {url}")

    res = requests.get(url, headers=HEADERS)
    soup = get_soup(res.text)

    products = []

    for item in soup.select("a.group"):
        href = item.get("href")
        link = urljoin(BASE, href) if href else None

        name = item.select_one("h3")
        name = name.text.strip() if name else None

        img = item.select_one("img")
        image = img.get("src") if img else None

        price = None
        old_price = None

        for p in item.select("p"):
            text = p.text.strip()
            classes = p.get("class", [])

            if "line-through" in classes:
                old_price = text
            elif "đ" in text:
                price = text

        products.append({
            "name": name,
            "price": price,
            "old_price": old_price,
            "image": image,
            "url": link
        })

    return products


# =========================
# 2. PARSE DETAIL (JSON + FALLBACK)
# =========================
def parse_product(url):
    try:
        res = requests.get(url, headers=HEADERS)
        soup = get_soup(res.text)

        # ===== TRY JSON (__NEXT_DATA__) =====
        script = soup.find("script", {"id": "__NEXT_DATA__"})

        if script:
            try:
                data = json.loads(script.string)

                pageProps = data.get("props", {}).get("pageProps", {})

                # ⚠️ có thể khác key → debug nếu cần
                product = pageProps.get("product") or pageProps.get("data") or {}

                name = product.get("name")
                price = product.get("price")
                old_price = product.get("original_price")

                images = []
                for img in product.get("images", []):
                    if isinstance(img, dict):
                        images.append(img.get("url"))
                    else:
                        images.append(img)

                specs = {}
                for spec in product.get("specifications", []):
                    key = spec.get("name")
                    value = spec.get("value")
                    if key:
                        specs[key] = value

                variants = []
                for v in product.get("variants", []):
                    variants.append({
                        "name": v.get("name"),
                        "price": v.get("price")
                    })

                description = product.get("description")

                return {
                    "detail_name": name,
                    "detail_price": price,
                    "detail_old_price": old_price,
                    "images": images,
                    "specifications": specs,
                    "variants": variants,
                    "description": description
                }

            except Exception as e:
                print("⚠️ JSON parse fail → fallback HTML", e)

        # ===== FALLBACK HTML =====
        name = soup.select_one("h1")
        name = name.text.strip() if name else None

        price = None
        old_price = None

        for p in soup.select("p"):
            txt = p.text.strip()
            cls = p.get("class", [])

            if "text-primary-700" in cls:
                price = txt
            if "line-through" in cls:
                old_price = txt

        images = []
        for img in soup.select(".swiper-slide img"):
            src = img.get("src") or img.get("data-src")
            if src:
                images.append(src)

        specs = {}
        for item in soup.select(".grid.grid-cols-2 > div"):
            texts = item.get_text(strip=True).split("\n")
            if len(texts) >= 2:
                specs[texts[0]] = texts[-1]

        description = soup.select_one(".content")
        description = str(description) if description else None

        return {
            "detail_name": name,
            "detail_price": price,
            "detail_old_price": old_price,
            "images": list(set(images)),
            "specifications": specs,
            "description": description
        }

    except Exception as e:
        print("❌ ERROR:", url, e)
        return None


# =========================
# 3. MAIN CRAWLER
# =========================
def crawl_accessories(pages=3, limit_per_page=20):
    all_products = []

    for p in range(1, pages + 1):
        print(f"\n📄 Page {p}")

        list_products = get_products_from_list(p)

        for i, item in enumerate(list_products[:limit_per_page]):
            print(f"🚀 {item['name']}")

            if item["url"]:
                detail = parse_product(item["url"])

                if detail:
                    item.update(detail)

            all_products.append(item)

            time.sleep(1)

    with open("cellphones_full.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=4)

    print("\n✅ DONE - saved to cellphones_full.json")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    crawl_accessories(pages=5, limit_per_page=20)