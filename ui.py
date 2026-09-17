import tkinter as tk
from tkinter import ttk, messagebox
import data_manager

class ApplicationDirectory:
    def __init__(self, root):
        self.root = root

        self.root.title("CITY OF MERIDIAN - INTERNAL IT APPLICATION DIRECTORY")
        self.root.geometry("1100x650")
        self.root.configure(bg="#F0F3F8")

        # --- Header Section ---
        self.create_header()

        # --- Search & Actions Toolbar ---
        self.create_toolbar()

        # --- Table Section ---
        self.create_table()

        # Load data on startup
        self.refresh_table()

    def create_header(self):
        title_label = tk.Label(
            self.root, 
            text="CITY OF MERIDIAN  -  INTERNAL IT APPLICATION DIRECTORY", 
            bg="#F0F3F8", 
            fg="#111827", 
            font=("Geist Mono", 13, "bold")
        )
        title_label.pack(fill=tk.X, anchor="center", padx=25, pady=(20, 15))

    def create_toolbar(self):
        toolbar_frame = tk.Frame(self.root, bg="#F0F3F8")
        toolbar_frame.pack(fill=tk.X, padx=25, pady=(0, 15))

        # Search Field
        search_frame = tk.Frame(toolbar_frame, bg="#F0F3F8")
        search_frame.pack(side=tk.TOP, anchor="w", pady=(0, 10))

        self.search_entry = tk.Entry(search_frame, font=("Geist Mono", 13), width=35, relief="solid", bd=1)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 15))
        self.search_entry.insert(0, "🔍 Search Directory...")

        # Action Buttons
        button_frame = tk.Frame(toolbar_frame, bg="#F0F3F8")
        button_frame.pack(side=tk.TOP, anchor="w")

        self.edit_button = tk.Button(
            button_frame, text="Edit Selected", 
            bg="white", fg="#111827", font=("Geist Mono", 9), relief="solid", bd=1, padx=12, pady=4
        )
        self.edit_button.pack(side=tk.LEFT, padx=(0, 10))

        self.delete_button = tk.Button(
            button_frame, text="Delete Selected", 
            bg="white", fg="#D9534F", font=("Geist Mono", 9), relief="solid", bd=1, padx=12, pady=4
        )
        self.delete_button.pack(side=tk.LEFT)


    def create_table(self):
        table_frame = tk.Frame(self.root, bg="#F0F3F8")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 10))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Geist Mono", 9, "bold"), background="#E5E7EB", foreground="#111827", anchor="w", relief="flat")
        style.configure("Treeview", font=("Geist Mono", 9), rowheight=28)

        columns = ("app_name", "category", "business_owner", "app_url")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)

        self.tree.heading("app_name", text="  APP NAME", anchor="w")
        self.tree.heading("category", text="  CATEGORY", anchor="w")
        self.tree.heading("business_owner", text="  BUSINESS OWNER", anchor="w")
        self.tree.heading("app_url", text="  APP URL / LINK", anchor="w")

        self.tree.column("app_name", width=200, anchor="w")
        self.tree.column("category", width=180, anchor="w")
        self.tree.column("business_owner", width=220, anchor="w")
        self.tree.column("app_url", width=250, anchor="w")

        # Scrollbar attached neatly inside the frame
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Status Label matching Figma format
        self.status_label = tk.Label(self.root, text="Showing 0 entries of 0", bg="#F0F3F8", fg="#6B7280", font=("Geist Mono", 8))
        self.status_label.pack(anchor="w", padx=25, pady=(4, 10))

    def refresh_table(self):
        # Clear existing table rows
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Load rows from applications.csv
        apps = data_manager.load_applications()
        for app in apps:
            # Pad values with leading spaces for clean indent alignment
            padded_app = [f"  {item}" for item in app]
            self.tree.insert("", tk.END, values=padded_app)
        
        # Update entry counter label
        total_count = len(apps)
        self.status_label.config(text=f"Showing {total_count} entries of {total_count}")