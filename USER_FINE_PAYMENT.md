# User Fine Payment Feature

## Summary

Users can now pay their own fines directly from their profile page with a simple "Pay" button.

## Features

### ✅ Self-Service Fine Payment
- **"Pay" button** next to each unpaid fine
- **One-click payment** - no additional steps
- **Immediate effect** - can checkout books right after payment
- **Security** - users can only pay their own fines

### How It Works

**User View:**
```
Outstanding Fines:
┌─────────────────────┬────────────┬─────────────┬────────┐
│ Book                │ Due Date   │ Fine Amount │ Action │
├─────────────────────┼────────────┼─────────────┼────────┤
│ Classical Mythology │ 2025-12-04 │ $1.50       │ [Pay]  │
└─────────────────────┴────────────┴─────────────┴────────┘
Total: $1.50
```

**After Clicking "Pay":**
```
✅ Fine of $1.50 paid successfully!

Outstanding Fines:
No outstanding fines
```

## User Experience

### Before Payment:
1. User sees unpaid fine on profile
2. Cannot checkout books (blocked by unpaid fines)
3. Sees "Pay" button next to fine

### Payment Process:
1. Click "Pay" button
2. Fine is marked as paid
3. Success message appears
4. Fine disappears from list

### After Payment:
1. No outstanding fines shown
2. Can checkout books again
3. Fine is permanently marked as paid

## Security Features

### Validation Checks:
✅ **User Authentication** - Must be logged in  
✅ **Ownership Verification** - Can only pay own fines  
✅ **Borrower Account** - Must have linked Card_id  
✅ **Fine Exists** - Validates loan_id is valid  
✅ **Not Already Paid** - Checks fine isn't already paid  

### Error Messages:
- "Loan ID is required."
- "You do not have a borrower account linked."
- "Fine not found."
- "You can only pay your own fines."
- "This fine has already been paid."
- "Fine of $X.XX paid successfully!" (success)

## Technical Implementation

### Route: `/profile/pay-fine` (POST)
```python
@app.route('/profile/pay-fine', methods=['POST'])
@login_required
def pay_fine():
    # Get loan_id from form
    # Verify user owns the fine
    # Mark fine as paid
    # Redirect to profile
```

### Template Changes: `profile.html`
- Added "Action" column to fines table
- Added form with hidden loan_id field
- Added "Pay" button for each unpaid fine
- Updated total colspan to account for new column

### Database Update:
```sql
UPDATE FINES SET Paid = 1 WHERE Loan_id = ?
```

## Testing the Feature

### Test with Existing Fine:

**Login as user with fine:**
```
Username: bob
Card ID: 1003
Fine: $1.50 (from test data)
```

**Steps:**
1. Login as `bob`
2. Go to Profile page
3. See $1.50 fine in "Outstanding Fines"
4. Click "Pay" button
5. See success message
6. Fine disappears
7. Can now checkout books!

### Verify Payment:

**Check database:**
```sql
SELECT * FROM FINES WHERE Loan_id = 6;
-- Paid should be 1
```

**Try to checkout:**
```
1. Go to Search page
2. Select a book
3. Click checkout
4. Should work! (no unpaid fines error)
```

## Benefits

### For Users:
✅ **Convenient** - Pay fines without admin help  
✅ **Fast** - One-click payment  
✅ **Immediate** - Can checkout right away  
✅ **Transparent** - Clear confirmation message  

### For System:
✅ **Self-Service** - Reduces admin workload  
✅ **Secure** - Users can't pay others' fines  
✅ **Simple** - Just marks fine as paid  
✅ **Auditable** - All payments logged  

## Comparison: User vs Admin Payment

### User Payment (Profile Page):
- Can only pay **their own** fines
- One fine at a time
- Simple "Pay" button
- Immediate confirmation

### Admin Payment (Fines Page):
- Can pay **any borrower's** fines
- All fines for a Card ID at once
- Enter Card ID, click "Pay Fines"
- Batch payment capability

Both methods work and are appropriate for different use cases!

## Example Workflow

**Scenario: User has overdue book**

1. **Checkout book** → Book checked out
2. **Due date passes** → Book becomes overdue
3. **Return book** → Fine created ($1.50)
4. **Try to checkout** → Blocked by unpaid fine
5. **Go to Profile** → See $1.50 fine with "Pay" button
6. **Click "Pay"** → Fine marked as paid
7. **Try to checkout** → Success! Can checkout again

## Notes

- **Payment is instant** - no processing delay
- **Fine amount doesn't change** - just marked as paid
- **Cannot unpay** - once paid, it's permanent
- **No actual money** - this is a simulation
- **Admin can still pay** - both user and admin payment work

The feature is live and ready to test! 🎉
