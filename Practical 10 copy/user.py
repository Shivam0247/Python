import hashlib
import os
import json
import getpass

# Path to user data file
user_data_file = r"/Users/patelshivam/Documents/PythonLab/Practical 10/users.json"

# Initialize the users file if it doesn't exist
if not os.path.exists(user_data_file):
    with open(user_data_file, 'w') as file:
        json.dump({}, file)

# Hash a password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load existing user data with error handling
def load_users():
    try:
        with open(user_data_file, 'r') as file:
            users = json.load(file)
        return users
    except json.JSONDecodeError:
        print("Error loading JSON data. The file format might be incorrect.")
        return {}

# Register a new user
def register_user(username, password):
    users = load_users()
    
    if username in users:
        print("Username already exists. Please choose a different username.")
        return False
    
    # Hash the password and save the user data
    hashed_password = hash_password(password)
    users[username] = {"password": hashed_password}

    # Save the updated user data back to the file
    with open(user_data_file, 'w') as file:
        json.dump(users, file)

    print("User registered successfully.")
    return True

# User login
def login_user(username, password):
    users = load_users()

    if username not in users:
        print("Username not found. Please register first.")
        return False

    hashed_password = hash_password(password)
    if users[username]["password"] == hashed_password:
        print("Login successful.")
        return True
    else:
        print("Incorrect password.")
        return False

# Command-line interface for user actions
def main():
    print("Welcome to the Task Management System")
    while True:
        print("\nOptions:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter a username: ")
            password = getpass.getpass("Enter a password: ")
            register_user(username, password)
        elif choice == "2":
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            login_user(username, password)
        elif choice == "3":
            print("Exiting the Task Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
