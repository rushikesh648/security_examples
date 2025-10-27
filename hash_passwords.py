import bcrypt
import time
from typing import bytes, str

# --- Security Functions ---

def hash_password(password: str) -> bytes:
    """
    Generates a secure hash for a given plaintext password using bcrypt.
    The salt is automatically generated and included in the hash.
    """
    # Convert the string password to bytes, which bcrypt requires
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password in one step.
    # The 'gensalt()' function determines the complexity (default is 12 rounds).
    # Increasing the rounds (e.g., gensalt(14)) makes it slower but more secure.
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    
    return hashed_password

def check_password(password: str, hashed_password: bytes) -> bool:
    """
    Compares a plaintext password to an existing bcrypt hash.
    Returns True if they match, False otherwise.
    """
    # Convert the string password to bytes
    password_bytes = password.encode('utf-8')
    
    # bcrypt.checkpw automatically extracts the salt from the hash
    # and uses it to hash the given password for comparison.
    return bcrypt.checkpw(password_bytes, hashed_password)

# --- Simulation ---

# 1. User signs up and the password needs to be stored securely.
user_password = "MyS3cr3tP@ssw0rd!"

print(f"Original Password: {user_password}")

# Hash the password for storage
start_time = time.time()
secure_hash = hash_password(user_password)
end_time = time.time()

print(f"---")
print(f"Stored Hash (bcrypt): {secure_hash.decode('utf-8')}")
print(f"Hashing Time: {end_time - start_time:.4f} seconds (shows computational expense)")
print(f"---")

# 2. User attempts to log in later.
login_attempt_1 = "MyS3cr3tP@ssw0rd!" # Correct password
login_attempt_2 = "wrongpassword"    # Incorrect password

# Check the correct password
is_correct = check_password(login_attempt_1, secure_hash)
print(f"Login Attempt with '{login_attempt_1}': {'SUCCESS' if is_correct else 'FAIL'}")

# Check the incorrect password
is_incorrect = check_password(login_attempt_2, secure_hash)
print(f"Login Attempt with '{login_attempt_2}': {'SUCCESS' if is_incorrect else 'FAIL'}")
