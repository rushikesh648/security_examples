import time
from typing import Dict, Any, List

# --- Configuration (Simulated Database/Rules) ---

# Stores user data: 'last_login_time', 'last_login_ip', 'transaction_history'
USER_DATA_STORE: Dict[str, Dict[str, Any]] = {
    "user123": {
        "last_login_time": time.time() - 3600,  # 1 hour ago
        "last_login_ip": "203.0.113.45",
        "transaction_history": [
            {"amount": 50.00, "timestamp": time.time() - 100},
            {"amount": 20.00, "timestamp": time.time() - 50},
        ]
    }
}

# --- Fraud Prevention Rules ---

# Velocity Rule: Maximum number of transactions allowed in the last 60 seconds
MAX_TXN_VELOCITY = 3

# Geo-Location Rule: Threshold for time difference between last login and current transaction
MAX_TIME_DIFF_FOR_IP_CHANGE = 30  # seconds

# --- Fraud Check Logic ---

def check_transaction_velocity(user_id: str) -> bool:
    """
    Checks if the user is making too many transactions in a short period.
    Returns True if safe, False if potentially fraudulent (high velocity).
    """
    current_time = time.time()
    user_info = USER_DATA_STORE.get(user_id, {})
    history: List[Dict[str, float]] = user_info.get("transaction_history", [])

    # Filter transactions that occurred within the last 60 seconds
    recent_transactions = [
        txn for txn in history
        if txn["timestamp"] > (current_time - 60)
    ]

    if len(recent_transactions) >= MAX_TXN_VELOCITY:
        print(f"FRAUD ALERT: High transaction velocity for {user_id}. {len(recent_transactions)} transactions in 60s.")
        return False
    return True

def check_geo_discrepancy(user_id: str, current_ip: str) -> bool:
    """
    Checks for impossible travel, i.e., an IP change in a very short time.
    Returns True if safe, False if potentially fraudulent (impossible travel).
    """
    user_info = USER_DATA_STORE.get(user_id, {})
    last_ip = user_info.get("last_login_ip")
    last_time = user_info.get("last_login_time", 0)
    current_time = time.time()

    if last_ip and last_ip != current_ip:
        time_diff = current_time - last_time
        if time_diff < MAX_TIME_DIFF_FOR_IP_CHANGE:
            print(f"FRAUD ALERT: Impossible travel for {user_id}. IP changed from {last_ip} to {current_ip} in {time_diff:.2f}s.")
            return False
    return True

def process_transaction(user_id: str, amount: float, ip_address: str) -> str:
    """
    Runs security checks before allowing a transaction.
    """
    print(f"\n--- Processing Transaction for {user_id} of ${amount:.2f} ---")

    # 1. Run Velocity Check
    if not check_transaction_velocity(user_id):
        return "DENIED: Transaction velocity exceeded."

    # 2. Run Geo-Discrepancy Check
    if not check_geo_discrepancy(user_id, ip_address):
        return "DENIED: Suspicious location change detected."

    # If all checks pass
    print("SUCCESS: All fraud checks passed.")

    # Update user history (simulated persistence)
    user_info = USER_DATA_STORE.get(user_id)
    if user_info:
        user_info["transaction_history"].append({"amount": amount, "timestamp": time.time()})
        user_info["last_login_ip"] = ip_address
        user_info["last_login_time"] = time.time()
        return "APPROVED"
    else:
        return "ERROR: User not found."

# --- Simulation/Execution ---

# Scenario 1: Legitimate Transaction
result1 = process_transaction("user123", 100.00, "203.0.113.45")
print(f"Result 1: {result1}")

# Scenario 2: High Velocity Attempt (Should be DENIED)
# We simulate two more rapid transactions, totaling 4 in 60s (MAX is 3)
process_transaction("user123", 5.00, "203.0.113.45")
result2 = process_transaction("user123", 5.00, "203.0.113.45") # This is the 4th recent transaction
print(f"Result 2: {result2}")

# Scenario 3: Impossible Travel (Should be DENIED)
# Simulate an immediate transaction from a completely new IP address
result3 = process_transaction("user123", 500.00, "192.168.1.1") # New IP instantly
print(f"Result 3: {result3}")
