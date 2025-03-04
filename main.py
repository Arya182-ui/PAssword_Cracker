import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as tb
from brute_force import brute_force_simulated, brute_force_zip
from hash_cracker import crack_hash
from file_cracker import brute_force_rar, brute_force_pdf
from utils import load_wordlist
import threading

# Professional Password Cracker GUI
class PasswordCrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Professional Password Cracker")
        self.root.geometry("800x500")
        self.root.resizable(True, True)

        # Theme and Styling
        self.style = tb.Style("darkly")  # Modern Dark Theme

        # Frame for Side Navigation
        self.nav_frame = tb.Frame(root, bootstyle="dark")
        self.nav_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.btn_brute = tb.Button(self.nav_frame, text="🔓 Brute Force Attack", bootstyle="info-outline", command=self.show_brute_tab)
        self.btn_brute.pack(fill="x", padx=10, pady=5)
        
        self.btn_hash = tb.Button(self.nav_frame, text="🔑 Hash Cracking", bootstyle="primary-outline", command=self.show_hash_tab)
        self.btn_hash.pack(fill="x", padx=10, pady=5)

        # Main Content Frame
        self.main_frame = tb.Frame(root, bootstyle="dark")
        self.main_frame.pack(side="right", expand=True, fill="both", padx=10, pady=5)

        self.current_tab = None
        self.show_brute_tab()  # Default tab

        # Status Bar
        self.status_label = tb.Label(root, text="🔍 Status: Ready", bootstyle="inverse-light", anchor="w")
        self.status_label.pack(side="bottom", fill="x")

    def show_brute_tab(self):
        if self.current_tab:
            self.current_tab.destroy()

        self.current_tab = tb.Frame(self.main_frame, bootstyle="dark")
        self.current_tab.pack(expand=True, fill="both")

        # Wordlist Selection
        tb.Label(self.current_tab, text="📄 Wordlist File:", bootstyle="inverse-light").pack(pady=5)
        self.wordlist_path = tk.StringVar()
        tb.Entry(self.current_tab, textvariable=self.wordlist_path, width=60).pack()
        tb.Button(self.current_tab, text="Browse", bootstyle="info", command=self.browse_wordlist).pack(pady=5)

        # Password Input (For Simulated Mode)
        tb.Label(self.current_tab, text="🔑 Target Password (For Simulated Attack):", bootstyle="inverse-light").pack(pady=5)
        self.target_password = tk.StringVar()
        tb.Entry(self.current_tab, textvariable=self.target_password, width=60).pack()

        # File Selection (ZIP, RAR, PDF)
        tb.Label(self.current_tab, text="📂 File Path (ZIP, RAR, PDF):", bootstyle="inverse-light").pack(pady=5)
        self.file_path = tk.StringVar()
        tb.Entry(self.current_tab, textvariable=self.file_path, width=60).pack()
        tb.Button(self.current_tab, text="Browse", bootstyle="info", command=self.browse_file).pack(pady=5)

        # Start Button
        tb.Button(self.current_tab, text="🚀 Start Brute Force", bootstyle="danger", command=self.start_brute_force).pack(pady=10)

    def show_hash_tab(self):
        if self.current_tab:
            self.current_tab.destroy()

        self.current_tab = tb.Frame(self.main_frame, bootstyle="dark")
        self.current_tab.pack(expand=True, fill="both")

        # Hash Cracking Section
        tb.Label(self.current_tab, text="🔢 Hash Algorithm:", bootstyle="inverse-light").pack(pady=5)
        self.hash_type = tb.Combobox(self.current_tab, values=["MD5", "SHA256", "SHA512"], state="readonly")
        self.hash_type.pack()

        tb.Label(self.current_tab, text="🔓 Enter Hash Value:", bootstyle="inverse-light").pack(pady=5)
        self.hash_value = tk.StringVar()
        tb.Entry(self.current_tab, textvariable=self.hash_value, width=60).pack()

        # Start Button
        tb.Button(self.current_tab, text="🚀 Start Hash Cracking", bootstyle="primary", command=self.start_hash_cracking).pack(pady=10)

    def browse_wordlist(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.wordlist_path.set(path)

    def browse_file(self):
        path = filedialog.askopenfilename()
        self.file_path.set(path)

    def update_status(self, message):
        self.status_label.config(text=f"🔍 Status: {message}")
        self.root.update_idletasks()

    def start_brute_force(self):
        wordlist = load_wordlist(self.wordlist_path.get())
        password = self.target_password.get()

        def run():
            self.update_status("Brute Force Running...")
            result = brute_force_simulated(password, wordlist, self.update_status)
            self.update_status(result)

        threading.Thread(target=run, daemon=True).start()

    def start_hash_cracking(self):
        wordlist = load_wordlist(self.wordlist_path.get())
        hash_algo = self.hash_type.get()

        def run():
            self.update_status("Hash Cracking Running...")
            result = crack_hash(self.hash_value.get(), hash_algo, wordlist, self.update_status)
            self.update_status(result)

        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = PasswordCrackerApp(root)
    root.mainloop()
