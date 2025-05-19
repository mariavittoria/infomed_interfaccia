import sqlite3
import datetime
import customtkinter as ctk

class PatientMainView(ctk.CTk):
    def __init__(self, patient_id):
        super().__init__()

        self.patient_id = patient_id
        self.answers = {}
        self.questionnaire_done = self.check_if_questionnaire_done()

        if self.questionnaire_done:
            self.load_answers_from_db()

        self.patient_name = self.get_patient_name(patient_id)
        self.notification_count = 0

        self.title(f"Patient Dashboard - {self.patient_name}")
        self.geometry("800x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.profile_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {self.patient_name}", font=("Arial", 14, "bold"))
        self.profile_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.show_home, width=140)
        self.home_button.grid(row=1, column=0, padx=10, pady=10)

        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", command=self.show_visual_data, width=140)
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        self.notification_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Notifiche (0)",  # inizialmente zero
            command=self.show_notifications,
            width=140
        )
        self.notification_button.grid(row=3, column=0, padx=10, pady=10)

        def update_notification_button(self):
            self.notification_button.configure(text=f"Notifiche ({self.notification_count})")

        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#e6f0ff")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    ###questionario
        self.question_text_map = {
            "Q1": "How many times did you wake up during the night?",
            "Q2": "Did you sleep well?",
            "Nota2": "Please describe what was wrong:",
            "Q3": "Have you encountered any problems with night measurements?",
            "Q4": "What kind of problems did you have?",
            "Q5": "Do you want to receive a daily reminder?",
            "Q6": "Is technical support needed?",
            "Q7": "Did you have any sleep apneas and if so, how many?",
            "Q8": "Did you follow the therapy?",
            "Q9": "What went wrong?",
            "Q10": "Do you want to insert a note for the doctor?",
            "Q11": "Insert your note:",
            "Q12": "Did you weigh yourself today?",
            "Q13": "Insert your weight:"
        }

        self.show_home()

    def show_home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.main_frame, text="Welcome to your Patient Portal", font=("Arial", 22, "bold"), text_color="#204080")
        title.pack(pady=20)

        if self.questionnaire_done:
            info_label = ctk.CTkLabel(self.main_frame, text="✅ Questionnaire already completed", font=("Arial", 16))
            info_label.pack(pady=10)

            button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            button_frame.pack(pady=5)

            self.questionnaire_button = ctk.CTkButton(button_frame, text="✔️ Questionnaire completed", width=220, state="disabled")
            self.questionnaire_button.pack(side="left", padx=(0, 5))

            self.answers_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.answers_container.pack_forget()

            self.answers_scroll_canvas = ctk.CTkCanvas(self.answers_container, bg="#e6f0ff", highlightthickness=0)
            self.answers_scroll_canvas.pack(side="left", fill="both", expand=True)

            scrollbar = ctk.CTkScrollbar(self.answers_container, orientation="vertical", command=self.answers_scroll_canvas.yview)
            scrollbar.pack(side="right", fill="y")

            self.answers_scroll_canvas.configure(yscrollcommand=scrollbar.set)

            self.answers_frame_inner = ctk.CTkFrame(self.answers_scroll_canvas, fg_color="transparent")
            self.answers_scroll_canvas.create_window((0, 0), window=self.answers_frame_inner, anchor="nw")

            def on_frame_configure(event):
                self.answers_scroll_canvas.configure(scrollregion=self.answers_scroll_canvas.bbox("all"))

            self.answers_frame_inner.bind("<Configure>", on_frame_configure)

            for key, answer in self.answers.items():
                if key in ["PatientID", "Date"]:
                    continue
                question = self.question_text_map.get(key, key)
                label = ctk.CTkLabel(self.answers_frame_inner, text=f"{question}\nAnswer: {answer}", anchor="w", justify="left", wraplength=700)
                label.pack(anchor="w", padx=10, pady=5)

            def toggle_answers():
                if self.answers_container.winfo_ismapped():
                    self.answers_container.pack_forget()
                    self.toggle_btn.configure(text="⬇️")
                else:
                    self.answers_container.pack(pady=10, fill="both", expand=True)
                    self.toggle_btn.configure(text="⬆️")

            self.toggle_btn = ctk.CTkButton(button_frame, text="⬇️", width=40, command=toggle_answers)
            self.toggle_btn.pack(side="left")

        else:
            self.questionnaire_button = ctk.CTkButton(self.main_frame, text="Questionnaire", width=250, command=self.open_questionnaire)
            self.questionnaire_button.pack(pady=15)

        self.visits_button = ctk.CTkButton(self.main_frame, text="Visits", width=250, command=self.open_visits)
        self.visits_button.pack(pady=15)

        self.medication_button = ctk.CTkButton(self.main_frame, text="Medication", width=250, command=self.open_medication)
        self.medication_button.pack(pady=15)

    def show_visual_data(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        title = ctk.CTkLabel(self.main_frame, text="Visual Data (coming soon)", font=("Arial", 22, "bold"), text_color="#204080")
        title.pack(pady=20)

    def open_questionnaire(self):
        self.current_question_index = 0
        self.answers = {}
        self.questions = [
            {"key": "Q1", "text": "How many times did you wake up during the night?", "type": "choice", "options": ["0", "1", "2", "3", "4", "5+"]},
            {"key": "Q2", "text": "Did you sleep well?", "type": "choice", "options": ["Yes", "No"]},
            {"key": "Nota2", "text": "Please describe what was wrong:", "type": "text", "conditional_on": {"key": "Q2", "value": "No"}},
            {"key": "Q3", "text": "Have you encountered any problems with night measurements?", "type": "choice", "options": ["Yes", "No"]},
            {"key": "Q4", "text": "What kind of problems did you have?", "type": "choice", "options": ["I forgot to turn on the device", "The device doesn't work", "I had problems with the application of the sensors"], "conditional_on": {"key": "Q3", "value": "Yes"}},
            {"key": "Q5", "text": "Do you want to receive a daily reminder?", "type": "choice", "options": ["Yes", "No"], "conditional_on": {"key": "Q4", "value": "I forgot to turn on the device"}},
            {"key": "Q6", "text": "Is technical support needed?", "type": "choice", "options": ["Yes", "No"], "conditional_on_any": {"key": "Q4", "values": ["The device doesn't work", "I had problems with the application of the sensors"]}},
            {"key": "Q7", "text": "Did you have any sleep apneas and if so, how many?", "type": "choice", "options": ["0", "1", "2", "3", "4", "5+"], "conditional_on_any": {"key": "Q4", "values": ["The device doesn't work", "I had problems with the application of the sensors"]}},
            {"key": "Q8", "text": "Did you follow the therapy?", "type": "choice", "options": ["Yes", "No"]},
            {"key": "Q9", "text": "What went wrong?", "type": "text", "conditional_on": {"key": "Q8", "value": "No"}},
            {"key": "Q10", "text": "Do you want to insert a note for the doctor?", "type": "choice", "options": ["Yes", "No"]},
            {"key": "Q11", "text": "Insert your note:", "type": "text", "conditional_on": {"key": "Q10", "value": "Yes"}},
            {"key": "Q12", "text": "Did you weigh yourself today?", "type": "choice", "options": ["No change in weight", "I didn't get weighed today", "Yes, I want to insert my weight"]},
            {"key": "Q13", "text": "Insert your weight:", "type": "text", "conditional_on": {"key": "Q12", "value": "Yes, I want to insert my weight"}},
        ]
        self.show_question()

    def show_question(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if self.current_question_index >= len(self.questions):
            label = ctk.CTkLabel(self.main_frame, text="Thanks for completing the questionnaire!", font=("Arial", 20, "bold"))
            label.pack(pady=40)
            self.save_answers_to_db()
            return

        q = self.questions[self.current_question_index]

        cond = q.get("conditional_on")
        cond_any = q.get("conditional_on_any")
        if cond and self.answers.get(cond["key"]) != cond["value"]:
            self.current_question_index += 1
            self.show_question()
            return
        elif cond_any and self.answers.get(cond_any["key"]) not in cond_any["values"]:
            self.current_question_index += 1
            self.show_question()
            return

        label = ctk.CTkLabel(self.main_frame, text=q["text"], font=("Arial", 18), text_color="#204080")
        label.pack(pady=20)

        self.answer_var = ctk.StringVar()
        self.answer_var.set(self.answers.get(q["key"], ""))

        if q["type"] == "choice":
            for opt in q["options"]:
                btn = ctk.CTkRadioButton(self.main_frame, text=opt, variable=self.answer_var, value=opt)
                btn.pack(anchor="w", padx=20)
        elif q["type"] == "text":
            entry = ctk.CTkEntry(self.main_frame, textvariable=self.answer_var, width=400)
            entry.pack(pady=10)

        self.error_label = ctk.CTkLabel(self.main_frame, text="", text_color="red", font=("Arial", 12))
        self.error_label.pack()

        nav = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        nav.pack(pady=30)

        if self.current_question_index > 0:
            back_btn = ctk.CTkButton(nav, text="Back", command=self.previous_question,fg_color="gray", hover_color="#a9a9a9")
            back_btn.grid(row=0, column=0, padx=10)

        next_btn = ctk.CTkButton(nav, text="Next", command=self.next_question)
        next_btn.grid(row=0, column=1, padx=10)

    def next_question(self):
        answer = self.answer_var.get()
        if not answer.strip():
            self.error_label.configure(text="Please answer before continuing.")
            return
        q = self.questions[self.current_question_index]
        self.answers[q["key"]] = answer
        self.current_question_index += 1
        self.show_question()

    def previous_question(self):
        self.current_question_index = max(0, self.current_question_index - 1)
        self.show_question()

    def save_answers_to_db(self):
        conn = sqlite3.connect("Database_proj.db")
        c = conn.cursor()
        values = {"PatientID": self.patient_id, "Date": datetime.date.today().isoformat(), **self.answers}
        columns = ', '.join(values.keys())
        placeholders = ', '.join('?' for _ in values)
        sql = f"INSERT INTO Questionnaire ({columns}) VALUES ({placeholders})"
        c.execute(sql, tuple(values.values()))
        conn.commit()

        apnea = self.answers.get("Q7")
        therapy = self.answers.get("Q8")
        note = self.answers.get("Q11")

        notify_medico = any([
            note and note.strip(),
            apnea and apnea.isdigit() and int(apnea) > 1,
            therapy == "No"
        ])

        if notify_medico:
            self.notify_doctor()

        if self.answers.get("Q5") == "Yes":
            self.schedule_daily_reminder()

        conn.close()
        self.questionnaire_done = True
        self.load_answers_from_db()
        self.show_home()

    def open_visits(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.current_start_date = datetime.date.today()
        # Adjust to start from Monday
        while self.current_start_date.weekday() != 0:  # 0 is Monday
            self.current_start_date -= datetime.timedelta(days=1)

        self.selected_date = None
        self.selected_time = None
        self.slot_buttons = {}

        title = ctk.CTkLabel(self.main_frame, text="Book a Visit", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=7, pady=10)

        # Navigation arrows
        left_arrow = ctk.CTkButton(self.main_frame, text="←", width=30, command=self.go_left_week)
        left_arrow.grid(row=1, column=0, padx=5)

        right_arrow = ctk.CTkButton(self.main_frame, text="→", width=30, command=self.go_right_week)
        right_arrow.grid(row=1, column=6, padx=5)

        # Show 5 days (Monday to Friday)
        days = [(self.current_start_date + datetime.timedelta(days=i)) for i in range(5)]
        slots = self.get_available_slots(self.current_start_date, self.current_start_date + datetime.timedelta(days=4))

        for i, date in enumerate(days):
            col = i + 1
            day_label = ctk.CTkLabel(self.main_frame, text=date.strftime("%A\n%d %b"), font=("Arial", 12, "bold"))
            day_label.grid(row=2, column=col, pady=5)

            day_slots = slots.get(date.isoformat(), [])
            for row, time in enumerate(day_slots):
                btn = ctk.CTkButton(
                    self.main_frame,
                    text=time,
                    width=100,
                    fg_color="#3498db",
                    command=lambda d=date, t=time: self.select_slot(d, t)
                )
                btn.grid(row=row + 3, column=col, pady=2)
                self.slot_buttons[(date, time)] = btn

        confirm_btn = ctk.CTkButton(self.main_frame, text="Confirm", width=120, fg_color="green", command=self.confirm_booking)
        confirm_btn.grid(row=20, column=6, pady=15, sticky="se", padx=15)

    def go_left_week(self):
        self.current_start_date -= datetime.timedelta(days=7)
        self.open_visits()

    def go_right_week(self):
        self.current_start_date += datetime.timedelta(days=7)
        self.open_visits()

    def get_available_slots(self, start_date, end_date):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        slots = {}

        cursor.execute("""
            SELECT date, time, doctor_name
            FROM Appointments
            WHERE status = 'available'
              AND date BETWEEN ? AND ?
            ORDER BY date, time
        """, (start_date.isoformat(), end_date.isoformat()))

        for date, time, doctor in cursor.fetchall():
            slots.setdefault(date, []).append(f"{time} - Dr. {doctor}")

        conn.close()
        return slots

    def select_slot(self, date, time_label):
        # Deselect all
        for btn in self.slot_buttons.values():
            btn.configure(fg_color="#3498db")

        self.selected_date = date
        self.selected_time = time_label
        selected_btn = self.slot_buttons.get((date, time_label))
        if selected_btn:
            selected_btn.configure(fg_color="gray")

    def confirm_booking(self):
        if not self.selected_date or not self.selected_time:
            error_label = ctk.CTkLabel(self.main_frame, text="Please select a time slot first", text_color="red")
            error_label.grid(row=21, column=0, columnspan=7, pady=5)
            return

        # Split doctor from time
        time, _, doctor_name = self.selected_time.partition(" - Dr. ")

        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Appointments
            SET patient_id = ?, status = 'booked'
            WHERE date = ? AND time = ? AND doctor_name = ? AND status = 'available'
        """, (self.patient_id, self.selected_date.isoformat(), time, doctor_name))

        conn.commit()
        conn.close()

        # Clear the main frame and show confirmation
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        confirmation_text = f"You confirmed your appointment with Dr. {doctor_name} on {self.selected_date.strftime('%A, %d %B')} at {time}"
        confirmation_label = ctk.CTkLabel(self.main_frame, text=confirmation_text, font=("Arial", 16))
        confirmation_label.pack(pady=50)

        back_button = ctk.CTkButton(self.main_frame, text="Back to Home", command=self.show_home)
        back_button.pack(pady=20)

    def open_medication(self):
        print("Open Medication window")

    def get_patient_name(self, patient_id):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Name, Surname FROM Patients WHERE PatientID = ?", (patient_id,))
        result = cursor.fetchone()
        conn.close()
        return f"{result[0]} {result[1]}" if result else "Unknown Patient"

    def notify_doctor(self):
        print(f"[NOTIFICA AL MEDICO] Il paziente {self.patient_name} ha inserito dati critici.")

    def schedule_daily_reminder(self): ###qua si fa che esce notifica nel posto adatto
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT PhoneNumber FROM Patients WHERE PatientID = ?", (self.patient_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            print(f"[REMINDER] SMS ogni sera alle 21 a {result[0]}: 'Ricorda di accendere il dispositivo per la notte.'")
        else:
            print("[ERRORE] Numero di telefono non trovato per il paziente.")

    def load_answers_from_db(self):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Questionnaire WHERE PatientID = ? ORDER BY Date DESC LIMIT 1", (self.patient_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            self.answers = dict(zip(columns, row))
        conn.close()

    def check_if_questionnaire_done(self):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM Questionnaire WHERE PatientID = ? LIMIT 1", (self.patient_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def show_notifications(self): ## medico che indice visita oppure nuova terapia
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        title = ctk.CTkLabel(self.main_frame, text="Notifiche", font=("Arial", 22, "bold"), text_color="#204080")
        title.pack(pady=20)

        if self.notification_count == 0:
            msg = ctk.CTkLabel(self.main_frame, text="✅ Nessuna nuova notifica", font=("Arial", 16))
            msg.pack(pady=10)
        else:
            for i in range(self.notification_count):
                n = ctk.CTkLabel(self.main_frame, text=f"🔔 Notifica {i+1}", font=("Arial", 14))
                n.pack(anchor="w", padx=20, pady=5)


if __name__ == "__main__":
    app = PatientMainView(patient_id="PAT001")
    app.mainloop()

