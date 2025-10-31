
from data_manager import load_data, save_data
from datetime import datetime

def create_stokvel(data, stokvel_name, current_user):
    if stokvel_name in data["stokvels"]:
        return False, "Stokvel already exists!"
    
    data["stokvels"][stokvel_name] = {
        "members": [current_user],
        "contributions": [],
        "balance": 0,
        "created_date": datetime.now().isoformat(),
        "created_by": current_user
    }
    data["users"][current_user]["stokvels"].append(stokvel_name)
    save_data(data)
    return True, f"Stokvel '{stokvel_name}' created and you have joined it!"

def contribute(data, stokvel_name, amount, current_user):
    if stokvel_name not in data["stokvels"]:
        return False, "Stokvel not found."
    if current_user not in data["stokvels"][stokvel_name]["members"]:
        return False, "You are not a member of this stokvel."
    
    # Add contribution
    data["stokvels"][stokvel_name]["balance"] += amount
    contribution_record = {
        "user": current_user, 
        "amount": amount,
        "date": datetime.now().isoformat()
    }
    data["stokvels"][stokvel_name]["contributions"].append(contribution_record)
    
    # Add transaction to user's history
    transaction = f"Contributed R{amount:.2f} to {stokvel_name} on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    data["users"][current_user]["transactions"].append(transaction)
    
    save_data(data)
    return True, f"You contributed R{amount:.2f} to {stokvel_name}."

def get_stokvel_data(data, stokvel_name):
    """Get stokvel data safely."""
    return data["stokvels"].get(stokvel_name, None)

def get_user_stokvels(data, username):
    """Get all stokvels for a user."""
    user_data = data["users"].get(username, {})
    return user_data.get("stokvels", [])

def join_stokvel(data, stokvel_name, username):
    """Allow a user to join an existing stokvel."""
    if stokvel_name not in data["stokvels"]:
        return False, "Stokvel not found."
    if username in data["stokvels"][stokvel_name]["members"]:
        return False, "You are already a member of this stokvel."
    
    data["stokvels"][stokvel_name]["members"].append(username)
    data["users"][username]["stokvels"].append(stokvel_name)
    save_data(data)
    return True, f"You have joined {stokvel_name}!"

def get_stokvel_summary(data, stokvel_name):
    """Get a summary of stokvel activity."""
    stokvel = data["stokvels"].get(stokvel_name)
    if not stokvel:
        return None
    
    total_contributions = sum(contrib["amount"] for contrib in stokvel["contributions"])
    member_count = len(stokvel["members"])
    
    return {
        "name": stokvel_name,
        "balance": stokvel["balance"],
        "total_contributions": total_contributions,
        "member_count": member_count,
        "members": stokvel["members"],
        "created_date": stokvel.get("created_date", "Unknown"),
        "created_by": stokvel.get("created_by", "Unknown")
    }


