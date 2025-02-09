import sqlite3

def initialize_database(db_name='chat_assistant.db'):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create Employees table
        cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            Department TEXT,
            Salary REAL,
            Hire_Date TEXT
        )''')

        # Create Departments table
        cursor.execute('''CREATE TABLE IF NOT EXISTS departments (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            Manager TEXT
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS table_metadata (
            table_name TEXT PRIMARY KEY,
            description TEXT
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS column_metadata (
            table_name TEXT,
            column_name TEXT,
            data_type TEXT,
            description TEXT,
            PRIMARY KEY (table_name, column_name),
            FOREIGN KEY (table_name) references table_metadata (table_name)
            )''')
        # Insert sample data into Employees table
        employees_data = [
            (1, 'Alice', 'Sales', 50000, '2021-01-15'),
            (2, 'Bob', 'Engineering', 70000, '2020-06-10'),
            (3, 'Charlie', 'Marketing', 60000, '2022-03-20'),
            (4, 'David', 'HR', 45000, '2019-11-05'),
            (5, 'Eve', 'Finance', 65000, '2020-03-18'),
            (6, 'Frank', 'IT', 72000, '2021-07-22'),
            (7, 'Grace', 'Operations', 55000, '2022-01-10'),
            (8, 'Hank', 'Customer Service', 48000, '2021-04-12'),
            (9, 'Ivy', 'Sales', 51000, '2018-09-30'),
            (10, 'Jack', 'Engineering', 80000, '2020-12-01'),
            (11, 'Kim', 'Marketing', 77000, '2021-08-15'),
            (12, 'Leo', 'HR', 50000, '2019-05-23'),
            (13, 'Mona', 'Finance', 51000, '2022-02-17'),
            (14, 'Nate', 'IT', 71000, '2020-07-07'),
            (15, 'Olivia', 'Operations', 62000, '2021-10-20'),
            (16, 'Paul', 'Customer Service', 46000, '2018-12-12'),
            (17, 'Quinn', 'Sales', 68000, '2020-04-05'),
            (18, 'Rose', 'Engineering', 75000, '2019-03-14'),
            (19, 'Steve', 'Marketing', 56000, '2021-06-30'),
            (20, 'Tracy', 'HR', 49000, '2020-02-02'),
            (21, 'Uma', 'Finance', 54000, '2022-08-08'),
            (22, 'Victor', 'IT', 81000, '2021-09-19'),
            (23, 'Wendy', 'Operations', 78000, '2019-07-27'),
            (24, 'Xander', 'Customer Service', 52000, '2020-11-11'),
            (25, 'Yvonne', 'Sales', 53000, '2021-12-31'),
        ]
        cursor.executemany('INSERT INTO Employees VALUES (?, ?, ?, ?, ?)', employees_data)

        # Insert sample data into Departments table
        departments_data = [
            (1, 'Sales', 'Alice'),               
            (2, 'Engineering', 'Bob'),           
            (3, 'Marketing', 'Charlie'),         
            (4, 'HR', 'David'),                  
            (5, 'Finance', 'Eve'),              
            (6, 'IT', 'Frank'),                  
            (7, 'Operations', 'Grace'),          
            (8, 'Customer Service', 'Hank'),     
        ]
        cursor.executemany('INSERT INTO Departments VALUES (?, ?, ?)', departments_data)
        cursor.execute("INSERT INTO table_metadata (table_name, description) VALUES ('Employees','Details of Employees in Department.')")
        cursor.execute("INSERT INTO table_metadata (table_name, description) VALUES ('Department','Details of Manager of the Department.')")

        cursor.execute("INSERT INTO column_metadata (table_name, column_name, data_type,description) VALUES ('Employees','id','INTEGER','Identification number of the Employee.')")
        cursor.execute("INSERT INTO column_metadata (table_name, column_name, data_type,description) VALUES ('Employees','name','TEXT','Name of the Employee.')")
        cursor.execute("INSERT INTO column_metadata (table_name, column_name, data_type,description) VALUES ('Employees','department','TEXT','Department of the Employee.')")
        cursor.execute("INSERT INTO column_metadata (table_name, column_name, data_type,description) VALUES ('Employees','Salary','INTEGER','Salary of the Employee.')")
        cursor.execute("INSERT INTO column_metadata (table_name, column_name, data_type,description) VALUES ('Employees','Hire_Date','DATE','Date in which the Employee was hired.')")

        cursor.execute("INSERT INTO column_metadata (table_name, column_name, data_type,description) VALUES ('Departments','id','INTEGER','Identification number of the Employee.')")
        cursor.execute("INSERT INTO column_metadata (table_name, column_name, data_type,description) VALUES ('Departments','name','TEXT','Name of the Department.')")
        cursor.execute("INSERT INTO column_metadata (table_name, column_name, data_type,description) VALUES ('Departments','manager','TEXT','Manager of the Department.')")
        conn.commit()
        
        print("Database initialized successfully.")

    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    initialize_database()
