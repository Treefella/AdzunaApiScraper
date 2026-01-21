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
def fetch_jobs():
    app_id = adzuna_app_id_entry.get()
    api_key = adzuna_api_key_entry.get()
    search_term = search_entry.get() or "python"
    location = location_entry.get() or "UK"

    adzuna_total = get_adzuna_jobs(app_id, api_key, search_term, location)

    result_text = f"Adzuna Total Jobs: {adzuna_total}"
    messagebox.showinfo("Job Totals", result_text)

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
