import tkinter as tk
from tkinter import ttk, messagebox
import data_manager
import validation

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

        # ---- Input form Section ------

        self.create_form()

        # Load data on startup
        self.refresh_table()

    def create_header(self):
        title_label = tk.Label(
            self.root, 
            text="CITY OF MERIDIAN  -  INTERNAL IT APPLICATION DIRECTORY", 
            bg="#F0F3F8", 
            fg="#111827", 
            font=("GeistMono", 13, "bold")
        )
        title_label.pack(fill=tk.X, anchor="center", padx=25, pady=(20, 15))

    def create_toolbar(self):
        toolbar_frame = tk.Frame(self.root, bg="#F0F3F8")
        toolbar_frame.pack(fill=tk.X, padx=25, pady=(0, 15))

        # Search Field
        search_frame = tk.Frame(toolbar_frame, bg="#F0F3F8")
        search_frame.pack(side=tk.TOP, anchor="w", pady=(0, 10))

        # Initialize StringVar for real-time search filtering
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_table)

        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Geist Mono", 9), 
        width=52, relief="solid", bd=1, fg="#9CA3AF")
        self.search_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=4)
        self.search_entry.insert(0, "🔍 Search Directory...")

        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)

        # Action Buttons Container
        button_frame = tk.Frame(toolbar_frame, bg="#F0F3F8")
        button_frame.pack(side=tk.TOP, anchor="w")

        # --- Edit Button with Guaranteed Square Corners ---
        edit_border_frame = tk.Frame(button_frame, bg="#111827", bd=0)
        edit_border_frame.pack(side=tk.LEFT, padx=(0, 10))

        self.edit_button = tk.Button(
            edit_border_frame, text="Edit Selected", 
            bg="white", fg="#111827", font=("Arial", 9), 
            relief="flat", bd=0, padx=12, pady=7,
            state=tk.DISABLED
        )
        self.edit_button.pack(padx=1, pady=1) # 1px padding creates the sharp border line

        # --- Delete Button with Guaranteed Square Red Corners ---
        delete_border_frame = tk.Frame(button_frame, bg="#D9534F", bd=0)
        delete_border_frame.pack(side=tk.LEFT)

        self.delete_button = tk.Button(
            delete_border_frame, text="Delete Selected", 
            bg="white", fg="#D9534F", font=("Arial", 9), 
            relief="flat", bd=0, padx=12, pady=7,
            state=tk.DISABLED
        )
        self.delete_button.pack(padx=1, pady=1) 

    def on_row_select(self, event):
        """Enables or disables edit/delete buttons based on whether a row is selected."""
        selected_items = self.tree.selection()
        if selected_items:
            self.edit_button.config(state=tk.NORMAL, cursor="hand2")
            self.delete_button.config(state=tk.NORMAL, cursor="hand2")
        else:
            self.edit_button.config(state=tk.DISABLED, cursor="")
            self.delete_button.config(state=tk.DISABLED, cursor="")

    def on_search_focus_in(self, event):
        if self.search_entry.get() == "🔍 Search Directory...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="#111827")  # Dark text for typing

    def on_search_focus_out(self, event):
        if not self.search_entry.get().strip():
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, "🔍 Search Directory...")
            self.search_entry.config(fg="#9CA3AF")  # Light gray placeholder color


    def create_table(self):
        # Outer wrapper frame to act as the solid black table border (#111827)
        table_outer_frame = tk.Frame(self.root, bg="#111827", bd=0)
        table_outer_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 10))

        # Inner container frame for the treeview and scrollbar
        table_frame = tk.Frame(table_outer_frame, bg="#F0F3F8")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)  # 1px padding reveals the black outer border

        style = ttk.Style()
        style.theme_use("clam")
        
        # Streamlined header configuration with reduced vertical padding for a precise height
        style.configure(
            "Treeview.Heading", 
            font=("Geist Mono", 12, "bold"), 
            background="#F9FAFB", 
            foreground="#111827", 
            anchor="w", 
            relief="flat", 
            borderwidth=0,
            padding=(10, 6)
        )
        
        style.configure(
            "Treeview", 
            font=("Geist Mono", 9), 
            rowheight=28, 
            background="white", 
            fieldbackground="white", 
            borderwidth=0, 
            relief="flat"
        )
        
        # Selected row highlight color matching Figma (#E0F2FE)
        style.map("Treeview", background=[('selected', '#E0F2FE')], foreground=[('selected', '#111827')])

        columns = ("app_name", "category", "business_owner", "app_url")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)

        self.tree.heading("app_name", text="APP NAME", anchor="w")
        self.tree.heading("category", text="CATEGORY", anchor="w")
        self.tree.heading("business_owner", text="BUSINESS OWNER", anchor="w")
        self.tree.heading("app_url", text="APP URL / LINK", anchor="w")

       # Define exact column widths that fill the container width proportionally (~1000px total)
        self.tree.column("app_name", width=250, minwidth=200, anchor="w")
        self.tree.column("category", width=180, minwidth=140, anchor="w")
        self.tree.column("business_owner", width=250, minwidth=200, anchor="w")
        self.tree.column("app_url", width=320, minwidth=250, anchor="w")

        # Force geometry propagation update immediately after packing
        self.tree.update_idletasks()

        # --- CONFIGURE ALTERNATE ROW TAGS ---
        self.tree.tag_configure("evenrow", background="#FFFFFF")  # Pure white
        self.tree.tag_configure("oddrow", background="#F3F4F6")   # Noticeable light gray tint

        # Pack treeview to fill the inner frame
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar placed specifically to start below the header section
        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview, width=12, bg="#F9FAFB", 
        troughcolor="#F3F4F6", activebackground="#D1D5DB", relief="flat", bd=0)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Position scrollbar flush against the absolute right edge (x=0) starting below the header (y=30)
        scrollbar.place(relx=1.0, x=0, y=30, relheight=1.0, height=-30, anchor="ne")

        # --- DEDICATED BOTTOM HEADER BORDER LINE ---
        header_border = tk.Frame(table_frame, bg="#111827", height=1)
        header_border.place(in_=self.tree, relx=0, rely=0, y=30, relwidth=1, anchor="nw")

        # Status Label matching Figma format
        self.status_label = tk.Label(self.root, text="Showing 0 entries of 0", bg="#F0F3F8", fg="#6B7280", font=("Geist Mono", 8))
        self.status_label.pack(anchor="w", padx=25, pady=(4, 10))

        # --- BIND ROW SELECTION EVENT ---
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)


    def _create_field(self, parent, label_text, placeholder, row, col, padx_val=(0, 0)):
        # 1. Label
        tk.Label(parent, text=label_text, bg="#F0F3F8", font=("Geist Mono", 8, "bold")).grid(
            row=row, column=col, sticky="w", pady=(0, 2)
        )
        
        # 2. Entry Field
        entry = tk.Entry(parent, font=("Geist Mono", 9), relief="solid", bd=1, fg="#9CA3AF", highlightthickness=0)
        entry.insert(0, placeholder)
        
        # 3. Dynamic Focus Handlers using lambda
        # Bind focus events cleanly
        entry.bind("<FocusIn>", self.on_field_focus_in)
        entry.bind("<FocusOut>", lambda e, p=placeholder: self.on_field_focus_out(e, p))
        
        # 4. Grid Placement (row + 1 because label is at 'row')
        entry.grid(row=row+1, column=col, padx=padx_val, pady=(0, 10 if row == 1 else 15), sticky="ew", ipady=4)
        return entry

    def on_field_focus_in(self, event):
        """Wipes the field clean if it is currently displaying placeholder text (gray color)."""
        widget = event.widget
        if widget.cget("fg").lower() == "#9CA3AF":
            widget.delete(0, tk.END)
            widget.config(fg="#111827")  # Switch to dark typing color

    def on_field_focus_out(self, event, placeholder):
        """Restores the placeholder if the user left the field completely empty."""
        widget = event.widget
        if not widget.get().strip():
            widget.delete(0, tk.END)
            widget.insert(0, placeholder)
            widget.config(fg="#9CA3AF")

    def create_required_label(self, parent, text):
        #Helper to create a field label with a red asterisk.
        label_frame = tk.Frame(parent, bg="#F0F3F8")  # Matches form background
        
    

        # Main label text
        tk.Label(
            label_frame, 
            text=text + " ",
            font=("Geist Mono", 9, "bold"), 
            fg="#111827", 
            bg="#F0F3F8"
        ).pack(side=tk.LEFT)
        
        # Red asterisk
        tk.Label(
            label_frame, 
            text="*", 
            font=("Geist Mono", 9, "bold"), 
            fg="#EF4444",  # Red accent matching your delete button style
            bg="#F0F3F8"
        ).pack(side=tk.LEFT)
        
        return label_frame

    def _create_field(self, parent, label_text, placeholder, row, col, padx_val=(0, 0)):
        """Helper to create the full form field container, label with red asterisk, and placeholder entry."""
        field_container = tk.Frame(parent, bg="#F0F3F8")
        field_container.grid(row=row, column=col, sticky="ew", padx=padx_val, pady=(0, 12))
        field_container.grid_columnconfigure(0, weight=1)

        # Use the required label helper for the label portion
        self.create_required_label(field_container, label_text).pack(anchor="w", pady=(0, 4))

        # Entry widget with placeholder behavior
        entry = tk.Entry(field_container, font=("Geist Mono", 9), relief="solid", bd=1, fg="#9CA3AF")
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: (entry.get() == placeholder and (entry.delete(0, tk.END), entry.config(fg="#111827"))))
        entry.bind("<FocusOut>", lambda e: (not entry.get() and (entry.insert(0, placeholder), entry.config(fg="#9CA3AF"))))
        entry.pack(fill=tk.X, ipady=3)
        
        return entry

    def create_form(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Explicit style configuration for the Save button (Solid Black)
        style.configure("Black.TButton", background="#111827", foreground="#FFFFFF", borderwidth=1,
            focusthickness=3, focuscolor="none", padding=9, font=("Geist Mono", 9)
        )
        style.map("Black.TButton", background=[("active", "#1F2937")])

        style.configure("White.TButton", background="#FFFFFF", foreground="#111827", borderwidth=1,
            bordercolor="#111827", focusthickness=3, focuscolor="none", padding=6
        )
        style.map("White.TButton", background=[("active", "#F3F4F6")])

        form_frame = tk.Frame(self.root, bg="#F0F3F8", relief="solid", bd=1, padx=20, pady=15)
        form_frame.pack(fill=tk.X, padx=25, pady=(0, 20))

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        title_label = tk.Label(form_frame, text="Application Details", bg="#F0F3F8", fg="#111827", font=("Geist Mono", 10, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

       # Row 1 & 2: App Name & Category
        self.app_name_entry = self._create_field(form_frame, "App Name", "Enter app name...", row=1, col=0, padx_val=(0, 20))
        self.category_entry = self._create_field(form_frame, "Category", "Select category...", row=1, col=1)

        # Row 3 & 4: Business Owner & App URL
        self.owner_entry = self._create_field(form_frame, "Business Owner", "Enter owner name...", row=3, col=0, padx_val=(0, 20))
        self.url_entry = self._create_field(form_frame, "App URL", "https://...", row=3, col=1)

        # Row 5: Action Button Frame
        action_button_frame = tk.Frame(form_frame, bg="#F0F3F8")
        action_button_frame.grid(row=5, column=0, columnspan=2, sticky="w", pady=(5, 0))

        self.save_button = ttk.Button(action_button_frame, text="Save", style="Black.TButton", command=self.save_record)
        self.save_button.pack(side=tk.LEFT, padx=(0, 8))

        # Clear button wrapped in a border frame to match your delete/edit style
        clear_border_frame = tk.Frame(action_button_frame, bg="#D1D5DB", bd=1, relief="solid")
        clear_border_frame.pack(side=tk.LEFT)

        self.clear_button = tk.Button(
            clear_border_frame, text="Clear", 
            bg="#FFFFFF", fg="#111827", font=("Geist Mono", 9), 
            relief="flat", bd=0, padx=16, pady=6, 
            cursor="hand2", command=self.clear_form
        )
        self.clear_button.pack(padx=1, pady=1)
    
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Load rows from applications.csv and save globally for filtering counts
        self.all_apps_data = data_manager.load_applications()
        
        for index, app in enumerate(self.all_apps_data):
            padded_app = [f"  {item}" for item in app]
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=padded_app, tags=(tag,))
        
        self.all_tree_items = self.tree.get_children()
        
        total_count = len(self.all_apps_data)
        self.status_label.config(text=f"Showing {total_count} entries of {total_count}")

    def show_custom_message(self, title, message):
        """A compact, beginner-friendly custom popup window."""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("320x160")
        dialog.resizable(False, False)
        dialog.configure(bg="#FFFFFF")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the popup relative to the main application window
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (320 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (160 // 2)
        dialog.geometry(f"+{x}+{y}")

        # Message Label
        tk.Label(dialog, text=message, bg="#FFFFFF", fg="#111827", font=("Geist Mono", 9), wraplength=280).pack(pady=(30, 15), expand=False)

        # OK Button to close (Single pack call!)
        tk.Button(dialog, text="OK", bg="#E5E7EB", fg="#111827", font=("Geist Mono", 9), 
        command=dialog.destroy, padx=20, pady=5).pack(pady=(0, 20), expand=False)

        self.root.wait_window(dialog)

    def save_record(self):
        app_name = self.app_name_entry.get().strip()
        category = self.category_entry.get().strip()
        owner = self.owner_entry.get().strip()
        url = self.url_entry.get().strip()

        # --- Use validation module ---
        is_valid, error_msg = validation.validate_app_input(app_name, category, owner, url)
        if not is_valid:
            self.show_custom_message("Validation Error", error_msg)
            return

        # --- Format URL via validation module ---
        url = validation.format_url(url)

        apps = data_manager.load_applications()

        if getattr(self, "selected_item_id", None) is not None:
            index = self.selected_item_id
            if 0 <= index < len(apps):
                apps[index] = [app_name, category, owner, url]
            self.selected_item_id = None
            self.save_button.config(text="Save")
        else:
            apps.append([app_name, category, owner, url])

        data_manager.save_all_applications(apps)
        self.refresh_table()
        self.clear_form()
        
        self.show_custom_message("Success", "Application record saved successfully.")

    def clear_form(self):
        """Resets all form fields back to their default placeholder states and resets selection state."""
        fields_data = [
            (self.app_name_entry, "Enter app name..."),
            (self.category_entry, "Select category..."),
            (self.owner_entry, "Enter owner name..."),
            (self.url_entry, "https://...")
        ]
        
        for entry, placeholder in fields_data:
            entry.delete(0, tk.END)
            entry.insert(0, placeholder)
            entry.icursor(0)
            entry.config(fg="#9CA3AF")
            
        self.selected_item_id = None
        self.save_button.config(text="Save")

    def filter_table(self, *args):
        """Instantly filters rows using the master item list and updates the count."""
        if not hasattr(self, "tree") or not hasattr(self, "all_tree_items"):
            return

        query = self.search_var.get().lower().strip()
        is_empty = (not query or query == "🔍 search directory...")

        visible_count = 0
        total_count = len(self.all_tree_items)

        for item in self.all_tree_items:
            if not self.tree.exists(item):
                continue
                
            values = self.tree.item(item, "values")
            
            if is_empty or any(query in str(cell).lower() for cell in values):
                self.tree.reattach(item, "", tk.END)
                visible_count += 1
            else:
                self.tree.detach(item)

        # Update the status label dynamically based on search results
        if is_empty:
            self.status_label.config(text=f"Showing {total_count} entries of {total_count}")
        else:
            self.status_label.config(text=f"Showing {visible_count} entries of {total_count} (filtered)")