import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import json
import threading

class ModernCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("API-Powered GUI Calculator")
        self.root.geometry("560x700")
        self.root.resizable(False, False)
        
        # Color Palette (Modern Dark Theme)
        self.bg_dark = "#111827"      # Slate 900
        self.bg_card = "#1F2937"      # Slate 800
        self.fg_light = "#F9FAFB"     # Slate 50
        self.fg_muted = "#9CA3AF"     # Slate 400
        self.accent_indigo = "#4F46E5" # Indigo 600
        self.accent_hover = "#6366F1"  # Indigo 500
        self.accent_teal = "#0D9488"   # Teal 600
        self.border_color = "#374151"  # Slate 700
        self.danger_color = "#EF4444"  # Red 500
        
        self.root.configure(bg=self.bg_dark)
        
        # Apply TTK Theme Styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configure TTK styles to match dark theme
        self.style.configure(".", background=self.bg_dark, foreground=self.fg_light)
        self.style.configure("TLabel", background=self.bg_dark, foreground=self.fg_light, font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", background=self.bg_dark, foreground=self.fg_light, font=("Segoe UI", 16, "bold"))
        self.style.configure("Sub.TLabel", background=self.bg_dark, foreground=self.fg_muted, font=("Segoe UI", 9))
        self.style.configure("Card.TFrame", background=self.bg_card, relief="flat")
        
        # Custom styles for entries & dropdowns
        self.style.configure("TCombobox", fieldbackground=self.bg_card, background=self.border_color, foreground=self.fg_light)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header / Title
        header_frame = tk.Frame(self.root, bg=self.bg_dark, pady=15)
        header_frame.pack(fill="x", padx=25)
        
        title_lbl = ttk.Label(header_frame, text="API Calculator Client", style="Header.TLabel")
        title_lbl.pack(anchor="w")
        
        desc_lbl = ttk.Label(header_frame, text="Configure your endpoint and send calculations seamlessly.", style="Sub.TLabel")
        desc_lbl.pack(anchor="w", pady=(2, 0))
        
        # --- API CONFIGURATION CARD ---
        config_frame = tk.Frame(self.root, bg=self.bg_card, bd=1, highlightbackground=self.border_color, highlightthickness=1)
        config_frame.pack(fill="x", padx=25, pady=(5, 15))
        
        # Inner padding for config card
        config_inner = tk.Frame(config_frame, bg=self.bg_card, padx=15, pady=15)
        config_inner.pack(fill="both", expand=True)
        
        # Card Title
        config_title = tk.Label(config_inner, text="ENDPOINT CONFIGURATION", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 9, "bold"))
        config_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # URL Input
        tk.Label(config_inner, text="API URL:", bg=self.bg_card, fg=self.fg_light, font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.url_var = tk.StringVar(value="https://p3gp1w5s-5000.inc1.devtunnels.ms/calculate")
        self.url_entry = tk.Entry(config_inner, textvariable=self.url_var, bg=self.bg_dark, fg=self.fg_light, 
                                  insertbackground=self.fg_light, bd=0, highlightbackground=self.border_color, highlightthickness=1, font=("Consolas", 10))
        self.url_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # Request Method Selector
        tk.Label(config_inner, text="HTTP Method:", bg=self.bg_card, fg=self.fg_light, font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.method_var = tk.StringVar(value="POST (JSON)")
        self.method_combo = ttk.Combobox(config_inner, textvariable=self.method_var, values=["GET", "POST (JSON)", "POST (Form)"], state="readonly", width=15)
        self.method_combo.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=5)
        
        # Parameter Keys Section
        tk.Label(config_inner, text="Param Keys:", bg=self.bg_card, fg=self.fg_light, font=("Segoe UI", 10)).grid(row=3, column=0, sticky="nw", pady=5)
        
        param_frame = tk.Frame(config_inner, bg=self.bg_card)
        param_frame.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        tk.Label(param_frame, text="Num1:", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 8)).grid(row=0, column=0, sticky="w")
        self.key_num1_var = tk.StringVar(value="num1")
        self.key_num1_entry = tk.Entry(param_frame, textvariable=self.key_num1_var, bg=self.bg_dark, fg=self.fg_light, bd=0, highlightbackground=self.border_color, highlightthickness=1, font=("Consolas", 9), width=8)
        self.key_num1_entry.grid(row=0, column=1, padx=(2, 8))
        
        tk.Label(param_frame, text="Num2:", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 8)).grid(row=0, column=2, sticky="w")
        self.key_num2_var = tk.StringVar(value="num2")
        self.key_num2_entry = tk.Entry(param_frame, textvariable=self.key_num2_var, bg=self.bg_dark, fg=self.fg_light, bd=0, highlightbackground=self.border_color, highlightthickness=1, font=("Consolas", 9), width=8)
        self.key_num2_entry.grid(row=0, column=3, padx=(2, 8))
        
        tk.Label(param_frame, text="Op:", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 8)).grid(row=0, column=4, sticky="w")
        self.key_op_var = tk.StringVar(value="operation")
        self.key_op_entry = tk.Entry(param_frame, textvariable=self.key_op_var, bg=self.bg_dark, fg=self.fg_light, bd=0, highlightbackground=self.border_color, highlightthickness=1, font=("Consolas", 9), width=10)
        self.key_op_entry.grid(row=0, column=5, padx=(2, 0))
        
        config_inner.grid_columnconfigure(1, weight=1)
        
        # --- CALCULATOR BODY CARD ---
        calc_frame = tk.Frame(self.root, bg=self.bg_card, bd=1, highlightbackground=self.border_color, highlightthickness=1)
        calc_frame.pack(fill="x", padx=25, pady=0)
        
        calc_inner = tk.Frame(calc_frame, bg=self.bg_card, padx=15, pady=20)
        calc_inner.pack(fill="both", expand=True)
        
        # Card Title
        calc_title = tk.Label(calc_inner, text="CALCULATOR INPUTS", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 9, "bold"))
        calc_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Input 1
        tk.Label(calc_inner, text="First Number (num1):", bg=self.bg_card, fg=self.fg_light, font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", pady=8)
        self.num1_entry = tk.Entry(calc_inner, bg=self.bg_dark, fg=self.fg_light, insertbackground=self.fg_light, bd=0, highlightbackground=self.border_color, highlightthickness=1, font=("Segoe UI", 12))
        self.num1_entry.grid(row=1, column=1, sticky="ew", padx=(15, 0), pady=8)
        
        # Input 2
        tk.Label(calc_inner, text="Second Number (num2):", bg=self.bg_card, fg=self.fg_light, font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w", pady=8)
        self.num2_entry = tk.Entry(calc_inner, bg=self.bg_dark, fg=self.fg_light, insertbackground=self.fg_light, bd=0, highlightbackground=self.border_color, highlightthickness=1, font=("Segoe UI", 12))
        self.num2_entry.grid(row=2, column=1, sticky="ew", padx=(15, 0), pady=8)
        
        # Operation Dropdown
        tk.Label(calc_inner, text="Operation:", bg=self.bg_card, fg=self.fg_light, font=("Segoe UI", 11)).grid(row=3, column=0, sticky="w", pady=8)
        self.op_var = tk.StringVar(value="Addition (+)")
        self.op_combo = ttk.Combobox(calc_inner, textvariable=self.op_var, values=[
            "Addition (+)", 
            "Subtraction (-)", 
            "Multiplication (*)", 
            "Division (/)"
        ], state="readonly", font=("Segoe UI", 11))
        self.op_combo.grid(row=3, column=1, sticky="ew", padx=(15, 0), pady=8)
        
        calc_inner.grid_columnconfigure(1, weight=1)
        
        # --- CALCULATE BUTTON ---
        btn_frame = tk.Frame(self.root, bg=self.bg_dark, pady=15)
        btn_frame.pack(fill="x", padx=25)
        
        self.calc_btn = tk.Button(
            btn_frame, 
            text="Calculate", 
            command=self.start_calculation, 
            bg=self.accent_indigo, 
            fg=self.fg_light, 
            activebackground=self.accent_hover, 
            activeforeground=self.fg_light, 
            font=("Segoe UI", 12, "bold"), 
            bd=0, 
            cursor="hand2", 
            pady=10
        )
        self.calc_btn.pack(fill="x")
        self.calc_btn.bind("<Enter>", lambda e: self.calc_btn.configure(bg=self.accent_hover))
        self.calc_btn.bind("<Leave>", lambda e: self.calc_btn.configure(bg=self.accent_indigo))
        
        # --- RESULT CARD ---
        result_frame = tk.Frame(self.root, bg=self.bg_card, bd=1, highlightbackground=self.border_color, highlightthickness=1)
        result_frame.pack(fill="both", expand=True, padx=25, pady=(5, 20))
        
        result_inner = tk.Frame(result_frame, bg=self.bg_card, padx=15, pady=15)
        result_inner.pack(fill="both", expand=True)
        
        result_title = tk.Label(result_inner, text="RESULT & STATUS", bg=self.bg_card, fg=self.fg_muted, font=("Segoe UI", 9, "bold"))
        result_title.pack(anchor="w", pady=(0, 10))
        
        # Status Label
        self.status_lbl = tk.Label(result_inner, text="Ready", bg=self.bg_card, fg=self.accent_teal, font=("Segoe UI", 10, "italic"))
        self.status_lbl.pack(anchor="w")
        
        # Huge Display for Result
        self.result_display = tk.Text(
            result_inner, 
            bg=self.bg_dark, 
            fg=self.fg_light, 
            bd=0, 
            highlightbackground=self.border_color, 
            highlightthickness=1, 
            font=("Consolas", 18, "bold"),
            height=3, 
            padx=10, 
            pady=10
        )
        self.result_display.pack(fill="both", expand=True, pady=(10, 0))
        self.result_display.insert("1.0", "---")
        self.result_display.configure(state="disabled")

    def log_status(self, text, color=None):
        if not color:
            color = self.fg_muted
        self.status_lbl.configure(text=text, fg=color)

    def display_result(self, result_text, is_error=False):
        self.result_display.configure(state="normal")
        self.result_display.delete("1.0", tk.END)
        self.result_display.insert("1.0", result_text)
        self.result_display.configure(state="disabled")
        
        if is_error:
            self.result_display.configure(fg=self.danger_color)
        else:
            self.result_display.configure(fg=self.fg_light)

    def start_calculation(self):
        # 1. Validate number inputs
        num1_raw = self.num1_entry.get().strip()
        num2_raw = self.num2_entry.get().strip()
        
        if not num1_raw or not num2_raw:
            messagebox.showerror("Invalid Input", "Please enter values in both number fields.")
            return
            
        try:
            # Check if they are valid numbers (integer or float)
            num1 = float(num1_raw)
            num2 = float(num2_raw)
            # Convert to int if it's a whole number for cleaner parameters
            if num1.is_integer(): num1 = int(num1)
            if num2.is_integer(): num2 = int(num2)
        except ValueError:
            messagebox.showerror("Invalid Input", "Inputs must be valid numeric values (e.g. 5 or 3.14).")
            return
            
        # 2. Get the operation mapping
        op_text = self.op_var.get()
        if "Addition" in op_text:
            op_value = "add"
        elif "Subtraction" in op_text:
            op_value = "subtract"
        elif "Multiplication" in op_text:
            op_value = "multiply"
        elif "Division" in op_text:
            op_value = "divide"
            if num2 == 0:
                messagebox.showerror("Invalid Operation", "Division by zero is not allowed.")
                return
        else:
            op_value = "add"

        # Update UI state to loading
        self.calc_btn.configure(state="disabled", text="Requesting API...")
        self.log_status("Sending request to backend API...", self.accent_indigo)
        self.display_result("Calculating...")
        
        # 3. Fire background thread to make the HTTP request (so the window doesn't freeze)
        thread = threading.Thread(target=self.perform_request, args=(num1, num2, op_value))
        thread.daemon = True
        thread.start()

    def perform_request(self, num1, num2, op_value):
        url = self.url_var.get().strip()
        method = self.method_var.get()
        
        key_num1 = self.key_num1_var.get().strip() or "num1"
        key_num2 = self.key_num2_var.get().strip() or "num2"
        key_op = self.key_op_var.get().strip() or "operation"
        
        params = {
            key_num1: num1,
            key_num2: num2,
            key_op: op_value
        }
        
        try:
            # Perform HTTP request based on method selection
            if method == "GET":
                self.root.after(0, lambda: self.log_status(f"GET -> {url}", self.accent_indigo))
                response = requests.get(url, params=params, timeout=12)
            elif method == "POST (JSON)":
                self.root.after(0, lambda: self.log_status(f"POST JSON -> {url}", self.accent_indigo))
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, headers=headers, json=params, timeout=12)
            else: # POST (Form)
                self.root.after(0, lambda: self.log_status(f"POST Form -> {url}", self.accent_indigo))
                response = requests.post(url, data=params, timeout=12)
                
            status_code = response.status_code
            
            # If request succeeded, parse and display
            if 200 <= status_code < 300:
                result = self.extract_result(response)
                self.root.after(0, lambda: self.handle_success(result, f"Success (HTTP {status_code})"))
            else:
                # API returned an error status
                error_msg = f"HTTP Error {status_code}\nResponse: {response.text[:200]}"
                self.root.after(0, lambda: self.handle_error(error_msg, f"Failed (HTTP {status_code})"))
                
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: self.handle_error("Request timed out. Please check if the server is running and accessible.", "Timeout Error"))
        except requests.exceptions.ConnectionError:
            self.root.after(0, lambda: self.handle_error(f"Could not connect to:\n{url}\n\nPlease check your URL and make sure your server/devtunnel is online.", "Connection Error"))
        except Exception as e:
            self.root.after(0, lambda: self.handle_error(str(e), "Error"))

    def extract_result(self, response):
        """
        Attempts to parse response as JSON and search for common calculation output keys.
        Falls back to raw text if it is not JSON or is in a different format.
        """
        try:
            data = response.json()
            if isinstance(data, dict):
                # Look for common key names where result might reside
                possible_keys = ["result", "output", "data", "value", "ans", "answer", "response", "sum"]
                for key in possible_keys:
                    if key in data:
                        return str(data[key])
                
                # If it's a dictionary but no common key is found, return formatted json string
                return json.dumps(data, indent=2)
            else:
                return str(data)
        except (ValueError, json.JSONDecodeError):
            # Not JSON - return raw text
            return response.text.strip()

    def handle_success(self, result_val, status_msg):
        self.calc_btn.configure(state="normal", text="Calculate")
        self.log_status(status_msg, self.accent_teal)
        self.display_result(result_val, is_error=False)

    def handle_error(self, error_val, status_msg):
        self.calc_btn.configure(state="normal", text="Calculate")
        self.log_status(status_msg, self.danger_color)
        self.display_result(error_val, is_error=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculatorGUI(root)
    root.mainloop()
