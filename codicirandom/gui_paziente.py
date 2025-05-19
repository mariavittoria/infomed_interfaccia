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

        self.title(f"Patient Dashboard - {self.patient_name}")
        self.geometry("800x500")

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.profile_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {self.patient_name}", font=("Arial", 14, "bold"))
        self.profile_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.show_home, width=140)
        self.home_button.grid(row=1, column=0, padx=10, pady=10)

        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", command=self.show_visual_data, width=140)
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        # Main content
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#e6f0ff")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

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

            # Frame orizzontale per pulsanti
            button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            button_frame.pack(pady=5)

            self.questionnaire_button = ctk.CTkButton(button_frame, text="✔️ Questionnaire completed", width=220, state="disabled")
            self.questionnaire_button.pack(side="left", padx=(0, 5))

            # Frame per le risposte (inizialmente nascosto)
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

            # Popola le risposte
            for key, answer in self.answers.items():
                if key in ["PatientID", "Date"]:
                    continue
                question = self.question_text_map.get(key, key)  # fallback al codice se mancante
                label = ctk.CTkLabel(self.answers_frame_inner, text=f"{question}\nAnswer: {answer}", anchor="w", justify="left", wraplength=700)
                label.pack(anchor="w", padx=10, pady=5)
        else:
                    self.questionnaire_button = ctk.CTkButton(self.main_frame, text="Questionnaire", width=250, command=self.open_questionnaire)
                    self.questionnaire_button.pack(pady=15)

        def toggle_answers():
            if self.answers_container.winfo_ismapped():
                self.answers_container.pack_forget()
                self.toggle_btn.configure(text="⬇️")
            else:
                self.answers_container.pack(pady=10, fill="both", expand=True)
                self.toggle_btn.configure(text="⬆️")

            self.toggle_btn = ctk.CTkButton(button_frame, text="⬇️", width=40, command=toggle_answers)
            self.toggle_btn.pack(side="left")

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
            {"key": "Q4", "text": "What kind of problems did you have?", "type": "choice",
             "options": ["I forgot to turn on the device", "The device doesn't work", "I had problems with the application of the sensors"],
             "conditional_on": {"key": "Q3", "value": "Yes"}},
            {"key": "Q5", "text": "Do you want to receive a daily reminder?", "type": "choice", "options": ["Yes", "No"],
             "conditional_on": {"key": "Q4", "value": "I forgot to turn on the device"}},
            {"key": "Q6", "text": "Is technical support needed?", "type": "choice", "options": ["Yes", "No"],
             "conditional_on_any": {"key": "Q4", "values": ["The device doesn't work", "I had problems with the application of the sensors"]}},
            {"key": "Q7", "text": "Did you have any sleep apneas and if so, how many?", "type": "choice",
             "options": ["0", "1", "2", "3", "4", "5+"],
             "conditional_on_any": {"key": "Q4", "values": ["The device doesn't work", "I had problems with the application of the sensors"]}},
            {"key": "Q8", "text": "Did you follow the therapy?", "type": "choice", "options": ["Yes", "No"]},
            {"key": "Q9", "text": "What went wrong?", "type": "text", "conditional_on": {"key": "Q8", "value": "No"}},
            {"key": "Q10", "text": "Do you want to insert a note for the doctor?", "type": "choice", "options": ["Yes", "No"]},
            {"key": "Q11", "text": "Insert your note:", "type": "text", "conditional_on": {"key": "Q10", "value": "Yes"}},
            {"key": "Q12", "text": "Did you weigh yourself today?", "type": "choice",
             "options": ["No change in weight", "I didn’t get weighed today", "Yes, I want to insert my weight"]},
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
        if cond:
            if self.answers.get(cond["key"]) != cond["value"]:
                self.current_question_index += 1
                self.show_question()
                return
        elif cond_any:
            if self.answers.get(cond_any["key"]) not in cond_any["values"]:
                self.current_question_index += 1
                self.show_question()
                return

        label = ctk.CTkLabel(self.main_frame, text=q["text"], font=("Arial", 18), text_color="#204080")
        label.pack(pady=20)

        self.answer_var = ctk.StringVar()
        previous_answer = self.answers.get(q["key"], "")
        self.answer_var.set(previous_answer)

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
            back_btn = ctk.CTkButton(nav, text="Back", command=self.previous_question)
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

        values = {
            "PatientID": self.patient_id,
            "Date": datetime.date.today().isoformat(),
            **self.answers
        }

        columns = ', '.join(values.keys())
        placeholders = ', '.join('?' for _ in values)
        sql = f"INSERT INTO Questionnaire ({columns}) VALUES ({placeholders})"
        c.execute(sql, tuple(values.values()))
        conn.commit()

        apnea = self.answers.get("Q7")
        therapy = self.answers.get("Q8")
        note = self.answers.get("Q11")

        notify_medico = False
        if note and note.strip():
            notify_medico = True
        if apnea and apnea.isdigit() and int(apnea) > 1:
            notify_medico = True
        if therapy == "No":
            notify_medico = True

        if notify_medico:
            self.notify_doctor()

        if self.answers.get("Q5") == "Yes":
            self.schedule_daily_reminder()

        conn.close()
        self.questionnaire_done = True
        self.load_answers_from_db()
        self.show_home()

    def open_visits(self):
        print("Open Visits window")

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

    def schedule_daily_reminder(self):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT PhoneNumber FROM Patients WHERE PatientID = ?", (self.patient_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            phone_number = result[0]
            print(f"[REMINDER] SMS ogni sera alle 21 a {phone_number}: 'Ricorda di accendere il dispositivo per la notte.'")
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

if __name__ == "__main__":
    app = PatientMainView(patient_id="PAT001")
    app.mainloop()

