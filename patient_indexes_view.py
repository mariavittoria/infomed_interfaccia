# patient_indexes_view.py
import customtkinter as ctk
import sqlite3

class PatientIndexes(ctk.CTk):
    def __init__(self, patient_id, patient_name="Unknown Patient"):
        super().__init__()
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.notification_count = self.get_notification_count()

        self.title(f"Patient Indexes - {self.patient_name}")
        self.geometry("900x600")
        self.center_window()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1f2a44")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.profile_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {self.patient_name}", font=("Arial", 14, "bold"), text_color="white")
        self.profile_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.go_home, width=140)
        self.home_button.grid(row=1, column=0, padx=10, pady=10)

        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", width=140)
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        self.notification_button = ctk.CTkButton(
            self.sidebar_frame,
            text=f"Notifications ({self.notification_count})",
            command=self.show_notifications,
            width=140
        )
        self.notification_button.grid(row=3, column=0, padx=10, pady=10)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#f4f9ff")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.show_indexes()

        self.mainloop()

    def center_window(self):
        w = 900
        h = 600
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def get_notification_count(self):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM Notifications 
            WHERE PatientID = ? AND IsRead = 0
        """, (self.patient_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def update_notification_button(self):
        self.notification_count = self.get_notification_count()
        self.notification_button.configure(text=f"Notifications ({self.notification_count})")

    def show_notifications(self):
        from patient_main_view import PatientMainView
        self.destroy()
        main_view = PatientMainView(patient_id=self.patient_id)
        main_view.show_notifications()

    def show_indexes(self):
        title = ctk.CTkLabel(self.main_frame, text="Select an Index", font=("Arial", 24, "bold"), text_color="#204080")
        title.pack(pady=30)

        # Create a frame for buttons to center them
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        # AHI button
        ahi_button = ctk.CTkButton(
            button_frame,
            text="AHI",
            width=200,
            fg_color="#3366cc",
            command=self.open_ahi
        )
        ahi_button.pack(pady=15)

        # ODI button
        odi_button = ctk.CTkButton(
            button_frame,
            text="ODI",
            width=200,
            fg_color="#3366cc",
            command=self.open_odi
        )
        odi_button.pack(pady=15)

        # SpO2 button
        spo2_button = ctk.CTkButton(
            button_frame,
            text="SpO₂",
            width=200,
            fg_color="#3366cc",
            command=self.open_spo2
        )
        spo2_button.pack(pady=15)

    def go_home(self):
        from patient_main_view import PatientMainView
        self.destroy()
        PatientMainView(patient_id=self.patient_id)

    def open_ahi(self):
        from ahi_view import AHIView
        self.destroy()
        AHIView(patient_id=self.patient_id, patient_name=self.patient_name)

    def open_odi(self):
        from odi_view import ODIView
        self.destroy()
        ODIView(patient_id=self.patient_id, patient_name=self.patient_name)

    def open_spo2(self):
        from spo2_view import SpO2View
        self.destroy()
        SpO2View(patient_id=self.patient_id, patient_name=self.patient_name)

if __name__ == "__main__":
    PatientIndexes(patient_id="PAT001", patient_name="Luca Bianchi")
