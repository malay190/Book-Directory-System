import sqlite3
import os

# Create database and table if not exists
def get_connection():
    # Check if the database file already exists
    if not os.path.exists("database.db"):
        print("Database file 'database.db' does not exist. Creating a new one.")
    
    # Connect to the SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS book (
            Title TEXT,
            Author TEXT,
            Year INTEGER,
            ISBN INTEGER PRIMARY KEY
        )
    """)
    conn.commit()  # Commit the transaction to save changes

    return conn, c

def fetch_book_by_isbn(c, isbn):
    c.execute("SELECT * FROM book WHERE ISBN = ?", (isbn,))
    return c.fetchone()

def fetch_all_books(c):
    c.execute("SELECT * FROM book")
    return c.fetchall()

def search_books(c, title, author, year, isbn):
    c.execute("SELECT * FROM book WHERE Title=? OR Author=? OR Year=? OR ISBN=?", 
              (title, author, year, isbn))
    return c.fetchall()

def insert_book(c, conn, title, author, year, isbn):
    c.execute("INSERT INTO book (Title, Author, Year, ISBN) VALUES (?, ?, ?, ?)", 
              (title, author, year, isbn))
    conn.commit()

def update_book(c, conn, title, author, year, isbn):
    c.execute("UPDATE book SET Title=?, Author=?, Year=?, ISBN=? WHERE ISBN=?", 
              (title, author, year, isbn, isbn))
    conn.commit()

def delete_book(c, conn, isbn):
    c.execute("DELETE FROM book WHERE ISBN=?", (isbn,))
    conn.commit()
