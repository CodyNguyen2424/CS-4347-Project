#!/usr/bin/env python3
"""
List all users and their admin status
"""
import sqlite3

def list_users(db_path='library.db'):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=" * 70)
    print("USER ACCOUNTS")
    print("=" * 70)
    
    users = cursor.execute("""
        SELECT Username, Is_admin, Card_id, Created_at
        FROM USERS
        ORDER BY Is_admin DESC, Username
    """).fetchall()
    
    if not users:
        print("No users found in database")
        return
    
    print(f"\nTotal users: {len(users)}\n")
    
    for user in users:
        role = "👑 ADMIN" if user['Is_admin'] else "👤 User"
        card_info = f"Card ID: {user['Card_id']}" if user['Card_id'] else "No card linked"
        
        print(f"{role:12} | {user['Username']:20} | {card_info}")
    
    print("\n" + "=" * 70)
    print("ADMIN LOGIN CREDENTIALS")
    print("=" * 70)
    print("Username: admin")
    print("Password: admin")
    print("\nAccess at: http://127.0.0.1:5000")
    print("=" * 70)
    
    conn.close()

if __name__ == '__main__':
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'library.db'
    list_users(db_path)
