#!/usr/bin/env python3
"""
StokWELL Desktop Application - Command Line Version for Testing
This version provides a command-line interface for testing the application logic
without requiring a GUI environment.
"""

import sys
import os
from data_manager import load_data, save_data
from user_manager import register_user, login_user
from stokvel_manager import create_stokvel, contribute
from utils import validate_amount

class StokWELLCLI:
    def __init__(self):
        self.data = load_data()
        self.current_user = None

    def run(self):
        print("=" * 50)
        print("Welcome to StokWELL - Command Line Interface")
        print("=" * 50)
        
        while True:
            if not self.current_user:
                self.show_auth_menu()
            else:
                self.show_main_menu()

    def show_auth_menu(self):
        print("\n--- Authentication ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("\nSelect an option: ").strip()
        
        if choice == "1":
            self.register()
        elif choice == "2":
            self.login()
        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

    def show_main_menu(self):
        print(f"\n--- StokWELL Dashboard for {self.current_user} ---")
        print("1. View Dashboard")
        print("2. Create Stokvel")
        print("3. Contribute to Stokvel")
        print("4. Logout")
        print("5. Exit")
        
        choice = input("\nSelect an option: ").strip()
        
        if choice == "1":
            self.view_dashboard()
        elif choice == "2":
            self.create_stokvel()
        elif choice == "3":
            self.contribute_to_stokvel()
        elif choice == "4":
            self.logout()
        elif choice == "5":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

    def register(self):
        print("\n--- User Registration ---")
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return
        
        password = input("Enter password: ").strip()
        if not password:
            print("Password cannot be empty.")
            return
        
        success, message = register_user(self.data, username, password)
        print(message)

    def login(self):
        print("\n--- User Login ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        success, message = login_user(self.data, username, password)
        print(message)
        
        if success:
            self.current_user = username

    def logout(self):
        print(f"Goodbye, {self.current_user}!")
        self.current_user = None

    def view_dashboard(self):
        print(f"\n--- Dashboard for {self.current_user} ---")
        user_data = self.data['users'][self.current_user]
        
        print(f"Balance: R{user_data['balance']:.2f}")
        
        print("\nRecent Transactions:")
        if user_data['transactions']:
            for i, tx in enumerate(user_data['transactions'][-5:], 1):  # Show last 5 transactions
                print(f"  {i}. {tx}")
        else:
            print("  No transactions yet.")
        
        print("\nYour Stokvels:")
        if user_data['stokvels']:
            for stokvel_name in user_data['stokvels']:
                stokvel = self.data['stokvels'][stokvel_name]
                print(f"  * {stokvel_name}")
                print(f"    Balance: R{stokvel['balance']:.2f}")
                print(f"    Members: {', '.join(stokvel['members'])}")
                print(f"    Total Contributions: {len(stokvel['contributions'])}")
        else:
            print("  You haven't joined any stokvels yet.")
        
        print("-" * 40)

    def create_stokvel(self):
        print("\n--- Create New Stokvel ---")
        stokvel_name = input("Enter stokvel name: ").strip()
        
        if not stokvel_name:
            print("Stokvel name cannot be empty.")
            return
        
        success, message = create_stokvel(self.data, stokvel_name, self.current_user)
        print(message)

    def contribute_to_stokvel(self):
        print("\n--- Contribute to Stokvel ---")
        user_stokvels = self.data['users'][self.current_user]['stokvels']
        
        if not user_stokvels:
            print("You haven't joined any stokvels yet. Create one first!")
            return
        
        print("Your Stokvels:")
        for i, stokvel_name in enumerate(user_stokvels, 1):
            print(f"  {i}. {stokvel_name}")
        
        try:
            choice = int(input("Select stokvel number: ")) - 1
            if choice < 0 or choice >= len(user_stokvels):
                print("Invalid selection.")
                return
            
            stokvel_name = user_stokvels[choice]
        except ValueError:
            print("Please enter a valid number.")
            return
        
        amount_str = input("Enter contribution amount (R): ").strip()
        amount, error = validate_amount(amount_str)
        
        if error:
            print(f"Error: {error}")
            return
        
        success, message = contribute(self.data, stokvel_name, amount, self.current_user)
        print(message)

def main():
    try:
        cli = StokWELLCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your data files and try again.")

if __name__ == "__main__":
    main()

