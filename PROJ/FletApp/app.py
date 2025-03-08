import flet as ft
import httpx  # HTTP client for FastAPI requests

API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    page.title = "Seedie Login"

    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True)
    message = ft.Text()

    def handle_register(e):
        msg = httpx.post(f"{API_URL}/register", json={"username": username.value, "password": password.value}).json()
        message.value = msg.get("message", msg.get("error", "Unknown error"))  # Show success or error message
        page.update()  # Stay on the login screen instead of auto-logging in

    def handle_login(e):
        msg = httpx.post(f"{API_URL}/login", json={"username": username.value, "password": password.value}).json()
        if "message" in msg:
            open_dashboard(page, username.value)
        else:
            message.value = msg.get("error", "Invalid credentials")
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

def assign_schedule_ui(page):
    username_field = ft.TextField(label="Volunteer Username")
    date_field = ft.TextField(label="Schedule Date (YYYY-MM-DD)")
    message = ft.Text()

    def handle_assign_schedule(e):
        msg = httpx.post(f"{API_URL}/assign-schedule", json={
            "username": username_field.value,
            "date": date_field.value
        }).json()
        message.value = msg.get("message", msg.get("error", "Unknown error"))
        page.update()

    page.clean()
    page.add(
        ft.Text("Assign Schedule to Volunteer"),
        username_field,
        date_field,
        ft.ElevatedButton("Assign Schedule", on_click=handle_assign_schedule),
        message,
        ft.ElevatedButton("Back", on_click=lambda e: open_dashboard(page, "admin"))
    )
    page.update()

def update_seed_status(page, username, seed_status, message):
    """Updates the seed status UI"""
    user_data = httpx.get(f"{API_URL}/get-user/{username}").json()
    seed_stage = user_data.get("seed_stage", 1)
    watered = user_data.get("watered", 0)
    fertilized = user_data.get("fertilized", 0)

    if seed_stage >= 3:
        seed_status.value = "🌳 Your seed is fully grown! You can now claim a new one. 🌳"
    else:
        seed_status.value = f"Seed Stage: {seed_stage} 🌱 | Watered: {watered} 💧 | Fertilized: {fertilized} 🌿"

    page.update()

def open_dashboard(page, username):
    page.clean()

    def logout(e):
        page.clean()
        main(page)

    message = ft.Text()
    seed_status = ft.Text()

    user_data = httpx.get(f"{API_URL}/get-user/{username}").json()
    seeds_claimed = user_data.get("seeds", 0)

    if username == "admin":
        users_list = ft.Text()

        def show_users(e):
            users = httpx.get(f"{API_URL}/users").json()
            users_list.value = "\n".join(user["username"] for user in users.get("users", []))
            page.update()

        page.add(
            ft.Text("Welcome, Admin!"),
            ft.ElevatedButton("Assign Schedules", on_click=lambda e: assign_schedule_ui(page)),
            ft.ElevatedButton("View Users", on_click=show_users),
            users_list,
            ft.ElevatedButton("Logout", on_click=logout)
        )
    else:
        if seeds_claimed == 0:
            # Show only the claim seed button
            def handle_claim_seed(e):
                msg = httpx.post(f"{API_URL}/claim-seed/{username}").json()
                message.value = msg.get("message", msg.get("error", "Something went wrong"))
                open_dashboard(page, username)  # Refresh UI after claiming

            page.add(
                ft.Text(f"Welcome {username}!"),
                ft.Text("You need to claim your first seed before growing it."),
                ft.ElevatedButton("Claim Your Seed 🌱", on_click=handle_claim_seed),
                message,
                ft.ElevatedButton("Logout", on_click=logout)
            )
        else:
            update_seed_status(page, username, seed_status, message)

            def handle_water(e):
                msg = httpx.post(f"{API_URL}/water-seed/{username}").json()
                message.value = msg["message"]
                update_seed_status(page, username, seed_status, message)

            def handle_fertilize(e):
                msg = httpx.post(f"{API_URL}/fertilize-seed/{username}").json()
                message.value = msg["message"]
                update_seed_status(page, username, seed_status, message)

            page.add(
                ft.Text(f"Welcome {username}!"),
                seed_status,
                ft.ElevatedButton("Water Your Seed 💧", on_click=handle_water),
                ft.ElevatedButton("Fertilize Your Seed 🌿", on_click=handle_fertilize),
                message,
                ft.ElevatedButton("Logout", on_click=logout)
            )

    page.update()

ft.app(target=main)
