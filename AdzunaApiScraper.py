import tkinter as tk
from tkinter import messagebox, ttk, filedialog, StringVar
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Global variable to store current jobs
current_jobs = []

# ----- API Functions -----
def get_adzuna_jobs(app_id, api_key, search_term="python", location="UK"):
    """Fetch jobs from Adzuna API."""
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id}&app_key={api_key}&what={search_term}&where={location}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        jobs = data.get('results', [])
        return jobs
    except Exception as e:
        print("Adzuna API error:", e)
        return []

# ----- Save/Export Functions -----
def save_to_json():
    """Save current jobs to JSON file."""
    if not current_jobs:
        messagebox.showwarning("Warning", "No jobs to save")
        return
    
    filename = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if filename:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(current_jobs, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Success", f"Saved {len(current_jobs)} jobs to {filename}")

# ----- GUI Functions -----
def on_table_click(event):
    """Open job link when table row is double-clicked."""
    item = table.identify_row(event.y)
    if item:
        values = table.item(item, "values")
        if len(values) > 4:  # Ensure link exists
            url = values[4]
            if url.startswith("http"):
                import webbrowser
                webbrowser.open(url)

def fetch_jobs():
    """Fetch jobs from Adzuna API and populate table."""
    global current_jobs
    
    search_term = search_entry.get() or "python"
    location = location_entry.get() or "UK"
    
    app_id = os.getenv("ADZUNA_APP_ID")
    api_key = os.getenv("ADZUNA_API_KEY")
    
    if not app_id or not api_key:
        messagebox.showerror("Error", "API credentials not found in .env file")
        return
    
    # Clear table
    for item in table.get_children():
        table.delete(item)
    
    jobs = get_adzuna_jobs(app_id, api_key, search_term, location)
    
    if jobs:
        current_jobs = jobs
        for job in jobs[:100]:  # Limit display to first 100
            title = job.get('title', 'N/A')
            company = job.get('company', {}).get('display_name', 'N/A')
            location_name = job.get('location', {}).get('display_name', 'N/A')
            salary = job.get('salary_max', job.get('salary_min', 'Not specified'))
            link = job.get('redirect_url', '')
            
            table.insert('', 'end', values=(title, company, location_name, salary, link))
        
        save_button.config(state="normal")
        messagebox.showinfo("Success", f"Fetched {len(jobs)} jobs")
    else:
        messagebox.showerror("Error", "Failed to fetch jobs. Check your API credentials.")

# ----- GUI Setup -----
root = tk.Tk()
root.title("Adzuna Job Scraper")
root.geometry("1200x600")

# Control Panel
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

tk.Label(control_frame, text="Search Term:").grid(row=0, column=0, sticky="e", padx=5)
search_entry = tk.Entry(control_frame, width=30)
search_entry.grid(row=0, column=1, padx=5)
search_entry.insert(0, "python")

tk.Label(control_frame, text="Location:").grid(row=0, column=2, sticky="e", padx=5)
location_entry = tk.Entry(control_frame, width=30)
location_entry.grid(row=0, column=3, padx=5)
location_entry.insert(0, "UK")

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Fetch Jobs", command=fetch_jobs, bg="green", fg="white", padx=15, pady=5).pack(side=tk.LEFT, padx=5)
save_button = tk.Button(button_frame, text="Save JSON", command=save_to_json, bg="blue", fg="white", padx=15, pady=5, state="disabled")
save_button.pack(side=tk.LEFT, padx=5)

# Results Table
columns = ("Title", "Company", "Location", "Salary", "Link")
table = ttk.Treeview(root, columns=columns, show='headings', height=20)

for col in columns:
    width = 300 if col == "Title" else (200 if col in ["Company", "Location"] else 100)
    table.column(col, width=width)
    table.heading(col, text=col)

# Add scrollbars
vsb = ttk.Scrollbar(root, orient=tk.VERTICAL, command=table.yview)
hsb = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=table.xview)
table.configure(yscroll=vsb.set, xscroll=hsb.set)

table.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
vsb.grid(row=2, column=1, sticky='ns')
hsb.grid(row=3, column=0, sticky='ew')

root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# Bind double-click to open links
table.bind("<Double-1>", on_table_click)

root.mainloop()
