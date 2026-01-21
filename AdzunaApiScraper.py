import tkinter as tk
from tkinter import messagebox, ttk, filedialog, StringVar
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Global variable to store current jobs
current_jobs = []
sort_reverse = False

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
        if len(values) > 2:  # Ensure link exists (it's in column index 2 - "Link")
            # Get all values: (Date, Score, Category, Title, Company, Location, Type, Rate, Skills, Applied, Link)
            link = values[-1]  # Link is the last column
            if link.startswith("http"):
                import webbrowser
                webbrowser.open(link)

# TODO: Implement sorting functionality for table columns
def sort_table(col):
    """Sort table by column (TODO: implement full sort)."""
    pass

# TODO: Check date filtering and sorting implementation
def filter_by_date():
    """Filter jobs by date (TODO: implement date filtering)."""
    pass

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
        for idx, job in enumerate(jobs[:100], 1):  # Limit display to first 100
            # Get job details
            date_str = job.get('created', datetime.now().isoformat())[:10]  # TODO: Check date extraction
            title = job.get('title', 'N/A')
            company = job.get('company', {}).get('display_name', 'N/A')
            location_name = job.get('location', {}).get('display_name', 'N/A')
            salary_max = job.get('salary_max', 0)
            salary_min = job.get('salary_min', 0)
            salary_str = f"£{salary_max:,.0f}" if salary_max else "N/A"
            job_type = job.get('contract_type', 'N/A')
            link = job.get('redirect_url', '')
            
            # Insert with all columns matching smart_ai_job_system.py structure
            # (Date, Title, Company, Location, Type, Salary, Link)
            table.insert('', 'end', values=(
                date_str,      # Date
                title,         # Title
                company,       # Company
                location_name, # Location
                job_type,      # Type
                salary_str,    # Salary
                link           # Link (hidden from display but used for opening)
            ))
        
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
control_frame.pack(pady=10, fill=tk.X, padx=10)

tk.Label(control_frame, text="Search Term:").pack(side=tk.LEFT, padx=5)
search_entry = tk.Entry(control_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)
search_entry.insert(0, "python")

tk.Label(control_frame, text="Location:").pack(side=tk.LEFT, padx=5)
location_entry = tk.Entry(control_frame, width=30)
location_entry.pack(side=tk.LEFT, padx=5)
location_entry.insert(0, "UK")

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Fetch Jobs", command=fetch_jobs, bg="green", fg="white", padx=15, pady=5).pack(side=tk.LEFT, padx=5)
save_button = tk.Button(button_frame, text="Save JSON", command=save_to_json, bg="blue", fg="white", padx=15, pady=5, state="disabled")
save_button.pack(side=tk.LEFT, padx=5)

# Results Table with scrollbars (matching smart_ai_job_system.py structure)
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tree_scroll = ttk.Scrollbar(table_frame)
tree_scroll.pack(side='right', fill='y')

table = ttk.Treeview(table_frame, yscrollcommand=tree_scroll.set, selectmode='browse')
table.pack(side='left', fill='both', expand=True)
tree_scroll.config(command=table.yview)

# Define columns matching smart_ai_job_system.py
table['columns'] = ('Date', 'Title', 'Company', 'Location', 'Type', 'Salary', 'Link')

# Column definitions
table.column('#0', width=50, minwidth=50)
table.column('Date', width=70, minwidth=60)
table.column('Title', width=250, minwidth=200)
table.column('Company', width=150, minwidth=100)
table.column('Location', width=150, minwidth=100)
table.column('Type', width=100, minwidth=80)
table.column('Salary', width=100, minwidth=80)
table.column('Link', width=0, stretch=False)  # Hidden column for job link

# Headings
table.heading('#0', text='#', anchor=tk.W)
table.heading('Date', text='Date', anchor=tk.W)
table.heading('Title', text='Job Title', anchor=tk.W)
table.heading('Company', text='Company', anchor=tk.W)
table.heading('Location', text='Location', anchor=tk.W)
table.heading('Type', text='Type', anchor=tk.W)
table.heading('Salary', text='Salary', anchor=tk.W)

# Add horizontal scrollbar
hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=table.xview)
hsb.pack(side='bottom', fill='x')
table.configure(xscroll=hsb.set)

# Bind double-click to open links
table.bind("<Double-1>", on_table_click)

root.mainloop()
