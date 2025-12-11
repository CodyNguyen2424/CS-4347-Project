# 📚 Books4U - Library Management System

A modern, full-featured library management system built with Flask, featuring user authentication, book search, loan management, borrower tracking, and fine calculation.

## ✨ Features

### 🔐 User Authentication & Roles
- **Admin/User Role System**: Separate admin and regular user accounts
- Secure login/logout with session management
- User registration with automatic borrower account creation
- Password hashing using Werkzeug
- Link existing borrower accounts to user profiles
- **Admin Badge**: Admins see a special badge on their profile

### 📖 Book Management
- Search 25,000+ books by ISBN, title, or author
- Pagination (50 books per page)
- Filter by availability status (All, Available, Checked Out)
- Real-time availability tracking
- **Multiple Book Checkout**: Admins can select and checkout multiple books at once

### 👥 Borrower Management (Admin Only)
- Create and manage borrower accounts
- View all borrowers with pagination
- Delete borrowers (with validation)
- Automatic SSN validation

### 📚 Loan Management (Admin Only)
- Check out single or multiple books to borrowers
- Search active loans by borrower name, card ID, or ISBN
- Bulk check-in functionality
- Due date tracking

### 💰 Fine Management (Admin Only)
- Automatic fine calculation for overdue books
- View outstanding fines by borrower
- Pay fines (with validation)
- Refresh fines on-demand

### 👤 User Profile
- View personal borrower information
- Track active loans
- Monitor outstanding fines
- Link/unlink borrower accounts
- **Admin status display** with special badge

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows (PowerShell) OR macOS/Linux (Bash)

### Installation

1. **Clone or download the project**
   ```bash
   cd path/to/CS-4347-Project
   ```

2. **Run the setup script**
   
   **Windows:**
   ```powershell
   .\setup.ps1
   ```
   
   **macOS / Linux:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   
   The setup script will:
   - Check Python installation
   - Install Flask and Werkzeug
   - Create/reload the database
   - Offer to start the application

3. **Access the application**
   - Open your browser to: http://127.0.0.1:5000
   - Login with default **admin** credentials:
     - Username: `admin`
     - Password: `admin`
   
   **Note**: The admin account has full access to all features. Regular users created through registration will only have access to the Search page and their Profile.

### Manual Installation

If you prefer manual setup:

**Windows:**
```powershell
# Install dependencies
py -m pip install -r requirements.txt

# Initialize database
py load_data.py

# Start the application
py app.py
```

**macOS / Linux:**
```bash
# Install dependencies
python3 -m pip install -r requirements.txt

# Initialize database
python3 load_data.py

# Start the application
python3 app.py
```

## 📁 Project Structure

```
CS-4347-Project/
├── app.py                 # Main Flask application
├── auth.py                # User authentication logic
├── borrowers.py           # Borrower management
├── loans.py               # Loan management
├── fines.py               # Fine calculation
├── search.py              # Book search functionality
├── db.py                  # Database utilities
├── load_data.py           # Database initialization
├── schema.sql             # Database schema
├── requirements.txt       # Python dependencies
├── setup.ps1              # Automated setup script
├── static/
│   └── style.css          # Application styling
└── templates/
    ├── layout.html        # Base template
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── index.html         # Home page
    ├── profile.html       # User profile
    ├── search.html        # Book search
    ├── loans.html         # Loan management
    ├── borrowers.html     # Borrower management
    └── fines.html         # Fine management
```

## 🎨 Design

- **Color Scheme**: Black, gray, and deep orange with deep red accents
- **Modern UI**: Glassmorphism effects, smooth animations, responsive design
- **Typography**: Inter font family for clean, professional look
- **Accessibility**: High contrast, clear labels, semantic HTML

## 🗄️ Database

The system uses SQLite with the following tables:
- **BOOK**: 25,001 books with ISBN, title
- **AUTHORS**: 15,549 authors
- **BOOK_AUTHORS**: Book-author relationships
- **BORROWER**: 1,000 borrowers with SSN, name, address, phone
- **BOOK_LOANS**: Loan records with dates and due dates
- **FINES**: Fine records linked to loans
- **USERS**: User accounts with authentication and role management (Is_admin field)

## 🔒 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control (admin vs regular users)
- Protected routes with login_required and admin_required decorators
- CSRF protection via Flask sessions
- Input validation on all forms

## 📝 Usage Guide

### 👑 User Roles

**Admin Users:**
- Full access to all features
- Can manage loans, borrowers, and fines
- Can checkout single or multiple books
- See admin badge (👑) on their profile
- Navigation shows: Search, Loans, Borrowers, Fines

**Regular Users:**
- Access to Search and Profile pages only
- Can view their own loans and fines
- Cannot manage other borrowers or process checkouts
- Navigation shows: Search only

### Creating a New Account
1. Click "Create Account" on login page
2. Fill in username, password, SSN, name, and address
3. A borrower account is automatically created and linked
4. **Note**: New accounts are created as regular users (not admins)

### Searching for Books
1. Navigate to "Search" tab
2. Enter ISBN, title, or author name
3. Filter by availability status
4. Use pagination to browse results

### Checking Out Books (Admin Only)

**Single Book Checkout:**
1. Go to "Search" tab
2. Find an available book
3. Click "Checkout" button
4. Enter the borrower's Card ID
5. System validates and processes the checkout

**Multiple Book Checkout:**
1. Go to "Search" tab
2. Check the boxes next to available books you want to checkout
3. Click "Checkout Selected Books" button
4. Enter the borrower's Card ID
5. All selected books will be checked out to that borrower

### Managing Borrowers (Admin Only)
1. Navigate to "Borrowers" tab
2. Create new borrowers with SSN, name, address
3. View all borrowers with pagination
4. Delete borrowers (if no active loans)

### Viewing Fines (Admin Only)
1. Go to "Fines" tab
2. Click "Refresh Fines" to calculate overdue fines
3. View outstanding fines by borrower
4. Pay fines for borrowers with no active loans

## 🛠️ Development

### Running in Debug Mode
The application runs in debug mode by default for development:
```python
if __name__ == '__main__':
    app.run(debug=True)
```

### Database Reset
To reset the database with fresh data:
```powershell
py load_data.py
```

## 📄 License

This project is for educational purposes as part of CS 4347. All rights reserved.

## Technology Stack

- Python 3.14
- Flask 3.0.0
- Werkzeug 3.0.0
- SQLite 3.42.0

## 👥 Credits

Developed for CS 4347 - Database Systems Team Hellium
