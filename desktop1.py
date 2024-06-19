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
        self.db1_frame = Frame(self.root)
        self.db1_frame.pack(padx=20, pady=10, side=tk.LEFT)  # Align to the left

        Label(self.db1_frame, text="Database 1 Configuration", font=("Arial", 12, "bold")).grid(row=0, columnspan=2,
                                                                                                pady=10)

        Label(self.db1_frame, text="IP Address:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.ip1_entry = Entry(self.db1_frame)
        self.ip1_entry.grid(row=1, column=1, padx=5, pady=5)
        self.ip1_entry.focus()

        Label(self.db1_frame, text="Port:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.port1_entry = Entry(self.db1_frame)
        self.port1_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(self.db1_frame, text="Username:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.username1_entry = Entry(self.db1_frame)
        self.username1_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(self.db1_frame, text="Password:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.password1_entry = Entry(self.db1_frame, show="*")
        self.password1_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(self.db1_frame, text="Database Name:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.db1_name_entry = Entry(self.db1_frame)
        self.db1_name_entry.grid(row=5, column=1, padx=5, pady=5)

        # Second Database Configuration Frame
        self.db2_frame = Frame(self.root)
        self.db2_frame.pack(padx=20, pady=10, side=tk.RIGHT)  # Align to the right

        Label(self.db2_frame, text="Database 2 Configuration", font=("Arial", 12, "bold")).grid(row=0, columnspan=2,
                                                                                                pady=10)

        Label(self.db2_frame, text="IP Address:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.ip2_entry = Entry(self.db2_frame)
        self.ip2_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(self.db2_frame, text="Port:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.port2_entry = Entry(self.db2_frame)
        self.port2_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(self.db2_frame, text="Username:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.username2_entry = Entry(self.db2_frame)
        self.username2_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(self.db2_frame, text="Password:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.password2_entry = Entry(self.db2_frame, show="*")
        self.password2_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(self.db2_frame, text="Database Name:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.db2_name_entry = Entry(self.db2_frame)
        self.db2_name_entry.grid(row=5, column=1, padx=5, pady=5)

        # Option to Set Same Details for Second Database
        self.set_same_var = BooleanVar()
        self.set_same_check = Checkbutton(self.root, text="Set Same Details for Second Database",
                                          variable=self.set_same_var)
        self.set_same_check.pack(padx=20, pady=10)

        # Options for Apply Changes and Print Details
        self.apply_changes_var = BooleanVar()
        self.apply_changes_check = Checkbutton(self.root, text="Apply Changes",
                                               variable=self.apply_changes_var)
        self.apply_changes_check.pack(padx=20, pady=5)

        self.print_details_var = BooleanVar()
        self.print_details_check = Checkbutton(self.root, text="Print Details",
                                               variable=self.print_details_var)
        self.print_details_check.pack(padx=20, pady=5)

        # Run Button
        self.run_button = Button(self.root, text="Run Comparison", command=self.run_comparison)
        self.run_button.pack(padx=20, pady=10)

        # Result Box
        self.result_box = Text(self.root, height=10, width=80)
        self.result_box.pack(padx=20, pady=10)

        # Set validation for required fields
        self.root.bind("<Return>", self.validate_entries)

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

    def compare_databases(self, priority_db_config, non_priority_db_config, apply_changes, print_details):
        try:
            priority_connection = pymysql.connect(**priority_db_config)
            non_priority_connection = pymysql.connect(**non_priority_db_config)

            comparison_result = self.compare_and_sync_schemas(priority_connection, non_priority_connection,
                                                              apply_changes, print_details)

            # Update result box with the comparison result
            self.result_box.delete('1.0', tk.END)  # Clear previous content
            self.result_box.insert(tk.END, comparison_result)

            # Close connections
            priority_connection.close()
            non_priority_connection.close()
        except Exception as e:
            print(f"Error comparing databases: {e}")
            self.result_box.delete('1.0', tk.END)  # Clear previous content
            self.result_box.insert(tk.END, e)

    def compare_and_sync_schemas(self, priority_connection, non_priority_connection, apply_changes, print_details):
        comparison_result = ""
        priority_tables = self.get_tables(priority_connection)
        non_priority_tables = self.get_tables(non_priority_connection)

        # Synchronize missing tables
        for table in priority_tables - non_priority_tables:
            if print_details:
                comparison_result += f"Table {table} not found in non-priority database.\n"
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
                    comparison_result += f"Column {column} ({priority_schema[column]}) not found in table {table} of non-priority database.\n"
                else:
                    comparison_result += f"Column {column} missing in table {table}\n"
                if apply_changes:
                    self.alter_table(priority_schema, non_priority_schema, table, non_priority_connection, apply_changes, print_details)

            for column in src_columns & dest_columns:
                if priority_schema[column] != non_priority_schema[column]:
                    changes_found = True  # Mark changes as found
                    if print_details:
                        comparison_result += f"Column {column} type mismatch in table {table}: {priority_schema[column]} (priority) vs {non_priority_schema[column]} (non-priority)\n"
                    else:
                        comparison_result += f"Column {column} type mismatch in table {table}\n"
                    if apply_changes:
                        self.alter_table(priority_schema, non_priority_schema, table, non_priority_connection, apply_changes, print_details)

            for column in dest_columns - src_columns:
                changes_found = True  # Mark changes as found
                if print_details:
                    comparison_result += f"Column {column} ({non_priority_schema[column]}) not found in table {table} of priority database.\n"
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
