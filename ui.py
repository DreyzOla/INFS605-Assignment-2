import tkinter as tk
from tkinter import ttk, messagebox

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
