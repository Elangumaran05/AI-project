import sqlite3

try:
    # Connects to or creates a database file
    conn = sqlite3.connect('predictions.db')
    
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    
    # Use the cursor to create a table
    c.execute('''
        CREATE TABLE predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregnancies REAL,
            glucose REAL,
            bp REAL,
            skin REAL,
            insulin REAL,
            bmi REAL,
            dpf REAL,
            age REAL,
            diagnosis TEXT,
            confidence REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Save (commit) the changes
    conn.commit()
    conn.close()
    
    print("Database 'predictions.db' created successfully.")
except sqlite3.OperationalError:
    print("Database table already exists.")
except Exception as e:
    print(f"An error occurred: {e}")