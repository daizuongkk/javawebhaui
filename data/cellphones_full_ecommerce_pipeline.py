#!/usr/bin/env python3
"""
CellphoneS full product crawler + ecommerce normalizer.

What this script does:
1. Discover product URLs from CellphoneS sitemap.
2. Scrape product detail pages using requests + BeautifulSoup.
3. Normalize data into tables matching the provided ecommerce schema.
4. Export JSON/CSV for each table and SQL INSERT file.

Note:
- Public website does not expose customer private data (users/carts/orders/etc.).
- For relational tables beyond product catalog, this script generates synthetic demo data
  linked consistently with scraped products so the full schema can be populated.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://cellphones.com.vn"
SITEMAP_INDEX_URL = "https://cellphones.com.vn/sitemap/sitemap_index.xml?v=google"

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

VI_PROVINCES = [
    "Hà Nội",
    "TP. Hồ Chí Minh",
    "Đà Nẵng",
    "Cần Thơ",
    "Hải Phòng",
]


def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_space(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def safe_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return int(float(value))
    text = str(value)
    numbers = re.findall(r"\d+", text.replace(".", "").replace(",", ""))
    if not numbers:
        return default
    try:
        return int(numbers[0])
    except Exception:
        return default


def sql_escape(value: Any) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    text = text.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{text}'"


def sql_values(rows: Sequence[Dict[str, Any]], columns: Sequence[str]) -> List[str]:
    values = []
    for row in rows:
        values.append("(" + ", ".join(sql_escape(row.get(c)) for c in columns) + ")")
    return values


def sha_seed(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)


def normalize_product_image_url(url: str) -> str:
    """Normalize CellphoneS image URL to prefer original/full-size image."""
    if not url:
        return ""

    cleaned = url.strip()
    if not cleaned:
        return ""

    # Remove query string fragments to keep canonical URL in DB.
    cleaned = cleaned.split("?")[0].split("#")[0]

    # Unwrap imgproxy URLs used for thumbnails, e.g.
    # https://cdn2.../insecure/rs:fill:50:50/q:90/plain/https://cellphones.com.vn/media/catalog/product/...
    if "/plain/http" in cleaned:
        plain_part = cleaned.split("/plain/", 1)[-1]
        if plain_part.startswith("http://") or plain_part.startswith("https://"):
            cleaned = plain_part

    # Convert common thumbnail prefixes to original path.
    # Example: https://cdn2.cellphones.com.vn/200x/media/catalog/product/... -> .../media/catalog/product/...
    cleaned = re.sub(r"/\d+x(?=/media/catalog/product/)", "", cleaned)
    cleaned = re.sub(r"/\d+x\d+(?=/media/catalog/product/)", "", cleaned)

    return cleaned


def is_product_image_candidate(url: str) -> bool:
    """Keep only likely product gallery images, skip icons/logo/menu assets."""
    if not url:
        return False

    lower = url.lower()
    if "media/catalog/product" not in lower:
        return False

    blocked_keywords = [
        "icon", "logo", "avatar", "banner", "placeholder", "favicon",
        "swatch", "sprite", "sticker", "label", "thumb",
    ]
    if any(k in lower for k in blocked_keywords):
        return False

    return True


@dataclass
class ProductRaw:
    url: str
    name: str
    description: str
    detail: str
    summary: str
    category: str
    price: int
    brand: str
    promotion: int
    images: List[str]
    rating_value: float
    rating_count: int


class CellphoneSCrawler:
    def __init__(self, delay: float = 0.2, timeout: int = 25):
        self.delay = max(0.0, delay)
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def _fetch_text(self, url: str) -> Optional[str]:
        try:
            resp = self.session.get(url, timeout=self.timeout)
            if resp.status_code != 200:
                return None
            resp.encoding = "utf-8"
            return resp.text
        except requests.RequestException:
            return None

    def _xml_loc_values(self, xml_text: str) -> List[str]:
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return []

        locs: List[str] = []
        for el in root.iter():
            tag = el.tag.lower()
            if tag.endswith("loc") and el.text:
                locs.append(el.text.strip())
        return locs

    def get_sitemap_urls(self, sitemap_index_url: str = SITEMAP_INDEX_URL) -> List[str]:
        text = self._fetch_text(sitemap_index_url)
        if not text:
            return []
        return self._xml_loc_values(text)

    def _looks_like_product_url(self, url: str) -> bool:
        parsed = urlparse(url)
        if parsed.netloc not in {"cellphones.com.vn", "www.cellphones.com.vn"}:
            return False

        path = (parsed.path or "").lower()
        if not path.endswith(".html"):
            return False

        slug = Path(path).name
        if slug in {
            "dien-thoai.html",
            "laptop.html",
            "tablet.html",
            "phu-kien.html",
            "man-hinh.html",
            "pc.html",
            "sim-so.html",
        }:
            return False

        banned = [
            "/sforum",
            "khuyen-mai",
            "thu-cu-doi-moi",
            "hang-cu",
            "danh-sach-khuyen-mai",
        ]
        if any(x in path for x in banned):
            return False

        return "-" in slug

    def discover_product_urls(self, max_products: int = 0) -> List[str]:
        sitemap_urls = self.get_sitemap_urls()
        if not sitemap_urls:
            return []

        candidate_sitemaps = [u for u in sitemap_urls if "product-sitemap" in u.lower()]
        if not candidate_sitemaps:
            candidate_sitemaps = sitemap_urls

        product_urls: List[str] = []
        seen = set()

        for sitemap_url in candidate_sitemaps:
            xml_text = self._fetch_text(sitemap_url)
            if not xml_text:
                continue

            for loc in self._xml_loc_values(xml_text):
                if not self._looks_like_product_url(loc):
                    continue
                if loc in seen:
                    continue
                seen.add(loc)
                product_urls.append(loc)
                if max_products > 0 and len(product_urls) >= max_products:
                    return product_urls

            if self.delay > 0:
                time.sleep(self.delay)

        return product_urls

    def _parse_json_ld(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        blocks: List[Dict[str, Any]] = []
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            raw = (script.string or script.get_text() or "").strip()
            if not raw:
                continue

            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue

            if isinstance(data, list):
                blocks.extend(x for x in data if isinstance(x, dict))
            elif isinstance(data, dict):
                blocks.append(data)

        return blocks

    def _find_product_json_ld(self, blocks: Sequence[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        def is_product(obj: Dict[str, Any]) -> bool:
            typ = obj.get("@type")
            if isinstance(typ, list):
                return any(str(x).lower() == "product" for x in typ)
            return str(typ).lower() == "product"

        for block in blocks:
            if is_product(block):
                return block
            graph = block.get("@graph")
            if isinstance(graph, list):
                for node in graph:
                    if isinstance(node, dict) and is_product(node):
                        return node
        return None

    def _extract_brand(self, name: str, product_json: Optional[Dict[str, Any]]) -> str:
        if product_json:
            brand = product_json.get("brand")
            if isinstance(brand, dict):
                val = clean_space(str(brand.get("name", "")))
                if val:
                    return val
            if isinstance(brand, str):
                val = clean_space(brand)
                if val:
                    return val

        known = [
            "Apple", "Samsung", "Xiaomi", "OPPO", "Vivo", "Realme", "ASUS",
            "Dell", "Lenovo", "HP", "Acer", "MSI", "Logitech", "Anker", "Baseus",
            "Ugreen", "Sony", "JBL", "Huawei", "Nokia", "Google", "OnePlus",
        ]
        lower = name.lower()
        for b in known:
            if b.lower() in lower:
                return b

        first = clean_space(name).split(" ")[0] if name else "Unknown"
        return first or "Unknown"

    def _extract_category(self, soup: BeautifulSoup, url: str) -> str:
        crumbs = []
        for a in soup.select(".breadcrumb a, .breadcrumbs a, nav[aria-label='breadcrumb'] a"):
            text = clean_space(a.get_text(" ", strip=True))
            if text and text.lower() not in {"trang chủ", "home"}:
                crumbs.append(text)

        if crumbs:
            return crumbs[-1]

        slug = Path(urlparse(url).path).name.lower()
        if "laptop" in slug:
            return "Laptop"
        if "tablet" in slug or "ipad" in slug:
            return "Tablet"
        if any(k in slug for k in ["iphone", "samsung", "xiaomi", "dien-thoai", "oppo", "vivo"]):
            return "Điện thoại"
        if any(k in slug for k in ["tai-nghe", "sac", "cap", "ban-phim", "chuot", "phu-kien"]):
            return "Phụ kiện"
        return "Khác"

    def _extract_price_and_promo(
        self,
        soup: BeautifulSoup,
        html: str,
        product_json: Optional[Dict[str, Any]],
    ) -> Tuple[int, int]:
        price = 0
        old_price = 0

        if product_json:
            offers = product_json.get("offers")
            if isinstance(offers, list) and offers:
                offers = offers[0]
            if isinstance(offers, dict):
                price = safe_int(offers.get("price"), 0)
                old_price = safe_int(offers.get("pricePriceCurrency"), 0)
                if old_price <= 0:
                    old_price = safe_int(offers.get("highPrice"), 0)

        if price <= 0:
            selectors = [
                "[class*='price'][class*='special']",
                "[class*='product__price']",
                "[class*='price']",
                ".box-price",
            ]
            for sel in selectors:
                for el in soup.select(sel):
                    text = clean_space(el.get_text(" ", strip=True))
                    p = safe_int(text, 0)
                    if p > 1000:
                        price = p
                        break
                if price > 0:
                    break

        if price <= 0:
            m = re.search(r'"price"\s*:\s*"?(\d{4,})"?', html)
            if m:
                price = safe_int(m.group(1), 0)

        if old_price <= 0:
            m = re.search(r"(\d{1,3}(?:[\.,]\d{3})+)\s*[đ₫]\s*</", html)
            if m:
                old_price = safe_int(m.group(1), 0)

        promo = 0
        text_pool = clean_space(soup.get_text(" ", strip=True))[:12000]
        promo_match = re.search(r"(\d{1,2})\s*%", text_pool)
        if promo_match:
            promo = max(0, min(99, safe_int(promo_match.group(1), 0)))
        elif old_price > price > 0:
            promo = int(round((old_price - price) * 100.0 / old_price))

        return max(0, price), max(0, promo)

    def _extract_detail(self, soup: BeautifulSoup, product_json: Optional[Dict[str, Any]]) -> str:
        lines: List[str] = []

        if product_json:
            props = product_json.get("additionalProperty")
            if isinstance(props, list):
                for it in props:
                    if not isinstance(it, dict):
                        continue
                    name = clean_space(str(it.get("name", "")))
                    value = clean_space(str(it.get("value", "")))
                    if name and value:
                        lines.append(f"- {name}: {value}")

        if not lines:
            for row in soup.select("table tr"):
                cols = row.find_all(["th", "td"])
                if len(cols) >= 2:
                    left = clean_space(cols[0].get_text(" ", strip=True))
                    right = clean_space(cols[1].get_text(" ", strip=True))
                    if left and right:
                        lines.append(f"- {left}: {right}")
                if len(lines) >= 40:
                    break

        if not lines:
            for li in soup.select(".specifications li, .technical-content li, .box-content li"):
                text = clean_space(li.get_text(" ", strip=True))
                if text and len(text) > 3:
                    lines.append(f"- {text}")
                if len(lines) >= 40:
                    break

        detail = "\n".join(lines)
        if len(detail) > 5000:
            detail = detail[:5000]
        return detail

    def _extract_images(self, soup: BeautifulSoup, product_json: Optional[Dict[str, Any]]) -> List[str]:
        urls: List[str] = []
        seen = set()

        def add(url: str) -> None:
            if not url:
                return
            url = url.strip()
            if not url:
                return
            if url.startswith("//"):
                url = "https:" + url
            if url.startswith("/"):
                url = BASE_URL + url
            if not url.startswith("http"):
                return
            url = normalize_product_image_url(url)
            if not is_product_image_candidate(url):
                return
            if url in seen:
                return
            seen.add(url)
            urls.append(url)

        if product_json:
            img = product_json.get("image")
            if isinstance(img, str):
                add(img)
            elif isinstance(img, list):
                for u in img:
                    add(str(u))

        # Extract image URLs from inline scripts where gallery arrays are often embedded.
        script_pattern = re.compile(
            r"https?://[^\s\"']*?/media/catalog/product/[^\s\"']+",
            re.IGNORECASE,
        )
        for script in soup.find_all("script"):
            raw = script.string or script.get_text() or ""
            if not raw:
                continue
            for match in script_pattern.findall(raw):
                add(match)

        og = soup.find("meta", attrs={"property": "og:image"})
        if og and og.get("content"):
            add(og.get("content", ""))

        for tag in soup.find_all("img"):
            candidate_attrs = [
                "src", "data-src", "data-lazy-src", "data-zoom-image",
                "data-image", "data-original", "srcset", "data-srcset",
            ]
            for attr in candidate_attrs:
                raw_val = tag.get(attr)
                if not raw_val:
                    continue
                raw_val = str(raw_val)

                # srcset format: "url1 1x, url2 2x"
                if attr in {"srcset", "data-srcset"}:
                    for part in raw_val.split(","):
                        token = part.strip().split(" ")[0].strip()
                        if "/media/catalog/product" in token:
                            add(token)
                else:
                    if "/media/catalog/product" in raw_val:
                        add(raw_val)
            if len(urls) >= 120:
                break

        # Keep all product gallery images (no low count cap) while deduplicated.
        return urls

    def scrape_product(self, url: str) -> Optional[ProductRaw]:
        html = self._fetch_text(url)
        if not html:
            return None

        soup = BeautifulSoup(html, "lxml")
        blocks = self._parse_json_ld(soup)
        product_json = self._find_product_json_ld(blocks)

        og_title = soup.find("meta", attrs={"property": "og:title"})
        page_title = soup.find("title")
        name = ""
        if product_json and product_json.get("name"):
            name = clean_space(str(product_json.get("name")))
        if not name and og_title and og_title.get("content"):
            name = clean_space(og_title.get("content", ""))
        if not name and page_title:
            name = clean_space(page_title.get_text(" ", strip=True))
        if "|" in name:
            name = clean_space(name.split("|")[0])
        if not name:
            return None

        desc = ""
        og_desc = soup.find("meta", attrs={"property": "og:description"})
        if product_json and product_json.get("description"):
            desc = clean_space(str(product_json.get("description")))
        if not desc and og_desc and og_desc.get("content"):
            desc = clean_space(og_desc.get("content", ""))
        if not desc:
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                desc = clean_space(meta_desc.get("content", ""))

        detail = self._extract_detail(soup, product_json)
        category = self._extract_category(soup, url)
        price, promotion = self._extract_price_and_promo(soup, html, product_json)
        brand = self._extract_brand(name, product_json)
        images = self._extract_images(soup, product_json)

        rating_value = 0.0
        rating_count = 0
        if product_json and isinstance(product_json.get("aggregateRating"), dict):
            agg = product_json.get("aggregateRating", {})
            try:
                rating_value = float(str(agg.get("ratingValue", 0)).replace(",", "."))
            except Exception:
                rating_value = 0.0
            rating_count = safe_int(agg.get("ratingCount"), 0)

        summary = desc[:255] if desc else name[:255]
        description = desc[:2000] if desc else name[:2000]

        if self.delay > 0:
            time.sleep(self.delay)

        return ProductRaw(
            url=url,
            name=name,
            description=description,
            detail=detail,
            summary=summary,
            category=category[:255],
            price=price,
            brand=brand[:255],
            promotion=promotion,
            images=images,
            rating_value=rating_value,
            rating_count=rating_count,
        )


class EcommerceNormalizer:
    def __init__(self, synthetic_relations: bool = True, seed: int = 20260328):
        self.synthetic_relations = synthetic_relations
        self.rng = random.Random(seed)

    def build(self, products_raw: Sequence[ProductRaw]) -> Dict[str, List[Dict[str, Any]]]:
        now = now_ts()

        tables: Dict[str, List[Dict[str, Any]]] = {
            "users": [],
            "products": [],
            "product_images": [],
            "addresses": [],
            "carts": [],
            "cart_items": [],
            "orders": [],
            "order_items": [],
            "reviews": [],
            "wishlists": [],
        }

        # Products + product_images
        img_id = 1
        for idx, p in enumerate(products_raw, start=1):
            # deterministic quantity by product URL hash
            qty = 5 + (sha_seed(p.url) % 196)
            tables["products"].append(
                {
                    "id": idx,
                    "name": p.name,
                    "description": p.description,
                    "detail": p.detail,
                    "summary": p.summary,
                    "category": p.category,
                    "price": p.price,
                    "brand": p.brand,
                    "promotion": p.promotion,
                    "quantity": qty,
                    "view": 0,
                    "created_at": now,
                    "updated_at": now,
                }
            )

            for image_url in p.images:
                tables["product_images"].append(
                    {
                        "id": img_id,
                        "product_id": idx,
                        "image_url": image_url,
                    }
                )
                img_id += 1

        # Create synthetic users for relation tables and reviews
        user_count = min(80, max(20, max(1, len(products_raw) // 15)))
        for uid in range(1, user_count + 1):
            username = f"customer_{uid:04d}"
            tables["users"].append(
                {
                    "id": uid,
                    "username": username,
                    "email": f"{username}@example.com",
                    "password": "$2b$12$abcdefghijklmnopqrstuv1234567890abcdefghi",
                    "first_name": f"User{uid}",
                    "last_name": "Demo",
                    "phone": f"09{uid:08d}"[-10:],
                    "avt_url": "",
                    "role": "CUSTOMER",
                    "status": "ACTIVE",
                    "verified": 1,
                    "last_login": now,
                    "created_at": now,
                    "updated_at": now,
                }
            )

        # Reviews from rating summary
        review_id = 1
        for pid, p in enumerate(products_raw, start=1):
            if p.rating_value <= 0 and p.rating_count <= 0:
                continue

            score = min(5, max(1, int(round(p.rating_value if p.rating_value > 0 else 4))))
            reviewer_id = 1 + (sha_seed(p.url) % user_count)
            feedback = (
                f"Đánh giá tổng hợp từ trang sản phẩm: {p.name}. "
                f"Điểm trung bình {p.rating_value:.1f} ({p.rating_count} lượt đánh giá)."
            )
            tables["reviews"].append(
                {
                    "id": review_id,
                    "feedback": feedback[:2000],
                    "score": score,
                    "user_id": reviewer_id,
                    "product_id": pid,
                    "created_at": now,
                }
            )
            review_id += 1

        # If website does not expose rating data in structured blocks,
        # create a light synthetic review set so review table is not empty.
        if not tables["reviews"] and products_raw:
            for pid, p in enumerate(products_raw, start=1):
                if self.rng.random() > 0.45:
                    continue
                reviewer_id = 1 + (sha_seed(f"fallback-review-{p.url}") % user_count)
                score = self.rng.choice([4, 4, 5, 5, 3])
                tables["reviews"].append(
                    {
                        "id": review_id,
                        "feedback": f"Đánh giá seed tự động cho sản phẩm: {p.name}"[:2000],
                        "score": score,
                        "user_id": reviewer_id,
                        "product_id": pid,
                        "created_at": now,
                    }
                )
                review_id += 1

        if self.synthetic_relations and tables["products"] and tables["users"]:
            self._build_relations(tables, now)

        return tables

    def _build_relations(self, tables: Dict[str, List[Dict[str, Any]]], now: str) -> None:
        user_ids = [u["id"] for u in tables["users"]]
        product_ids = [p["id"] for p in tables["products"]]

        # addresses: one default address per user
        addr_id = 1
        for uid in user_ids:
            province = VI_PROVINCES[(uid - 1) % len(VI_PROVINCES)]
            tables["addresses"].append(
                {
                    "id": addr_id,
                    "user_id": uid,
                    "recipient_name": f"User{uid} Demo",
                    "phone": f"09{uid:08d}"[-10:],
                    "province": province,
                    "district": f"Quận {(uid % 12) + 1}",
                    "ward": f"Phường {(uid % 20) + 1}",
                    "street": f"{100 + uid} Đường Mẫu",
                    "detail": "Địa chỉ tạo tự động để seed dữ liệu quan hệ.",
                    "is_default": 1,
                    "created_at": now,
                }
            )
            addr_id += 1

        # carts: one cart per user
        cart_id = 1
        for uid in user_ids:
            tables["carts"].append({"id": cart_id, "user_id": uid})
            cart_id += 1

        # cart_items: each cart 1-3 products
        cart_item_id = 1
        for cart in tables["carts"]:
            uid = cart["user_id"]
            local_rng = random.Random(sha_seed(f"cart-{uid}"))
            pick_count = min(len(product_ids), local_rng.randint(1, 3))
            picks = local_rng.sample(product_ids, pick_count)
            for pid in picks:
                tables["cart_items"].append(
                    {
                        "id": cart_item_id,
                        "cart_id": cart["id"],
                        "product_id": pid,
                        "quantity": local_rng.randint(1, 2),
                    }
                )
                cart_item_id += 1

        # orders + order_items: around 35% users have one order
        order_id = 1
        order_item_id = 1
        for uid in user_ids:
            local_rng = random.Random(sha_seed(f"order-{uid}"))
            if local_rng.random() > 0.35:
                continue

            pick_count = min(len(product_ids), local_rng.randint(1, 3))
            picks = local_rng.sample(product_ids, pick_count)
            price_map = {p["id"]: int(p.get("price", 0) or 0) for p in tables["products"]}

            total = 0
            item_rows: List[Dict[str, Any]] = []
            for pid in picks:
                qty = local_rng.randint(1, 2)
                price = max(0, price_map.get(pid, 0))
                total += price * qty
                item_rows.append(
                    {
                        "id": order_item_id,
                        "order_id": order_id,
                        "product_id": pid,
                        "price": price,
                        "quantity": qty,
                    }
                )
                order_item_id += 1

            tables["orders"].append(
                {
                    "id": order_id,
                    "user_id": uid,
                    "total_price": total,
                    "status": local_rng.choice(["PENDING", "PAID", "SHIPPED", "COMPLETED"]),
                    "recipient_name": f"User{uid} Demo",
                    "phone": f"09{uid:08d}"[-10:],
                    "address": f"{100 + uid} Đường Mẫu, Quận {(uid % 12) + 1}, {VI_PROVINCES[uid % len(VI_PROVINCES)]}",
                    "created_at": now,
                }
            )

            tables["order_items"].extend(item_rows)
            order_id += 1

        # wishlists: 0-2 products per user
        for uid in user_ids:
            local_rng = random.Random(sha_seed(f"wishlist-{uid}"))
            pick_count = min(len(product_ids), local_rng.randint(0, 2))
            if pick_count == 0:
                continue
            for pid in local_rng.sample(product_ids, pick_count):
                tables["wishlists"].append({"user_id": uid, "product_id": pid})


class Exporter:
    CSV_COLUMNS: Dict[str, List[str]] = {
        "users": [
            "id", "username", "email", "password", "first_name", "last_name", "phone", "avt_url",
            "role", "status", "verified", "last_login", "created_at", "updated_at",
        ],
        "products": [
            "id", "name", "description", "detail", "summary", "category", "price", "brand", "promotion",
            "quantity", "view", "created_at", "updated_at",
        ],
        "product_images": ["id", "product_id", "image_url"],
        "addresses": [
            "id", "user_id", "recipient_name", "phone", "province", "district", "ward", "street", "detail",
            "is_default", "created_at",
        ],
        "carts": ["id", "user_id"],
        "cart_items": ["id", "cart_id", "product_id", "quantity"],
        "orders": ["id", "user_id", "total_price", "status", "recipient_name", "phone", "address", "created_at"],
        "order_items": ["id", "order_id", "product_id", "price", "quantity"],
        "reviews": ["id", "feedback", "score", "user_id", "product_id", "created_at"],
        "wishlists": ["user_id", "product_id"],
    }

    SQL_TABLE_COLUMNS: Dict[str, List[str]] = CSV_COLUMNS

    INSERT_ORDER = [
        "users",
        "products",
        "product_images",
        "addresses",
        "carts",
        "cart_items",
        "orders",
        "order_items",
        "reviews",
        "wishlists",
    ]

    def __init__(self, output_dir: Path, prefix: str):
        self.output_dir = output_dir
        self.prefix = prefix
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_json(self, tables: Dict[str, List[Dict[str, Any]]]) -> Path:
        out = self.output_dir / f"{self.prefix}_normalized.json"
        payload = {
            "metadata": {
                "source": BASE_URL,
                "generated_at": now_ts(),
                "tables": {k: len(v) for k, v in tables.items()},
            },
            "tables": tables,
        }
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return out

    def export_csv(self, tables: Dict[str, List[Dict[str, Any]]]) -> List[Path]:
        files: List[Path] = []
        for table, rows in tables.items():
            out = self.output_dir / f"{self.prefix}_{table}.csv"
            cols = self.CSV_COLUMNS[table]
            with out.open("w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=cols)
                writer.writeheader()
                for row in rows:
                    writer.writerow({k: row.get(k) for k in cols})
            files.append(out)
        return files

    def export_sql(self, tables: Dict[str, List[Dict[str, Any]]]) -> Path:
        out = self.output_dir / f"{self.prefix}_seed.sql"
        lines: List[str] = []
        lines.append("-- Auto-generated by cellphones_full_ecommerce_pipeline.py")
        lines.append(f"-- Source: {BASE_URL}")
        lines.append(f"-- Generated at: {now_ts()}")
        lines.append("SET NAMES utf8mb4;")
        lines.append("SET FOREIGN_KEY_CHECKS = 0;")
        lines.append("")

        for table in self.INSERT_ORDER:
            rows = tables.get(table, [])
            if not rows:
                lines.append(f"-- {table}: no rows")
                lines.append("")
                continue

            cols = self.SQL_TABLE_COLUMNS[table]
            vals = sql_values(rows, cols)
            lines.append(f"-- {table}: {len(rows)} rows")
            lines.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES")
            for i, val in enumerate(vals):
                suffix = "," if i < len(vals) - 1 else ";"
                lines.append(val + suffix)
            lines.append("")

        lines.append("SET FOREIGN_KEY_CHECKS = 1;")
        out.write_text("\n".join(lines), encoding="utf-8")
        return out


def run_pipeline(args: argparse.Namespace) -> int:
    crawler = CellphoneSCrawler(delay=args.delay, timeout=args.timeout)
    max_products = args.max_products
    if max_products <= 0 or max_products > 500:
        max_products = 500

    print("[1/4] Discovering product URLs from sitemap...")
    product_urls = crawler.discover_product_urls(max_products=max_products)
    if not product_urls:
        print("No product URLs found from sitemap. Stop.")
        return 1

    print(f"  Found {len(product_urls)} product URLs (limit={max_products})")

    print("[2/4] Scraping product pages...")
    scraped: List[ProductRaw] = []
    for i, url in enumerate(product_urls, start=1):
        item = crawler.scrape_product(url)
        if item and item.price > 0:
            scraped.append(item)
        if i % 50 == 0 or i == len(product_urls):
            print(f"  Progress: {i}/{len(product_urls)} | valid products: {len(scraped)}")

    if not scraped:
        print("No valid products scraped. Stop.")
        return 2

    print("[3/4] Normalizing to ecommerce tables...")
    normalizer = EcommerceNormalizer(synthetic_relations=not args.no_synthetic_relations)
    tables = normalizer.build(scraped)

    print("[4/4] Exporting JSON/CSV/SQL...")
    output_dir = Path(args.output_dir)
    exporter = Exporter(output_dir=output_dir, prefix=args.prefix)
    json_file = exporter.export_json(tables)
    csv_files = exporter.export_csv(tables)
    sql_file = exporter.export_sql(tables)

    print("\nDone.")
    print(f"  Products scraped: {len(scraped)}")
    print("  Table rows:")
    for table, rows in tables.items():
        print(f"    - {table}: {len(rows)}")
    print(f"\n  JSON: {json_file}")
    print(f"  SQL : {sql_file}")
    print(f"  CSV : {len(csv_files)} files in {output_dir}")

    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Crawl CellphoneS and normalize data to ecommerce schema"
    )
    parser.add_argument(
        "--max-products",
        type=int,
        default=500,
        help="Limit number of product URLs to scrape (1-500, default: 500)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.1,
        help="Delay in seconds between HTTP requests",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=25,
        help="HTTP timeout in seconds",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory for JSON/CSV/SQL files",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default=f"cellphones_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        help="Output file prefix",
    )
    parser.add_argument(
        "--no-synthetic-relations",
        action="store_true",
        help="Do not generate synthetic rows for addresses/carts/orders/wishlists",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        return run_pipeline(args)
    except KeyboardInterrupt:
        print("Interrupted by user")
        return 130


if __name__ == "__main__":
    sys.exit(main())
