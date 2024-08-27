# Birth and Death System
This project is aimed at recording births and deaths of individuals and provide a basic metric graph
based on years.

# Table of Contents
1. [Features](#features)
2. [User Roles](#user-roles)
3. [Dashboards](#dashboards)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Usage](#usage)

## Features
- **User Authentication**: Secure user authentication and authorization system.
- **Dashboard**: A dashboard to display a metric graph of birth and death records according to years. There is a total number of death and birth records.
- **Birth Registration**: Users can add birth record to database.
- **Death Registration**: Users can add death record to database.
- **Update Birth Record**: Users can update or edit a birth record.
- **Update Death Record**: Users can update or edit a death record.
- **Delete Birth Record**: Users can delete a birth record.
- **Delete Death Record**: Users can delete a death record.
- **Update Profile**: Users can update their profile. They can change name, email, password, dob and gender.

## User Roles
- **Admin**: Creates users(nurses and doctors)
- **Nurse**
- **Doctor**

## Dashboard
A universal dashboard that displays total number of births and deaths. It also displays a graph of birth and death according to years.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python (version 3.6 or higher)
- pip (You can install using: python -m ensurepip --upgrade or python -m pip install --upgrade pip)
- You can install pycharm IDE for smooth building and running the project.


## Installation
1. **Clone the repository**
    ```bash
    git clone https://github.com/Birth-and-Death-Recording-System/Backend.git
    ```

2. **Create an environment for your dependencies**
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows, use myenv\Scripts\activate
   ```

3. **Install dependencies from requirements.txt file**
    ```bash
   pip install -r requirements.txt
   ```
   
4. **Make migrations**
    ```bash
   python manage.py makemigrations #On Mac use python3 manage.py makemigrations
   python manage.py migrate #On Mac use python3 manage.py migrate
   ```

5. **Run the application**
    ```bash
   python manage.py runserver #On Mac use python3 manage.py runserver
   ```
   
## Usage
1. **Access the Application**:

   Once the application is running, access it in your web browser at `http://localhost:8080`.

2. **Log In**:

   Users can log in using their credentials.

3. **Add a birth and death record**:

   Click on the "Add Birth" or "Add Death" button to add a new birth record. Fill in the required details such as First Name, Last Name, Gender, etc.

4. **View List**:

   Browse through existing list of birth and death records, search, and filter based on your preferences.

5. **Edit and delete birth and death records**:
Click on the delete and edit icon to edit or update field record.

6. **Log Out**:

    Log out by clicking on log out button.
