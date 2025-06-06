# employee-management-system-using-python-with-ui
🧑‍💼 Employee Management System
A desktop application built with Python, PyQt5, and MySQL to streamline HR operations. It features modules for managing employee records, attendance tracking, salary details, and daily HR tasks—all through an intuitive and user-friendly interface.


🧠 About the Project:
This application helps streamline day-to-day HR operations by allowing the user to:

	- Add, update, view, and delete employee records
	- Track daily attendance (In-time, Out-time)
	- View salary based on designation
	- Maintain HR tasks and to-do lists
	- Operate through a secure login/signup system


🔧 How I Made It – Step-by-Step:
1. Installed Python:
Installed Python 3.10.11 from python.org
Configured Python in system PATH

2. Installed PyCharm:
Set up the project in PyCharm IDE for better organization and development

3. Installed MySQL & Connector:
Installed MySQL Server and created the required database and tables
Installed MySQL connector using pip install mysql-connector-python

4. Designed UI with Qt Designer:
Created .ui files for login, signup, dashboard, employee manager, salary window, and attendance


🖌️ UI Design (via Qt Designer):
Each window was built with a clean and organized layout:

	- Login/Signup: QLineEdit, QPushButton
	- Dashboard: Displays employee stats, average attendance, HR tasks, and to-do list
	- Employee Management: QTableWidget for viewing, adding, updating, deleting records
	- Attendance: Uses current date/time, dropdowns for employee names
	- Salary: Displays salary based on roles


💻 Core Functionalities

  Feature	                                Description
Login/Signup	                User authentication for HR staff
Add Employee	                Add details like name, email, post, and salary
Update/Delete Employee      	Modify or remove existing employee records
Attendance Tracking	          Track in-time and out-time with auto-generated timestamps
Salary Management	            View salary info filtered by employee post
Dashboard Overview	          Displays real-time HR metrics, task list, and summaries


🧑‍💻 Technologies Used

	- Python 3.10.11
	- PyQt5 (for UI)
	- Qt Designer (for designing .ui files)
	- MySQL (for storing employee, attendance, and salary data)
	- MySQL Connector (mysql-connector-python for database connection)


🚀 How to Run the Project

1. Clone the Repository:
git clone https://github.com/yourusername/employee-management-system.git
cd employee-management-system

2. Install Required Libraries:
pip install PyQt5 mysql-connector-python

3. Setup MySQL Database:
Run setup_database.py or import tables manually using MySQL Workbench

4. Run the Application:
python main.py


📂 File Structure

employee-management-system/
├── main.py                 # Entry point for login/signup
├── dashboard.py            # Dashboard with task list and stats
├── manage_employee.py      # Add, view, update, delete employees
├── attendance.py           # Attendance tracking window
├── salary.py               # Salary info and filtering
├── setup_database.py       # MySQL DB setup script
├── *.ui                    # Qt Designer UI files
├── README.md               # Project documentation


📌 Future Improvements
	- Email notifications for attendance
	- Export salary and attendance reports to PDF
	- Admin role with user access controls
	- Charts/Graphs for analytics

📝 License
This project is open-source under the MIT License.

🙋‍♀️ Author
Created by Khushi Singh

