"""Used to initialize the database
"""

import sqlite3 as sl

def delete_db():
    """Erases the database
    """
    con = sl.connect('data.db')
    cursor = con.cursor()

    cursor.execute('''drop table if exists users;''')

    con.commit()

def create_db():
    """Creates new table into the database
    """
    con = sl.connect('data.db')
    cursor = con.cursor()

    cursor.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL CHECK (role IN ('user', 'admin')) DEFAULT 'user')''')

    cursor.execute('''INSERT INTO users(username, password, role) VALUES (?, ?, ?)''', ("admin", "admin", "admin"))

    # Broken authentication + Security Misconfiguration, admin admin user usable by anyone who finds it.

    con.commit()
    con.close()

if __name__ == "__main__":
    delete_db()
    create_db()