import sqlite3
import datetime
import customtkinter as ctk

# matplotlib
import matplotlib
matplotlib.use("TkAgg")  # Use TkAgg backend for matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class AHIView(ctk.CTk):
    def __init__(self, patient_id, patient_name="Unknown Patient"):
        super().__init__()
        self.patient_id = patient_id
        self.patient_name = patient_name

        self.title(f"AHI - {self.patient_name}")
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

        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", command=self.go_visual_data, width=140)
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#e6f0ff")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.show_ahi()

        self.mainloop()

    def center_window(self):
        w = 800
        h = 500
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def get_indexes_data(self):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Date, ValueAHI FROM Indexes WHERE PatientID = ? ORDER BY Date DESC", (self.patient_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    def show_ahi(self):
        data = self.get_indexes_data()
        last_night_value = data[0][1] if data else "N/A"

        #today = datetime.date.today() se voglio la data di oggi dal pc
        today = datetime.date(2025, 4, 21)  # finto oggi
        seven_days_ago = today - datetime.timedelta(days=7)
        seven_days_data = [value for date_str, value in data if datetime.date.fromisoformat(date_str) >= seven_days_ago]
        seven_days_mean = round(sum(seven_days_data) / len(seven_days_data), 2) if seven_days_data else "N/A"

        ctk.CTkLabel(self.main_frame, text="AHI", font=("Arial", 20, "bold"), fg_color="#c8b4e3", width=120).pack(pady=10)
        ctk.CTkLabel(self.main_frame, text=f"Last Night Value: {last_night_value}", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(self.main_frame, text=f"7 Days Mean: {seven_days_mean}", font=("Arial", 16)).pack(pady=10)

        plot_frame = ctk.CTkFrame(self.main_frame, height=300, width=700, fg_color="white")
        plot_frame.pack(pady=20)

        # estraiamo dati
        data = self.get_indexes_data()
        dates = [datetime.datetime.strptime(date_str, "%Y-%m-%d").date() for date_str, value in data]
        values = [value for date_str, value in data]

        # creiamo figura
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(dates, values, marker="o", color="#3366cc")
        ax.set_title("AHI values over time")
        ax.set_xlabel("Date")
        ax.set_ylabel("AHI value")
        ax.grid(True)
        fig.autofmt_xdate()

        # inseriamo nel frame
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        
    def go_home(self):
        from patient_main_view import PatientMainView
        self.destroy()
        PatientMainView(patient_id=self.patient_id)

    def go_visual_data(self):
        from patient_indexes_view import PatientIndexes
        self.destroy()
        PatientIndexes(patient_id=self.patient_id, patient_name=self.patient_name)

if __name__ == "__main__":
    AHIView(patient_id="PAT001")