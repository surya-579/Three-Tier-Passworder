# This project implements a three-level password authentication system to enhance security.
# So my idea is to set up a password system that is more secure than the traditional password system.
# This system includes textual passwords, graphical passwords, and OTP verification.
# providing strong protection against bots and hackers while remaining user-friendly.

import hashlib
import secrets
import tkinter as tk
from tkinter import messagebox
import random

# Level 1: Textual Password
# The first level of authentication is a textual password. The user must create a textual password during registration.
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password(stored_password_hash, input_password):
    return stored_password_hash == hash_password(input_password)

# Level 2: Graphical Password with Pattern (Tkinter)

class PatternLockApp:
    def __init__(self, root, correct_sequence):
        self.root = root
        self.correct_sequence = correct_sequence
        self.selected_sequence = []
        self.buttons = []
        self.locked = False
        self.create_ui()
        
    def create_ui(self):
        self.root.title("Pattern Lock")
        for i in range(1, 10):
            button = tk.Button(self.root, text=str(i), width=10, height=4,
                               command=lambda i=i: self.select_number(i))
            button.grid(row=(i-1)//3, column=(i-1)%3, padx=10, pady=10)
            self.buttons.append(button)
            
    def select_number(self, number):
        if number not in self.selected_sequence and not self.locked:
            self.selected_sequence.append(number)
            self.buttons[number-1].config(bg="lightblue")  # Highlight the selected button
        if len(self.selected_sequence) == len(self.correct_sequence):
            self.check_password()
    
    def check_password(self):
        self.locked = True  # Lock further input
        if self.selected_sequence == self.correct_sequence:
            messagebox.showinfo("Success", "Graphical pattern validated.")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid pattern.")
            self.reset()

    def reset(self):
        self.locked = False
        self.selected_sequence = []
        for button in self.buttons:
            button.config(bg="SystemButtonFace")  # Reset button colors to default

# Level 3: OTP Generation
def generate_otp():
    return secrets.randbelow(1000000)

def validate_otp(stored_otp, input_otp):
    return stored_otp == input_otp

# Main Program
def main():
    # User Registration
    print("Register your account:")
    password = input("Create a textual password: ")
    hashed_password = hash_password(password)
    
    print("Create a graphical pattern password (via the UI window):")
    root = tk.Tk()
    # graphical_password = [1, 5, 9, 7]  # Example correct pattern (hardcoded for demo purposes)
    graphical_password = [random.randint(1, 9) for _ in range(4)]
    print(f"Your graphical pattern is: {graphical_password}")
    
    app = PatternLockApp(root, graphical_password)
    root.mainloop()
    
    # User Login
    print("\nLogin:")
    input_password = input("Enter your textual password: ")
    
    if validate_password(hashed_password, input_password):
        print("Textual password validated.")
        
        print("Enter your graphical pattern password (via the UI window):")
        root = tk.Tk()
        app = PatternLockApp(root, graphical_password)
        root.mainloop()
        
        otp = generate_otp()
        print(f"Your OTP is: {otp:06d}")  # Ensure OTP is displayed as a 6-digit number
        
        input_otp = int(input("Enter the OTP: "))
        if validate_otp(otp, input_otp):
            print("Login successful!")
        else:
            print("Invalid OTP.")
    else:
        print("Invalid textual password.")

if __name__ == "__main__":
    main()