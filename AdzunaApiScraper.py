import tkinter as tk
from tkinter import messagebox
import requests

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
def show_results_window(adzuna_total, search_term, location):
    """Display results in a new window."""
    results_window = tk.Toplevel(root)
    results_window.title("Job Search Results")
    results_window.geometry("400x300")
    
    # Title
    title = tk.Label(results_window, text="Job Search Results", font=("Arial", 14, "bold"))
    title.pack(pady=10)
    
    # Results details
    info_frame = tk.Frame(results_window)
    info_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
    
    tk.Label(info_frame, text=f"Search Term: {search_term}", font=("Arial", 10)).pack(anchor="w", pady=5)
    tk.Label(info_frame, text=f"Location: {location}", font=("Arial", 10)).pack(anchor="w", pady=5)
    tk.Label(info_frame, text=f"Total Jobs Found: {adzuna_total}", font=("Arial", 12, "bold"), fg="green").pack(anchor="w", pady=10)
    
    # Close button
    tk.Button(results_window, text="Close", command=results_window.destroy).pack(pady=10)

def fetch_jobs():
    app_id = adzuna_app_id_entry.get()
    api_key = adzuna_api_key_entry.get()
    search_term = search_entry.get() or "python"
    location = location_entry.get() or "UK"

    adzuna_total = get_adzuna_jobs(app_id, api_key, search_term, location)
    
    if adzuna_total is not None:
        show_results_window(adzuna_total, search_term, location)
    else:
        messagebox.showerror("Error", "Failed to fetch jobs. Check your API credentials.")

# ----- GUI Setup -----
root = tk.Tk()
root.title("Job Scraper GUI")

# Adzuna Inputs
tk.Label(root, text="Adzuna Application ID:").grid(row=0, column=0, sticky="e")
adzuna_app_id_entry = tk.Entry(root, width=40)
adzuna_app_id_entry.grid(row=0, column=1)

tk.Label(root, text="Adzuna API Key:").grid(row=1, column=0, sticky="e")
adzuna_api_key_entry = tk.Entry(root, width=40)
adzuna_api_key_entry.grid(row=1, column=1)

# Search Term & Location
tk.Label(root, text="Search Term:").grid(row=2, column=0, sticky="e")
search_entry = tk.Entry(root, width=40)
search_entry.grid(row=2, column=1)

tk.Label(root, text="Location:").grid(row=3, column=0, sticky="e")
location_entry = tk.Entry(root, width=40)
location_entry.grid(row=3, column=1)

# Fetch Button
tk.Button(root, text="Fetch Total Jobs", command=fetch_jobs).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
