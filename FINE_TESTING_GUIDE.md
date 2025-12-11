# Fine Testing Guide

## Test Data Created ✅

Successfully created an overdue loan with unpaid fine for testing.

### Test Account Details:
- **Username:** `bob`
- **Card ID:** 1003
- **Borrower Name:** Bob bob

### Overdue Loan Details:
- **Book:** Classical Mythology (ISBN: 0195153445)
- **Loan ID:** 6
- **Date Out:** 2025-11-20 (20 days ago)
- **Due Date:** 2025-12-04 (6 days ago)
- **Days Overdue:** 6 days
- **Fine Amount:** $1.50 (6 days × $0.25/day)
- **Fine Status:** UNPAID

---

## Test Scenarios

### 1. View Fine on Profile Page
**Steps:**
1. Login as user `bob`
2. Go to Profile page
3. Check "My Active Loans" section
   - Should see "Classical Mythology" loan
   - Should show due date: 2025-12-04
4. Check "Outstanding Fines" section
   - Should see $1.50 fine
   - Should show book title and due date

**Expected Result:**
```
My Active Loans:
┌──────────────┬─────────────────────┬─────────────┬────────────┬──────────────┐
│ ISBN         │ Title               │ Checked Out │ Due Date   │ Action       │
├──────────────┼─────────────────────┼─────────────┼────────────┼──────────────┤
│ 0195153445   │ Classical Mythology │ 2025-11-20  │ 2025-12-04 │ [Return Book]│
└──────────────┴─────────────────────┴─────────────┴────────────┴──────────────┘

Outstanding Fines:
┌─────────────────────┬────────────┬─────────────┐
│ Book                │ Due Date   │ Fine Amount │
├─────────────────────┼────────────┼─────────────┤
│ Classical Mythology │ 2025-12-04 │ $1.50       │
└─────────────────────┴────────────┴─────────────┘
Total: $1.50
```

### 2. Test Checkout Block (Unpaid Fines)
**Steps:**
1. While logged in as `bob`
2. Go to Search page
3. Try to checkout any available book
4. Click "Checkout" or "Checkout Selected Books"

**Expected Result:**
```
❌ Checkout failed: Bob bob (Card ID: 1003) has 1 unpaid fine(s) 
   totaling $1.50. Please pay all fines before checking out books.
```

### 3. Return Overdue Book
**Steps:**
1. While logged in as `bob`
2. Go to Profile page
3. Click "Return Book" next to "Classical Mythology"

**Expected Result:**
```
✅ Book returned successfully!

My Active Loans:
(No active loans)

Outstanding Fines:
┌─────────────────────┬────────────┬─────────────┐
│ Book                │ Due Date   │ Fine Amount │
├─────────────────────┼────────────┼─────────────┤
│ Classical Mythology │ 2025-12-04 │ $1.50       │
└─────────────────────┴────────────┴─────────────┘
Total: $1.50
```

**Note:** Fine persists even after book is returned!

### 4. Admin View Fines (Admin Only)
**Steps:**
1. Logout from `bob` account
2. Login as `admin` / `admin`
3. Go to Fines page
4. Look for Card ID 1003

**Expected Result:**
- Should see Bob bob (Card ID: 1003)
- Should show $1.50 unpaid fine
- Should have option to pay fine

### 5. Admin Pay Fine (Admin Only)
**Steps:**
1. While logged in as admin on Fines page
2. Enter Card ID: 1003
3. Click "Pay Fines"

**Expected Result:**
```
✅ Fines paid for Card ID 1003.
```

### 6. Verify Fine Paid
**Steps:**
1. Logout from admin
2. Login as `bob`
3. Go to Profile page
4. Check "Outstanding Fines" section

**Expected Result:**
```
Outstanding Fines:
No outstanding fines
```

### 7. Verify Can Checkout After Fine Paid
**Steps:**
1. While logged in as `bob`
2. Go to Search page
3. Try to checkout a book

**Expected Result:**
```
✅ Book [ISBN] checked out to Card 1003.
```

---

## Fine Calculation Rules

### Automatic Calculation:
- **Rate:** $0.25 per day overdue
- **Trigger:** When book is returned after due date
- **Creation:** Automatic via `loans.checkin()` function

### Example Calculations:
- 1 day overdue = $0.25
- 6 days overdue = $1.50
- 10 days overdue = $2.50
- 30 days overdue = $7.50

### Fine Lifecycle:
1. **Book Checked Out** → No fine
2. **Due Date Passes** → Book becomes overdue
3. **Book Returned Late** → Fine automatically created
4. **Fine Unpaid** → Cannot checkout more books
5. **Admin Pays Fine** → Can checkout again

---

## Database Queries for Verification

### Check Loan Status:
```sql
SELECT * FROM BOOK_LOANS WHERE Loan_id = 6;
```

### Check Fine Status:
```sql
SELECT * FROM FINES WHERE Loan_id = 6;
```

### Check User's Active Loans:
```sql
SELECT bl.*, b.Title 
FROM BOOK_LOANS bl
JOIN BOOK b ON bl.Isbn = b.Isbn
WHERE bl.Card_id = 1003 AND bl.Date_in IS NULL;
```

### Check User's Unpaid Fines:
```sql
SELECT f.*, bl.Isbn, b.Title
FROM FINES f
JOIN BOOK_LOANS bl ON f.Loan_id = bl.Loan_id
JOIN BOOK b ON bl.Isbn = b.Isbn
WHERE bl.Card_id = 1003 AND f.Paid = 0;
```

---

## Expected Behaviors

### ✅ Correct Behaviors:
1. **Fine appears on profile** immediately
2. **Cannot checkout** with unpaid fines
3. **Fine persists** after book return
4. **Admin can pay** fines
5. **Can checkout** after fine is paid
6. **Fine amount** calculated correctly ($0.25/day)

### ❌ Should NOT Happen:
1. Fine disappears when book returned
2. Can checkout with unpaid fines
3. Fine amount incorrect
4. Regular user can pay own fines
5. Fine appears before book is returned

---

## Cleanup (Optional)

To remove test data and start fresh:

```sql
-- Remove the fine
DELETE FROM FINES WHERE Loan_id = 6;

-- Remove the loan
DELETE FROM BOOK_LOANS WHERE Loan_id = 6;
```

Or run the script again to create another test case!

---

## Additional Test Cases

Want to test more scenarios? Run:

```bash
# Create another overdue loan for different user
python3 create_test_fine.py 1001

# Create for Card ID 1002
python3 create_test_fine.py 1002
```

Each run creates a new overdue loan with calculated fine!
