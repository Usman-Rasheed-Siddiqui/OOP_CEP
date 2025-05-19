# Car Rental System

A Python-based Car Rental System that allows users to rent cars, manage accounts, and view rental history, with an admin interface for fleet management.
---

## 🗂️ Table of Contents

- [🗃️ Project File Structure](#️project-file-structure-cli)
- [⚡ Getting Started](#getting-started)
  - [🔧 Installation](#installation)
  - [▶️ Running the App](#running-the-app)
- [🌟 Features](#features)
- [👤 Roles in the System](#roles-within-system)
  - [🙋‍♂️ Customer (User)](#customer-user)
  - [🛠️ Administrator (Admin)](#administrator-admin)
- [📦 Requirements](#requirements)
- [❗ Potential Problems](#potential-problems)
- [🧪 Testing Checklist](#testing)
- [📘 License](#license)
- [🤝 Contributors](#contributors)

---

## Project File Structure (CLI)

```bash
terminal_app/
│
├── data/
│ ├── users/
│ │ ├── admin_info.txt
│ │ ├── available_cars.txt
│ │ ├── cars.txt
│ │ ├── cars_rental_history.txt
│ │ ├── feedbacks.txt
│ │ ├── rented_cars.txt
│ │ └── users.txt
│
├── exception_handling/
│ └── CustomExceptions.py
│
├── file_handler/
│ ├── init.py
│ └── file_handler.py
│
├── rental_management/
│ ├── init.py
│ └── rental_manager.py
│
├── users/
│ ├── init.py
│ ├── admin.py
│ ├── basic_user.py
│ └── customer.py
│
├── vehicle/
│ ├── init.py
│ ├── car.py
│ └── vehicle.py
│
├── main.py
└── main_interface.py```

---

## Getting Started

### Installation

```bash
#pip install -r requirements.txt
```

Make sure you have Python 3.9+ installed.

### Running the App

### For CLI:
```bash
python main.py
```

#Visit `http://localhost:5000` in your browser.

---

## Features

- **User Authentication and Profile Management**
  - Create account, login, and update personal details
  - Secure login system with limited login attempts
  - Ability to check user status (e.g., rented car, balance)

- **Car Rental and Return**
  - Rent one car at a time based on availability
  - Return cars with late penalty enforcement
  - Rental receipt generation after each booking

- **Car Fleet Management (Admin)**
  - Add or remove entire car fleets or specific cars
  - View all available cars or specific car details
  - Manage and monitor current reservations

- **Rental History and Feedback**
  - View rental history by user or car
  - Feedback submission by users, accessible by admin

- **Admin Reports and Dashboard**
  - Generate reports for all customers and current rentals
  - Access feedback and rental history summaries

- **Exception Handling System**
  - Custom exceptions for cleaner error messages and safer exits
  - Allows quitting any operation without crashing the system

- **File-based Data Management**
  - Save and load data (users, rentals, cars) using text files
  - Updates reflected in real-time across system operations

- **Interactive Command-Line Interface**
  - Clean, user-friendly CLI navigation for customers and admins
  - Flash-style messaging through printed interface responses
---

## Roles Within System

### For CLI:

### Customer (User)

* Can register a new account and login securely
* Can rent one car at a time based on availability
* Can return a rented car (with penalties if late)
* Can view their rental status (rented car, balance, etc.)
* Can update personal information (password, address)
* Can view available cars or search for a specific car
* Can review their rental history and any car’s history
* Can provide feedback to the admin
* Cannot manage or modify the car fleet

### Administrator (Admin)

* Can login using admin credentials
* Can add an entire car fleet or individual cars
* Can remove specific cars or entire fleets
* Can view all customers and their rental history
* Can monitor all current rentals and reserved cars
* Can access user feedback for system improvement
* Can view all available car IDs and details
* Can update admin password
* Cannot rent or reserve cars
---

## Requirements

The project requires:

* Python 3.9+
* Flask
* pdfkit
* wkhtmltopdf (for generating PDFs)

Install via `pip install -r requirements.txt`.

---

## Potential Problems:

### For CLI:

### 1. No Screen Clearing after each operation

This problem arose on Pycharm IDE. If encountered this problem. Use VS Code to run the program. 

### 2. Not Able to Remember Car ID:

If you forget to take a screenshot of the receipt, you can use "Check Status" to check and copy your rented Car ID.

---

## Testing

### FOR CLI:

Make sure to:

* Register a new user account and login successfully
* Rent an available car and verify receipt generation
* Return a car and check if penalties apply for late returns
* Attempt login as Admin using admin credentials
* Add new cars or remove specific cars via Admin interface
* View and verify reports for:
  - All customers and their current rentals
  - Rental history of specific users and cars
  - Currently reserved cars
* Submit feedback as a user and access it via Admin panel
* Update user balance and personal information
* Exit gracefully from any operation to test exception handling
---

## License

This project is developed solely for educational use and academic evaluation. It is not intended for commercial deployment or distribution.

---

## Contributors

* Usman Rasheed Siddiqui (CS-24038)
* Huzaifa Hanif (CS-24039)

---
