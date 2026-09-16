"""
main.py
City of Meridian - IT Application Directory
Entry point for launching the Tkinter application.
"""

import tkinter as tk
from ui import ApplicationDirectory

def main():
    root = tk.Tk()
    app = ApplicationDirectory(root)
    root.mainloop()

if __name__ == "__main__":
    main()
