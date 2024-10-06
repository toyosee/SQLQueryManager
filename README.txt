# SQL to JSON Converter

## Overview
This application is designed to connect to a MySQL database, execute SQL queries, and display the results in JSON format. Users can export the query results as either JSON or CSV files. The application features a modern and user-friendly interface built with Tkinter and ttkbootstrap.

## Features
- Connect to MySQL database using connection strings (Host, User, Password).
- Load available databases into a dropdown list after a successful connection.
- Execute SQL queries and display results in JSON format.
- Export query results as JSON or CSV files.
- Modern UI with ttkbootstrap styling.

## Libraries Used
This project requires the following Python libraries:
- `ttkbootstrap`: For modern styling of the Tkinter interface.
- `mysql-connector-python`: To connect and interact with MySQL databases.
- `pandas`: For data manipulation and exporting to CSV.

## Installation
To set up this application, follow these steps:

1. Clone the repository or download the project files.
2. Navigate to the project directory in your terminal or command prompt.
3. Install the required libraries using the following command:
   pip install -r requirements.txt


## Usage
1. Run the application:
   python your_application_file.py

2. Enter the connection details (Host, User, Password) to connect to the database.
3. Select the desired database and enter your SQL query in the provided text area.
4. Click the "Execute" button to run the query and view the results.
5. Use the "Export" button to save the results as JSON or CSV.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

For inquiry and collaboration:
Elijah Abolaji
tyabolaji@gmail.com
