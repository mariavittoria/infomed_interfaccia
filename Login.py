import customtkinter as ctk
import sqlite3
import os
from PIL import Image
import tkinter.ttk as ttk

class AppProg:
    def __init__(self):
        self.user = ""
        self.conn = None
        self.cursor = None
        self.setup_database()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("E-Health | Login")
        self.root.geometry("420x320")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_login()
        self.root.mainloop()

    def setup_database(self):
        try:
            self.conn = sqlite3.connect("Database_proj.db")
            self.cursor = self.conn.cursor()
            # Test the connection
            self.cursor.execute("SELECT 1")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            self.root.destroy()

    def setup_login(self):
        self.login_frame = ctk.CTkFrame(self.root, width=400, height=300, corner_radius=10)
        self.login_frame.pack(pady=30)

        title = ctk.CTkLabel(self.login_frame, text="Login", font=("Arial", 20, "bold"))
        title.pack(pady=(10, 20))

        self.role_option = ctk.CTkOptionMenu(self.login_frame, values=["Doctor", "Patient"])
        self.role_option.set("Doctor")  # Default
        self.role_option.pack(pady=10)

        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="ID", width=250)
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login, width=150)
        self.login_button.pack(pady=10)

        self.message_label = ctk.CTkLabel(self.login_frame, text="", font=("Arial", 12))
        self.message_label.pack(pady=(10, 0))

    def go_to_home_doctor(self):
        try:
            from doctor_main_view import DoctorMainView
            # Create new window before destroying the old one
            doctor_window = DoctorMainView(self.user_id)
            self.root.withdraw()  # Hide the login window instead of destroying it
            doctor_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(doctor_window))
            doctor_window.mainloop()
        except Exception as e:
            self.message_label.configure(text=f"Error loading doctor interface: {str(e)}", text_color="red")
            self.root.deiconify()  # Show the login window again if there's an error

    def go_to_home_patient(self):
        try:
            from patient_main_view import PatientMainView
            # Create new window before destroying the old one
            patient_window = PatientMainView(self.user_id)
            self.root.withdraw()  # Hide the login window instead of destroying it
            patient_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(patient_window))
            patient_window.mainloop()
        except Exception as e:
            self.message_label.configure(text=f"Error loading patient interface: {str(e)}", text_color="red")
            self.root.deiconify()  # Show the login window again if there's an error

    def login(self):
        user_id = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_option.get()

        if not user_id or not password:
            self.message_label.configure(text="Please fill in all fields", text_color="red")
            return

        try:
            if role == "Doctor":
                self.cursor.execute(
                    "SELECT * FROM Doctors WHERE doctorID = ? AND DoctorPassword = ?", 
                    (user_id, password)
                )
                result = self.cursor.fetchone()
                
                if result:
                    self.user_id = user_id
                    self.message_label.configure(text="Doctor login successful", text_color="green")
                    self.go_to_home_doctor()
                else:
                    self.message_label.configure(text="Invalid doctor credentials", text_color="red")

            elif role == "Patient":
                self.cursor.execute(
                    "SELECT * FROM Patients WHERE PatientID = ? AND PatientPassword = ?", 
                    (user_id, password)
                )
                result = self.cursor.fetchone()

                if result:
                    self.user_id = user_id
                    self.message_label.configure(text="Patient login successful", text_color="green")
                    self.go_to_home_patient()
                else:
                    self.message_label.configure(text="Invalid patient credentials", text_color="red")

        except sqlite3.Error as e:
            self.message_label.configure(text=f"Database error: {str(e)}", text_color="red")
        except Exception as e:
            self.message_label.configure(text=f"An error occurred: {str(e)}", text_color="red")

    def on_closing(self, window=None):
        if window:
            window.destroy()
        if self.conn:
            self.conn.close()
        self.root.destroy()

    def __del__(self):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    AppProg()