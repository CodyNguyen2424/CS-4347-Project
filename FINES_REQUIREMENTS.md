# Fines Requirements Compliance Checklist

## Requirements Analysis: 20 Points Total

### ✅ REQUIREMENT 1: Search for Fines
**Requirement:** "Use your GUI to search for fines by either Borrower ID or any substring of borrower name."

**Status:** ⚠️ **PARTIALLY IMPLEMENTED**

**Current Implementation:**
- Fines page shows ALL outstanding fines grouped by borrower
- No search/filter functionality yet

**What's Missing:**
- Search box to filter by Card ID
- Search box to filter by borrower name substring

**Recommendation:** ADD search functionality to fines.html

---

### ✅ REQUIREMENT 2: Fine Amount Format
**Requirement:** "fine_amt attribute is a dollar amount that should have two decimal places."

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# fines.py line 43
fine_amt = round(days_late * DAILY_FINE, 2)

# fines.html line 29
${{ "%.2f"|format(fine.Total_Fines) }}
```

**Evidence:**
- All fine amounts rounded to 2 decimal places
- Display formatted with 2 decimals

---

### ✅ REQUIREMENT 3: Paid Attribute
**Requirement:** "paid attribute is a boolean value (or integer 0/1) that indicates whether a fine has been paid."

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```sql
-- schema.sql line 41
Paid INTEGER NOT NULL CHECK (Paid IN (0, 1))
```

**Evidence:**
- Paid is INTEGER with CHECK constraint (0 or 1)
- 0 = unpaid, 1 = paid

---

### ✅ REQUIREMENT 4: Fine Rate
**Requirement:** "Fines are assessed at a rate of $0.25/day (twenty-five cents per day)."

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# fines.py line 6
DAILY_FINE = 0.25

# fines.py line 43
fine_amt = round(days_late * DAILY_FINE, 2)
```

**Evidence:**
- Constant defined as $0.25
- Used in all fine calculations

---

### ✅ REQUIREMENT 5: Refresh/Update Button
**Requirement:** "You should provide a button, menu item, etc. that updates/refreshes entries in the FINES table."

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```html
<!-- fines.html line 7-10 -->
<button type="submit" class="btn btn-primary">Refresh Fines</button>
```

**Evidence:**
- "Refresh Fines" button on fines page
- Calls `refresh_fines()` function
- Updates all overdue loans

---

### ✅ REQUIREMENT 6: Late Book Scenarios
**Requirement:** "There are two scenarios for late books"

#### Scenario 1: Late books that have been returned
**Formula:** `[(difference in days between due_date and date_in) * $0.25]`

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# fines.py lines 36-37
if row["Date_in"]:
    end_date = _parse_iso(row["Date_in"])
```

#### Scenario 2: Late books still out
**Formula:** `[(difference between due_date and TODAY) * $0.25]`

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# fines.py lines 38-39
else:
    end_date = today
```

**Evidence:**
- Both scenarios handled in `refresh_fines()`
- Uses Date_in if available, otherwise uses today

---

### ✅ REQUIREMENT 7: Existing Fine Handling
**Requirement:** "If a row already exists in FINES for a particular late BOOK_LOANS record"

#### If paid == FALSE
**Requirement:** "do not create a new row, only update the fine_amt if different than current value"

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# fines.py lines 49-55
if existing:
    if existing["Paid"]:
        continue
    conn.execute(
        "UPDATE FINES SET Fine_amt = ? WHERE Loan_id = ? AND Paid = 0",
        (fine_amt, row["Loan_id"]),
    )
```

#### If paid == TRUE
**Requirement:** "do nothing"

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# fines.py lines 50-51
if existing["Paid"]:
    continue
```

**Evidence:**
- Checks if fine exists
- If paid, skips (does nothing)
- If unpaid, updates amount

---

### ✅ REQUIREMENT 8: Payment Mechanism
**Requirement:** "Provide a mechanism for librarians to enter payment of fines (i.e. to update a FINES record where paid == TRUE)"

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# app.py lines 592-599
elif action == 'pay':
    card_id = request.form.get('card_id')
    fines.pay_fines(conn, card_id)
```

**Evidence:**
- "Pay Full Amount" button for each borrower
- Updates all unpaid fines for that borrower to Paid = 1

---

### ✅ REQUIREMENT 9: No Payment for Unreturned Books
**Requirement:** "Do not allow payment of a fine for books that are not yet returned."

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# fines.py lines 85-95
open_loans = conn.execute(
    """
    SELECT COUNT(*)
    FROM FINES f
    JOIN BOOK_LOANS bl ON f.Loan_id = bl.Loan_id
    WHERE bl.Card_id = ? AND f.Paid = 0 AND bl.Date_in IS NULL
    """,
    (card_id,),
).fetchone()[0]
if open_loans:
    raise ValueError("Borrower still has books checked out")
```

**Evidence:**
- Checks for unreturned books (Date_in IS NULL)
- Raises error if any books still out
- Payment blocked until all books returned

---

### ✅ REQUIREMENT 10: Display Grouped by Card_no
**Requirement:** "Display of Fines should be grouped by card_no. One line per borrower. i.e. SUM the fine_amt for each Borrower."

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# fines.py lines 63-79
SELECT
    bor.Card_id,
    bor.Bname,
    SUM(f.Fine_amt) AS Total_Fines
FROM FINES f
JOIN BOOK_LOANS bl ON f.Loan_id = bl.Loan_id
JOIN BORROWER bor  ON bl.Card_id = bor.Card_id
WHERE f.Paid = 0
GROUP BY bor.Card_id, bor.Bname
ORDER BY bor.Bname
```

**Evidence:**
- Uses GROUP BY Card_id
- SUM(f.Fine_amt) aggregates all fines
- One row per borrower

---

### ✅ REQUIREMENT 11: No Partial Payments
**Requirement:** "Do not allow paying partial FINES."

**Status:** ✅ **FULLY IMPLEMENTED**

**Implementation:**
```python
# fines.py lines 97-109
UPDATE FINES
SET Paid = 1
WHERE Loan_id IN (
    SELECT f.Loan_id
    FROM FINES f
    JOIN BOOK_LOANS bl ON f.Loan_id = bl.Loan_id
    WHERE bl.Card_id = ? AND f.Paid = 0
)
```

**Evidence:**
- "Pay Full Amount" button
- Pays ALL unpaid fines for borrower
- No option to pay individual fines

---

### ✅ REQUIREMENT 12: Filter Paid Fines
**Requirement:** "Display of Fines should provide a mechanism to filter out previously paid fines (either by default or choice)."

**Status:** ✅ **FULLY IMPLEMENTED (by default)**

**Implementation:**
```python
# fines.py line 74
WHERE f.Paid = 0
```

**Evidence:**
- Only shows unpaid fines (Paid = 0)
- Paid fines automatically filtered out
- Default behavior (no toggle needed)

---

## Summary

### ✅ Fully Implemented: 11/12 requirements (91.7%)

1. ⚠️ Search for fines - **NEEDS IMPROVEMENT**
2. ✅ Fine amount format (2 decimals)
3. ✅ Paid attribute (0/1)
4. ✅ Fine rate ($0.25/day)
5. ✅ Refresh button
6. ✅ Late book scenarios (both)
7. ✅ Existing fine handling
8. ✅ Payment mechanism
9. ✅ No payment for unreturned books
10. ✅ Display grouped by borrower
11. ✅ No partial payments
12. ✅ Filter paid fines

### What's Missing:

**Search Functionality:**
- Need to add search box to filter by Card ID
- Need to add search box to filter by borrower name

### Recommendation:

Add search functionality to the fines page to achieve 100% compliance.

---

## Additional Features Implemented (Bonus):

✅ **User Self-Service Payment**
- Users can pay their own fines from profile page
- Not required but enhances user experience

✅ **Automatic Fine Calculation on Return**
- Fines automatically calculated when book returned
- No manual refresh needed for individual returns

✅ **Profile Page Fine Display**
- Users see their own fines on profile
- Detailed breakdown by book

✅ **Security Validation**
- Users can only pay own fines
- Admins can pay any fines
- Proper ownership verification

---

## Score Estimate: 18-19/20 points

**Deductions:**
- Missing search by Card ID: -0.5 points
- Missing search by borrower name: -0.5 points

**To achieve full 20/20:**
Add search functionality to fines page!
