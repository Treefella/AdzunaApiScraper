#!/usr/bin/env python3
"""
Adzuna Job Scraper - Smart GUI with Tab-based Interface
Combines: run_gui.sh launch pattern + AdzunaApiScraper + smart_ai_job_system GUI structure
"""

import tkinter as tk
from tkinter import messagebox, ttk, filedialog, StringVar, IntVar
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import webbrowser

load_dotenv()

# Global variables
current_jobs = []
sort_reverse = False


class AdzunaJobScraperGUI:
    """Smart Adzuna Job Scraper with tabbed interface"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Adzuna Job Scraper - Smart Dashboard")
        self.root.geometry("1600x950")
        
        self.current_jobs = []
        self.selected_job_id = None
        self.processing = False
        
        self.setup_ui()
        self.check_credentials()
    
    def setup_ui(self):
        """Create tabbed interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tab 1: Job Search
        self.search_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.search_tab, text='🔍 Job Search')
        
        # Tab 2: Results
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text='📋 Results')
        
        # Tab 3: Tools
        self.tools_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.tools_tab, text='🛠️ Tools')
        
        self.setup_search_tab()
        self.setup_results_tab()
        self.setup_tools_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side='bottom', fill='x')
    
    def setup_search_tab(self):
        """Setup job search tab"""
        main_frame = ttk.Frame(self.search_tab, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🧠 Adzuna Job Scraper",
                                font=("Arial", 18, "bold"))
        title_label.pack(side='top', pady=10)
        
        # Search controls
        control_frame = ttk.LabelFrame(main_frame, text="Search Parameters", padding="10")
        control_frame.pack(fill='x', pady=10)
        
        # Search term
        ttk.Label(control_frame, text="Search Term:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.search_entry = ttk.Entry(control_frame, width=30)
        self.search_entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.search_entry.insert(0, "python")
        
        # Location
        ttk.Label(control_frame, text="Location:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.location_entry = ttk.Entry(control_frame, width=30)
        self.location_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.location_entry.insert(0, "UK")
        
        # Max results
        ttk.Label(control_frame, text="Max Results:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.max_results_var = IntVar(value=50)
        ttk.Spinbox(control_frame, from_=10, to=500, textvariable=self.max_results_var, width=10).grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="🚀 Fetch Jobs", command=self.fetch_jobs).pack(side='left', padx=5)
        ttk.Button(button_frame, text="💾 Save Results", command=self.save_to_json).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📊 Refresh", command=self.refresh_results).pack(side='left', padx=5)
        
        # Info section
        info_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        info_frame.pack(fill='both', expand=True, pady=10)
        
        self.info_text = tk.Text(info_frame, height=20, width=80)
        self.info_text.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(info_frame, command=self.info_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.info_text.config(yscrollcommand=scrollbar.set)
        
        self.log_message("Ready to search for jobs")
    
    def setup_results_tab(self):
        """Setup results table tab"""
        main_frame = ttk.Frame(self.results_tab, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Results table
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill='both', expand=True)
        
        tree_scroll = ttk.Scrollbar(table_frame)
        tree_scroll.pack(side='right', fill='y')
        
        self.tree = ttk.Treeview(table_frame, yscrollcommand=tree_scroll.set, selectmode='browse')
        self.tree.pack(side='left', fill='both', expand=True)
        tree_scroll.config(command=self.tree.yview)
        
        # Define columns
        self.tree['columns'] = ('Date', 'Title', 'Company', 'Location', 'Type', 'Salary', 'Link')
        
        self.tree.column('#0', width=50, minwidth=50)
        self.tree.column('Date', width=70, minwidth=60)
        self.tree.column('Title', width=250, minwidth=200)
        self.tree.column('Company', width=150, minwidth=100)
        self.tree.column('Location', width=150, minwidth=100)
        self.tree.column('Type', width=100, minwidth=80)
        self.tree.column('Salary', width=100, minwidth=80)
        self.tree.column('Link', width=0, stretch=False)
        
        # Headings
        self.tree.heading('#0', text='#', anchor=tk.W)
        self.tree.heading('Date', text='Date', anchor=tk.W)
        self.tree.heading('Title', text='Job Title', anchor=tk.W)
        self.tree.heading('Company', text='Company', anchor=tk.W)
        self.tree.heading('Location', text='Location', anchor=tk.W)
        self.tree.heading('Type', text='Type', anchor=tk.W)
        self.tree.heading('Salary', text='Salary', anchor=tk.W)
        
        # Add horizontal scrollbar
        hsb = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        hsb.pack(side='bottom', fill='x')
        self.tree.configure(xscroll=hsb.set)
        
        # Bind double-click to open link
        self.tree.bind('<Double-1>', self.on_tree_click)
    
    def setup_tools_tab(self):
        """Setup tools tab"""
        main_frame = ttk.Frame(self.tools_tab, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="🛠️ Tools & Utilities", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Tools section
        tools_frame = ttk.LabelFrame(main_frame, text="Available Tools", padding="10")
        tools_frame.pack(fill='x', pady=10)
        
        ttk.Button(tools_frame, text="📥 Import JSON", command=self.import_json).pack(fill='x', pady=5)
        ttk.Button(tools_frame, text="📤 Export CSV", command=self.export_csv).pack(fill='x', pady=5)
        ttk.Button(tools_frame, text="🧹 Clear Results", command=self.clear_results).pack(fill='x', pady=5)
        
        # Statistics
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.pack(fill='x', pady=10)
        
        ttk.Label(stats_frame, text=f"Total Jobs Loaded: {len(self.current_jobs)}").pack(pady=5)
    
    def check_credentials(self):
        """Check if API credentials are available"""
        app_id = os.getenv("ADZUNA_APP_ID")
        api_key = os.getenv("ADZUNA_API_KEY")
        
        if app_id and api_key:
            self.log_message("✓ API credentials found")
        else:
            messagebox.showwarning("Warning", "API credentials not found in .env file")
            self.log_message("✗ API credentials missing - check .env file")
    
    def log_message(self, message):
        """Log message to info text"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.info_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.info_text.see(tk.END)
    
    def fetch_jobs(self):
        """Fetch jobs from Adzuna API"""
        search_term = self.search_entry.get() or "python"
        location = self.location_entry.get() or "UK"
        max_results = self.max_results_var.get()
        
        app_id = os.getenv("ADZUNA_APP_ID")
        api_key = os.getenv("ADZUNA_API_KEY")
        
        if not app_id or not api_key:
            messagebox.showerror("Error", "API credentials not found")
            return
        
        self.log_message(f"Fetching jobs for '{search_term}' in {location}...")
        self.status_var.set("Fetching jobs...")
        
        try:
            url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id}&app_key={api_key}&what={search_term}&where={location}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            jobs = data.get('results', [])
            
            if not jobs:
                messagebox.showinfo("Info", "No jobs found")
                self.log_message("No jobs found for this search")
                return
            
            self.current_jobs = jobs[:max_results]
            
            # Clear and populate results table
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for idx, job in enumerate(self.current_jobs, 1):
                date_str = job.get('created', datetime.now().isoformat())[:10]
                title = job.get('title', 'N/A')
                company = job.get('company', {}).get('display_name', 'N/A')
                location_name = job.get('location', {}).get('display_name', 'N/A')
                job_type = job.get('contract_type', 'N/A')
                salary_max = job.get('salary_max', 0)
                salary_str = f"£{salary_max:,.0f}" if salary_max else "N/A"
                link = job.get('redirect_url', '')
                
                self.tree.insert('', 'end', text=str(idx), values=(
                    date_str, title, company, location_name, job_type, salary_str, link
                ))
            
            self.log_message(f"✓ Fetched {len(jobs)} jobs")
            self.status_var.set(f"Loaded {len(jobs)} jobs")
            messagebox.showinfo("Success", f"Loaded {len(jobs)} jobs!")
            
        except Exception as e:
            self.log_message(f"✗ Error: {e}")
            messagebox.showerror("Error", f"Failed to fetch jobs: {e}")
            self.status_var.set("Error fetching jobs")
    
    def on_tree_click(self, event):
        """Handle double-click on table row"""
        item = self.tree.identify_row(event.y)
        if item:
            values = self.tree.item(item, "values")
            if len(values) > 6:
                link = values[6]
                if link.startswith("http"):
                    self.log_message(f"Opening job link...")
                    webbrowser.open(link)
    
    def save_to_json(self):
        """Save results to JSON"""
        if not self.current_jobs:
            messagebox.showwarning("Warning", "No jobs to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.current_jobs, f, ensure_ascii=False, indent=4)
            self.log_message(f"✓ Saved {len(self.current_jobs)} jobs to {filename}")
            messagebox.showinfo("Success", f"Saved {len(self.current_jobs)} jobs!")
    
    def export_csv(self):
        """Export results to CSV (TODO)"""
        self.log_message("TODO: CSV export feature")
        messagebox.showinfo("Info", "CSV export coming soon!")
    
    def import_json(self):
        """Import jobs from JSON (TODO)"""
        self.log_message("TODO: JSON import feature")
        messagebox.showinfo("Info", "JSON import coming soon!")
    
    def clear_results(self):
        """Clear results table"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.current_jobs = []
        self.log_message("Cleared all results")
    
    def refresh_results(self):
        """Refresh results display"""
        self.log_message("Refreshed display")


def main():
    """Launch the application"""
    root = tk.Tk()
    app = AdzunaJobScraperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
