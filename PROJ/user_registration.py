import hashlib
import json
import os
import getpass  # Importing getpass to hide password input

class User:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = self.load_users()  # Load existing users if the file exists

    def hash_password(self, password):
        """Hashes the password using SHA-256 for security."""
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        """Loads user data from the JSON file if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file)
        return {}

    def save_users(self):
        """Saves the user data to a JSON file."""
        with open(self.filename, "w") as file:
            json.dump(self.users, file, indent=4)

    def register(self, username, password, email):
        """Registers a new user with a hashed password and saves to a file."""
        if username in self.users:
            return "Error: Username already exists!"
        
        self.users[username] = {
            "email": email,
            "password": self.hash_password(password)  # Store hashed password
        }
        self.save_users()  # Save the updated user list
        return f"User {username} registered successfully!"

# Create an instance of User class
user_system = User()

# Interactive User Input
print("🔹 Welcome to the Volunteer Registration System 🔹")

while True:
    print("\n--- Register a New User ---")
    username = input("Enter a username: ")
    password = getpass.getpass("Enter a password: ")  # Hidden password input
    email = input("Enter an email: ")

    # Register the user and print result
    print(user_system.register(username, password, email))

    # Ask if they want to register another user
    another = input("Do you want to register another user? (yes/no): ").strip().lower()
    if another != "yes":
        break
