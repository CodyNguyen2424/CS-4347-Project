# Mark as Late Feature

## Summary

Added "Mark as Late" button to the Loans page so admins can manually trigger fine calculation for selected overdue books without checking them in.

## Features

### ✅ Manual Fine Calculation
- **"Mark as Late" button** on Loans page
- **Select multiple loans** with checkboxes
- **Calculate fines** without checking in books
- **Immediate feedback** with success message

## How It Works

### Admin View (Loans Page):

```
Check In / Find Loans
┌────────────────────────────────────────────────────┐
│ Search: [Borrower Name ▼] [Search term...] [Find] │
├────────────────────────────────────────────────────┤
│ ☐ | ID | Book              | Borrower  | Due Date │
│ ☐ | 6  | Classical Mythology| Bob bob   | 2025-12-04│
│ ☐ | 7  | Another Book      | Jane Doe  | 2025-12-05│
├────────────────────────────────────────────────────┤
│ [Check In Selected] [Mark as Late (Calculate Fines)]│
└────────────────────────────────────────────────────┘
```

### Workflow:

1. **Admin searches for loans** (by borrower name, Card ID, or ISBN)
2. **Selects overdue loans** using checkboxes
3. **Clicks "Mark as Late"** button
4. **System calculates fines** for selected loans
5. **Success message** confirms fines calculated

## Technical Implementation

### Frontend (`templates/loans.html`):
```html
<button type="submit" name="action" value="mark_late" 
        class="btn btn-danger" 
        style="background: var(--warning);">
    Mark as Late (Calculate Fines)
</button>
```

### Backend (`app.py`):
```python
elif action == 'mark_late':
    loan_ids = request.form.getlist('loan_id')
    if loan_ids:
        ids = [int(x) for x in loan_ids]
        with get_connection() as conn:
            for loan_id in ids:
                fines.refresh_fines(conn, loan_id=loan_id)
        flash(f"Successfully calculated fines for {len(loan_ids)} loan(s).", "success")
```

### Fine Calculation (`fines.py`):
- Uses existing `refresh_fines()` function
- Calculates fine based on:
  - **If returned:** (date_in - due_date) × $0.25/day
  - **If still out:** (today - due_date) × $0.25/day
- Creates or updates FINES record
- Respects paid status (won't update paid fines)

## Use Cases

### 1. Overdue Books Still Out
**Scenario:** Book is overdue but not yet returned

**Action:**
1. Search for the loan
2. Select it
3. Click "Mark as Late"

**Result:**
- Fine created/updated based on days overdue
- Book remains checked out
- Borrower can see fine on profile
- Borrower blocked from checking out more books

### 2. Batch Fine Calculation
**Scenario:** Multiple books are overdue

**Action:**
1. Search for all loans
2. Select multiple overdue loans
3. Click "Mark as Late"

**Result:**
- Fines calculated for all selected loans
- One success message for all
- Efficient batch processing

### 3. Manual Fine Update
**Scenario:** Fine amount needs to be recalculated

**Action:**
1. Find the loan
2. Click "Mark as Late"

**Result:**
- Fine amount updated to current calculation
- Reflects current days overdue
- Only updates if fine is unpaid

## Comparison: Mark as Late vs Check In

### Mark as Late:
- ✅ Calculates fines
- ❌ Does NOT check in book
- ✅ Book remains checked out
- ✅ Can be done multiple times
- ✅ Updates fine amount if unpaid

### Check In:
- ✅ Calculates fines (automatically)
- ✅ Checks in book (sets date_in)
- ❌ Book becomes available
- ❌ Can only be done once per loan
- ✅ Final fine calculation

## Benefits

### For Admins:
✅ **Proactive fine management** - Calculate fines before return  
✅ **Batch processing** - Handle multiple loans at once  
✅ **Flexibility** - Calculate without checking in  
✅ **Transparency** - Borrowers see fines immediately  

### For System:
✅ **Accurate fines** - Always up-to-date  
✅ **Automated calculation** - Uses existing logic  
✅ **Audit trail** - All fines logged  
✅ **Prevents checkout** - Blocks users with unpaid fines  

## Example Workflow

**Scenario: Admin wants to notify borrowers of overdue books**

1. **Search for overdue loans**
   - Use date filter or manual review
   
2. **Select overdue loans**
   - Check boxes for all overdue items
   
3. **Click "Mark as Late"**
   - Fines calculated immediately
   
4. **Borrowers see fines**
   - On their profile page
   - Blocked from checkout
   
5. **Borrowers pay or return**
   - Can pay fine on profile
   - Or return book (fine persists)

## Notes

- **Does not check in books** - Books remain checked out
- **Updates existing fines** - If unpaid, recalculates amount
- **Respects paid fines** - Won't modify already paid fines
- **Uses same logic** - As automatic fine calculation
- **Admin only** - Regular users cannot mark as late

The feature is live and ready to use! 🎉
