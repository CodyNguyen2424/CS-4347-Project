# 📚 Books4U - Library Management System

A modern, full-featured library management system built with Flask, featuring user authentication, book search, loan management, borrower tracking, and fine calculation.

## ✨ Features

### 🔐 User Authentication
- Secure login/logout with session management
- User registration with automatic borrower account creation
- Password hashing using Werkzeug
- Link existing borrower accounts to user profiles

### 📖 Book Management
- Search 25,000+ books by ISBN, title, or author
- Pagination (50 books per page)
- Filter by availability status (All, Available, Checked Out)
- Real-time availability tracking

### 👥 Borrower Management
- Create and manage borrower accounts
- View all borrowers with pagination
- Delete borrowers (with validation)
- Automatic SSN validation

### 📚 Loan Management
- Check out books to borrowers
- Search active loans by borrower name, card ID, or ISBN
- Bulk check-in functionality
- Due date tracking

### 💰 Fine Management
- Automatic fine calculation for overdue books
- View outstanding fines by borrower
- Pay fines (with validation)
- Refresh fines on-demand

### 👤 User Profile
- View personal borrower information
- Track active loans
- Monitor outstanding fines
- Link/unlink borrower accounts

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows (PowerShell)

### Installation

1. **Clone or download the project**
   ```powershell
   cd path/to/CS-4347-Project
   ```

2. **Run the setup script**
   ```powershell
   .\setup.ps1
   ```
   
   The setup script will:
   - Check Python installation
   - Install Flask and Werkzeug
   - Create/reload the database
   - Offer to start the application

3. **Access the application**
   - Open your browser to: http://127.0.0.1:5000
   - Login with default credentials:
     - Username: `admin`
     - Password: `admin`

### Manual Installation

If you prefer manual setup:

```powershell
# Install dependencies
py -m pip install -r requirements.txt

# Initialize database
py load_data.py

# Start the application
py app.py
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
- **USERS**: User accounts with authentication

## 🔒 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Protected routes with login_required decorator
- CSRF protection via Flask sessions
- Input validation on all forms

## 📝 Usage Guide

### Creating a New Account
1. Click "Create Account" on login page
2. Fill in username, password, SSN, name, and address
3. A borrower account is automatically created and linked

### Searching for Books
1. Navigate to "Search" tab
2. Enter ISBN, title, or author name
3. Filter by availability status
4. Use pagination to browse results

### Checking Out Books
1. Go to "Loans" tab
2. Enter ISBN and Card ID
3. Click "Checkout Book"
4. System validates borrower, book availability, and loan limits

### Managing Borrowers
1. Navigate to "Borrowers" tab
2. Create new borrowers with SSN, name, address
3. View all borrowers with pagination
4. Delete borrowers (if no active loans)

### Viewing Fines
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

This project is for educational purposes as part of CS 4347.

## 👥 Credits

Developed for CS 4347 - Database Systems
