import customtkinter
import os
from PIL import Image
import sqlite3
import tkinter.ttk as ttk

class Seven_Days_Ok_PatientsView(customtkinter.CTk):
    def __init__(self, parent_frame, user_id):
    # Titolo
        title = customtkinter.CTkLabel(parent_frame, text="7 days ok patients", font=("Arial", 20, "bold"), text_color="black")
        title.grid(row=0, column=0, columnspan=4, pady=20)

    # Recupera dati dal database
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Seven_days_patients_ok")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()

    # Treeview style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#f0f4ff", foreground="black", rowheight=25, fieldbackground="#f0f4ff")
        style.map("Treeview", background=[('selected', '#4a7abc')])

    # Tabella
        tree = ttk.Treeview(parent_frame, columns=column_names, show='headings', height=12)
        tree.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        for col in column_names:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        for row in rows:
            tree.insert("", "end", values=row)


    def get_7_days_ok_patients(self):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Seven_days_patients_ok")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()
        return column_names, rows


if __name__ == "__main__":
    app = Seven_Days_Ok_PatientsView(user_id=1)  # oppure un altro id valido
    app.mainloop()

