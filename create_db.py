import sqlite3

# Function to create the database and table
def create_database():
    conn = sqlite3.connect('email.db')
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY,
            recipient_email TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Create the database and table if they don't exist
create_database()
