import customtkinter as ctk
import sqlite3
import datetime

DB_PATH = "appointments.db"

def get_available_slots_grouped():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = datetime.date.today().isoformat()

    cursor.execute('''
        SELECT id, date, time, doctor_name 
        FROM appointments 
        WHERE status = 'available' AND date >= ?
        ORDER BY date, time
    ''', (today,))

    rows = cursor.fetchall()
    conn.close()

    grouped = {}
    for row in rows:
        date = row[1]
        grouped.setdefault(date, []).append(row)
    return grouped

def book_visit(appointment_id, patient_id, patient_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE appointments
        SET patient_id = ?, patient_name = ?, status = 'booked'
        WHERE id = ?
    ''', (patient_id, patient_name, appointment_id))

    conn.commit()
    conn.close()

def get_appointments_by_patient(patient_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT date, time, doctor_name 
        FROM appointments 
        WHERE patient_id = ?
        ORDER BY date, time
    ''', (patient_id,))

    appts = cursor.fetchall()
    conn.close()
    return appts

class VisitView(ctk.CTk):
    def __init__(self, patient_id, patient_name):
        super().__init__()
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.current_start_date = datetime.date.today()

        self.title("Visita")
        self.geometry("900x600")
        self.center_window()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.profile_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {patient_name}", anchor="w", font=("Arial", 14, "bold"))
        self.profile_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.show_home, width=140)
        self.home_button.grid(row=1, column=0, padx=10, pady=10)

        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", width=140, command=self.visual_data)
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#e6f0ff")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.main_frame.grid_rowconfigure((1, 2), weight=1)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)

        title = ctk.CTkLabel(self.main_frame, text="Visits", font=("Arial", 24, "bold"), text_color="#204080")
        title.grid(row=0, column=0, columnspan=2, pady=40)

        book_button = ctk.CTkButton(self.main_frame, text="Book a visit", width=150, fg_color="#9b59b6", command=self.book_visit)
        book_button.grid(row=1, column=0, padx=20)

        check_button = ctk.CTkButton(self.main_frame, text="Check appointments", width=150, fg_color="#b76ba3", command=self.check_appointment)
        check_button.grid(row=1, column=1, padx=20)

        self.mainloop()

    def center_window(self):
        w = 900
        h = 600
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def show_home(self):
        self.clear_main()
        label = ctk.CTkLabel(self.main_frame, text="Home Page", font=("Arial", 18))
        label.pack(pady=20)

    def visual_data(self):
        self.clear_main()
        label = ctk.CTkLabel(self.main_frame, text="Dati Visualizzati", font=("Arial", 18))
        label.pack(pady=20)

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def book_visit(self):
        self.clear_main()
        title = ctk.CTkLabel(self.main_frame, text="Book a Visit", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        slots_by_date = get_available_slots_grouped()

        for date, slots in list(slots_by_date.items())[:5]:
            frame = ctk.CTkFrame(self.main_frame)
            frame.pack(padx=10, pady=5, fill="x")
            label = ctk.CTkLabel(frame, text=date, font=("Arial", 14, "bold"))
            label.pack(anchor="w")

            for slot in slots:
                text = f"{slot[2]} - Dr. {slot[3]}"
                btn = ctk.CTkButton(frame, text=text, command=lambda s=slot: self.confirm_booking(s))
                btn.pack(padx=5, pady=2, anchor="w")
        
    scrollbar = ctk.CTkScrollbar(self.answers_container, orientation="vertical", command=self.answers_scroll_canvas.yview)
    scrollbar.pack(side="right", fill="y")
    
    def confirm_booking(self, slot):
        book_visit(slot[0], self.patient_id, self.patient_name)
        self.book_visit()

    def check_appointment(self):
        self.clear_main()
        title = ctk.CTkLabel(self.main_frame, text="Your Appointments", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        appts = get_appointments_by_patient(self.patient_id)

        if not appts:
            label = ctk.CTkLabel(self.main_frame, text="No appointments found.")
            label.pack(pady=5)
        else:
            for appt in appts:
                info = f"{appt[0]} at {appt[1]} with Dr. {appt[2]}"
                label = ctk.CTkLabel(self.main_frame, text=info)
                label.pack(pady=2, anchor="w")

if __name__ == "__main__":
    VisitView(patient_id="PAT001", patient_name="Luca Bianchi")
