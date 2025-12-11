#!/usr/bin/env python3
"""
Script to create an admin user
"""
import sqlite3
from werkzeug.security import generate_password_hash

def create_admin_user(db_path='library.db', username='admin', password='admin'):
    """Create an admin user"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT Username, Is_admin FROM USERS WHERE Username = ?", (username,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"User '{username}' already exists")
            if existing[1] == 1:
                print(f"✓ '{username}' already has admin privileges")
            else:
                # Update to admin
                cursor.execute("UPDATE USERS SET Is_admin = 1 WHERE Username = ?", (username,))
                conn.commit()
                print(f"✓ Updated '{username}' to admin")
        else:
            # Create new admin user
            password_hash = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO USERS (Username, Password, Card_id, Is_admin) VALUES (?, ?, NULL, 1)",
                (username, password_hash)
            )
            conn.commit()
            print(f"✓ Created admin user '{username}' with password '{password}'")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        return False

if __name__ == '__main__':
    import sys
    username = sys.argv[1] if len(sys.argv) > 1 else 'admin'
    password = sys.argv[2] if len(sys.argv) > 2 else 'admin'
    create_admin_user(username=username, password=password)
