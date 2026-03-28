import json
import random
from datetime import datetime, timedelta

# Danh sách thông tin chi tiết cho các danh mục phụ kiện
accessories_info = {
    "Cáp, sạc điện thoại iPhone, Android": {
        "products": [
            {
                "brand": "Apple",
                "name": "Lightning Cable 2m",
                "price": 25.00,
                "promotion": 10,
                "description": "Cáp Lightning chính hãng Apple dài 2m, tương thích với iPhone, iPad, AirPods. Tiêu chuẩn MFi, an toàn và bền bỉ.",
                "detail": "• Chiều dài: 2 mét\n• Loại kết nối: Lightning (8 pin)\n• Tương thích: iPhone XS/XS Max/XR và mới hơn\n• Chứng chỉ MFi: Có\n• Tốc độ truyền dữ liệu: 480Mbps\n• Tính năng: Hỗ trợ sạc nhanh, chuyển dữ liệu\n• Bảo hành: 12 tháng",
                "summary": "Lightning Cable 2m - Cáp Lightning chính hãng Apple, hỗ trợ sạc và truyền dữ liệu - Giá $25.00"
            },
            {
                "brand": "Belkin",
                "name": "USB-C Fast Charger 65W",
                "price": 59.99,
                "promotion": 15,
                "description": "Bộ sạc nhanh Belkin công suất 65W với cổng USB-C, tương thích với điện thoại Android, tablet, laptop. Công nghệ GaN tiên tiến.",
                "detail": "• Công suất: 65W\n• Cổng: 2x USB-C\n• Công nghệ: GaN (Gallium Nitride)\n• Tương thích: Android, Tablet, Laptop\n• Bảo vệ: Quá dòng, quá áp, quá nhiệt\n• Chứng chỉ: FCC, CE, RoHS\n• Bảo hành: 24 tháng",
                "summary": "USB-C Fast Charger 65W - Sạc nhanh 65W, 2 cổng USB-C, tương thích đa thiết bị - Giá $59.99"
            },
            {
                "brand": "Anker",
                "name": "USB-C Cable 3.1 2m",
                "price": 15.99,
                "promotion": 8,
                "description": "Cáp USB-C 3.1 Anker dài 2m, hỗ trợ truyền dữ liệu nhanh 10Gbps và sạc nhanh 100W.",
                "detail": "• Chiều dài: 2 mét\n• Chuẩn: USB 3.1 Gen 2\n• Tốc độ truyền: 10Gbps\n• Công suất hỗ trợ: Lên tới 100W\n• Bảo vệ: 10,000 lần uốn cong\n• Vật liệu: Nylon dệt chỉ\n• Bảo hành: 18 tháng",
                "summary": "USB-C Cable 3.1 2m - Cáp USB-C tốc độ 10Gbps, hỗ trợ sạc 100W - Giá $15.99"
            },
            {
                "brand": "Samsung",
                "name": "Super Fast Charger 45W",
                "price": 39.99,
                "promotion": 12,
                "description": "Bộ sạc nhanh Samsung 45W với cổng USB-C, tương thích với Galaxy S series. Sạc đầy pin trong thời gian ngắn.",
                "detail": "• Công suất: 45W\n• Cổng: USB-C\n• Tương thích: Galaxy S25, S24, S23 series\n• Chế độ sạc nhanh: Super Fast Charging\n• Bảo vệ: Nhiệt độ, dòng điện, điện áp\n• Chứng chỉ: KC, FCC, CE\n• Bảo hành: 12 tháng",
                "summary": "Super Fast Charger 45W - Sạc nhanh 45W cho Galaxy, tương thích Samsung - Giá $39.99"
            },
            {
                "brand": "Baseus",
                "name": "GaN Charger 120W 4 Port",
                "price": 79.99,
                "promotion": 20,
                "description": "Bộ sạc Baseus GaN công suất 120W với 4 cổng USB-C, sạc tới 4 thiết bị cùng lúc.",
                "detail": "• Công suất: 120W\n• Cổng: 4x USB-C\n• Công nghệ: GaN Gallium Nitride\n• Tương thích: Phổ biến tất cả Android, Laptop\n• Tính năng: Sạc 4 thiết bị cùng lúc\n• Bảo vệ: 9 lớp bảo vệ\n• Bảo hành: 24 tháng",
                "summary": "GaN Charger 120W 4 Port - Sạc nhanh 120W với 4 cổng USB-C - Giá $79.99"
            }
        ]
    },
    "Dán màn hình điện thoại": {
        "products": [
            {
                "brand": "Nillkin",
                "name": "Tempered Glass H+ Pro",
                "price": 12.99,
                "promotion": 5,
                "description": "Kính cường lực Nillkin H+ Pro độ cứng 9H, bảo vệ toàn màn hình, khả năng chống xước cao.",
                "detail": "• Độ cứng: 9H\n• Độ dày: 0.33mm\n• Khả năng chuyên sâu ánh sáng xanh: Có\n• Bảo vệ: Góc 2.5D\n• Không ảnh hưởng độ sáng: 100% nhạy cảm cảm ứng\n• Tương thích: iPhone, Samsung, OPPO, Xiaomi\n• Bảo hành: 6 tháng",
                "summary": "Tempered Glass H+ Pro - Kính cường lực 9H, chống xước, bảo vệ góc 2.5D - Giá $12.99"
            },
            {
                "brand": "Tech21",
                "name": "Screen Protector Clear 3D",
                "price": 19.99,
                "promotion": 8,
                "description": "Miếng dán màn hình Tech21 công nghệ 3D, độ cứng 9H, chống vỡ và chống xước hiệu quả.",
                "detail": "• Công nghệ: 3D curved glass\n• Độ cứng: 9H\n• Chống bỏng nước: 100%\n• Khả năng chược xước: Cao\n• Thiết kế: Không viền đen\n• Tương thích: Phổ biến iOS, Android\n• Bảo hành: 12 tháng",
                "summary": "Screen Protector Clear 3D - Kính cường lực 9H công nghệ 3D - Giá $19.99"
            },
            {
                "brand": "ESR",
                "name": "Tempered Glass Premium",
                "price": 14.99,
                "promotion": 6,
                "description": "Miếng dán kính ESR Premium độ cứng 9H, trong suốt, bảo vệ tốt, dễ lắp đặt.",
                "detail": "• Độ cứng: 9H\n• Độ trong suốt: 99%\n• Tương thích: iPhone 15, 14, 13, Samsung S24\n• Lớp phủ: Oleophobic coating\n• Dễ lắp: Có khung căn chỉnh\n• Khả năng bảo vệ: Góc 2.5D\n• Bảo hành: 12 tháng",
                "summary": "Tempered Glass Premium - Kính cường lực 9H trong suốt 99% - Giá $14.99"
            }
        ]
    },
    "Phụ Kiện Apple": {
        "products": [
            {
                "brand": "Apple",
                "name": "AirPods Pro 2nd Gen",
                "price": 299.99,
                "promotion": 10,
                "description": "Tai nghe không dây Apple AirPods Pro thế hệ thứ 2, công nghệ chống ồn chủ động, âm thanh spatial audio 3D.",
                "detail": "• Công nghệ chống ồn: Active Noise Cancellation (ANC)\n• Chế độ trong suốt: Adaptive Audio\n• Âm thanh: Spatial Audio với dynamic head tracking\n• Pin: Lên tới 6 giờ (chế độ ANC), 30 giờ với hộp sạc\n• Kết nối: Bluetooth 5.3, Apple H2 chip\n• Tính năng: Cảm biến chạm, phát hiện tai\n• Bảo hành: 12 tháng",
                "summary": "AirPods Pro 2nd Gen - Tai nghe không dây, chống ồn, spatial audio - Giá $299.99"
            },
            {
                "brand": "Apple",
                "name": "AirTag",
                "price": 29.99,
                "promotion": 5,
                "description": "Thiết bị định vị Apple AirTag, theo dõi vị trí túi, chìa khóa, động vật cưng dễ dàng.",
                "detail": "• Công nghệ: Bluetooth LE\n• Phạm vi: Lên tới 120m (không chướng ngại vật)\n• Pin: CR2032 (thay thế dễ)\n• Tính năng: Chế độ Mất Tìm Kiếm, âm thanh cảnh báo\n• Tương thích: iPhone 11 trở lên\n• Chống nước: IPX7\n• Bảo hành: 12 tháng",
                "summary": "AirTag - Thiết bị định vị thông minh, phạm vi 120m, pin 1 năm - Giá $29.99"
            },
            {
                "brand": "Apple",
                "name": "Magic Mouse 2",
                "price": 99.99,
                "promotion": 8,
                "description": "Chuột Magic Mouse 2 không dây của Apple, bề mặt touch, pin sạc lâu dài.",
                "detail": "• Kiểu: Wireless (Bluetooth)\n• Bề mặt: Multi-touch\n• Pin: Sạc USB-C, thời lượng 1 tháng\n• Tìm kiếm: Sạc 2 phút = dùng 9 ngày\n• Tương thích: Mac, iPad\n• Trọng lượng: Nhẹ, cầm thoải mái\n• Bảo hành: 12 tháng",
                "summary": "Magic Mouse 2 - Chuột không dây Apple, multi-touch, pin 1 tháng - Giá $99.99"
            },
            {
                "brand": "Apple",
                "name": "Smart Keyboard Folio",
                "price": 179.99,
                "promotion": 12,
                "description": "Bàn phím thông minh Apple Smart Keyboard Folio cho iPad, bảo vệ và tích hợp bàn phím.",
                "detail": "• Tương thích: iPad Pro 11-inch, 12.9-inch\n• Loại kết nối: Smart Connector (không cần pin)\n• Phím: Cơ học, hành trình thoải mái\n• Bảo vệ: Bao da tích hợp\n• Trọng lượng: Gọn nhẹ\n• Ngôn ngữ: Tiếng Việt sẵn sàng\n• Bảo hành: 12 tháng",
                "summary": "Smart Keyboard Folio - Bàn phím thông minh cho iPad, bảo vệ 2 chiều - Giá $179.99"
            }
        ]
    },
    "Pin dự phòng": {
        "products": [
            {
                "brand": "Anker",
                "name": "PowerCore 26800mAh",
                "price": 49.99,
                "promotion": 15,
                "description": "Pin sạc dự phòng Anker 26800mAh, sạc nhanh 3 thiết bị cùng lúc, dung lượng lớn.",
                "detail": "• Dung lượng: 26800mAh (real capacity)\n• Cổng: 2x USB-A, 1x USB-C input\n• Công suất: 5V/3A per port\n• Tương thích: Điện thoại, tablet, camera\n• Sạc nhanh: Hỗ trợ iPhone Fast Charging\n• Trọng lượng: 520g\n• Bảo hành: 18 tháng",
                "summary": "PowerCore 26800mAh - Pin dự phòng 26800mAh, 2 cổng USB-A, sạc 3 thiết bị - Giá $49.99"
            },
            {
                "brand": "Xiaomi",
                "name": "Mi Power Bank 3 Pro 20000mAh",
                "price": 39.99,
                "promotion": 10,
                "description": "Pin sạc Xiaomi 20000mAh, sạc nhanh USB-C 18W, thiết kế nhỏ gọn, pin lâu bền.",
                "detail": "• Dung lượng: 20000mAh\n• Cổng: 2x USB-A, 1x USB-C (input/output)\n• Công suất: USB-C 18W sạc nhanh\n• Tương thích: iPhone, Android, Tablet\n• Trọng lượng: 278g\n• LED hiển thị: 4 cấp độ pin\n• Bảo hành: 12 tháng",
                "summary": "Mi Power Bank 3 Pro 20000mAh - Pin 20000mAh, sạc nhanh 18W, đủ pin cả ngày - Giá $39.99"
            },
            {
                "brand": "Samsung",
                "name": "25000mAh Fast Charging",
                "price": 59.99,
                "promotion": 18,
                "description": "Pin dự phòng Samsung 25000mAh với công nghệ sạc nhanh super fast, pin bền bỉ.",
                "detail": "• Dung lượng: 25000mAh (typ)\n• Sạc nhanh: Super Fast Charging 25W\n• Cổng: USB-C in/out, 2x USB\n• Tương thích: Galaxy series, điện thoại khác\n• Chế độ sạc ngược: Có (Wireless PowerShare)\n• Trọng lượng: 544g\n• Bảo hành: 12 tháng",
                "summary": "25000mAh Fast Charging - Pin Samsung 25000mAh, sạc nhanh 25W, wireless - Giá $59.99"
            }
        ]
    },
    "Sim 5G | Sim 4G | Sim 3G": {
        "products": [
            {
                "brand": "Viettel",
                "name": "Sim 4G Viettel MAX15",
                "price": 2.99,
                "promotion": 0,
                "description": "Sim 4G Viettel MAX15 tốc độ cao, gói cước 15k/tháng, miễn phí 4G 90 ngày đầu.",
                "detail": "• Nhà mạng: Viettel\n• Công nghệ: 4G LTE\n• Gói cước: MAX15 - 15,000 đồng/tháng\n• Data: 8GB 4G, không giới hạn 3G\n• Cuộc gọi: Gọi trọn gói\n• Ưu đãi: Miễn phí 4G 90 ngày đầu\n• Bảng giá: Hỗ trợ all-in-one",
                "summary": "Sim 4G Viettel MAX15 - Gói 15k/tháng, 8GB 4G, miễn phí 90 ngày - Giá $2.99"
            },
            {
                "brand": "Mobifone",
                "name": "Sim 5G Mobifone MAX10",
                "price": 2.49,
                "promotion": 5,
                "description": "Sim 5G Mobifone MAX10, tốc độ 5G ultra-fast, gói cước phổ biến 10,000 đồng/tháng.",
                "detail": "• Nhà mạng: Mobifone\n• Công nghệ: 5G/4G LTE\n• Gói cước: MAX10 - 10,000 đồng/tháng\n• Data: 5GB 5G, 20GB 4G\n• Tốc độ 5G: Lên tới 1Gbps\n• Miễn phí: 30 ngày gói cước\n• Bảng giá: Hỗ trợ all-in-one",
                "summary": "Sim 5G Mobifone MAX10 - Gói 10k/tháng, 5G tốc độ cao, 20GB - Giá $2.49"
            },
            {
                "brand": "Vinaphone",
                "name": "Sim 5G Vinaphone 4G60",
                "price": 5.99,
                "promotion": 8,
                "description": "Sim 5G Vinaphone 4G60, tốc độ 5G nhanh, gói cước 60,000 đồng, lợi ích cao.",
                "detail": "• Nhà mạng: Vinaphone\n• Công nghệ: 5G/4G LTE\n• Gói cước: 4G60 - 60,000 đồng/tháng\n• Data: 30GB 5G, 30GB 4G, miễn phí data\n• Tốc độ: 5G 1Gbps+, 4G 150Mbps\n• Ngoại quốc: Roaming 150 nước\n• Bảng giá: Hỗ trợ businesshàng tháng",
                "summary": "Sim 5G Vinaphone 4G60 - Gói 60k/tháng, 60GB data hàng tháng - Giá $5.99"
            }
        ]
    },
    "Thẻ nhớ, USB": {
        "products": [
            {
                "brand": "SanDisk",
                "name": "Ultra microSD 256GB",
                "price": 34.99,
                "promotion": 12,
                "description": "Thẻ nhớ microSD SanDisk Ultra 256GB, tốc độ đọc 150MB/s, tương thích điện thoại, camera.",
                "detail": "• Dung lượng: 256GB\n• Tốc độ đọc: 150MB/s\n• Tốc độ ghi: 90MB/s\n• Chuẩn: microSD UHS-I\n• Chống chịu: Nước, nhiệt, chống từ\n• Bảo hành: Vĩnh viễn\n• Tương thích: Điện thoại Android, camera, drone",
                "summary": "Ultra microSD 256GB - Thẻ nhớ 256GB, tốc độ 150MB/s, chống chịu - Giá $34.99"
            },
            {
                "brand": "Kingston",
                "name": "DataTraveler USB 3.0 64GB",
                "price": 15.99,
                "promotion": 8,
                "description": "USB 3.0 Kingston DataTraveler 64GB, tốc độ truyền nhanh, thiết kế nhỏ gọn.",
                "detail": "• Dung lượng: 64GB\n• Chuẩn: USB 3.0\n• Tốc độ đọc: 110MB/s\n• Tốc độ ghi: 70MB/s\n• Kết nối: USB 3.0 / 2.0 compatible\n• Thiết kế: Cực nhỏ gọn 46 x 21 x 13 mm\n• Bảo hành: 5 năm",
                "summary": "DataTraveler USB 3.0 64GB - USB 64GB tốc độ 110MB/s, cực nhỏ - Giá $15.99"
            },
            {
                "brand": "Samsung",
                "name": "microSD Card Pro 128GB",
                "price": 24.99,
                "promotion": 10,
                "description": "Thẻ nhớ Samsung Pro Plus 128GB, tốc độ 160MB/s, hỗ trợ 4K video, bền bỉ.",
                "detail": "• Dung lượng: 128GB\n• Tốc độ đọc: 160MB/s\n• Tốc độ ghi: 120MB/s\n• Video: Hỗ trợ 4K UHD\n• Độ bền: -13°C đến 85°C\n• Chống chịu: Nước, chống từ trường, chống tác động\n• Bảo hành: 10 năm",
                "summary": "microSD Card Pro 128GB - Thẻ nhớ 128GB, tốc độ 160MB/s, hỗ trợ 4K - Giá $24.99"
            }
        ]
    },
    "Ốp lưng điện thoại | Bao da": {
        "products": [
            {
                "brand": "Spigen",
                "name": "Rugged Armor Case",
                "price": 18.99,
                "promotion": 10,
                "description": "Ốp lưng Spigen Rugged Armor, bảo vệ toàn diện, chống sốc, thiết kế mỏng nhẹ.",
                "detail": "• Chất liệu: TPU + PC hybrid\n• Bảo vệ: Chống sốc lên tới 10ft\n• Thiết kế: Mỏng nhẹ, dễ cất\n• Tương thích: iPhone 15, 14, 13, Samsung S24\n• Cảm ứng: Không ảnh hưởng\n• Khí thải: Thoát khí qua thiết kế\n• Bảo hành: 12 tháng",
                "summary": "Rugged Armor Case - Ốp lưng chống sốc 10ft, mỏng nhẹ, hybrid TPU+PC - Giá $18.99"
            },
            {
                "brand": "OtterBox",
                "name": "Defender Series Case",
                "price": 49.99,
                "promotion": 15,
                "description": "Ốp lưng OtterBox Defender, bảo vệ cấp quân đội, chống sốc tối đa, bao da chắc chắn.",
                "detail": "• Chất liệu: Polycarbonate + Synthetic rubber\n• Bảo vệ: Cấp quân đội MIL-STD-810G\n• Chống sốc: Lên tới 15ft\n• Bao da: Góc bảo vệ toàn diện\n• Tương thích: iPhone 15 Pro Max, Galaxy S24 Ultra\n• Khiếc: Cắt Precisions để dễ sử dụng\n• Bảo hành: 2 năm",
                "summary": "Defender Series Case - Ốp lưng cấp quân đội, chống sốc 15ft, bao da chắc - Giá $49.99"
            },
            {
                "brand": "Apple",
                "name": "Silicone Case",
                "price": 39.99,
                "promotion": 8,
                "description": "Ốp lưng Silicone chính hãng Apple, mềm mại, bảo vệ tốt, nhiều màu sắc.",
                "detail": "• Chất liệu: Silicone nguyên chất\n• Thiết kế: Vừa vặn hoàn hảo\n• Màu sắc: 12+ tùy chọn\n• Tương thích: iPhone 15, 14, 13 series\n• Bảo vệ: Chống bụi, chống trầy xước\n• Mềm mại: Cảm giác thoải mái khi cầm\n• Bảo hành: 12 tháng",
                "summary": "Silicone Case - Ốp lưng silicone Apple, mềm mại, 12+ màu sắc - Giá $39.99"
            }
        ]
    }
}

def generate_normalized_accessories():
    """Sinh dữ liệu phụ kiện chuẩn hóa theo format v2"""
    
    normalized_data = {
        "products": [],
        "product_images": [],
        "reviews": []
    }
    
    product_id = 1
    base_date = datetime(2026, 1, 1)
    
    for category, category_data in accessories_info.items():
        for product in category_data["products"]:
            # Xác định category code
            category_code = category.upper().replace(" ", "_").replace("|", "")[:30]
            
            # Sinh ngày tạo random (từ 2026-01-01 đến 2026-03-28)
            random_days = random.randint(0, 86)  # ~3 tháng
            created_date = (base_date + timedelta(days=random_days)).isoformat()
            
            # Tạo product record
            product_record = {
                "name": product["name"],
                "description": product["description"],
                "detail": product["detail"],
                "summary": product["summary"],
                "category": category_code,
                "price": product["price"],
                "brand": product["brand"],
                "promotion": product["promotion"],
                "created_date": created_date
            }
            
            normalized_data["products"].append(product_record)
            
            # Tạo hình ảnh CHỈ cho product_id từ 15 trở lên
            if product_id >= 15:
                product_slug = product["name"].lower().replace(" ", "-")
                for i in range(3):
                    image_url = f"https://cdn.example.com/accessories/{product['brand'].lower()}/{product_slug}-{i+1}.jpg"
                    product_images = {
                        "product_id": product_id,
                        "image_url": image_url
                    }
                    normalized_data["product_images"].append(product_images)
            
            # Tạo sample reviews (CHỈ cho product_id từ 15 trở lên)
            if product_id >= 15:
                reviews_count = random.randint(10, 50)
                for j in range(min(3, reviews_count)):
                    review = {
                        "product_id": product_id,
                        "rating": random.randint(3, 5),
                        "comment": f"Sản phẩm chất lượng tốt, đúng với mô tả. Đóng gói cẩn thận. Giao hàng nhanh.",
                        "created_date": datetime.now().isoformat()
                    }
                    normalized_data["reviews"].append(review)
            
            product_id += 1
    
    return normalized_data

def save_to_file():
    """Lưu dữ liệu vào file"""
    data = generate_normalized_accessories()
    
    with open("normalized_accessories_v2.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Generated normalized_accessories_v2.json")
    print(f"  - Total products: {len(data['products'])}")
    print(f"  - Total product images: {len(data['product_images'])}")
    print(f"  - Total reviews: {len(data['reviews'])}")
    
    # In preview
    print("\n=== Preview của 3 sản phẩm đầu tiên (1-3, không có hình ảnh) ===")
    for i, product in enumerate(data['products'][:3]):
        print(f"\n{i+1}. {product['name']}")
        print(f"   Brand: {product['brand']}")
        print(f"   Price: ${product['price']}")
        print(f"   Category: {product['category']}")
        print(f"   Promotion: {product['promotion']}%")
        print(f"   Created: {product['created_date']}")
    
    print("\n=== Preview của 2 sản phẩm từ #15 (có hình ảnh) ===")
    for i, product in enumerate(data['products'][14:16]):
        print(f"\n{i+15}. {product['name']}")
        print(f"   Brand: {product['brand']}")
        print(f"   Price: ${product['price']}")
        print(f"   Created: {product['created_date']}")

if __name__ == "__main__":
    save_to_file()
