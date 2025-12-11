# Complete Requirements Compliance Checklist

## 1. Graphical User Interface (GUI) and Overall Design [20 points]

### ✅ REQUIREMENT: GUI for all database interactions
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
- Flask web application with HTML templates
- All database operations through web interface
- No command-line required for normal operations

**Evidence:**
- `app.py`: Flask routes for all operations
- `templates/`: HTML pages for all features
- SQLite connector via `sqlite3` module

### ✅ REQUIREMENT: Intuitive usability
**Status:** ✅ **FULLY IMPLEMENTED**

**Features:**
- Clear navigation menu
- Role-based interface (admin vs user)
- Flash messages for feedback
- Consistent design patterns
- Search, checkout, return all via GUI

---

## 2. Book Search and Availability [20 points]

### ✅ REQUIREMENT: Search by ISBN, title, and/or author
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# app.py lines 218-222
if query:
    where_conditions.append("(LOWER(b.Isbn) LIKE ? OR LOWER(b.Title) LIKE ? OR LOWER(a.Name) LIKE ?)")
    search_term = f"%{query.lower()}%"
    params.extend([search_term, search_term, search_term])
```

### ✅ REQUIREMENT: Single text search field
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```html
<!-- search.html line 11 -->
<input type="text" name="q" class="form-control" 
       placeholder="Search by Title, Author, or ISBN...">
```

### ✅ REQUIREMENT: Case insensitive
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# Uses LOWER() in SQL query
LOWER(b.Isbn) LIKE ? OR LOWER(b.Title) LIKE ? OR LOWER(a.Name) LIKE ?
```

### ✅ REQUIREMENT: Substring matching
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# Uses % wildcards for substring matching
search_term = f"%{query.lower()}%"
```

### ⚠️ REQUIREMENT: Five column table display
**Required Columns:**
1. ISBN
2. Book title
3. Book author(s) (comma separated)
4. Book availability (checked out?)
5. Borrower ID (if checked out)

**Status:** ⚠️ **PARTIALLY IMPLEMENTED - Missing Borrower ID column**

**Current Implementation (4 columns):**
```html
<!-- search.html -->
<th>ISBN</th>
<th>Title</th>
<th>Authors</th>
<th>Status</th>  <!-- Shows IN/OUT -->
<th>Action</th>
```

**What's Missing:**
- Borrower ID column not displayed
- Need to show Card_id when book is checked out

**Fix Needed:** Add Borrower ID column to search results

---

## 3. Book Loans [20 points]

### Checking Out Books

### ✅ REQUIREMENT: Select book by ISBN or from search results
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
- Checkout button on each search result
- Multi-select checkboxes for batch checkout
- Prompts for Card ID (or auto-uses user's Card ID)

### ✅ REQUIREMENT: Prompt for Card_no
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```javascript
// search.html - prompts admin for Card ID
const cardId = prompt("Enter Borrower Card ID to checkout:");
// Auto-uses user's Card ID for regular users
```

### ✅ REQUIREMENT: Create BOOK_LOANS tuple
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# loans.py lines 67-74
cursor.execute(
    """
    INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Due_date, Date_in)
    VALUES (?, ?, ?, ?, NULL)
    """,
    (isbn, card_id, today.isoformat(), due.isoformat()),
)
```

### ✅ REQUIREMENT: Auto-generate unique primary key
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```sql
-- schema.sql line 28
Loan_id INTEGER PRIMARY KEY AUTOINCREMENT
```

### ✅ REQUIREMENT: date_out defaults to today
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# loans.py line 29
today = date.today()
```

### ✅ REQUIREMENT: due_date is 14 days after date_out
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# loans.py line 30
due = today + timedelta(days=14)
```

### ✅ REQUIREMENT: Maximum 3 active loans per borrower
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# loans.py lines 41-46
active_loans = cursor.execute(
    "SELECT COUNT(*) FROM BOOK_LOANS WHERE Card_id = ? AND Date_in IS NULL",
    (card_id,),
).fetchone()[0]
if active_loans >= MAX_ACTIVE_LOANS:
    raise ValueError(...)
```

### ✅ REQUIREMENT: Prevent checkout if book already checked out
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# loans.py lines 60-88
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
    raise ValueError(...)
```

### ✅ REQUIREMENT: Block checkout if unpaid fines
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# loans.py lines 48-62
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
    raise ValueError(...)
```

### Checking In Books

### ✅ REQUIREMENT: Search by ISBN, Card_no, or borrower name
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# app.py lines 284-290
if search_type == 'card_id':
    open_loans = loans.find_open_loans(conn, card_id=search_term)
elif search_type == 'isbn':
    open_loans = loans.find_open_loans(conn, isbn=search_term)
else:
    open_loans = loans.find_open_loans(conn, borrower_name=search_term)
```

### ✅ REQUIREMENT: Select and check in books
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```html
<!-- loans.html -->
<input type="checkbox" name="loan_id" value="{{ loan.Loan_id }}">
<button type="submit">Check In Selected</button>
```

### ✅ REQUIREMENT: Use today as date_in
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# loans.py line 109
today = date.today().isoformat()
```

---

## 4. Borrower Management [20 points]

### ✅ REQUIREMENT: Create new borrowers via GUI
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```html
<!-- borrowers.html -->
<form action="{{ url_for('manage_borrowers') }}" method="POST">
    <!-- Form fields for new borrower -->
</form>
```

### ✅ REQUIREMENT: All required fields (name, SSN, address)
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# app.py lines 56-57
elif not ssn or not full_name or not address:
    flash('SSN, full name, and address are required.', 'error')
```

### ✅ REQUIREMENT: Auto-generate card_no
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# borrowers.py lines 17-23
max_id = cursor.execute("SELECT MAX(Card_id) FROM BORROWER").fetchone()[0]
if max_id is None:
    new_id = 1
else:
    new_id = max_id + 1
```

**Format:** Sequential integers (1, 2, 3, ..., 1001, 1002, 1003)
**Compatible:** Yes, matches existing format

### ✅ REQUIREMENT: Prevent duplicate SSN
**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# borrowers.py lines 25-27
if cursor.execute("SELECT 1 FROM BORROWER WHERE Ssn = ?", (ssn,)).fetchone():
    raise ValueError("A borrower with this SSN already exists")
```

---

## Summary by Section

### 1. GUI and Overall Design: ✅ 20/20 points
- All requirements met
- Web-based GUI
- Intuitive design
- All operations via interface

### 2. Book Search and Availability: ⚠️ 18/20 points
- Single search field: ✅
- Case insensitive: ✅
- Substring matching: ✅
- ISBN, Title, Author search: ✅
- **Missing: Borrower ID column** ❌

**Deduction:** -2 points for missing Borrower ID column

### 3. Book Loans: ✅ 20/20 points
- All checkout requirements: ✅
- All check-in requirements: ✅
- All validations: ✅
- Error messages: ✅

### 4. Borrower Management: ✅ 20/20 points
- Create borrowers: ✅
- Required fields: ✅
- Auto-generate Card_no: ✅
- Prevent duplicate SSN: ✅

### 5. Fines: ✅ 20/20 points (from previous analysis)
- All requirements met with search functionality

---

## Total Score Estimate: 98/100 points

**Only Issue:**
- Missing Borrower ID column in search results (-2 points)

**To achieve 100/100:**
Add Borrower ID column to book search results showing Card_id when book is checked out.

---

## Recommendation

Add one column to search results to show Borrower ID when book is checked out. This is a simple fix that will bring the score to 100/100.
