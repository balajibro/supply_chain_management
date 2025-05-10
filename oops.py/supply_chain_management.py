import pandas as pd

class Product:
    def __init__(self, product_id, name, stock, reorder_level, price):
        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.reorder_level = reorder_level
        self.price = price

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'stock': self.stock,
            'reorder_level': self.reorder_level,
            'price': self.price
        }

class Supplier:
    def __init__(self, supplier_id, name, supplied_products):
        self.supplier_id = supplier_id
        self.name = name
        self.supplied_products = supplied_products

    def to_dict(self):
        return {
            'supplier_id': self.supplier_id,
            'name': self.name,
            'supplied_products': ', '.join(self.supplied_products)
        }

class SupplyChainSystem:
    def __init__(self):
        self.products = pd.DataFrame()
        self.suppliers = pd.DataFrame()
        self.init_data()

    def init_data(self):
        product_list = [
            Product(1, "Laptop", 10, 5, 1000),
            Product(2, "Smartphone", 50, 20, 500),
            Product(3, "Headphones", 30, 10, 100),
        ]
        self.products = pd.DataFrame([p.to_dict() for p in product_list])

        supplier_list = [
            Supplier(101, "TechCorp", ["Laptop", "Headphones"]),
            Supplier(102, "MobileMakers", ["Smartphone"]),
        ]
        self.suppliers = pd.DataFrame([s.to_dict() for s in supplier_list])

    def view_inventory(self):
        print("\nCurrent Inventory:")
        print(self.products[['product_id', 'name', 'stock', 'reorder_level']])

    def sell_product(self, product_id, quantity):
        if product_id not in self.products['product_id'].values:
            print("Invalid Product ID.")
            return

        index = self.products.index[self.products['product_id'] == product_id][0]
        current_stock = self.products.at[index, 'stock']
        if current_stock < quantity:
            print(f"Insufficient stock. Available: {current_stock}")
        else:
            self.products.at[index, 'stock'] -= quantity
            print(f"Sold {quantity} units of {self.products.at[index, 'name']}")
            self.check_reorder(product_id)

    def check_reorder(self, product_id):
        index = self.products.index[self.products['product_id'] == product_id][0]
        stock = self.products.at[index, 'stock']
        reorder_level = self.products.at[index, 'reorder_level']
        if stock <= reorder_level:
            print(f"Reorder Alert: Stock for {self.products.at[index, 'name']} is low ({stock} units).")

    def place_order(self, product_id, quantity):
        if product_id not in self.products['product_id'].values:
            print("Invalid Product ID.")
            return

        index = self.products.index[self.products['product_id'] == product_id][0]
        self.products.at[index, 'stock'] += quantity
        print(f"Reordered {quantity} units of {self.products.at[index, 'name']}")

    def view_suppliers(self):
        print("\nSupplier Information:")
        print(self.suppliers)

    def generate_report(self):
        print("\nInventory Report:")
        low_stock = self.products[self.products['stock'] <= self.products['reorder_level']]
        if not low_stock.empty:
            print("Low Stock Items:")
            print(low_stock[['product_id', 'name', 'stock']])
        else:
            print("All items are well-stocked.")

def menu():
    system = SupplyChainSystem()
    while True:
        print("\n=== Supply Chain Management System ===")
        print("1. View Inventory")
        print("2. Sell Product")
        print("3. Place Order")
        print("4. View Suppliers")
        print("5. Generate Low Stock Report")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            system.view_inventory()
        elif choice == '2':
            try:
                pid = int(input("Enter Product ID: "))
                qty = int(input("Enter Quantity to Sell: "))
                system.sell_product(pid, qty)
            except:
                print("Invalid input.")
        elif choice == '3':
            try:
                pid = int(input("Enter Product ID: "))
                qty = int(input("Enter Quantity to Order: "))
                system.place_order(pid, qty)
            except:
                print("Invalid input.")
        elif choice == '4':
            system.view_suppliers()
        elif choice == '5':
            system.generate_report()
        elif choice == '6':
            print("Exiting... Thank you.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
