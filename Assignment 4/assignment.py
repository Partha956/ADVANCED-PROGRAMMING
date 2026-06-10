inventory = [
    {"name": "Mobile", "stock": 15},
    {"name": "Mouse", "stock": 5},
    {"name": "Keyboard", "stock": 8},
    {"name": "Monitor", "stock": 12},
    {"name": "USB Cable", "stock": 3},
    {"name": "Headphones", "stock": 20}
]

print("--- Low Stock Alert (Less than 10 units) ---")

found_low_stock = False
for product in inventory:
    if product["stock"] < 10:
        print(f"Product: {product['name']} | Remaining Stock: {product['stock']}")
        found_low_stock = True

if not found_low_stock:
    print("All products are well-stocked!")