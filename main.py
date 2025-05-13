from abc import ABC, abstractmethod
from datetime import datetime
import json

# ---------------------- Product Base Class ----------------------
# *1. Abstract Base Class: Product*
# Use the abc module to make Product an abstract base class.
# Attributes (with encapsulation):
# * _product_id
# * _name
# * _price
# * _quantity_in_stock


class Product(ABC):
    def __init__(self, productId, name, price, quantity_in_stock):
        self._product_id = productId
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity_in_stock

# Methods (abstract & concrete):
# * restock(amount)
    def restock(self, amount):
        self._quantity_in_stock += amount

# * sell(quantity)

    def sell(self, quantity):
        if quantity <= self._quantity_in_stock:
            self._quantity_in_stock -= quantity
        else:
            print("Insufficient stock!"
                  )
# * get_total_value() --> price \ stock
    def get_total_value(self):
        return self._price * self._quantity_in_stock
    
# * __str__() --> formatted product info
    def __str__(self):
        return (f"Product ID: {self._product_id}, Name: {self._name}, Price: {self._price}, "
                f"Stock: {self._quantity_in_stock}, Total Value: {self.get_total_value()}")

#abstract method
    @abstractmethod
    def display_info(self):
        pass

# ---------------------- Subclasses ----------------------
# *2. Subclasses of Product:*
# Create at least 3 different product types, each with extra attributes and overridden behavior where needed:
# Each subclass must override __str__() to include their specific info.

# * *Electronics* --> warranty_years, brand

class Electronics(Product):
    def __init__(self, productId, name, price, quantity_in_stock, warranty_years, brand):
        super().__init__(productId, name, price, quantity_in_stock)
        self._warranty_years = warranty_years
        self._brand = brand

    def display_info(self):
        return f"{self._brand} - {self._name}, Warranty: {self._warranty_years} years"

    def __str__(self):
        return super().__str__() + f", Brand: {self._brand}, Warranty: {self._warranty_years} years"

# * *Grocery* --> expiry_date, is_expired()

class Grocery(Product):
    def __init__(self, productId, name, price, quantity_in_stock, expiry_date):
        super().__init__(productId, name, price, quantity_in_stock)
        self.expiry_date = expiry_date  # format: 'YYYY-MM-DD'

    def is_expired(self):
        today = datetime.now().date()
        expiry = datetime.strptime(self.expiry_date, '%Y-%m-%d').date()
        return today > expiry

    def display_info(self):
        return f"{self._name} - Expires on: {self.expiry_date}"

    def __str__(self):
        status = "Expired" if self.is_expired() else "Fresh"
        return super().__str__() + f", Expiry Date: {self.expiry_date}, Status: {status}"

# * *Clothing*  --> size, material
class Clothing(Product):
    def __init__(self, productId, name, price, quantity_in_stock, size, material):
        super().__init__(productId, name, price, quantity_in_stock)
        self.size = size
        self.material = material

    def display_info(self):
        return f"{self._name} - Size: {self.size}, Material: {self.material}"

    def __str__(self):
        return super().__str__() + f", Size: {self.size}, Material: {self.material}"


# ---------------------- Inventory Class ----------------------
# *3. Class: Inventory*
# This class will manage a collection of products.
# Attributes:
# * _products --> a dict or list of products

class Inventory:
    def __init__(self):
        self._products = []
# * add_product(product: Product)
    def add_product(self, product: Product):
        self._products.append(product)
        return f"{product._name} added. Total products: {len(self._products)}"
    
# * remove_product(product_id)
    def remove_product(self, product_id):
        for product in self._products:
            if product._product_id == product_id:
                self._products.remove(product)
                return f"Product ID {product_id} removed."
        return f"Product ID {product_id} not found."

# * search_by_name(name)
    def search_by_name(self, name):
        results = [product for product in self._products if name.lower() in product._name.lower()]
        return results if results else f"No products found with name '{name}'."
    
# * search_by_type(product_type)
    def search_by_type(self, product_type):
        results = [product for product in self._products if isinstance(product, product_type)]
        return results if results else f"No products found of type '{product_type.__name__}'."

# * list_all_products()
    def list_all_products(self):
        return [str(product) for product in self._products] if self._products else ["No products in inventory."]

# * sell_product(product_id, quantity)
    def sell_product(self, product_id, quantity):
        for product in self._products:
            if product._product_id == product_id:
                product.sell(quantity)
                return f"Sold {quantity} of {product._name}."
        return f"Product ID {product_id} not found."

# * restock_product(product_id, quantity)
    def restock_product(self, product_id, quantity):
        for product in self._products:
            if product._product_id == product_id:
                product.restock(quantity)
                return f"Restocked {quantity} of {product._name}."
        return f"Product ID {product_id} not found."
    
# * total_inventory_value()
    def total_inventory_value(self):
        return sum(product.get_total_value() for product in self._products)

# * remove_expired_products() (for groceries only) -->
    def remove_expired_products(self):
        removed = []
        for product in self._products[:]:
            if isinstance(product, Grocery) and product.is_expired():
                self._products.remove(product)
                removed.append(product._name)
        return f"Removed expired products: {', '.join(removed)}" if removed else "No expired grocery products found."


    # ... save Inventory in json file ...

    def save_to_file(self, filename):
        try:
           data = []
           for product in self._products:
               product_data = {
                   "type": product.__class__.__name__,
                   "product_id": product._product_id,
                   "name": product._name,
                   "price": product._price,
                   "quantity_in_stock": product._quantity_in_stock
               }
   
               if isinstance(product, Electronics):
                   product_data["warranty_years"] = product._warranty_years
                   product_data["brand"] = product._brand
               elif isinstance(product, Grocery):
                   product_data["expiry_date"] = product.expiry_date
               elif isinstance(product, Clothing):
                   product_data["size"] = product.size
                   product_data["material"] = product.material
   
               data.append(product_data)

           with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
             print("Error saving inventory to file:", e)

    def load_from_file(self, filename):
        try:
          with open(filename, 'r') as f:
            data = json.load(f)

          self._products = []

          for item in data:
            try:
                pType = item["type"]
                pid = item["product_id"]
                name = item["name"]
                price = item["price"]
                stock = item["quantity_in_stock"]

                if pType == "Electronics":
                    product = Electronics(pid, name, price, stock, item["warranty_years"], item["brand"])
                elif pType == "Grocery":
                    product = Grocery(pid, name, price, stock, item["expiry_date"])
                elif pType == "Clothing":
                    product = Clothing(pid, name, price, stock, item["size"], item["material"])
                else:
                    continue

                self._products.append(product)
            except Exception as e:
                print(f"Error loading a product: {e}")
        except FileNotFoundError:
            print(f"{filename} not found.")
        except json.JSONDecodeError:
           print(f"Error decoding JSON from {filename}.")
        except Exception as e:
            print("Unexpected error during loading inventory:", e)
   

#istance of class Inventory
inventory = Inventory()
def save_inventory():
    inventory.save_to_file("inventory.json")
    print("Inventory saved to file.")

def load_inventory():
    global inventory
    try:
        inventory.load_from_file("inventory.json")
        print("Inventory loaded from file.")
    except FileNotFoundError:
        print("No saved inventory found.")

# ---------------------- CLI Menu ----------------------
while True:
    print("\n--- Inventory Menu ---")
    print("1. Add Product")
    print("2. Sell Product")
    print("3. Search/View Product")
    print("4. Save Inventory")
    print("5. Load Inventory")
    print("6. Restock Product")
    print("7. Remove Expired Grocery Products")
    print("8. Show Total Inventory Value")
    print("9. Exit")

    choice = input("Enter your choice (1-9): ")

    try:
        if choice == "1":
            print("\na. Clothing\nb. Grocery\nc. Electronics")
            pType = input("Choose type: ").lower()

            try:
                pid = int(input("Product ID: "))
                name = input("Name: ")
                price = float(input("Price: "))
                stock = int(input("Quantity in stock: "))
            except ValueError:
                print("Invalid input type. Please enter correct data types.")
                continue

            try:
                if pType == "a":
                    size = input("Size: ")
                    material = input("Material: ")
                    product = Clothing(pid, name, price, stock, size, material)
                elif pType == "b":
                    expiry = input("Expiry Date (YYYY-MM-DD): ")
                    product = Grocery(pid, name, price, stock, expiry)
                elif pType == "c":
                    warranty = int(input("Warranty (in years): "))
                    brand = input("Brand: ")
                    product = Electronics(pid, name, price, stock, warranty, brand)
                else:
                    print("Invalid product type.")
                    continue
            except Exception as e:
                print("Error creating product:", e)
                continue

            print(inventory.add_product(product))

        elif choice == "2":
            try:
                pid = int(input("Enter Product ID to sell: "))
                qty = int(input("Enter quantity to sell: "))
                print(inventory.sell_product(pid, qty))
            except ValueError:
                print("Invalid input. Product ID and quantity must be numbers.")

        elif choice == "3":
            print("\na. Search by Name\nb. List All")
            sub = input("Choose option: ").lower()
            if sub == "a":
                name = input("Enter name to search: ")
                results = inventory.search_by_name(name)
                if isinstance(results, list):
                    for r in results:
                        print(r)
                else:
                    print(results)
            elif sub == "b":
                for p in inventory.list_all_products():
                    print(p)
            else:
                print("Invalid sub-choice.")

        elif choice == "4":
            try:
                save_inventory()
            except Exception as e:
                print("Failed to save inventory:", e)

        elif choice == "5":
            try:
                load_inventory()
            except Exception as e:
                print("Failed to load inventory:", e)

        elif choice == "6":
            try:
                pid = int(input("Enter Product ID to restock: "))
                qty = int(input("Enter quantity to restock: "))
                print(inventory.restock_product(pid, qty))
            except ValueError:
                print("Invalid input. Enter numeric values.")

        elif choice == "7":
            try:
                print(inventory.remove_expired_products())
            except Exception as e:
                print("Error removing expired products:", e)

        elif choice == "8":
            try:
                print(f"Total Inventory Value: {inventory.total_inventory_value()}")
            except Exception as e:
                print("Error calculating total inventory value:", e)

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")

    except Exception as e:
        print("An unexpected error occurred:", e)
