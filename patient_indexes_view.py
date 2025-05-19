# patient_indexes_view.py
import customtkinter as ctk

class PatientIndexes(ctk.CTk):
    def __init__(self, patient_id, patient_name="Unknown Patient"):
        super().__init__()
        self.patient_id = patient_id
        self.patient_name = patient_name

        self.title(f"Patient Indexes - {self.patient_name}")
        self.geometry("800x500")
        self.center_window()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.profile_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {self.patient_name}", font=("Arial", 14, "bold"))
        self.profile_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.go_home, width=140)
        self.home_button.grid(row=1, column=0, padx=10, pady=10)

        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", width=140, state="disabled")
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#e6f0ff")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.show_indexes()

        self.mainloop()

    def center_window(self):
        w = 800
        h = 500
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def show_indexes(self):
        ctk.CTkLabel(self.main_frame, text="Select an Index", font=("Arial", 18, "bold"), text_color="#204080").pack(pady=30)
        ctk.CTkButton(self.main_frame, text="AHI", width=200, fg_color="#c8b4e3", command=self.open_ahi).pack(pady=15)
        ctk.CTkButton(self.main_frame, text="ODI", width=200, fg_color="#e0cda9", command=self.open_odi).pack(pady=15)
        ctk.CTkButton(self.main_frame, text="SpO2", width=200, fg_color="#a8d5ba", command=self.open_spo2).pack(pady=15)

    def go_home(self):
        from patient_main_view import PatientMainView  # attenzione al nome file!
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
        print("ODI")

    def open_spo2(self):
        from spo2_view import SpO2View
        self.destroy()
        SpO2View(patient_id=self.patient_id, patient_name=self.patient_name)
        print("SpO2")

if __name__ == "__main__":
    PatientIndexes(patient_id="PAT001", patient_name="Luca Bianchi")
