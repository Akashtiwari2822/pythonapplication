import tkinter as tk
from tkinter import ttk
from tkinter import Frame, Label, Entry, Checkbutton, BooleanVar, Button, Text, messagebox

import pymysql


class DatabaseComparerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Comparer")

        self.create_widgets()

    def create_widgets(self):
        # First Database Configuration Frame
        self.db1_frame = tk.Frame(self.root, padx=20, pady=10)
        self.db1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(self.db1_frame, text="Database 1 Configuration", font=("Arial", 12, "bold")).pack(pady=(0, 10))

        self.create_db_config_section(self.db1_frame, "IP Address:")
        self.create_db_config_section(self.db1_frame, "Port:")
        self.create_db_config_section(self.db1_frame, "Username:")
        self.create_db_config_section(self.db1_frame, "Password:", show="*")
        self.create_db_config_section(self.db1_frame, "Database Name:")

        # Second Database Configuration Frame
        self.db2_frame = tk.Frame(self.root, padx=20, pady=10)
        self.db2_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(self.db2_frame, text="Database 2 Configuration", font=("Arial", 12, "bold")).pack(pady=(0, 10))

        self.create_db_config_section(self.db2_frame, "IP Address:")
        self.create_db_config_section(self.db2_frame, "Port:")
        self.create_db_config_section(self.db2_frame, "Username:")
        self.create_db_config_section(self.db2_frame, "Password:", show="*")
        self.create_db_config_section(self.db2_frame, "Database Name:")

        # self.db3_frame = tk.Frame(self.root, padx=20, pady=10)
        # self.db3_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Option to Set Same Details for Second Database
        self.set_same_var = tk.BooleanVar()
        self.set_same_check = tk.Checkbutton(self.root, text="Set Same Details for Second Database",
                                             variable=self.set_same_var, command=self.set_same_details)
        self.set_same_check.pack(padx=20, pady=(10, 5), anchor=tk.W)

        # Buttons for Fetching Tables
        self.create_button("Fetch Tables for DB1", self.fetch_tables_db1)
        self.create_button("Fetch Tables for DB2", self.fetch_tables_db2)

        # Selected Tables Comboboxes
        self.create_combobox("Selected Tables DB1:")
        self.create_combobox("Selected Tables DB2:")

        # Button to Compare Selected Tables
        self.compare_tables_btn = tk.Button(self.root, text="Compare Selected Tables", command=self.compare_tables)
        self.compare_tables_btn.pack(padx=20, pady=10, anchor=tk.W)

        # Options for Apply Changes and Print Details
        tk.Label(self.root, text="Options:").pack(padx=20, pady=5, anchor=tk.W)
        self.apply_changes_check = self.create_checkbox("Apply Changes")
        self.print_details_check = self.create_checkbox("Print Details")

        # Run Button
        self.run_button = tk.Button(self.root, text="Run Comparison", command=self.run_comparison)
        self.run_button.pack(padx=20, pady=10, anchor=tk.W)

        # Separator (Vertical)
        ttk.Separator(self.root, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=50)

        # Result Box
        self.result_box = tk.Text(self.root, width=80, height=20)
        self.result_box.pack(side=tk.LEFT, padx=20, pady=10, anchor=tk.W)

    def create_db_config_section(self, parent, label_text, show=None):
        frame = tk.Frame(parent)
        frame.pack(fill=tk.X)

        tk.Label(frame, text=label_text, width=15, anchor=tk.E).pack(side=tk.LEFT)
        entry = tk.Entry(frame, show=show)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    def create_button(self, text, command):
        btn = tk.Button(self.root, text=text, command=command, width=20)
        btn.pack(padx=20, pady=5, anchor=tk.W)

    def create_combobox(self, label_text):
        tk.Label(self.root, text=label_text, width=15, anchor=tk.W).pack(padx=20, pady=5, anchor=tk.W)
        combobox = ttk.Combobox(self.root, width=30, state="readonly")
        combobox.pack(padx=20, pady=5, anchor=tk.W)

    def create_checkbox(self, text):
        var = tk.BooleanVar()
        check = tk.Checkbutton(self.root, text=text, variable=var, anchor=tk.W)
        check.pack(padx=20, pady=5, anchor=tk.W)
        return var
        # def create_widgets(self):
    #     # First Database Configuration Frame
    #     # First Database Configuration Frame
    #     self.db1_frame = Frame(self.root)
    #     self.db1_frame.pack(padx=20, pady=10, side=tk.LEFT)  # Align to the left
    #
    #     Label(self.db1_frame, text="Database 1 Configuration", font=("Arial", 12, "bold")).grid(row=0, columnspan=2,
    #                                                                                             pady=10)
    #
    #     Label(self.db1_frame, text="IP Address:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    #     self.ip1_entry = Entry(self.db1_frame)
    #     self.ip1_entry.grid(row=1, column=1, padx=5, pady=5)
    #     self.ip1_entry.focus()
    #
    #     Label(self.db1_frame, text="Port:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    #     self.port1_entry = Entry(self.db1_frame)
    #     self.port1_entry.grid(row=2, column=1, padx=5, pady=5)
    #
    #     Label(self.db1_frame, text="Username:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
    #     self.username1_entry = Entry(self.db1_frame)
    #     self.username1_entry.grid(row=3, column=1, padx=5, pady=5)
    #
    #     Label(self.db1_frame, text="Password:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
    #     self.password1_entry = Entry(self.db1_frame, show="*")
    #     self.password1_entry.grid(row=4, column=1, padx=5, pady=5)
    #
    #     Label(self.db1_frame, text="Database Name:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
    #     self.db1_name_entry = Entry(self.db1_frame)
    #     self.db1_name_entry.grid(row=5, column=1, padx=5, pady=5)
    #
    #     # Second Database Configuration Frame
    #     self.db2_frame = Frame(self.root)
    #     self.db2_frame.pack(padx=20, pady=10, side=tk.LEFT)  # Align to the left
    #
    #     Label(self.db2_frame, text="Database 2 Configuration", font=("Arial", 12, "bold")).grid(row=0, columnspan=2,
    #                                                                                             pady=10)
    #
    #     Label(self.db2_frame, text="IP Address:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    #     self.ip2_entry = Entry(self.db2_frame)
    #     self.ip2_entry.grid(row=1, column=1, padx=5, pady=5)
    #
    #     Label(self.db2_frame, text="Port:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    #     self.port2_entry = Entry(self.db2_frame)
    #     self.port2_entry.grid(row=2, column=1, padx=5, pady=5)
    #
    #     Label(self.db2_frame, text="Username:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
    #     self.username2_entry = Entry(self.db2_frame)
    #     self.username2_entry.grid(row=3, column=1, padx=5, pady=5)
    #
    #     Label(self.db2_frame, text="Password:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
    #     self.password2_entry = Entry(self.db2_frame, show="*")
    #     self.password2_entry.grid(row=4, column=1, padx=5, pady=5)
    #
    #     Label(self.db2_frame, text="Database Name:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
    #     self.db2_name_entry = Entry(self.db2_frame)
    #     self.db2_name_entry.grid(row=5, column=1, padx=5, pady=5)
    #
    #     # Option to Set Same Details for Second Database
    #     self.set_same_var = BooleanVar()
    #     self.set_same_check = Checkbutton(self.root, text="Set Same Details for Second Database",
    #                                       variable=self.set_same_var, command=self.set_same_details)
    #     self.set_same_check.pack(padx=20, pady=5)
    #
    #     # Buttons for Fetching Tables
    #     self.fetch_tables_btn1 = Button(self.root, text="Fetch Tables for DB1", command=self.fetch_tables_db1)
    #     self.fetch_tables_btn1.pack(padx=20, pady=5)
    #
    #     self.fetch_tables_btn2 = Button(self.root, text="Fetch Tables for DB2", command=self.fetch_tables_db2)
    #     self.fetch_tables_btn2.pack(padx=20, pady=5)
    #
    #     # Selected Tables Comboboxes
    #     Label(self.root, text="Selected Tables DB1:").pack(padx=20, pady=5)
    #     self.selected_tables_db1 = ttk.Combobox(self.root, width=30, state="readonly")
    #     self.selected_tables_db1.pack(padx=20, pady=5)
    #
    #     Label(self.root, text="Selected Tables DB2:").pack(padx=20, pady=5)
    #     self.selected_tables_db2 = ttk.Combobox(self.root, width=30, state="readonly")
    #     self.selected_tables_db2.pack(padx=20, pady=5)
    #
    #     # Button to Compare Selected Tables
    #     self.compare_tables_btn = Button(self.root, text="Compare Selected Tables", command=self.compare_tables)
    #     self.compare_tables_btn.pack(padx=20, pady=10)
    #
    #     # Options for Apply Changes and Print Details
    #     Label(self.root, text="Options:").pack(padx=20, pady=5)
    #     self.apply_changes_var = BooleanVar()
    #     self.apply_changes_check = Checkbutton(self.root, text="Apply Changes", variable=self.apply_changes_var)
    #     self.apply_changes_check.pack(padx=20, pady=5)
    #
    #     self.print_details_var = BooleanVar()
    #     self.print_details_check = Checkbutton(self.root, text="Print Details", variable=self.print_details_var)
    #     self.print_details_check.pack(padx=20, pady=5)
    #
    #     # Run Button
    #     self.run_button = Button(self.root, text="Run Comparison", command=self.run_comparison)
    #     self.run_button.pack(padx=20, pady=10)
    #
    #     # Result Box
    #     self.result_box = Text(self.root, height=20, width=150)
    #     self.result_box.pack(padx=20, pady=10)
    #
    #     # Set validation for required fields
    #     self.root.bind("<Return>", self.validate_entries)

    def set_same_details(self):
        if self.set_same_var.get():
            # Copy details from DB1 to DB2
            self.ip2_entry.insert(0, self.ip1_entry.get())
            self.port2_entry.insert(0, self.port1_entry.get())
            self.username2_entry.insert(0, self.username1_entry.get())
            self.password2_entry.insert(0, self.password1_entry.get())
            self.db2_name_entry.insert(0, self.db1_name_entry.get())
        else:
            # Clear DB2 details if checkbox is unchecked
            self.ip2_entry.delete(0, tk.END)
            self.port2_entry.delete(0, tk.END)
            self.username2_entry.delete(0, tk.END)
            self.password2_entry.delete(0, tk.END)
            self.db2_name_entry.delete(0, tk.END)
    def validate_entries(self, event):
        ip1 = self.ip1_entry.get()
        port1 = self.port1_entry.get()
        username1 = self.username1_entry.get()
        password1 = self.password1_entry.get()
        db1_name = self.db1_name_entry.get()

        ip2 = self.ip2_entry.get()
        port2 = self.port2_entry.get()
        username2 = self.username2_entry.get()
        password2 = self.password2_entry.get()
        db2_name = self.db2_name_entry.get()

        if not ip1 or not port1 or not username1 or not password1 or not db1_name:
            messagebox.showerror("Error", "Please fill in all fields for Database 1.")
        elif not ip2 or not port2 or not username2 or not password2 or not db2_name:
            messagebox.showerror("Error", "Please fill in all fields for Database 2.")
        else:
            self.run_comparison()

    def fetch_tables_db1(self):
        ip1 = self.ip1_entry.get()
        port1 = self.port1_entry.get()
        username1 = self.username1_entry.get()
        password1 = self.password1_entry.get()
        db1_name = self.db1_name_entry.get()

        # Connect to the database
        try:
            db1_connection = pymysql.connect(host=ip1, port=int(port1), user=username1, password=password1,
                                             database=db1_name)
            with db1_connection.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                db1_tables = [row[0] for row in cursor.fetchall()]  # Fetch all table names
                self.selected_tables_db1['values'] = db1_tables
                if db1_tables:
                    self.selected_tables_db1.current(0)  # Select the first table by default
                else:
                    messagebox.showinfo("Info", "No tables found in Database 1.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching tables from Database 1: {e}")

        finally:
            if db1_connection:
                db1_connection.close()

    def fetch_tables_db2(self):
        ip2 = self.ip2_entry.get()
        port2 = self.port2_entry.get()
        username2 = self.username2_entry.get()
        password2 = self.password2_entry.get()
        db2_name = self.db2_name_entry.get()

        # Connect to DB2 and fetch tables
        try:
            db2_connection = pymysql.connect(host=ip2, port=int(port2), user=username2, password=password2,
                                             database=db2_name)
            with db2_connection.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                db2_tables = [row[0] for row in cursor.fetchall()]  # Fetch all table names
                self.selected_tables_db2['values'] = db2_tables
                if db2_tables:
                    self.selected_tables_db2.current(0)  # Select the first table by default
                else:
                    messagebox.showinfo("Info", "No tables found in Database 2.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching tables from Database 2: {e}")

        finally:
            if db2_connection:
                db2_connection.close()

    def compare_tables(self):
        selected_table1 = self.selected_tables_db1.get()
        selected_table2 = self.selected_tables_db2.get()
        print_details = self.print_details_var.get()

        if not selected_table1 or not selected_table2:
            messagebox.showerror("Error", "Please select tables from both databases.")
            return

        # Get the database names
        db1_name = self.db1_name_entry.get()
        db2_name = self.db2_name_entry.get()

        # Fetch column information for both tables from both databases
        db1_columns = self.get_columns(self.ip1_entry.get(), self.port1_entry.get(), self.username1_entry.get(),
                                       self.password1_entry.get(), db1_name, selected_table1)
        db2_columns = self.get_columns(self.ip2_entry.get(), self.port2_entry.get(), self.username2_entry.get(),
                                       self.password2_entry.get(), db2_name, selected_table2)

        # Compare the columns and generate comparison result
        comparison_result = self.compare_columns(db1_columns, db2_columns, db1_name, db2_name, selected_table1,
                                                 selected_table2, print_details)

        # Display the comparison result
        self.result_box.delete('1.0', tk.END)  # Clear previous content
        self.result_box.insert(tk.END, comparison_result)

    def get_columns(self, ip, port, username, password, dbname, tablename):
        try:
            connection = pymysql.connect(host=ip, port=int(port), user=username, password=password, database=dbname)
            with connection.cursor() as cursor:
                cursor.execute(f"DESCRIBE {tablename}")
                columns = {row[0]: row[1] for row in cursor.fetchall()}
                return columns
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error fetching columns from database: {e}")
        finally:
            connection.close()

    def compare_columns(self, db1_columns, db2_columns, db1_name, db2_name, table1, table2, print_details):
        comparison_result = f"Comparison results for tables {table1} and {table2} in {db1_name} and {db2_name}:\n"

        db1_columns_set = set(db1_columns.keys())
        db2_columns_set = set(db2_columns.keys())

        common_columns = db1_columns_set & db2_columns_set
        mismatched_columns = []
        missing_columns_db1 = db2_columns_set - db1_columns_set
        missing_columns_db2 = db1_columns_set - db2_columns_set

        for column in common_columns:
            if db1_columns[column] != db2_columns[column]:
                mismatched_columns.append((column, db1_columns[column], db2_columns[column]))

        if print_details:
            if mismatched_columns:
                comparison_result += "Columns with type mismatches:\n"
                for column, type_db1, type_db2 in mismatched_columns:
                    comparison_result += f"{column}: {type_db1} (DB1), {type_db2} (DB2)\n"
            else:
                comparison_result += "No columns with type mismatches.\n"
        else:
            comparison_result += "Common columns:\n"
            for column in common_columns:
                comparison_result += f"{column}\n"

        if missing_columns_db1:
            comparison_result += f"Columns missing in {db1_name} {table1}: {', '.join(missing_columns_db1)}\n"

        if missing_columns_db2:
            comparison_result += f"Columns missing in {db2_name} {table2}: {', '.join(missing_columns_db2)}\n"

        return comparison_result

    def compare_selected_tables(self):
        selected_table1 = self.selected_tables_db1.get()
        selected_table2 = self.selected_tables_db2.get()
        print_details = self.print_details_var.get()

        if not selected_table1 or not selected_table2:
            messagebox.showerror("Error", "Please select tables from both databases.")
            return

        # Get the database names
        db1_name = self.db1_name_entry.get()
        db2_name = self.db2_name_entry.get()

        # Fetch column information for both tables from both databases
        db1_columns = self.get_columns(self.ip1_entry.get(), self.port1_entry.get(), self.username1_entry.get(),
                                       self.password1_entry.get(), db1_name, selected_table1)
        db2_columns = self.get_columns(self.ip2_entry.get(), self.port2_entry.get(), self.username2_entry.get(),
                                       self.password2_entry.get(), db2_name, selected_table2)

        # Compare the columns and generate comparison result
        comparison_result = self.compare_columns(db1_columns, db2_columns, db1_name, db2_name, selected_table1,
                                                 selected_table2, print_details)

        # Display the comparison result
        self.result_box.delete('1.0', tk.END)  # Clear previous content
        self.result_box.insert(tk.END, comparison_result)

    def check_database_exists(self, host, port, user, password, database):
        try:
            connection = pymysql.connect(host=host, port=int(port), user=user, password=password, database=database)
            connection.close()
            return True
        except pymysql.err.OperationalError:
            return False

    def create_database(self, host, port, user, password, database):
        try:
            connection = pymysql.connect(host=host, port=int(port), user=user, password=password)
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            connection.close()
        except pymysql.err.OperationalError as e:
            print(f"Error creating database: {e}")
    def run_comparison(self):
        ip1 = self.ip1_entry.get()
        port1 = self.port1_entry.get()
        username1 = self.username1_entry.get()
        password1 = self.password1_entry.get()
        db1_name = self.db1_name_entry.get()

        ip2 = ip1 if self.set_same_var.get() else self.ip2_entry.get()
        port2 = port1 if self.set_same_var.get() else self.port2_entry.get()
        username2 = username1 if self.set_same_var.get() else self.username2_entry.get()
        password2 = password1 if self.set_same_var.get() else self.password2_entry.get()
        db2_name = self.db2_name_entry.get()

        # Check if the database names exist, or create them if needed
        if not self.check_database_exists(ip1, port1, username1, password1, db1_name):
            self.create_database(ip1, port1, username1, password1, db1_name)
        if not self.check_database_exists(ip2, port2, username2, password2, db2_name):
            self.create_database(ip2, port2, username2, password2, db2_name)

        # Perform the comparison
        db1_config = {
            'host': ip1,
            'port': int(port1),
            'user': username1,
            'password': password1,
            'database': db1_name
        }
        db2_config = {
            'host': ip2,
            'port': int(port2),
            'user': username2,
            'password': password2,
            'database': db2_name
        }

        apply_changes = self.apply_changes_var.get()
        print_details = self.print_details_var.get()

        self.compare_databases(db1_config, db2_config, apply_changes, print_details)

    def compare_databases(self, db1_config, db2_config, apply_changes, print_details):
        try:
            db1_connection = pymysql.connect(**db1_config)
            db2_connection = pymysql.connect(**db2_config)

            comparison_result = self.compare_and_sync_schemas(db1_connection, db2_connection,
                                                              apply_changes, print_details)

            # Update result box with the comparison result
            self.result_box.delete('1.0', tk.END)  # Clear previous content
            self.result_box.insert(tk.END, comparison_result)

            # Close connections
            db1_connection.close()
            db2_connection.close()
        except Exception as e:
            print(f"Error comparing databases: {e}")
            self.result_box.delete('1.0', tk.END)  # Clear previous content
            self.result_box.insert(tk.END, e)

    def compare_and_sync_schemas(self, priority_connection, non_priority_connection, apply_changes, print_details):
        comparison_result = ""

        # Get database names from connection configurations
        db1_name = None
        db2_name = None
        try:
            with priority_connection.cursor() as cursor:
                cursor.execute("SELECT DATABASE()")
                db1_name = cursor.fetchone()[0]
        except Exception as e:
            print(f"Error retrieving database name from priority connection: {e}")

        try:
            with non_priority_connection.cursor() as cursor:
                cursor.execute("SELECT DATABASE()")
                db2_name = cursor.fetchone()[0]
        except Exception as e:
            print(f"Error retrieving database name from non-priority connection: {e}")

        priority_tables = self.get_tables(priority_connection)
        non_priority_tables = self.get_tables(non_priority_connection)

        # Synchronize missing tables
        for table in priority_tables - non_priority_tables:
            if print_details:
                comparison_result += f"Table {table} not found in {db2_name} database.\n"
            else:
                comparison_result += f"Table {table} not found\n"
            if apply_changes:
                self.create_table(priority_connection, non_priority_connection, table, apply_changes, print_details)

        common_tables = priority_tables & non_priority_tables

        changes_found = False  # Flag to track if any changes are found

        for table in common_tables:
            priority_schema = self.get_table_schema(priority_connection, table)
            non_priority_schema = self.get_table_schema(non_priority_connection, table)

            if priority_schema is None or non_priority_schema is None:
                if print_details:
                    comparison_result += f"Skipping table: {table} due to schema fetch error.\n"
                continue

            src_columns = set(priority_schema.keys())
            dest_columns = set(non_priority_schema.keys())

            for column in src_columns - dest_columns:
                changes_found = True  # Mark changes as found
                if print_details:
                    comparison_result += f"Column {column} ({priority_schema[column]}) not found in table {table} of {db2_name} database.\n"
                else:
                    comparison_result += f"Column {column} missing in table {table}\n"
                if apply_changes:
                    self.alter_table(priority_schema, non_priority_schema, table, non_priority_connection,
                                     apply_changes, print_details)

            for column in src_columns & dest_columns:
                if priority_schema[column] != non_priority_schema[column]:
                    changes_found = True  # Mark changes as found
                    if print_details:
                        comparison_result += f"Column {column} type mismatch in table {table}: {priority_schema[column]} ({db1_name}) vs {non_priority_schema[column]} ({db2_name})\n"
                    else:
                        comparison_result += f"Column {column} type mismatch in table {table}\n"
                    if apply_changes:
                        self.alter_table(priority_schema, non_priority_schema, table, non_priority_connection,
                                         apply_changes, print_details)

            for column in dest_columns - src_columns:
                changes_found = True  # Mark changes as found
                if print_details:
                    comparison_result += f"Column {column} ({non_priority_schema[column]}) not found in table {table} of {db1_name} database.\n"
                else:
                    comparison_result += f"Column {column} extra in table {table}\n"
                if apply_changes:
                    self.alter_table(priority_schema, non_priority_schema, table, non_priority_connection)

        if not changes_found:
            comparison_result += "No changes found."

        return comparison_result

    def create_table(self, src_connection, dest_connection, table_name, apply_changes, print_details):
        with src_connection.cursor() as cursor:
            cursor.execute(f"SHOW CREATE TABLE {table_name}")
            create_table_sql = cursor.fetchone()[1]
            if apply_changes:
                with dest_connection.cursor() as dest_cursor:
                    dest_cursor.execute(create_table_sql)
                    if print_details:
                        return f"Created table {table_name} in the non-priority database."
            else:
                if print_details:
                    return f"CREATE TABLE SQL for {table_name}: {create_table_sql}"
            return f"CREATE table {table_name}"

    def get_tables(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            return {row[0] for row in cursor.fetchall()}

    def get_table_schema(self, connection, table_name):
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"DESCRIBE {table_name}")
                return {row[0]: row[1] for row in cursor.fetchall()}
            except pymysql.err.OperationalError as e:
                print(f"Error: {e}")
                print(f"Failed to describe table: {table_name}")
                return None

    def alter_table(self, src_schema, dest_schema, table_name, dest_connection, apply_changes, print_details):
        alter_statements = []
        src_columns = set(src_schema.keys())
        dest_columns = set(dest_schema.keys())

        # Columns to be added in the non-priority database
        for column in src_columns - dest_columns:
            alter_statements.append(f"ADD COLUMN {column} {src_schema[column]}")

        # Columns to be altered in the non-priority database
        for column in src_columns & dest_columns:
            if src_schema[column] != dest_schema[column]:
                alter_statements.append(f"MODIFY COLUMN {column} {src_schema[column]}")

        if alter_statements:
            alter_sql = f"ALTER TABLE {table_name} " + ", ".join(alter_statements)
            if apply_changes:
                with dest_connection.cursor() as cursor:
                    cursor.execute(alter_sql)
                    if print_details:
                        print(f"Altered table {table_name} in the non-priority database.")
            else:
                if print_details:
                    print(f"ALTER TABLE SQL for {table_name}: {alter_sql}")
                else:
                    print(f"ALTER table {table_name}")


# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseComparerApp(root)
    root.mainloop()
