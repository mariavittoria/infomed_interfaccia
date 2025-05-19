import customtkinter as ctk
import sqlite3 
import datetime

class VisitView(ctk.CTk):
    def __init__(self, patient_id, patient_name):
        super().__init__()
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.current_start_date = datetime.date.today() + datetime.timedelta(days=1)

        self.title("Visita")
        self.geometry("800x500")
        self.center_window()

        # Layout principale
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Nome paziente
        self.profile_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {patient_name}", anchor="w", font=("Arial", 14, "bold"))
        self.profile_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")

        # Pulsante evidenziato Home
        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.show_home, width=140)
        self.home_button.grid(row=1, column=0, padx=10, pady=10)

        # Pulsante Visual Data
        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", width=140, command=self.visual_data)
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        # --- Area centrale ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#e6f0ff")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.main_frame.grid_rowconfigure((1, 2), weight=1)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)

        # Titolo centrale
        title = ctk.CTkLabel(self.main_frame, text="Visits", font=("Arial", 24, "bold"), text_color="#204080")
        title.grid(row=0, column=0, columnspan=2, pady=40)

        # Bottone "book visit"
        book_button = ctk.CTkButton(self.main_frame, text="Book a visit", width=150, fg_color="#9b59b6", command=self.book_visit)
        book_button.grid(row=1, column=0, padx=20)

        # Bottone "check appointment"
        check_button = ctk.CTkButton(self.main_frame, text="Check appointments", width=150, fg_color="#b76ba3", command=self.check_appointment)
        check_button.grid(row=1, column=1, padx=20)

        self.mainloop()

    def book_visit(self):
        self.render_booking_interface()

    def render_booking_interface(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.main_frame, text="Book a Visit", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=6, pady=10)

        # Frecce di navigazione
        left_arrow = ctk.CTkButton(self.main_frame, text="←", width=30, command=self.go_left)
        left_arrow.grid(row=1, column=0, padx=5)

        right_arrow = ctk.CTkButton(self.main_frame, text="→", width=30, command=self.go_right)
        right_arrow.grid(row=1, column=5, padx=5)

        # Giorni da visualizzare
        days = [(self.current_start_date + datetime.timedelta(days=i)) for i in range(4)]

        slots = self.get_available_slots(
            self.current_start_date,
            self.current_start_date + datetime.timedelta(days=3)
        )

        for i, date in enumerate(days):
            col = i + 1  # colonne 1-4
            day_label = ctk.CTkLabel(self.main_frame, text=date.strftime("%d %b"), font=("Arial", 12, "bold"))
            day_label.grid(row=2, column=col, pady=5)

            day_slots = slots.get(date.isoformat(), [])
            for row, time in enumerate(day_slots):
                btn = ctk.CTkButton(
                    self.main_frame,
                    text=time,
                    width=100,
                    command=lambda d=date, t=time: self.book_slot(d, t)
                )
                btn.grid(row=row + 3, column=col, pady=2)

    def go_left(self):
        self.current_start_date -= datetime.timedelta(days=1)
        self.render_booking_interface()

    def go_right(self):
        self.current_start_date += datetime.timedelta(days=1)
        self.render_booking_interface()

    def check_appointment(self):
        print(f"[{self.patient_id}] Controllo appuntamenti...")

    def visual_data(self):
        print("Visual Data clicked")

    def show_home(self):
        print("Home clicked")

    def center_window(self):
        w = 800
        h = 500
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    
def book_slot(self, date, time):
    conn = sqlite3.connect("Database_proj.db")
    cursor = conn.cursor()

    # Aggiungi prenotazione
    cursor.execute("""
        INSERT INTO Appointments (PatientID, Date, TimeSlot)
        VALUES (?, ?, ?)
    """, (self.patient_id, date.isoformat(), time))

    # Segna lo slot come prenotato
    cursor.execute("""
        UPDATE AvailableSlots SET IsBooked = 1
        WHERE Date = ? AND TimeSlot = ?
    """, (date.isoformat(), time))

    conn.commit()
    conn.close()

    print(f"{self.patient_id} ha prenotato il {date} alle {time}")
    self.render_booking_interface()  # ricarica la vista aggiornata


if __name__ == "__main__":
    VisitView(patient_id="PAT001", patient_name="Luca Bianchi")
