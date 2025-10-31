
import hashlib

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify a password against its hash."""
    return hash_password(password) == hashed

def format_currency(amount):
    """Format amount as currency."""
    return f"R{amount:.2f}"

def validate_amount(amount_str):
    """Validate and convert amount string to float."""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return None, "Amount must be positive"
        return amount, None
    except ValueError:
        return None, "Invalid amount format"

