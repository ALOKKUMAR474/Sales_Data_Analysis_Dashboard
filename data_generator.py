import csv
import random
from datetime import datetime, timedelta

# Product Catalog
PRODUCTS = {
    "Technology": {
        "Phones": [
            ("Apple iPhone 15 Pro", 999.00),
            ("Samsung Galaxy S24 Ultra", 1199.00),
            ("Google Pixel 8 Pro", 999.00),
            ("OnePlus 12", 799.00),
        ],
        "Accessories": [
            ("Logitech MX Master 3S Mouse", 99.00),
            ("Apple AirPods Pro (2nd Gen)", 249.00),
            ("Anker 511 USB-C Charger", 22.99),
            ("Samsung T7 Shield 2TB SSD", 159.99),
        ],
        "Copiers": [
            ("Canon imageCLASS Wireless Printer", 299.00),
            ("HP LaserJet Pro Multifunction", 449.00),
            ("Brother Monochrome Laser Printer", 199.00),
        ],
        "Machines": [
            ("Apple MacBook Pro 16 M3", 2499.00),
            ("Dell XPS 15 Laptop", 1899.00),
            ("Lenovo ThinkPad X1 Carbon", 1699.00),
            ("ASUS ROG Zephyrus G14", 1599.00),
        ]
    },
    "Furniture": {
        "Chairs": [
            ("Herman Miller Aeron Chair", 1499.00),
            ("Steelcase Gesture Office Chair", 1399.00),
            ("Secretlab TITAN Evo Gaming Chair", 549.00),
            ("Ergonomic Mesh Office Chair", 249.00),
        ],
        "Tables": [
            ("Standing Desk Wood Top 60x30", 499.00),
            ("Solid Oak Dining Table", 899.00),
            ("Minimalist Glass Coffee Table", 199.00),
            ("Industrial Writing Desk", 149.00),
        ],
        "Bookcases": [
            ("5-Shelf Wood Bookcase", 129.00),
            ("Industrial Metal & Wood Bookshelf", 189.00),
            ("Corner Ladder Shelf", 79.99),
        ],
        "Furnishings": [
            ("LED Desk Lamp with USB Charger", 34.99),
            ("Anti-Fatigue Comfort Floor Mat", 42.50),
            ("Acoustic Desk Divider Partition", 89.00),
            ("Ergonomic Memory Foam Seat Cushion", 29.99),
        ]
    },
    "Office Supplies": {
        "Paper": [
            ("Premium Multipurpose Copy Paper Case", 54.00),
            ("Eco-Friendly Recycled Printer Paper", 8.99),
            ("Heavyweight Cardstock Paper 100 Sheets", 14.50),
        ],
        "Art": [
            ("Dual Tip Brush Marker Pens 72-Color Set", 39.99),
            ("Acrylic Paint Set 24 Colors", 24.50),
            ("Professional Sketchbook 2-Pack", 18.99),
            ("Fiskars Precision Scissors 8-Inch", 11.25),
        ],
        "Binders": [
            ("Heavy Duty 3-Ring Binder 3-Pack", 21.99),
            ("Plastic Pocket Folders 10-Pack", 10.50),
            ("Clear Sheet Protectors 200-Pack", 14.99),
        ],
        "Appliances": [
            ("Compact Countertop Microwave 0.7 Cu Ft", 89.00),
            ("Keurig K-Mini Single Serve Coffee Maker", 79.00),
            ("Dyson Pure Cool Air Purifier Fan", 399.00),
            ("Mini Fridge with Freezer 3.2 Cu Ft", 159.00),
        ]
    }
}

# Geographies
CITIES = [
    ("New York City", "New York", "East", "10001"),
    ("Los Angeles", "California", "West", "90001"),
    ("Chicago", "Illinois", "Central", "60601"),
    ("Houston", "Texas", "Central", "77001"),
    ("Philadelphia", "Pennsylvania", "East", "19101"),
    ("Phoenix", "Arizona", "West", "85001"),
    ("San Antonio", "Texas", "Central", "78201"),
    ("San Diego", "California", "West", "92101"),
    ("Dallas", "Texas", "Central", "75201"),
    ("San Jose", "California", "West", "95101"),
    ("Austin", "Texas", "Central", "78701"),
    ("Jacksonville", "Florida", "South", "32201"),
    ("San Francisco", "California", "West", "94101"),
    ("Columbus", "Ohio", "Central", "43201"),
    ("Indianapolis", "Indiana", "Central", "46201"),
    ("Charlotte", "North Carolina", "South", "28201"),
    ("Seattle", "Washington", "West", "98101"),
    ("Denver", "Colorado", "West", "80201"),
    ("Boston", "Massachusetts", "East", "02101"),
    ("Nashville", "Tennessee", "South", "37201"),
    ("Miami", "Florida", "South", "33101"),
    ("Atlanta", "Georgia", "South", "30301"),
]

# Customers
CUSTOMERS = [
    ("Claire Gute", "Consumer", "CG-12520"),
    ("Brosina Hoffman", "Consumer", "BH-11710"),
    ("Andrew Allen", "Consumer", "AA-10315"),
    ("Irene Maddox", "Consumer", "IM-15055"),
    ("Harold Ryan", "Corporate", "HR-14830"),
    ("Pete Kriz", "Corporate", "PK-19075"),
    ("Alejandro Grove", "Consumer", "AG-10270"),
    ("Zuschlich Donavan", "Corporate", "ZD-21925"),
    ("Ken Black", "Corporate", "KB-16585"),
    ("Sandra Flanagan", "Consumer", "SF-20065"),
    ("Emily Phan", "Consumer", "EP-13915"),
    ("Tracy Blumstein", "Consumer", "TB-21520"),
    ("Gene Hale", "Corporate", "GH-14485"),
    ("Steve Nguyen", "Home Office", "SN-20785"),
    ("Linda Cazaress", "Home Office", "LC-16885"),
    ("Duane Noonan", "Consumer", "DN-13690"),
    ("Roy Phan", "Corporate", "RP-19390"),
    ("Liz Flachtemeier", "Consumer", "LF-17185"),
    ("Raymond Buch", "Consumer", "RB-19705"),
    ("Tom Boeckenhauer", "Consumer", "TB-21400"),
]

def generate_data(num_rows=10500):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 6, 30)
    delta_days = (end_date - start_date).days
    
    data = []
    
    for i in range(num_rows):
        order_date = start_date + timedelta(days=random.randint(0, delta_days))
        
        # Monthly base seasonal factor
        month = order_date.month
        year = order_date.year
        seasonal_multiplier = 1.0
        
        if month in [11, 12]:
            seasonal_multiplier = 1.4
        elif month in [1, 2]:
            seasonal_multiplier = 0.8
            
        # SPECIFIC RESUME INJECTION:
        # Detect a 20% revenue decline in Q3 2025 (July, August, September 2025)
        # We apply a 22% reduction in transaction sales value during Q3 2025 to model this decline
        is_q3_2025 = (year == 2025 and month in [7, 8, 9])
        decline_multiplier = 0.78 if is_q3_2025 else 1.0
        
        ship_days = random.choices([1, 2, 3, 4, 5, 6, 7], weights=[10, 20, 30, 20, 10, 5, 5])[0]
        ship_date = order_date + timedelta(days=ship_days)
        
        ship_modes = ["Same Day", "First Class", "Second Class", "Standard Class"]
        if ship_days == 1:
            ship_mode = "Same Day"
        elif ship_days <= 3:
            ship_mode = random.choices(ship_modes[:3], weights=[10, 40, 50])[0]
        else:
            ship_mode = "Standard Class"
            
        order_id = f"CA-{order_date.year}-{100000 + i}"
        cust_name, cust_segment, cust_id = random.choice(CUSTOMERS)
        city, state, region, postal_code = random.choice(CITIES)
        
        category = random.choices(list(PRODUCTS.keys()), weights=[30, 30, 40])[0]
        sub_category = random.choice(list(PRODUCTS[category].keys()))
        product_name, base_price = random.choice(PRODUCTS[category][sub_category])
        
        unit_price = base_price * random.uniform(0.9, 1.1)
        quantity = random.choices(list(range(1, 11)), weights=[30, 25, 15, 10, 8, 5, 3, 2, 1, 1])[0]
        discount = random.choices([0.0, 0.1, 0.2, 0.3, 0.4], weights=[60, 15, 15, 7, 3])[0]
        
        # Calculate gross sales incorporating multipliers
        sales = unit_price * quantity * (1.0 - discount) * seasonal_multiplier * decline_multiplier
        sales = round(sales, 2)
        
        # Margin setup
        margin_map = {
            "Technology": (0.15, 0.35),
            "Office Supplies": (0.10, 0.25),
            "Furniture": (-0.05, 0.15)
        }
        min_m, max_m = margin_map[category]
        margin = random.uniform(min_m, max_m)
        
        cost = unit_price * quantity * (1.0 - margin) * decline_multiplier
        profit = round(sales - cost, 2)
        
        product_id = f"{category[:3]}-{sub_category[:3]}-{10000000 + random.randint(1000, 9999)}"
        
        data.append({
            "Row ID": i + 1,
            "Order ID": order_id,
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Ship Date": ship_date.strftime("%Y-%m-%d"),
            "Ship Mode": ship_mode,
            "Customer ID": cust_id,
            "Customer Name": cust_name,
            "Segment": cust_segment,
            "Country": "United States",
            "City": city,
            "State": state,
            "Postal Code": postal_code,
            "Region": region,
            "Product ID": product_id,
            "Category": category,
            "Sub-Category": sub_category,
            "Product Name": product_name,
            "Sales": sales,
            "Quantity": quantity,
            "Discount": discount,
            "Profit": profit
        })
        
    return data

def main():
    print("Generating 10,500 e-commerce sales records with injected Q3 2025 20% decline...")
    rows = generate_data(10500)
    
    filename = "sales_data.csv"
    fields = [
        "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode", 
        "Customer ID", "Customer Name", "Segment", "Country", "City", 
        "State", "Postal Code", "Region", "Product ID", "Category", 
        "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "Profit"
    ]
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Dataset saved successfully as '{filename}' with {len(rows)} rows.")

if __name__ == "__main__":
    main()
