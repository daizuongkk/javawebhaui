import csv

f = open('normalized_products_v2.csv')
reader = csv.DictReader(f)
rows = list(reader)

print('=== SAMPLE PRODUCTS ===\n')
for i, r in enumerate(rows[:5], 1):
    print(f"{i}. {r['name']}")
    print(f"   Price: ${r['price']} USD")
    print(f"   Summary: {r['summary']}")
    print(f"   Promotion: {r['promotion']}%")
    print()
    
f.close()
