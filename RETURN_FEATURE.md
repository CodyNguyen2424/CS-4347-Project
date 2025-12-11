# Book Return Feature

## Summary

Added the ability for users to return their own books directly from their profile page.

## Features

### ✅ Return Button on Profile
- Each active loan now has a "Return Book" button
- Located in the "My Active Loans" section of the profile page
- One-click return functionality

### ✅ Security & Validation
- Users can **only return their own books**
- Cannot return books that don't belong to them
- Cannot return books that are already returned
- Validates user has a linked borrower account

### ✅ Automatic Fine Calculation
- When a book is returned, fines are automatically calculated
- If the book is overdue, a fine is created
- Fine amount: $0.25 per day overdue
- Fines appear in the "Outstanding Fines" section

## How It Works

### User Experience:
1. User logs in and goes to Profile page
2. Sees their active loans in "My Active Loans" table
3. Clicks "Return Book" button next to any loan
4. Book is immediately returned
5. Success message appears
6. If overdue, fine is automatically calculated and shown

### Backend Process:
1. Receives loan_id from form submission
2. Verifies user is logged in
3. Checks user has a linked borrower account
4. Verifies the loan belongs to the current user
5. Checks the book hasn't already been returned
6. Calls `loans.checkin()` to process return
7. Sets `Date_in` to today's date
8. Calculates and creates fine if overdue
9. Redirects back to profile with success message

## Security Features

### Validation Checks:
✅ **User Authentication**: Must be logged in  
✅ **Ownership Verification**: Can only return own books  
✅ **Borrower Account**: Must have linked Card_id  
✅ **Loan Exists**: Validates loan_id is valid  
✅ **Not Already Returned**: Checks Date_in is NULL  

### Error Messages:
- "Loan ID is required."
- "You do not have a borrower account linked."
- "Loan not found."
- "You can only return your own books."
- "This book has already been returned."
- "Book returned successfully!" (success)

## Technical Implementation

### Route: `/profile/return-book` (POST)
```python
@app.route('/profile/return-book', methods=['POST'])
@login_required
def return_book():
    # Get loan_id from form
    # Verify user owns the loan
    # Call loans.checkin()
    # Redirect to profile
```

### Template Changes: `profile.html`
- Added "Action" column to active loans table
- Added form with hidden loan_id field
- Added "Return Book" button for each loan

### Database Changes:
- Uses existing `loans.checkin()` function
- Sets `BOOK_LOANS.Date_in` to current date
- Creates `FINES` record if book is overdue

## Example Usage

**Before Return:**
```
My Active Loans:
ISBN         | Title              | Checked Out | Due Date   | Action
0195153445   | Classical Mythology| 2025-12-10  | 2025-12-24 | [Return Book]
```

**After Clicking "Return Book":**
```
✓ Book returned successfully!

My Active Loans:
(No active loans)

Outstanding Fines:
Book                  | Due Date   | Fine Amount
Classical Mythology   | 2025-12-24 | $0.00
(No overdue - returned on time)
```

**If Overdue:**
```
✓ Book returned successfully!

Outstanding Fines:
Book                  | Due Date   | Fine Amount
Classical Mythology   | 2025-12-24 | $1.25
(5 days overdue × $0.25/day)
```

## Benefits

### For Users:
✅ **Convenience**: Return books without visiting library  
✅ **Self-Service**: No need for admin assistance  
✅ **Immediate**: Instant return processing  
✅ **Transparent**: See fines immediately if overdue  

### For System:
✅ **Automated**: No manual processing needed  
✅ **Secure**: Users can't return others' books  
✅ **Accurate**: Automatic fine calculation  
✅ **Auditable**: All returns logged with timestamps  

## Testing

To test the return feature:

1. **Login as a user with active loans** (e.g., `bob67`)
2. **Go to Profile page**
3. **Check "My Active Loans" section**
4. **Click "Return Book" on any loan**
5. **Verify:**
   - Success message appears
   - Loan disappears from active loans
   - If overdue, fine appears in "Outstanding Fines"

## Integration

Works seamlessly with existing features:
- ✅ Checkout system
- ✅ Fine calculation
- ✅ Admin loan management
- ✅ Profile page
- ✅ Borrower accounts
