import hashlib
import json
import getpass
import os

class LoginSystem:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = self.load_users()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file)
        return {}

    def login(self, username, password):
        if username in self.users and self.users[username]["password"] == self.hash_password(password):
            print("Login successful!\n")
        else:
            print("Invalid credentials. Please try again.")

login_system = LoginSystem()

print("Login")
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")
login_system.login(username, password)
