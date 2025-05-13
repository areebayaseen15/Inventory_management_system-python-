

🛒 Inventory Management System
This is a Python-based Inventory Management System using Object-Oriented Programming principles like abstraction, inheritance, encapsulation, and polymorphism. It includes a CLI interface to manage different types of products like Electronics, Grocery, and Clothing.

📁 Project Structure
```pgsql

├── inventory_management.py
├── inventory.json
└── README.md
```
📌 Features
Abstract Base Class: Product with shared functionality

Subclasses: Electronics, Grocery, Clothing with unique attributes

Class: Inventory to manage a collection of products

Save and load inventory to/from a JSON file

CLI Menu to interact with the inventory

🧱 Product Classes
🔹 Product (Abstract Base Class)
Common attributes:
```
product_id

name

price

quantity_in_stock

Common methods:

restock(amount)

sell(quantity)

get_total_value()

__str__()

display_info() (abstract)
```

🔹 Electronics
Extra attributes: warranty_years, brand

🔹 Grocery
Extra attribute: expiry_date

Extra method: is_expired()

🔹 Clothing
Extra attributes: size, material

🏪 Inventory Class
Handles all products using a list and supports:

Add/Remove product

Search by name or type

Restock/Sell products

Remove expired grocery items

List all products

Calculate total inventory value

Save/load inventory from JSON file

💻 CLI Menu Options
markdown
Copy
Edit
1. Add Product
2. Sell Product
3. Search/View Product
4. Save Inventory
5. Load Inventory
6. Restock Product
7. Remove Expired Grocery Products
8. Show Total Inventory Value
9. Exit
💾 File Persistence
Inventory is saved and loaded from a file named inventory.json in JSON format.

🛠 How to Run
Make sure you have Python installed.

Open terminal/command prompt.

Run the script:

python inventory_management.py
📎 Example Usage
Adding a Product:

Choose type: a (for Clothing)
Product ID: 101
Name: T-shirt
Price: 15.99
Quantity: 20
Size: M
Material: Cotton
Saving Inventory:

Option 4 → Save Inventory
📚 Concepts Used
Object-Oriented Programming (OOP)

Abstract Classes (abc)

Inheritance & Polymorphism

JSON file handling

CLI-based user interaction

👩‍💻 Author
Areeba Yaseen
📍 Certified Applied for Cloud Native for Artificial Intelligence
🔗 LinkedIn | GitHub
