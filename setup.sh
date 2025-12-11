#!/bin/bash
# Books4U Library Management System - Setup Script
# This script will install all dependencies and set up the database

echo -e "\033[0;36m========================================\033[0m"
echo -e "\033[0;36m  Books4U Library Management System\033[0m"
echo -e "\033[0;36m  Setup Script\033[0m"
echo -e "\033[0;36m========================================\033[0m"
echo ""

# Check if Python is installed
echo -e "\033[1;33mChecking Python installation...\033[0m"

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "\033[0;31m✗ Python not found!\033[0m"
    echo -e "\033[0;31mPlease install Python 3.8 or higher from https://www.python.org/\033[0m"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
echo -e "\033[0;32m✓ Python found: $PYTHON_VERSION\033[0m"

# Install required packages
echo ""
echo -e "\033[1;33mInstalling required packages...\033[0m"
echo -e "\033[0;37m  - Flask (web framework)\033[0m"
echo -e "\033[0;37m  - Werkzeug (password hashing)\033[0m"

$PYTHON_CMD -m pip install --upgrade pip --quiet
$PYTHON_CMD -m pip install Flask Werkzeug --quiet

if [ $? -eq 0 ]; then
    echo -e "\033[0;32m✓ Packages installed successfully\033[0m"
else
    echo -e "\033[0;31m✗ Failed to install packages\033[0m"
    exit 1
fi

# Check if database exists
echo ""
if [ -f "library.db" ]; then
    echo -e "\033[1;33mDatabase 'library.db' already exists.\033[0m"
    read -p "Do you want to reload the database? This will delete all existing data. (y/N) " response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "\033[1;33mReloading database...\033[0m"
        $PYTHON_CMD load_data.py
        if [ $? -eq 0 ]; then
            echo -e "\033[0;32m✓ Database reloaded successfully\033[0m"
        else
            echo -e "\033[0;31m✗ Failed to reload database\033[0m"
            exit 1
        fi
    else
        echo -e "\033[0;37mSkipping database reload\033[0m"
    fi
else
    echo -e "\033[1;33mCreating database...\033[0m"
    $PYTHON_CMD load_data.py
    if [ $? -eq 0 ]; then
        echo -e "\033[0;32m✓ Database created successfully\033[0m"
    else
        echo -e "\033[0;31m✗ Failed to create database\033[0m"
        exit 1
    fi
fi

# Setup complete
echo ""
echo -e "\033[0;36m========================================\033[0m"
echo -e "\033[0;32m  Setup Complete!\033[0m"
echo -e "\033[0;36m========================================\033[0m"
echo ""
echo -e "\033[1;33mTo start the application, run:\033[0m"
echo -e "  $PYTHON_CMD app.py"
echo ""
echo -e "\033[1;33mThen open your browser to:\033[0m"
echo -e "  http://127.0.0.1:5000"
echo ""
echo -e "\033[1;33mDefault login credentials:\033[0m"
echo -e "  Username: admin"
echo -e "  Password: admin"
echo ""
read -p "Press Enter to start the application now, or Ctrl+C to exit..."

# Start the application
echo -e "\033[0;36mStarting Books4U...\033[0m"
$PYTHON_CMD app.py
