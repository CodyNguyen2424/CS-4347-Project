from werkzeug.security import generate_password_hash, check_password_hash
from db import db_transaction

def create_user(conn, username: str, password: str, card_id: int = None) -> int:
    """Create a new user with hashed password."""
    username = (username or "").strip()
    password = (password or "").strip()
    
    if not username or not password:
        raise ValueError("Username and password are required")
    
    if len(password) < 4:
        raise ValueError("Password must be at least 4 characters")
    
    password_hash = generate_password_hash(password)
    
    with db_transaction(conn):
        # Check if username already exists
        if conn.execute("SELECT 1 FROM USERS WHERE Username = ?", (username,)).fetchone():
            raise ValueError("Username already exists")
        
        cursor = conn.execute(
            "INSERT INTO USERS (Username, Password, Card_id) VALUES (?, ?, ?)",
            (username, password_hash, card_id)
        )
        return cursor.lastrowid

def verify_user(conn, username: str, password: str) -> bool:
    """Verify user credentials."""
    username = (username or "").strip()
    password = (password or "").strip()
    
    if not username or not password:
        return False
    
    row = conn.execute(
        "SELECT Password FROM USERS WHERE Username = ?",
        (username,)
    ).fetchone()
    
    if not row:
        return False
    
    return check_password_hash(row['Password'], password)

def get_user_info(conn, username: str) -> dict:
    """Get user information including borrower details."""
    row = conn.execute(
        """
        SELECT u.User_id, u.Username, u.Card_id, b.Bname, b.Ssn, b.Address, b.Phone
        FROM USERS u
        LEFT JOIN BORROWER b ON u.Card_id = b.Card_id
        WHERE u.Username = ?
        """,
        (username,)
    ).fetchone()
    
    return dict(row) if row else None

def initialize_default_user(conn):
    """Create default admin user if no users exist. Creates USERS table if needed."""
    try:
        # Try to create the USERS table if it doesn't exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                User_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                Username  VARCHAR(50) NOT NULL UNIQUE,
                Password  VARCHAR(255) NOT NULL,
                Card_id   INTEGER,
                Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (Card_id) REFERENCES BORROWER(Card_id)
            )
        """)
        conn.commit()
        
        count = conn.execute("SELECT COUNT(*) FROM USERS").fetchone()[0]
        if count == 0:
            create_user(conn, 'admin', 'admin', card_id=None)
            print("Created default admin user (username: admin, password: admin)")
    except Exception as e:
        print(f"Could not initialize users: {e}")

