# Author: Elijah Abolaji
# mail: tyabolaji@gmail.com

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import mysql.connector as mc
import json
import pandas as pd

# Function to switch to the query screen
def show_query_screen():
    connection_frame.grid_remove()
    query_frame.grid()

# Function to switch back to the connection screen
def logout():
    query_frame.grid_remove()
    connection_frame.grid()

# Function to handle database connection
def connect_to_database():
    host = host_entry.get()
    user = user_entry.get()
    password = pass_entry.get()
    port = port_entry.get() if port_entry.get() else 3306  # Default to 3306 if no port is provided

    try:
        conn = mc.connect(host=host, user=user, password=password, port=int(port))
        if conn.is_connected():
            messagebox.showinfo("Connection", "Connection Successful")
            load_databases(conn)
            show_query_screen()
        else:
            messagebox.showerror("Connection", "Connection Failed")

    except ValueError:
        # Handle non-integer values in the port field
        messagebox.showerror("Connection Error", "Invalid port number. Please enter a valid port number.")
    
    except mc.InterfaceError:
        # Handle cases where the connection interface fails (e.g., unreachable host or wrong port)
        messagebox.showerror("Connection Error", "Cannot connect to the specified host. Please check the host address and port.")
    
    except mc.Error as e:
        messagebox.showerror("Connection Error", str(e))

# Function to load databases into the dropdown
def load_databases(conn):
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    
    db_dropdown['values'] = [db[0] for db in databases]  # Updating the dropdown with databases
    db_dropdown.current(0)

# Function to execute query and display results as JSON
def execute_query():
    selected_db = db_dropdown.get()
    query = query_entry.get("1.0", tk.END).strip()

    try:
        conn = mc.connect(host=host_entry.get(), user=user_entry.get(), password=pass_entry.get(), database=selected_db)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        #print(results)

        if results:
            # Display query results as JSON
            json_output = json.dumps(results, indent=4)
            query_output.delete("1.0", tk.END)
            query_output.insert(tk.END, json_output)
        else:
            query_output.delete("1.0", tk.END)
            query_output.insert(tk.END, "No results found.")

    except mc.Error as e:
        messagebox.showerror("Query Error", str(e))

# Function to export query results to JSON or CSV
def export_data():
    data = query_output.get("1.0", tk.END).strip()
    if data:
        filetypes = [("JSON files", "*.json"), ("CSV files", "*.csv")]
        file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=filetypes)
        
        if file:
            if file.endswith('.json'):
                with open(file, 'w') as f:
                    f.write(data)
                messagebox.showinfo("Export", "Data exported successfully to JSON.")
            elif file.endswith('.csv'):
                # Convert JSON data to pandas DataFrame and export to CSV
                df = pd.read_json(data)
                df.to_csv(file, index=False)
                messagebox.showinfo("Export", "Data exported successfully to CSV.")
    else:
        messagebox.showwarning("Export", "No data to export.")

# Function to close the application
def exit_app():
    root.quit()

# Creating the GUI window with ttkbootstrap for modern styling
root = ttk.Window(themename="superhero")  # 'superhero' theme for dark mode
root.title("SQL to JSON Converter")

# Connection frame - the first screen
connection_frame = ttk.Frame(root)
connection_frame.grid(row=0, column=0, padx=10, pady=10)

# Label to prompt user to connect to the database
ttk.Label(connection_frame, text="Enter Connection Strings", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Database connection inputs
ttk.Label(connection_frame, text="Host:").grid(row=1, column=0, padx=10, pady=5)
host_entry = ttk.Entry(connection_frame)
host_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(connection_frame, text="User:").grid(row=2, column=0, padx=10, pady=5)
user_entry = ttk.Entry(connection_frame)
user_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(connection_frame, text="Password:").grid(row=3, column=0, padx=10, pady=5)
pass_entry = ttk.Entry(connection_frame, show="*")
pass_entry.grid(row=3, column=1, padx=10, pady=5)

# Port entry for remote database connection (optional)
ttk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=10, pady=5)
port_entry = ttk.Entry(connection_frame)
port_entry.grid(row=4, column=1, padx=10, pady=5)


# Connect button
connect_button = ttk.Button(connection_frame, text="Connect", command=connect_to_database, bootstyle=SUCCESS)
connect_button.grid(row=5, column=0, columnspan=2, pady=10)

# Query frame - hidden until connection is successful
query_frame = ttk.Frame(root)

# Database selection dropdown
ttk.Label(query_frame, text="Database:").grid(row=0, column=0, padx=10, pady=5)
db_dropdown = ttk.Combobox(query_frame, state="readonly")
db_dropdown.grid(row=0, column=1, padx=10, pady=5)

# Query input with syntax highlighting (basic)
ttk.Label(query_frame, text="Query:").grid(row=1, column=0, padx=10, pady=5)
query_entry = tk.Text(query_frame, height=5, width=40)
query_entry.grid(row=1, column=1, padx=10, pady=5)

# Execute button
execute_button = ttk.Button(query_frame, text="Execute", command=execute_query, bootstyle=INFO)
execute_button.grid(row=2, column=0, columnspan=2, pady=10)

# Query output (JSON result)
ttk.Label(query_frame, text="Query Output (JSON):").grid(row=3, column=0, padx=10, pady=5)
query_output = tk.Text(query_frame, height=10, width=50)
query_output.grid(row=3, column=1, padx=10, pady=5)

# Frame to hold both Export, Logout, and Exit buttons
button_frame = ttk.Frame(query_frame)
button_frame.grid(row=4, column=0, columnspan=2, pady=10)

# Export button
export_button = ttk.Button(button_frame, text="Export", command=export_data, bootstyle=PRIMARY)
export_button.pack(side=tk.LEFT, padx=10)


# Exit button
exit_button = ttk.Button(button_frame, text="Exit", command=exit_app, bootstyle=INFO)
exit_button.pack(side=tk.LEFT, padx=10)

# Logout button
logout_button = ttk.Button(button_frame, text="Logout", command=logout, bootstyle=DANGER)
logout_button.pack(side=tk.LEFT, padx=10)

# Initially hide the query frame
query_frame.grid_remove()

root.mainloop()
