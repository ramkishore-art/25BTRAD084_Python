# Sales Data Analyzer
# Mini Project

products = {}

def add_product():
    name = input("Enter product name: ").strip().title()
    if not name:
        print("Product name cannot be empty.")
        return
    try:
        quantity = int(input("Enter quantity sold: "))
        price = float(input("Enter price per unit (Rs.): "))
        if quantity < 0 or price < 0:
            print("Quantity and price cannot be negative.")
            return
    except ValueError:
        print("Please enter valid numeric values.")
        return
    
    if name in products:
        products[name]["quantity"] += quantity
        products[name]["price"] = price
        print("Existing product record updated successfully.")
    else:
        products[name] = {"quantity": quantity, "price": price}
        print("Product added successfully.")

def update_sales():
    name = input("Enter product name to update: ").strip().title()
    if name not in products:
        print("Product not found. Add it first.")
        return
    try:
        quantity = int(input("Enter new total quantity sold: "))
        price = float(input("Enter price per unit (Rs.): "))
        if quantity < 0 or price < 0:
            print("Quantity and price cannot be negative.")
            return
    except ValueError:
        print("Please enter valid numeric values.")
        return
    
    products[name] = {"quantity": quantity, "price": price}
    print("Sales record updated successfully.")

def display_report():
    if not products:
        print("No sales records available.")
        return
    print("\n" + "=" * 68)
    print(f"{'PRODUCT':<20}{'QUANTITY':>12}{'UNIT PRICE':>16}{'REVENUE':>18}")
    print("-" * 68)
    for name, details in products.items():
        revenue = details["quantity"] * details["price"]
        print(f"{name:<20}{details['quantity']:>12}{details['price']:>16.2f}{revenue:>18.2f}")
    print("-" * 68)

def calculate_total_revenue():
    total = sum(item["quantity"] * item["price"] for item in products.values())
    print(f"Total sales revenue: Rs. {total:,.2f}")

def best_selling_product():
    if not products:
        print("No products available.")
        return
    best = max(products, key=lambda item: products[item]["quantity"])
    details = products[best]
    print(f"Highest-selling product: {best}")
    print(f"Quantity sold: {details['quantity']} units")
    print(f"Revenue: Rs. {details['quantity'] * details['price']:,.2f}")

def compare_performance():
    if not products:
        print("No products available.")
        return
    print("\nProduct-wise performance (ranked by quantity sold):")
    ranked = sorted(products.items(), key=lambda item: item[1]["quantity"], reverse=True)
    for rank, (name, details) in enumerate(ranked, start=1):
        revenue = details["quantity"] * details["price"]
        print(f"{rank}. {name}: {details['quantity']} units | Revenue: Rs. {revenue:,.2f}")

def main():
    while True:
        print("\n========== SALES DATA ANALYZER ==========")
        print("1. Add Product")
        print("2. Update Sales")
        print("3. Display Sales Report")
        print("4. Calculate Total Revenue")
        print("5. Highest-Selling Product")
        print("6. Compare Product Performance")
        print("7. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            add_product()
        elif choice == "2":
            update_sales()
        elif choice == "3":
            display_report()
        elif choice == "4":
            calculate_total_revenue()
        elif choice == "5":
            best_selling_product()
        elif choice == "6":
            compare_performance()
        elif choice == "7":
            print("Thank you for using Sales Data Analyzer!")
            break
        else:
            print("Invalid choice. Please select 1 to 7.")

if __name__ == "__main__":
    main()
