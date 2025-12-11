from datetime import date, timedelta
from typing import List, Optional

from db import db_transaction

MAX_ACTIVE_LOANS = 3

OPEN_LOANS_SELECT = """
SELECT
    bl.Loan_id,
    bl.Isbn,
    b.Title,
    bl.Card_id,
    bor.Bname,
    bl.Date_out,
    bl.Due_date
FROM BOOK_LOANS bl
JOIN BOOK b   ON bl.Isbn = b.Isbn
JOIN BORROWER bor ON bl.Card_id = bor.Card_id
"""


def checkout(conn, isbn: str, card_id: int) -> int:
    """
    Checkout a book to a borrower.
    
    Validations:
    - Book must exist
    - Borrower must exist
    - Borrower cannot have 3 or more active loans
    - Borrower cannot have unpaid fines
    - Book cannot already be checked out
    
    Returns the new Loan_id
    """
    isbn = (isbn or "").strip()
    card_id = int(card_id)
    if not isbn:
        raise ValueError("ISBN is required")

    today = date.today()
    due = today + timedelta(days=14)

    with db_transaction(conn):
        cursor = conn.cursor()

        # Check if book exists
        book = cursor.execute("SELECT Title FROM BOOK WHERE Isbn = ?", (isbn,)).fetchone()
        if not book:
            raise ValueError(f"Book with ISBN '{isbn}' not found in the system")

        # Check if borrower exists
        borrower = cursor.execute(
            "SELECT Bname FROM BORROWER WHERE Card_id = ?", 
            (card_id,)
        ).fetchone()
        if not borrower:
            raise ValueError(f"Borrower with Card ID {card_id} not found")

        # Check active loan count (max 3)
        active_loans = cursor.execute(
            "SELECT COUNT(*) FROM BOOK_LOANS WHERE Card_id = ? AND Date_in IS NULL",
            (card_id,),
        ).fetchone()[0]
        if active_loans >= MAX_ACTIVE_LOANS:
            raise ValueError(
                f"Checkout failed: {borrower['Bname']} (Card ID: {card_id}) already has "
                f"{active_loans} active loans. Maximum allowed is {MAX_ACTIVE_LOANS}."
            )

        # Check for unpaid fines
        unpaid_fines = cursor.execute(
            """
            SELECT COUNT(*), SUM(f.Fine_amt)
            FROM FINES f
            JOIN BOOK_LOANS bl ON f.Loan_id = bl.Loan_id
            WHERE bl.Card_id = ? AND f.Paid = 0
            """,
            (card_id,),
        ).fetchone()
        
        if unpaid_fines[0] > 0:
            fine_amount = unpaid_fines[1] or 0
            raise ValueError(
                f"Checkout failed: {borrower['Bname']} (Card ID: {card_id}) has "
                f"{unpaid_fines[0]} unpaid fine(s) totaling ${fine_amount:.2f}. "
                f"Please pay all fines before checking out books."
            )

        # Check if book is already checked out
        current_loan = cursor.execute(
            """
            SELECT bl.Card_id, bor.Bname, bl.Due_date
            FROM BOOK_LOANS bl
            JOIN BORROWER bor ON bl.Card_id = bor.Card_id
            WHERE bl.Isbn = ? AND bl.Date_in IS NULL
            """,
            (isbn,),
        ).fetchone()
        
        if current_loan:
            if current_loan['Card_id'] == card_id:
                raise ValueError(
                    f"Checkout failed: {borrower['Bname']} already has this book checked out "
                    f"(due {current_loan['Due_date']})"
                )
            else:
                raise ValueError(
                    f"Checkout failed: '{book['Title']}' is currently checked out by "
                    f"{current_loan['Bname']} (Card ID: {current_loan['Card_id']}) "
                    f"and is due back on {current_loan['Due_date']}"
                )

        # All validations passed - create the loan
        cursor.execute(
            """
            INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Due_date, Date_in)
            VALUES (?, ?, ?, ?, NULL)
            """,
            (isbn, card_id, today.isoformat(), due.isoformat()),
        )
        return cursor.lastrowid


def find_open_loans(
    conn,
    isbn: Optional[str] = None,
    card_id: Optional[int] = None,
    borrower_name: Optional[str] = None,
):
    isbn = (isbn or "").strip()
    borrower_name = (borrower_name or "").strip()
    conditions = ["bl.Date_in IS NULL"]
    params = []

    if isbn:
        conditions.append("LOWER(bl.Isbn) = LOWER(?)")
        params.append(isbn)
    if card_id is not None:
        conditions.append("bl.Card_id = ?")
        params.append(int(card_id))
    if borrower_name:
        conditions.append("LOWER(bor.Bname) LIKE ?")
        params.append(f"%{borrower_name.lower()}%")

    if len(conditions) == 1:
        raise ValueError("Provide at least one search parameter")

    where_clause = " WHERE " + " AND ".join(conditions)
    cursor = conn.cursor()
    cursor.execute(OPEN_LOANS_SELECT + where_clause + " ORDER BY bl.Due_date", params)
    return [dict(row) for row in cursor.fetchall()]


def checkin(conn, loan_id: int) -> None:
    loan_id = int(loan_id)
    today = date.today().isoformat()

    with db_transaction(conn):
        cursor = conn.cursor()
        row = cursor.execute(
            "SELECT Date_in FROM BOOK_LOANS WHERE Loan_id = ?",
            (loan_id,),
        ).fetchone()
        if not row:
            raise ValueError("Loan not found")
        if row["Date_in"] is not None:
            raise ValueError("Loan already closed")

        cursor.execute(
            "UPDATE BOOK_LOANS SET Date_in = ? WHERE Loan_id = ?",
            (today, loan_id),
        )

        from fines import refresh_fines
        refresh_fines(conn, loan_id=loan_id)


def checkin_multiple(conn, loan_ids: List[int]) -> None:
    """Check in 1–3 loans in a single action."""
    for loan_id in loan_ids:
        checkin(conn, loan_id)
