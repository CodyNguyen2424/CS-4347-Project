#!/usr/bin/env python3
"""
Migration script to add Is_admin column to USERS table
"""
import sqlite3
import sys

def migrate_database(db_path='library.db'):
    """Add Is_admin column to existing USERS table"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if Is_admin column already exists
        cursor.execute("PRAGMA table_info(USERS)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'Is_admin' in columns:
            print("✓ Is_admin column already exists")
        else:
            print("Adding Is_admin column to USERS table...")
            cursor.execute("""
                ALTER TABLE USERS 
                ADD COLUMN Is_admin INTEGER NOT NULL DEFAULT 0 CHECK (Is_admin IN (0, 1))
            """)
            conn.commit()
            print("✓ Is_admin column added successfully")
        
        # Set admin user to have admin privileges
        cursor.execute("UPDATE USERS SET Is_admin = 1 WHERE Username = 'admin'")
        rows_updated = cursor.rowcount
        conn.commit()
        
        if rows_updated > 0:
            print(f"✓ Set admin privileges for 'admin' user")
        else:
            print("ℹ No 'admin' user found to update")
        
        # Show current users and their admin status
        cursor.execute("SELECT Username, Is_admin FROM USERS")
        users = cursor.fetchall()
        
        if users:
            print("\nCurrent users:")
            for username, is_admin in users:
                admin_badge = "👑 Admin" if is_admin else "User"
                print(f"  - {username}: {admin_badge}")
        
        conn.close()
        print("\n✅ Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == '__main__':
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'library.db'
    success = migrate_database(db_path)
    sys.exit(0 if success else 1)
