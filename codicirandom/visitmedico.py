import customtkinter as ctk
import sqlite3 
import datetime

class DoctorSlotManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestione Slot Medico")
        self.geometry("500x400")
        self.center_window()

        self.date_entry = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD")
        self.date_entry.pack(pady=10)

        self.slot_entry = ctk.CTkEntry(self, placeholder_text="Es: 10:00")
        self.slot_entry.pack(pady=10)

        self.add_button = ctk.CTkButton(self, text="Aggiungi Slot", command=self.add_slot)
        self.add_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack()

        self.mainloop()

    def center_window(self):
        w = 500
        h = 400
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def add_slot(self):
        date = self.date_entry.get()
        slot = self.slot_entry.get()

        if not date or not slot:
            self.status_label.configure(text="Inserisci data e orario")
            return

        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO AvailableSlots (Date, TimeSlot, IsBooked)
            VALUES (?, ?, 0)
        """, (date, slot))

        conn.commit()
        conn.close()

        self.status_label.configure(text=f"Slot {slot} per il {date} aggiunto con successo.")
        self.date_entry.delete(0, 'end')
        self.slot_entry.delete(0, 'end')

if __name__ == "__main__":
    DoctorSlotManager(doctor_id="DOC001")
