import sqlite3

# Create a new database for chat history
DB_NAME = 'chat_history.db'

def setup_chat_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create table for chat sessions
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_data TEXT,
            diagnosis TEXT,
            confidence REAL
        )
    ''')
    
    # Create table for individual messages
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            message_type TEXT NOT NULL,
            message_content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Chat history database created successfully!")

if __name__ == '__main__':
    setup_chat_database()
