# Vehicle Maintenance Service Management System (VMSMS)

## 📚 IE304: Production and Service Information Systems Course Project

This project was developed as part of the **IE304: Production and Service Information Systems** course at METU. It is a comprehensive web-based vehicle maintenance service management system built with Django.

## 🚗 Project Overview

VMSMS is a full-featured vehicle maintenance service management system that allows different user roles to manage appointments, invoices, vehicle information, and maintenance records. The system supports multiple user types with different permissions and capabilities.

### Key Features

- **Multi-role User Management**: Admin, Receptionist, Mechanic, Inventory Manager, and Customer roles
- **Appointment Management**: Create, schedule, and track vehicle service appointments
- **Invoice System**: Automatic invoice generation and payment tracking
- **Vehicle Management**: Comprehensive vehicle and insurance information tracking
- **Test & Diagnosis**: Vehicle testing and repair suggestion system
- **Analytics Dashboard**: Cost and statistics analytics for business insights
- **Inventory Management**: Spare parts and supplier management

## 🛠️ Technology Stack

- **Backend**: Django 4.2.1
- **Database**: SQLite (default) / MySQL (configurable)
- **Frontend**: HTML, CSS, Bootstrap
- **Authentication**: Custom Django authentication system

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/oguzalpcakmak/vmsms.git
cd vmsms
```

### 2. Navigate to Project Directory

```bash
cd base_project_py
```

### 3. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Database Setup

#### Option A: Using SQLite (Default - Recommended for Development)

The project is configured to use SQLite by default. No additional setup is required.

#### Option B: Using MySQL

1. Install MySQL and create a database
2. Install MySQL connector:
   ```bash
   pip install mysql-connector-python
   ```
3. Update database settings in `base_project_py/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'mysql.connector.django',
           'NAME': 'your_database_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'your_host',
           'PORT': '3306',
           'OPTIONS': {
               'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
           },
       }
   }
   ```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Sample Data (Optional)

To populate the database with sample data for testing:

```bash
python manage.py generate_all_data
```

This will create sample users, vehicles, appointments, and other data for demonstration purposes.

### 8. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 👥 User Roles and Permissions

### Admin
- Full system access
- Can register all user types
- Manage users and view analytics
- Oversee all operations

### Receptionist
- Register customers
- Create and manage appointments
- Generate invoices
- Manage vehicle information

### Mechanic
- View assigned appointments
- Assign tests to appointments
- Diagnose tests and suggest repairs
- Update test results

### Inventory Manager
- Manage spare parts inventory
- View analytics and reports
- Track suppliers and parts

### Customer
- Register vehicles
- Create appointments
- View invoices and make payments
- Access test results

## 🔧 Sample Data Credentials

After running `python manage.py generate_all_data`, you can log in with:

- **Admin**: `admin` / `admin123`
- **Mechanic**: `Mechanic_1` / `1234`
- **Receptionist**: `Receptionist_1` / `1234`
- **Inventory Manager**: `Inventory_Manager_1` / `1234`
- **Customer**: `Customer_1` / `1234`

## 📁 Project Structure

```
vmsms/
├── base_project_py/
│   ├── base_project_py/
│   │   ├── settings.py      # Django settings
│   │   ├── urls.py          # Main URL configuration
│   │   └── wsgi.py          # WSGI configuration
│   ├── vmsms/
│   │   ├── models.py        # Database models
│   │   ├── views.py         # View logic
│   │   ├── forms.py         # Form definitions
│   │   ├── urls.py          # App URL patterns
│   │   ├── templates/       # HTML templates
│   │   └── management/      # Custom management commands
│   ├── manage.py            # Django management script
│   └── requirements.txt     # Python dependencies
├── README.md                # This file
└── Dockerfile              # Docker configuration
```

## 🔒 Security Notes

- The `SECRET_KEY` is configured to use environment variables for production
- Default database is SQLite for development simplicity
- Change default passwords in production environments
- Configure `DEBUG = False` for production deployment

## 🐳 Docker Deployment

The project includes a Dockerfile for containerized deployment:

```bash
docker build -t vmsms .
docker run -p 8000:8000 vmsms
```

## 📝 Contributing

This is an academic project, but if you find any issues or have suggestions:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is developed for educational purposes as part of the IE304 course.

## 👨‍💻 Author

- **Student Name**: [Your Name]
- **Course**: IE304 - Production and Service Information Systems
- **Institution**: [Your University Name]
- **Year**: [Academic Year]

## 🙏 Acknowledgments

- Django framework and community
- Bootstrap for UI components
- Course instructor and teaching assistants
- Fellow students for testing and feedback

---

**Note**: This project is developed for educational purposes. Please ensure proper security measures when deploying to production environments.