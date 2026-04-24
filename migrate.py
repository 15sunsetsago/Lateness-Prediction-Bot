import json
import sqlite3

def migrate():
    # 1. Open the old JSON-formatted .dat file
    try:
        with open("event_data.dat", "r") as f:
            old_data = json.load(f)
    except FileNotFoundError:
        print("❌ Could not find event_data.dat")
        return

    # 2. Connect to your new SQL database
    conn = sqlite3.connect("events.db")
    c = conn.cursor()

    # 3. Create the table structure if it's not there
    c.execute('''CREATE TABLE IF NOT EXISTS events 
                 (user_id TEXT, name TEXT, time TEXT, lateness INTEGER, started INTEGER)''')

    count = 0
    # 4. Loop through the old dictionary structure
    # Structure: { "user_id": { "events": [...] } }
    for user_id, content in old_data.items():
        for e in content.get("events", []):
            # Map old keys to new SQL columns
            name = e.get("name")
            timestamp = e.get("datetime")
            lateness = e.get("lateness")
            # SQL doesn't have 'True/False', so we use 1 or 0
            started = 1 if e.get("started") else 0

            c.execute("INSERT INTO events (user_id, name, time, lateness, started) VALUES (?, ?, ?, ?, ?)", 
                      (user_id, name, timestamp, lateness, started))
            count += 1

    conn.commit()
    conn.close()
    print(f"✅ Success! Moved {count} events into the SQL database.")

if __name__ == "__main__":
    migrate()