import sqlite3

def main():
    db_path = "PPA_DB_LR5.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM GUIDE;")
    guides = cursor.fetchall()
    print("\nGUIDE Table Data:")
    for guide in guides:
        print(guide)
    
    cursor.execute("SELECT * FROM CUSTOMER;")
    customers = cursor.fetchall()
    print("\nCUSTOMER Table Data:")
    for customer in customers:
        print(customer)
    
    cursor.execute("SELECT * FROM RESERVATION;")
    reservations = cursor.fetchall()
    print("\nRESERVATION Table Data:")
    for reservation in reservations:
        print(reservation)
    
    cursor.execute("SELECT * FROM TRIP;")
    trips = cursor.fetchall()
    print("\nTRIP Table Data:")
    for trip in trips:
        print(trip)
    
    cursor.execute("SELECT * FROM TRIP_GUIDES;")
    trip_guides = cursor.fetchall()
    print("\nTRIP_GUIDES Table Data:")
    for trip_guide in trip_guides:
        print(trip_guide)
    
    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()
