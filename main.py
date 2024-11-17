import tkinter as tk
from gui import BookDirectoryApp

def main():
    root = tk.Tk()
    app = BookDirectoryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
