import hashlib
import json
import os
import getpass  # Importing getpass to hide password input

class User:
    volunteer_id_counter = 1
    
    def __init__(self, username, password, role):
        self.username = username
        self.password = self.hash_password(password)
        self.role = role
        self.volunteer_id = None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self):
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []
        
        if self.role == "volunteer":
            self.volunteer_id = User.volunteer_id_counter
            User.volunteer_id_counter += 1
            user_data = {"username": self.username, "password": self.password, "role": self.role, "volunteer_id": self.volunteer_id, "approved": False}
        else:
            user_data = {"username": self.username, "password": self.password, "role": self.role}
        
        users.append(user_data)
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)
        return True

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
