#!/usr/bin/env python3
"""
Verify that users have their Card IDs properly linked for auto-checkout
"""
import sqlite3

def check_user_cards(db_path='library.db'):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=" * 70)
    print("USER CHECKOUT STATUS")
    print("=" * 70)
    
    users = cursor.execute("""
        SELECT u.Username, u.Is_admin, u.Card_id, b.Bname
        FROM USERS u
        LEFT JOIN BORROWER b ON u.Card_id = b.Card_id
        ORDER BY u.Is_admin DESC, u.Username
    """).fetchall()
    
    print("\n")
    for user in users:
        role = "👑 ADMIN" if user['Is_admin'] else "👤 User "
        
        if user['Card_id']:
            status = f"✅ Auto-checkout enabled (Card ID: {user['Card_id']}, Name: {user['Bname']})"
        else:
            status = "⚠️  Needs to link borrower account"
        
        print(f"{role} | {user['Username']:15} | {status}")
    
    print("\n" + "=" * 70)
    print("CHECKOUT BEHAVIOR")
    print("=" * 70)
    print("\n👑 ADMIN users:")
    print("  - Always prompted for Card ID (can checkout to anyone)")
    print("  - Can use multi-select checkout")
    print("\n👤 Regular users WITH linked Card ID:")
    print("  - Auto-checkout to their account (no prompt)")
    print("  - Can use multi-select checkout")
    print("\n👤 Regular users WITHOUT linked Card ID:")
    print("  - Cannot checkout (shown warning message)")
    print("  - Need to link account on Profile page first")
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'library.db'
    check_user_cards(db_path)
