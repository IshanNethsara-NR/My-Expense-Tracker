import customtkinter as ctk
import sqlite3
from datetime import datetime
import os

# UI Theme Settings
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

# New database name (forget the old one)
DB_NAME = 'my_expenses_v2.db'

class ExpenseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("My Expense Tracker 💰")
        self.geometry("500x600")

        # Initialize Database
        self.init_db()

        # --- UI Components ---
        
        # Title
        self.label = ctk.CTkLabel(self, text="Daily Expense Tracker", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # Amount Input
        self.entry_amount = ctk.CTkEntry(self, placeholder_text="Enter Amount (e.g. 500)")
        self.entry_amount.pack(pady=10, padx=20, fill="x")

        # Reason Input
        self.entry_reason = ctk.CTkEntry(self, placeholder_text="Description (e.g. Lunch)")
        self.entry_reason.pack(pady=10, padx=20, fill="x")

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        # Add Button
        self.btn_add = ctk.CTkButton(self.button_frame, text="Add Expense", command=self.add_expense, fg_color="#2CC985", hover_color="#229966")
        self.btn_add.pack(side="left", padx=10)

        # Clear Button
        self.btn_clear = ctk.CTkButton(self.button_frame, text="Clear Data", command=self.clear_data, fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_clear.pack(side="left", padx=10)

        # Expense List (Display)
        self.textbox = ctk.CTkTextbox(self, width=450, height=300)
        self.textbox.pack(pady=10)

        # Load initial data
        self.load_expenses()

    def init_db(self):
        """Creates the database and table if not exists"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                reason TEXT,
                date TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_expense(self):
        """Adds a new expense to the database"""
        amount = self.entry_amount.get()
        reason = self.entry_reason.get()
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M")

        if amount and reason:
            try:
                # Check if amount is a number
                float(amount)
                
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO expenses (amount, reason, date) VALUES (?, ?, ?)", (amount, reason, date_now))
                conn.commit()
                conn.close()

                # Update UI
                self.textbox.insert("0.0", f"[{date_now}] Rs. {amount} - {reason}\n")
                
                # Clear inputs
                self.entry_amount.delete(0, "end")
                self.entry_reason.delete(0, "end")
            except ValueError:
                print("Error: Amount must be a number!")
        else:
            print("Error: Please fill all fields!")

    def load_expenses(self):
        """Loads all expenses from database to UI"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT amount, reason, date FROM expenses ORDER BY id DESC")
        rows = cursor.fetchall()
        
        self.textbox.delete("0.0", "end")
        for row in rows:
            text = f"[{row[2]}] Rs. {row[0]} - {row[1]}\n"
            self.textbox.insert("end", text)
            
        conn.close()

    def clear_data(self):
        """Deletes all data"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()
        self.load_expenses()

if __name__ == "__main__":
    app = ExpenseApp()
    app.mainloop()