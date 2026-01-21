import tkinter as tk
from tkinter import messagebox, ttk
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ----- API Functions -----
def get_adzuna_jobs(app_id, api_key, search_term="python", location="UK"):
    """Fetch total jobs from Adzuna API."""
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id}&app_key={api_key}&what={search_term}&where={location}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('count', 0)
    except Exception as e:
        print("Adzuna API error:", e)
        return None

# ----- GUI Functions -----
def show_results_window(results_list):
    """Display results in a new window with a table."""
    results_window = tk.Toplevel(root)
    results_window.title("Job Search Results")
    results_window.geometry("600x400")
    
    # Title
    title = tk.Label(results_window, text="Job Search Results", font=("Arial", 14, "bold"))
    title.pack(pady=10)
    
    # Create Treeview (table)
    columns = ("Search Term", "Location", "Total Jobs")
    tree = ttk.Treeview(results_window, columns=columns, height=15, show="headings")
    
    for col in columns:
        tree.column(col, width=180)
        tree.heading(col, text=col)
    
    # Add data rows
    for result in results_list:
        tree.insert("", tk.END, values=(result["search_term"], result["location"], result["count"]))
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(results_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Close button
    tk.Button(results_window, text="Close", command=results_window.destroy).pack(pady=10)

def fetch_jobs():
    search_term = search_entry.get() or "python"
    location = location_entry.get() or "UK"
    
    app_id = os.getenv("ADZUNA_APP_ID")
    api_key = os.getenv("ADZUNA_API_KEY")
    
    if not app_id or not api_key:
        messagebox.showerror("Error", "API credentials not found in .env file")
        return

    adzuna_total = get_adzuna_jobs(app_id, api_key, search_term, location)
    
    if adzuna_total is not None:
        results = [{"search_term": search_term, "location": location, "count": adzuna_total}]
        show_results_window(results)
    else:
        messagebox.showerror("Error", "Failed to fetch jobs. Check your API credentials.")

# ----- GUI Setup -----
root = tk.Tk()
root.title("Job Scraper GUI")

# Search Term & Location
tk.Label(root, text="Search Term:").grid(row=0, column=0, sticky="e")
search_entry = tk.Entry(root, width=40)
search_entry.grid(row=0, column=1)

tk.Label(root, text="Location:").grid(row=1, column=0, sticky="e")
location_entry = tk.Entry(root, width=40)
location_entry.grid(row=1, column=1)

# Fetch Button
tk.Button(root, text="Fetch Total Jobs", command=fetch_jobs).grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
