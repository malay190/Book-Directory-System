import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from database import *
from tooltip import ToolTip

class BookDirectoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Directory")
        self.root.geometry("800x600")
        self.root.config(bg="light pink")

        # Configure grid weights for resizing
        self.root.grid_rowconfigure(4, weight=1)  # Allow row 4 (Listbox area) to expand
        self.root.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Allow all columns to expand

        # Input fields
        self.setup_input_fields()

        # Buttons
        self.setup_buttons()

        # Listbox with Scrollbar
        self.setup_listbox()

    def setup_input_fields(self):
        tk.Label(self.root, text="Title").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_title = tk.Entry(self.root)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ToolTip(self.entry_title, "Input: text")

        tk.Label(self.root, text="Author").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_author = tk.Entry(self.root)
        self.entry_author.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        ToolTip(self.entry_author, "Input: text")

        tk.Label(self.root, text="Year").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_year = tk.Entry(self.root)
        self.entry_year.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ToolTip(self.entry_year, "Input: integer")

        tk.Label(self.root, text="ISBN").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_isbn = tk.Entry(self.root)
        self.entry_isbn.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        ToolTip(self.entry_isbn, "Input: integer")

    def setup_buttons(self):
        tk.Button(self.root, text="View All", command=self.view_all).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(self.root, text="Search Entry", command=self.search_entry).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(self.root, text="Add Entry", command=self.add_entry).grid(row=2, column=2, padx=5, pady=5, sticky="ew")
        tk.Button(self.root, text="Update Selected", command=self.update_selected).grid(row=2, column=3, padx=5, pady=5, sticky="ew")
        tk.Button(self.root, text="Delete Selected", command=self.delete).grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(self.root, text="Exit", command=self.exit_app).grid(row=3, column=2, padx=5, pady=5, sticky="ew")

    def setup_listbox(self):
        frame = tk.Frame(self.root)
        frame.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.scrollbar = tk.Scrollbar(frame, orient="vertical")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Listbox to display books
        self.book_listbox = tk.Listbox(frame, yscrollcommand=self.scrollbar.set, height=10)
        self.book_listbox.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.book_listbox.yview)

        # Bind selection event
        self.book_listbox.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, event):
        try:
            # Get the index of the selected item
            selected_index = self.book_listbox.curselection()
            
            if not selected_index:
                return
            
            # Get the actual selected data (book details)
            selected = self.book_listbox.get(selected_index)

            # Ignore header or separator rows
            if selected.startswith("Title") or selected.startswith("-"):
                return

            # Use a consistent delimiter for splitting (assuming `|` was used)
            details = selected.split("|")

            # Ensure correct length
            if len(details) == 4:
                title, author, year, isbn = [field.strip() for field in details]
                
                # Fill the input fields with the selected book's details
                self.entry_title.delete(0, tk.END)
                self.entry_title.insert(0, title)
                
                self.entry_author.delete(0, tk.END)
                self.entry_author.insert(0, author)
                
                self.entry_year.delete(0, tk.END)
                self.entry_year.insert(0, year)
                
                self.entry_isbn.delete(0, tk.END)
                self.entry_isbn.insert(0, isbn)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing selection: {e}")

            
    def view_all(self):
        conn, c = get_connection()
        try:
            books = fetch_all_books(c)
            self.book_listbox.delete(0, tk.END)

            # Add headers with proper formatting
            self.book_listbox.insert(tk.END, f"{'Title':<30} | {'Author':<30} | {'Year':<10} | {'ISBN':<15}")
            self.book_listbox.insert(tk.END, "-" * 85)

            for row in books:
                # Format each field properly
                self.book_listbox.insert(tk.END, f"{row[0]:<30}{row[1]:<30}{row[2]:<10}{row[3]:<15}")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")
        finally:
            conn.close()

    def search_entry(self):
        conn, c = get_connection()
        try:
            title, author, year, isbn = self.entry_title.get(), self.entry_author.get(), self.entry_year.get(), self.entry_isbn.get()
            self.book_listbox.delete(0, tk.END)
            
            books = search_books(c, title, author, year, isbn)

            # Add headers with proper formatting
            self.book_listbox.insert(tk.END, f"{'Title':<30}{'Author':<30}{'Year':<10}{'ISBN':<15}")
            self.book_listbox.insert(tk.END, "-" * 85)

            for row in books:
                # Format each field properly
                self.book_listbox.insert(tk.END, f"{row[0]:<30}{row[1]:<30}{row[2]:<10}{row[3]:<15}")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {e}")
        finally:
            conn.close()

    def add_entry(self):
        if not self.entry_title.get() or not self.entry_author.get() or not self.entry_year.get().isdigit() or not self.entry_isbn.get().isdigit():
            messagebox.showerror("Error", "All fields must be filled correctly!")
            return
        conn, c = get_connection()
        try:
            insert_book(c, conn, self.entry_title.get(), self.entry_author.get(), int(self.entry_year.get()), int(self.entry_isbn.get()))
            messagebox.showinfo("Success", "Entry added successfully!")
            self.view_all()

            # Clear the input fields after successful insertion
            self.entry_title.delete(0, tk.END)
            self.entry_author.delete(0, tk.END)
            self.entry_year.delete(0, tk.END)
            self.entry_isbn.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Error adding entry: {e}")
        finally:
            conn.close()

    def update_selected(self):
        if not self.book_listbox.curselection():
            messagebox.showerror("Error", "No item selected!")
            return

        selected = self.book_listbox.get(tk.ACTIVE)
        if selected and selected != "Title\tAuthor\tYear\tISBN":
            isbn = selected.split("\t")[-1]

            # Get the data from the input fields
            title = self.entry_title.get()
            author = self.entry_author.get()
            year = self.entry_year.get()
            isbn_input = self.entry_isbn.get()

            # Validate inputs
            if not title or not author or not year.isdigit() or not isbn_input.isdigit():
                messagebox.showerror("Error", "Please fill all fields correctly!")
                return

            conn, c = get_connection()
            try:
                # Update the book details in the database
                update_book(c, conn, title, author, int(year), int(isbn_input))
                messagebox.showinfo("Success", "Record updated successfully!")
                self.view_all()  # Refresh the listbox to show the updated data
            except Exception as e:
                messagebox.showerror("Error", f"Error updating entry: {e}")
            finally:
                conn.close()

    def delete(self):
        if not self.book_listbox.curselection():
            messagebox.showerror("Error", "No item selected!")
            return
        conn, c = get_connection()
        try:
            selected = self.book_listbox.get(tk.ACTIVE)
            if selected and selected != "Title\tAuthor\tYear\tISBN":
                isbn = selected.split("\t")[-1]
                delete_book(c, conn, isbn)
                messagebox.showinfo("Success", "Record deleted successfully!")
                self.view_all()  # Refresh the listbox
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting entry: {e}")
        finally:
            conn.close()

    def exit_app(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookDirectoryApp(root)
    root.mainloop()
