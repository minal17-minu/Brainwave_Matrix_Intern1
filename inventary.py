import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Create a database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='programmer@123',
    database='inventory'
)
cursor = conn.cursor()

# Create tables if they do not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        quantity INT NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    )
''')

conn.commit()

class InventorySystem:
    def __init__(self, root):
        self.root = root
        self.root.title('Inventory Management System')
        self.root.geometry('800x600')
        self.root.config(bg='#e0f7fa')

        # Style configuration
        style = ttk.Style()
        style.configure('TFrame', background='#80deea')
        style.configure('TLabel', background='#80deea', font=('Arial', 12))
        style.configure('TButton', background='#26c6da', font=('Arial', 12), relief='raised')

        # Login frame
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(pady=100, padx=20)

        ttk.Label(self.login_frame, text='Username').grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.login_frame, text='Password').grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = ttk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.login_frame, text='Login', command=self.login).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        user = cursor.fetchone()

        if user:
            self.login_frame.pack_forget()
            self.main_menu()
        else:
            messagebox.showerror('Invalid Credentials', 'Invalid username or password')

    def main_menu(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(pady=100)

        ttk.Button(self.main_frame, text='Add Product', command=self.add_product).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(self.main_frame, text='Edit Product', command=self.edit_product).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.main_frame, text='Delete Product', command=self.delete_product).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(self.main_frame, text='Track Inventory', command=self.track_inventory).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(self.main_frame, text='Generate Reports', command=self.generate_reports).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(self.main_frame, text='Logout', command=self.logout).grid(row=1, column=2, padx=10, pady=10)

    def add_product(self):
        self.main_frame.pack_forget()
        self.add_frame = ttk.Frame(self.root)
        self.add_frame.pack(pady=100)

        ttk.Label(self.add_frame, text='Product Name').grid(row=0, column=0, padx=10, pady=10)
        self.product_name_entry = ttk.Entry(self.add_frame)

        self.product_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.add_frame, text='Quantity').grid(row=1, column=0, padx=10, pady=10)
        self.quantity_entry = ttk.Entry(self.add_frame)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.add_frame, text='Price').grid(row=2, column=0, padx=10, pady=10)
        self.price_entry = ttk.Entry(self.add_frame)
        self.price_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(self.add_frame, text='Add', command=self.add_product_to_db).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        ttk.Button(self.add_frame, text='Back', command=self.back_to_main).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def add_product_to_db(self):
        product_name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if product_name and quantity and price:
            try:
                quantity = int(quantity)
                price = float(price)
                cursor.execute('INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)', (product_name, quantity, price))
                conn.commit()
                messagebox.showinfo('Product Added', 'Product added successfully')
                self.add_frame.pack_forget()
                self.main_menu()
            except ValueError:
                messagebox.showerror('Invalid Input', 'Quantity and price must be numbers')
        else:
            messagebox.showerror('Invalid Input', 'All fields are required')

    def edit_product(self):
        self.main_frame.pack_forget()
        self.edit_frame = ttk.Frame(self.root)
        self.edit_frame.pack(pady=100)

        ttk.Label(self.edit_frame, text='Product ID').grid(row=0, column=0, padx=10, pady=10)
        self.product_id_entry = ttk.Entry(self.edit_frame)
        self.product_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(self.edit_frame, text='Get Product', command=self.get_product_to_edit).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def get_product_to_edit(self):
        product_id = self.product_id_entry.get()

        if product_id:
            try:
                product_id = int(product_id)
                cursor.execute('SELECT * FROM products WHERE id=%s', (product_id,))
                product = cursor.fetchone()

                if product:
                    self.edit_frame.pack_forget()
                    self.edit_product_frame = ttk.Frame(self.root)
                    self.edit_product_frame.pack(pady=100)

                    ttk.Label(self.edit_product_frame, text='Product Name').grid(row=0, column=0, padx=10, pady=10)
                    self.product_name_entry_to_edit = ttk.Entry(self.edit_product_frame)
                    self.product_name_entry_to_edit.insert(0, product[1])
                    self.product_name_entry_to_edit.grid(row=0, column=1, padx=10, pady=10)

                    ttk.Label(self.edit_product_frame, text='Quantity').grid(row=1, column=0, padx=10, pady=10)
                    self.quantity_entry_to_edit = ttk.Entry(self.edit_product_frame)
                    self.quantity_entry_to_edit.insert(0, product[2])
                    self.quantity_entry_to_edit.grid(row=1, column=1, padx=10, pady=10)

                    ttk.Label(self.edit_product_frame, text='Price').grid(row=2, column=0, padx=10, pady=10)
                    self.price_entry_to_edit = ttk.Entry(self.edit_product_frame)
                    self.price_entry_to_edit.insert(0, product[3])
                    self.price_entry_to_edit.grid(row=2, column=1, padx=10, pady=10)

                    ttk.Button(self.edit_product_frame, text='Save Changes', command=lambda: self.save_changes_to_product(product_id)).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
                else:
                    messagebox.showerror('Product Not Found', 'Product not found')
            except ValueError:
                messagebox.showerror('Invalid Input', 'Product ID must be a number')
        else:
            messagebox.showerror('Invalid Input', 'Product ID is required')

    def save_changes_to_product(self, product_id):
        product_name = self.product_name_entry_to_edit.get()
        quantity

        quantity = self.quantity_entry_to_edit.get()
        price = self.price_entry_to_edit.get()

        if product_name and quantity and price:
            try:
                quantity = int(quantity)
                price = float(price)
                cursor.execute('UPDATE products SET name=%s, quantity=%s, price=%s WHERE id=%s', (product_name, quantity, price, product_id))
                conn.commit()
                messagebox.showinfo('Changes Saved', 'Changes saved successfully')
                self.edit_product_frame.pack_forget()
                self.main_menu()
            except ValueError:
                messagebox.showerror('Invalid Input', 'Quantity and price must be numbers')
        else:
            messagebox.showerror('Invalid Input', 'All fields are required')

    def delete_product(self):
        self.main_frame.pack_forget()
        self.delete_frame = ttk.Frame(self.root)
        self.delete_frame.pack(pady=100)

        ttk.Label(self.delete_frame, text='Product ID').grid(row=0, column=0, padx=10, pady=10)
        self.product_id_entry_to_delete = ttk.Entry(self.delete_frame)
        self.product_id_entry_to_delete.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(self.delete_frame, text='Delete', command=self.delete_product_from_db).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def delete_product_from_db(self):
        product_id = self.product_id_entry_to_delete.get()

        if product_id:
            try:
                product_id = int(product_id)
                cursor.execute('SELECT * FROM products WHERE id=%s', (product_id,))
                product = cursor.fetchone()

                if product:
                    cursor.execute('DELETE FROM products WHERE id=%s', (product_id,))
                    conn.commit()
                    messagebox.showinfo('Product Deleted', 'Product deleted successfully')
                    self.delete_frame.pack_forget()
                    self.main_menu()
                else:
                    messagebox.showerror('Product Not Found', 'Product not found')
            except ValueError:
                messagebox.showerror('Invalid Input', 'Product ID must be a number')
        else:
            messagebox.showerror('Invalid Input', 'Product ID is required')

    def track_inventory(self):
        self.main_frame.pack_forget()
        self.track_frame = ttk.Frame(self.root)
        self.track_frame.pack(pady=100)

        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()

        for widget in self.track_frame.winfo_children():
            widget.destroy()

        for i, product in enumerate(products):
            ttk.Label(self.track_frame, text=f'Product ID: {product[0]}').grid(row=i, column=0, padx=10, pady=10)
            ttk.Label(self.track_frame, text=f'Product Name: {product[1]}').grid(row=i, column=1, padx=10, pady=10)
            ttk.Label(self.track_frame, text=f'Quantity: {product[2]}').grid(row=i, column=2, padx=10, pady=10)
            ttk.Label(self.track_frame, text=f'Price: {product[3]}').grid(row=i, column=3, padx=10, pady=10)

        ttk.Button(self.track_frame, text='Back', command=self.back_to_main).grid(row=len(products), column=0, columnspan=4, padx=10, pady=10)

    def generate_reports(self):
        self.main_frame.pack_forget()
        self.report_frame = ttk.Frame(self.root)
        self.report_frame.pack(pady=100)

        cursor.execute('SELECT * FROM products WHERE quantity < 10')
        low_stock_products = cursor.fetchall()

        for widget in self.report_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.report_frame, text='Low Stock Products:', font=('Arial', 14, 'bold')).grid(row=0, column=0, padx=10, pady=10)

        for i, product in enumerate(low_stock_products):
            ttk.Label(self.report_frame, text=f'Product ID: {product[0]}').grid(row=i+1, column=0, padx=10, pady=10)
            ttk.Label(self.report_frame, text=f'Product Name: {product[1]}').grid(row=i+1, column=1, padx=10, pady=10)
            ttk.Label(self.report_frame, text=f'Quantity: {product[2]}').grid(row=i+1, column=2, padx=10, pady=10)
            ttk.Label(self.report_frame, text=f'Price: {product[3]}').grid(row=i+1, column=3, padx=10, pady=10)

        ttk.Button(self.report_frame, text='Back', command=self.back_to_main).grid(row=len(low_stock_products) + 1, column=0, columnspan=4, padx=10, pady=10)

    def logout(self):
        self.main_frame.pack_forget()
        self.login_frame.pack(pady=100)

    def back_to_main(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.main_menu()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = InventorySystem(tk.Tk())
    app.run()