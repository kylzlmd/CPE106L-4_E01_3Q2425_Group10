import flet as ft
import httpx  # HTTP client for FastAPI requests



API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    logo = ft.Container(
            content=ft.Image(src="logo.png", width=150, height=150),
            border_radius=ft.border_radius.all(75), 
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
    page.title = "Seedie"

    title = ft.Text("Welcome to Seedie! 🌱", color=ft.colors.GREEN, size=24, weight=ft.FontWeight.BOLD)

    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True)
    message = ft.Text()


    

    def handle_register(e):
        msg = httpx.post(f"{API_URL}/register", json={"username": username.value, "password": password.value}).json()
        message.value = msg.get("message", msg.get("error", "Unknown error"))
        page.update()

    def handle_login(e):
        msg = httpx.post(f"{API_URL}/login", json={"username": username.value, "password": password.value}).json()
        if "message" in msg:
            open_dashboard(page, username.value)
        else:
            message.value = msg.get("error", "Invalid credentials")
            page.update()

    page.add(
            ft.Column(
                [logo, title, username, password, 
                 ft.Row([
                    ft.ElevatedButton("Register", on_click=handle_register),
                    ft.ElevatedButton("Login", on_click=handle_login),
                 ]),
                 message
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

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

def update_seed_status(page, username, seed_status, message, claim_seed_button, seeds_claimed_text):
    user_data = httpx.get(f"{API_URL}/get-user/{username}").json()
    seed_stage = user_data.get("seed_stage", 1)
    seeds_claimed = user_data.get("seeds", 0)

    seed_status.value = f"🌱 Seed Stage: {seed_stage}/3"
    seeds_claimed_text.value = f"🪴 Total Seeds Claimed: {seeds_claimed}"

    if seed_stage >= 3:
        def handle_claim_seed(e):
            msg = httpx.post(f"{API_URL}/claim-seed/{username}").json()
            message.value = msg.get("message", msg.get("error", "Something went wrong"))
            open_dashboard(page, username)

        claim_seed_button.content = ft.ElevatedButton("Claim a New Seed 🌱", on_click=handle_claim_seed)
    else:
        claim_seed_button.content = None  

    page.update()

def plot_all_gardens(page, sort_by_species=True):
    # Get all plants data from the backend
    url = f"{API_URL}/get-all-plants-by-species" if sort_by_species else f"{API_URL}/get-all-plants-by-color"
    plants = httpx.get(url).json()
    sorted_plants = plants.get("plants", [])

    # Create the garden plot (grid of color boxes)
    garden_grid = ft.Row([], wrap=True, alignment=ft.MainAxisAlignment.CENTER)

    # Color mapping for visualization
    color_map = {
        "red": ft.colors.RED,
        "orange": ft.colors.ORANGE,
        "yellow": ft.colors.YELLOW,
        "green": ft.colors.GREEN,
        "blue": ft.colors.BLUE,
        "violet": ft.colors.PURPLE
    }

    # First occurrence of each plant's color or species
    first_row = []
    color_positions = {}
    color_counts = {}

    for p in sorted_plants:
        key = p["species"] if sort_by_species else p["color"].lower()

        # Add to the first row if it hasn't been added before
        if key not in color_positions:
            color_positions[key] = len(first_row)
            first_row.append(
                ft.Tooltip(
                    message=p["species"],  # Show plant species on hover
                    content=ft.Container(
                        width=30, height=30, bgcolor=color_map.get(p["color"].lower(), ft.colors.GREY), border_radius=5
                    )
                )
            )

        color_counts[key] = color_counts.get(key, 0) + 1  # Count occurrences of each color or species

    # Calculate extra rows for duplicate plants
    max_duplicates = max(color_counts.values()) - 1
    extra_rows = [[None] * len(first_row) for _ in range(max(1, max_duplicates))]

    # Fill extra rows with duplicates
    color_used = {key: 0 for key in color_positions}
    for p in sorted_plants:
        key = p["species"] if sort_by_species else p["color"].lower()
        if color_used[key] == 0:
            color_used[key] += 1
            continue

        row_index = color_used[key] - 1
        col_index = color_positions[key]

        if row_index < len(extra_rows):
            extra_rows[row_index][col_index] = ft.Tooltip(
                message=p["species"],
                content=ft.Container(width=30, height=30, bgcolor=color_map.get(p["color"].lower(), ft.colors.GREY), border_radius=5)
            )

        color_used[key] += 1

    # Create rows from extra rows data
    extra_rows_ui = [
        ft.Row([cell if cell else ft.Container(width=30, height=30) for cell in row], alignment=ft.MainAxisAlignment.CENTER)
        for row in extra_rows if any(cell for cell in row)
    ]

    # Create the garden grid
    garden_grid.controls = [
        ft.Row(first_row, alignment=ft.MainAxisAlignment.CENTER),
        *extra_rows_ui
    ]

    # Replace the old plot with the new one without clearing the whole screen
    garden_plot = ft.Text()  # Or use a placeholder for your plot if needed
    if hasattr(page, 'garden_plot'):  # Check if the plot already exists
        page.garden_plot.controls = garden_grid.controls  # Replace the plot controls
        page.garden_plot.update()
    else:
        page.garden_plot = garden_grid
        page.add(page.garden_plot)  # Add the new plot if it doesn't exist

    page.update()


garden_plot = ft.Text()


def open_dashboard(page, username):
    page.clean()

    def logout(e):
        page.clean()
        main(page)

    message = ft.Text()
    seed_status = ft.Text()
    claim_seed_button = ft.Container()
    seeds_claimed_text = ft.Text()
    plants_list = ft.Text()
    weather_text = ft.Text()

    user_data = httpx.get(f"{API_URL}/get-user/{username}").json()
    seeds_claimed = user_data.get("seeds", 0)
    seed_stage = user_data.get("seed_stage", 1)

    def show_plants(e):
        plants = httpx.get(f"{API_URL}/get-plants/{username}").json()
        if "plants" in plants and plants["plants"]:
            plants_list.value = "\n".join(f"{p['color']} {p['species']}" for p in plants["plants"])
        else:
            plants_list.value = "🌱 You haven't grown any plants yet!"
        page.update()

    def show_weather():
        location = "Manila"
        weather = httpx.get(f"{API_URL}/get-weather/{location}").json()
        if "error" in weather:
            weather_text.value = "Weather data unavailable"
        else:
            weather_text.value = f"🌤️ Current Weather: {weather['temperature']}°C, {weather['condition']}"
        page.update()

    # GARDEN PLOT CONTAINER
    garden_grid = ft.Row([], wrap=True, alignment=ft.MainAxisAlignment.CENTER)

    def show_garden_plot(e, sort_by_species=False):
        plants = httpx.get(f"{API_URL}/get-plants/{username}").json()

        if "plants" not in plants or not plants["plants"]:
            garden_grid.controls = [ft.Text("🌱 No plants yet! Grow a seed first.")]
        else:
            color_map = {
                "red": ft.colors.RED,
                "orange": ft.colors.ORANGE,
                "yellow": ft.colors.YELLOW,
                "green": ft.colors.GREEN,
                "blue": ft.colors.BLUE,
                "violet": ft.colors.PURPLE
            }

            # Sort plants in ROYGBIV order by default (for color sort)
            color_order = ["red", "orange", "yellow", "green", "blue", "violet"]
            sorted_plants = sorted(plants["plants"], key=lambda p: color_order.index(p["color"].lower()))

            if sort_by_species:
                # Sort plants by species alphabetically
                sorted_plants = sorted(sorted_plants, key=lambda p: p["species"].lower())

            # Build the first row with sorted plants
            first_row = []
            color_positions = {}  # Track where each color or species appears in the first row
            color_counts = {}  # Track occurrences of each color or species

            for p in sorted_plants:
                key = p["species"] if sort_by_species else p["color"].lower()

                # First occurrence of each color or species
                if key not in color_positions:
                    color_positions[key] = len(first_row)
                    first_row.append(
                        ft.Tooltip(
                            message=p["species"],  # Show plant species on hover
                            content=ft.Container(
                                width=30, height=30, bgcolor=color_map.get(p["color"].lower(), ft.colors.GREY), border_radius=5
                            )
                        )
                    )

                color_counts[key] = color_counts.get(key, 0) + 1  # Count occurrences

            # Determine extra rows if needed
            max_duplicates = max(color_counts.values()) - 1
            extra_rows = [[None] * len(first_row) for _ in range(max(1, max_duplicates))]

            # Fill in extra rows with duplicates under the correct column
            color_used = {key: 0 for key in color_positions}
            for p in sorted_plants:
                key = p["species"] if sort_by_species else p["color"].lower()
                if color_used[key] == 0:
                    color_used[key] += 1
                    continue

                row_index = color_used[key] - 1
                col_index = color_positions[key]

                if row_index < len(extra_rows):
                    extra_rows[row_index][col_index] = ft.Tooltip(
                        message=p["species"],
                        content=ft.Container(width=30, height=30, bgcolor=color_map.get(p["color"].lower(), ft.colors.GREY), border_radius=5)
                    )

                color_used[key] += 1

            # Update the UI with the rows
            extra_rows_ui = [
                ft.Row([cell if cell else ft.Container(width=30, height=30) for cell in row], alignment=ft.MainAxisAlignment.CENTER)
                for row in extra_rows if any(cell for cell in row)
            ]

            garden_grid.controls = [
                ft.Row(first_row, alignment=ft.MainAxisAlignment.CENTER),
                *extra_rows_ui
            ]
        
        page.update()

    if username == "admin":
        users_list = ft.Text()
    
        def show_users(e):
            users = httpx.get(f"{API_URL}/users").json()
            users_list.value = "\n".join(user["username"] for user in users.get("users", []))
            page.update()
    
        # Function to plot garden for all users, sorted by species or color
        
        
        
    
        garden_plot = ft.Text()  # Text container to show the garden plot
    
        page.add(
                    ft.Text("Welcome, Admin!"),
                    ft.ElevatedButton("📅 Assign Schedules", on_click=lambda e: assign_schedule_ui(page)),
                    ft.ElevatedButton("📋 View Users", on_click=show_users),
                    ft.ElevatedButton("Plot All Gardens by Species 🐝", on_click=lambda e: plot_all_gardens(page, sort_by_species=True)),
                    ft.ElevatedButton("Plot All Gardens by Color 🎨", on_click=lambda e: plot_all_gardens(page, sort_by_species=False)),
                    users_list,
                    ft.ElevatedButton("🚪 Logout", on_click=logout)
                )
    else:
        show_weather()

        if seeds_claimed == 0:
            def handle_claim_seed(e):
                msg = httpx.post(f"{API_URL}/claim-seed/{username}").json()
                message.value = msg.get("message", msg.get("error", "Something went wrong"))
                open_dashboard(page, username)

            page.add(
                ft.Text(f"Welcome, {username}!", size=28, weight=ft.FontWeight.BOLD),
                weather_text,
                ft.Text("You need to claim your first seed before growing it."),
                ft.ElevatedButton("Claim Your Seed 🌱", on_click=handle_claim_seed),
                message,
                ft.ElevatedButton("🚪 Logout", on_click=logout)
            )
        else:
            update_seed_status(page, username, seed_status, message, claim_seed_button, seeds_claimed_text)

            def handle_water(e):
                msg = httpx.post(f"{API_URL}/water-seed/{username}").json()
                message.value = msg["message"]
                update_seed_status(page, username, seed_status, message, claim_seed_button, seeds_claimed_text)

            def handle_fertilize(e):
                msg = httpx.post(f"{API_URL}/fertilize-seed/{username}").json()
                message.value = msg["message"]
                update_seed_status(page, username, seed_status, message, claim_seed_button, seeds_claimed_text)

            page.add(
                ft.Text(f"Welcome, {username}!", size=28, weight=ft.FontWeight.BOLD),
                weather_text,
                seeds_claimed_text,
                seed_status,
                ft.Row([
                    ft.ElevatedButton("Water Seed 💧", on_click=handle_water),
                    ft.ElevatedButton("Fertilize Seed 🌿", on_click=handle_fertilize),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=10),
                ft.ElevatedButton("View My Plants 🌿", on_click=show_plants),
                plants_list,
                garden_grid,
                message,
                claim_seed_button,
                ft.ElevatedButton("Plot Garden by Species 🐝", on_click=lambda e: show_garden_plot(e, sort_by_species=True)),
                ft.ElevatedButton("Plot Garden by Color 🎨", on_click=lambda e: show_garden_plot(e, sort_by_species=False)),
                ft.ElevatedButton("Logout", on_click=logout)
            )

    page.update()



        
    

ft.app(target=main)
