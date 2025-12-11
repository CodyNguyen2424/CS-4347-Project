#!/usr/bin/env python3
"""
Test script to verify all checkout requirements are working correctly.
"""
import sqlite3
from datetime import date, timedelta
import sys

def test_checkout_requirements(db_path='library.db'):
    """Test all checkout requirements"""
    print("=" * 70)
    print("TESTING CHECKOUT REQUIREMENTS")
    print("=" * 70)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get a test borrower
    borrower = cursor.execute("SELECT Card_id, Bname FROM BORROWER LIMIT 1").fetchone()
    if not borrower:
        print("❌ No borrowers found in database")
        return False
    
    card_id = borrower['Card_id']
    borrower_name = borrower['Bname']
    
    # Get an available book
    available_book = cursor.execute("""
        SELECT b.Isbn, b.Title
        FROM BOOK b
        WHERE NOT EXISTS (
            SELECT 1 FROM BOOK_LOANS bl 
            WHERE bl.Isbn = b.Isbn AND bl.Date_in IS NULL
        )
        LIMIT 1
    """).fetchone()
    
    if not available_book:
        print("❌ No available books found")
        return False
    
    isbn = available_book['Isbn']
    book_title = available_book['Title']
    
    print(f"\nTest Borrower: {borrower_name} (Card ID: {card_id})")
    print(f"Test Book: {book_title} (ISBN: {isbn})")
    print()
    
    # Test 1: Verify checkout creates proper BOOK_LOANS entry
    print("TEST 1: Checkout creates BOOK_LOANS with correct dates")
    print("-" * 70)
    
    today = date.today()
    expected_due = today + timedelta(days=14)
    
    try:
        import loans
        loan_id = loans.checkout(conn, isbn, card_id)
        
        # Verify the loan was created
        loan = cursor.execute("""
            SELECT Loan_id, Isbn, Card_id, Date_out, Due_date, Date_in
            FROM BOOK_LOANS
            WHERE Loan_id = ?
        """, (loan_id,)).fetchone()
        
        if loan:
            print(f"✅ Loan created with ID: {loan_id}")
            print(f"   - ISBN: {loan['Isbn']}")
            print(f"   - Card ID: {loan['Card_id']}")
            print(f"   - Date Out: {loan['Date_out']} (Expected: {today.isoformat()})")
            print(f"   - Due Date: {loan['Due_date']} (Expected: {expected_due.isoformat()})")
            print(f"   - Date In: {loan['Date_in']} (Should be NULL)")
            
            if loan['Date_out'] == today.isoformat():
                print("✅ Date_out is today's date")
            else:
                print("❌ Date_out is not today's date")
            
            if loan['Due_date'] == expected_due.isoformat():
                print("✅ Due_date is 14 days from today")
            else:
                print("❌ Due_date is not 14 days from today")
            
            if loan['Date_in'] is None:
                print("✅ Date_in is NULL (book is checked out)")
            else:
                print("❌ Date_in should be NULL")
        else:
            print("❌ Loan not found after creation")
            return False
    except Exception as e:
        print(f"❌ Failed to create loan: {e}")
        return False
    
    # Test 2: Verify book cannot be checked out twice
    print("\nTEST 2: Book already checked out validation")
    print("-" * 70)
    
    try:
        loans.checkout(conn, isbn, card_id)
        print("❌ Should have failed - book is already checked out")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")
    
    # Test 3: Verify max 3 loans limit
    print("\nTEST 3: Maximum 3 active loans validation")
    print("-" * 70)
    
    # Get current active loans
    active_count = cursor.execute("""
        SELECT COUNT(*) FROM BOOK_LOANS 
        WHERE Card_id = ? AND Date_in IS NULL
    """, (card_id,)).fetchone()[0]
    
    print(f"Current active loans: {active_count}")
    
    if active_count < 3:
        # Checkout more books to reach the limit
        books_needed = 3 - active_count
        print(f"Checking out {books_needed} more book(s) to reach limit...")
        
        more_books = cursor.execute("""
            SELECT b.Isbn
            FROM BOOK b
            WHERE NOT EXISTS (
                SELECT 1 FROM BOOK_LOANS bl 
                WHERE bl.Isbn = b.Isbn AND bl.Date_in IS NULL
            )
            AND b.Isbn != ?
            LIMIT ?
        """, (isbn, books_needed)).fetchall()
        
        for book in more_books:
            try:
                loans.checkout(conn, book['Isbn'], card_id)
                print(f"✅ Checked out book {book['Isbn']}")
            except Exception as e:
                print(f"❌ Failed to checkout: {e}")
    
    # Now try to checkout a 4th book
    fourth_book = cursor.execute("""
        SELECT b.Isbn
        FROM BOOK b
        WHERE NOT EXISTS (
            SELECT 1 FROM BOOK_LOANS bl 
            WHERE bl.Isbn = b.Isbn AND bl.Date_in IS NULL
        )
        LIMIT 1
    """).fetchone()
    
    if fourth_book:
        try:
            loans.checkout(conn, fourth_book['Isbn'], card_id)
            print("❌ Should have failed - borrower already has 3 loans")
        except ValueError as e:
            print(f"✅ Correctly rejected 4th loan: {e}")
    
    # Test 4: Verify unpaid fines block checkout
    print("\nTEST 4: Unpaid fines block checkout")
    print("-" * 70)
    
    # Create a fine for this borrower
    cursor.execute("""
        INSERT INTO FINES (Loan_id, Fine_amt, Paid)
        VALUES (?, 10.00, 0)
    """, (loan_id,))
    conn.commit()
    
    print("Created unpaid fine of $10.00")
    
    # Try to checkout (should fail)
    another_book = cursor.execute("""
        SELECT b.Isbn
        FROM BOOK b
        WHERE NOT EXISTS (
            SELECT 1 FROM BOOK_LOANS bl 
            WHERE bl.Isbn = b.Isbn AND bl.Date_in IS NULL
        )
        LIMIT 1
    """).fetchone()
    
    if another_book:
        # First, return one book to make room
        cursor.execute("""
            UPDATE BOOK_LOANS 
            SET Date_in = ? 
            WHERE Loan_id = ? AND Card_id = ?
        """, (today.isoformat(), loan_id, card_id))
        conn.commit()
        
        try:
            loans.checkout(conn, another_book['Isbn'], card_id)
            print("❌ Should have failed - borrower has unpaid fines")
        except ValueError as e:
            print(f"✅ Correctly blocked checkout: {e}")
    
    # Clean up - pay the fine
    cursor.execute("UPDATE FINES SET Paid = 1 WHERE Loan_id = ?", (loan_id,))
    conn.commit()
    print("✅ Fine marked as paid for cleanup")
    
    # Test 5: Verify borrower/book validation
    print("\nTEST 5: Invalid borrower/book validation")
    print("-" * 70)
    
    try:
        loans.checkout(conn, "9999999999", card_id)
        print("❌ Should have failed - invalid ISBN")
    except ValueError as e:
        print(f"✅ Correctly rejected invalid ISBN: {e}")
    
    try:
        loans.checkout(conn, isbn, 999999)
        print("❌ Should have failed - invalid Card ID")
    except ValueError as e:
        print(f"✅ Correctly rejected invalid Card ID: {e}")
    
    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)
    
    conn.close()
    return True

if __name__ == '__main__':
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'library.db'
    
    # Add parent directory to path to import loans module
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    success = test_checkout_requirements(db_path)
    sys.exit(0 if success else 1)
