#!/usr/bin/env python3
"""
Create test data: overdue book loan with fines for Card ID 1003
"""
import sqlite3
from datetime import date, timedelta

def create_overdue_loan_with_fine(db_path='library.db', card_id=1003):
    """Create an overdue loan with calculated fine"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=" * 70)
    print("CREATING TEST DATA: OVERDUE LOAN WITH FINE")
    print("=" * 70)
    
    # Get borrower info
    borrower = cursor.execute(
        "SELECT Card_id, Bname FROM BORROWER WHERE Card_id = ?",
        (card_id,)
    ).fetchone()
    
    if not borrower:
        print(f"❌ Borrower with Card ID {card_id} not found")
        conn.close()
        return False
    
    print(f"\n📋 Borrower: {borrower['Bname']} (Card ID: {card_id})")
    
    # Get an available book
    book = cursor.execute("""
        SELECT b.Isbn, b.Title
        FROM BOOK b
        WHERE NOT EXISTS (
            SELECT 1 FROM BOOK_LOANS bl 
            WHERE bl.Isbn = b.Isbn AND bl.Date_in IS NULL
        )
        LIMIT 1
    """).fetchone()
    
    if not book:
        print("❌ No available books found")
        conn.close()
        return False
    
    print(f"📚 Book: {book['Title']} (ISBN: {book['Isbn']})")
    
    # Create an overdue loan (checked out 20 days ago, due 6 days ago)
    today = date.today()
    date_out = today - timedelta(days=20)  # Checked out 20 days ago
    due_date = date_out + timedelta(days=14)  # Due 14 days after checkout (6 days ago)
    days_overdue = (today - due_date).days
    
    print(f"\n📅 Loan Details:")
    print(f"   - Date Out: {date_out.isoformat()}")
    print(f"   - Due Date: {due_date.isoformat()}")
    print(f"   - Today: {today.isoformat()}")
    print(f"   - Days Overdue: {days_overdue}")
    
    # Create the loan (not returned yet)
    cursor.execute("""
        INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Due_date, Date_in)
        VALUES (?, ?, ?, ?, NULL)
    """, (book['Isbn'], card_id, date_out.isoformat(), due_date.isoformat()))
    
    loan_id = cursor.lastrowid
    print(f"\n✅ Created loan with ID: {loan_id}")
    
    # Calculate fine ($0.25 per day)
    fine_amount = days_overdue * 0.25
    
    # Create the fine
    cursor.execute("""
        INSERT INTO FINES (Loan_id, Fine_amt, Paid)
        VALUES (?, ?, 0)
    """, (loan_id, fine_amount))
    
    print(f"💰 Created fine: ${fine_amount:.2f} ({days_overdue} days × $0.25/day)")
    print(f"   - Status: UNPAID")
    
    conn.commit()
    
    # Show summary
    print("\n" + "=" * 70)
    print("TEST DATA CREATED SUCCESSFULLY")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"   - Borrower: {borrower['Bname']} (Card ID: {card_id})")
    print(f"   - Book: {book['Title']}")
    print(f"   - Loan ID: {loan_id}")
    print(f"   - Days Overdue: {days_overdue}")
    print(f"   - Fine Amount: ${fine_amount:.2f}")
    print(f"   - Fine Status: UNPAID")
    
    print(f"\n🧪 Test Scenarios:")
    print(f"   1. Login as user with Card ID {card_id}")
    print(f"   2. Go to Profile page")
    print(f"   3. See overdue loan in 'My Active Loans'")
    print(f"   4. See unpaid fine in 'Outstanding Fines'")
    print(f"   5. Try to checkout another book (should fail - unpaid fines)")
    print(f"   6. Return the book to see fine persist")
    print(f"   7. Admin can pay the fine from Fines page")
    
    # Get username for this card_id
    user = cursor.execute(
        "SELECT Username FROM USERS WHERE Card_id = ?",
        (card_id,)
    ).fetchone()
    
    if user:
        print(f"\n🔑 Login Credentials:")
        print(f"   - Username: {user['Username']}")
        print(f"   - (Use your password)")
    
    print("\n" + "=" * 70)
    
    conn.close()
    return True

if __name__ == '__main__':
    import sys
    
    card_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1003
    db_path = sys.argv[2] if len(sys.argv) > 2 else 'library.db'
    
    success = create_overdue_loan_with_fine(db_path, card_id)
    sys.exit(0 if success else 1)
