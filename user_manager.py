
from data_manager import load_data, save_data
from utils import hash_password, verify_password

def register_user(data, username, password):
    if username in data["users"]:
        return False, "Username already exists!"
    
    # Hash the password before storing
    hashed_password = hash_password(password)
    
    data["users"][username] = {
        "password": hashed_password,
        "balance": 0,
        "transactions": [],
        "stokvels": []
    }
    save_data(data)
    return True, f"User {username} registered successfully!"

def login_user(data, username, password):
    user = data["users"].get(username)
    if user and verify_password(password, user["password"]):
        return True, f"Welcome back, {username}!"
    return False, "Invalid credentials."

def get_user_data(data, username):
    """Get user data safely."""
    return data["users"].get(username, None)

def update_user_balance(data, username, amount):
    """Update user balance."""
    if username in data["users"]:
        data["users"][username]["balance"] += amount
        save_data(data)
        return True
    return False

def add_user_transaction(data, username, transaction):
    """Add transaction to user's history."""
    if username in data["users"]:
        data["users"][username]["transactions"].append(transaction)
        save_data(data)
        return True
    return False


