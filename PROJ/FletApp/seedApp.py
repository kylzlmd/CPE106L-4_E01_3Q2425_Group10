import flet as ft
from pymongo import MongoClient

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://jom:jom123@irricluster.dkeaq.mongodb.net/?retryWrites=true")
db = client["RandomSeedSystem"]  # Change to your preferred database name
users_collection = db["users"]

# Ensure admin user exists
if not users_collection.find_one({"username": "admin"}):
    users_collection.insert_one({"username": "admin", "password": "123456"})

def register_user(username, password):
    if users_collection.find_one({"username": username}):
        return "Username already exists!"
    users_collection.insert_one({"username": username, "password": password})
    return "Registration successful!"

def login_user(username, password):
    return users_collection.find_one({"username": username, "password": password})

def view_registered_users():
    users = users_collection.find({}, {"_id": 0, "username": 1})
    return [user["username"] for user in users]

def open_dashboard(page, username):
    page.clean()
    
    def logout(e):
        main(page)
    
    if username == "admin":
        page.add(ft.Text("Welcome, Admin!"))
        
        def show_users(e):
            users_list.value = "\n".join(view_registered_users())
            page.update()
        
        users_list = ft.Text()
        page.add(ft.ElevatedButton("View All Users", on_click=show_users), users_list)
    else:
        page.add(ft.Text("Congratulations for Registering! Here is your first seed to start your journey"))
        page.add(ft.ElevatedButton("Claim Your Seed", on_click=lambda e: None))
    
    page.add(ft.ElevatedButton("Logout", on_click=logout))
    page.update()

def main(page: ft.Page):
    page.clean()
    page.title = "Login & Register"
    
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True)
    message = ft.Text()
    
    def handle_register(e):
        msg = register_user(username.value, password.value)
        message.value = msg
        page.update()
    
    def handle_login(e):
        user = login_user(username.value, password.value)
        if user:
            open_dashboard(page, username.value)
        else:
            message.value = "Invalid credentials."
            page.update()
    
    page.add(
        username,
        password,
        ft.Row([
            ft.ElevatedButton("Register", on_click=handle_register),
            ft.ElevatedButton("Login", on_click=handle_login),
        ]),
        message
    )
    page.update()

ft.app(target=main)
