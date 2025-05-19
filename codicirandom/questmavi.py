import sqlite3
import customtkinter as ctk

conn = sqlite3.connect("quest.db")  # connessione al database
c = conn.cursor() 

# QUESTIONNAIRE
c.execute("""
CREATE TABLE IF NOT EXISTS Questionnaire (
    QuestID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Date DATE,
    Q1 INTEGER,    
    Q2 INTEGER,
    Nota2 TEXT,
    Q4 INTEGER,
    Q4_1 INTEGER,      
    Q4_2 INTEGER,
    Q4_3 INTEGER,
    Q4_4 INTEGER,
    Q4_5 INTEGER,
    Q5 INTEGER,
    Nota5 TEXT,
    Q6 INTEGER,
    Nota6 TEXT,
    Q7 INTEGER,
    Nota7 INTEGER,
    
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

class PatientMainView(ctk.CTk):
    def __init__(self, patient_id, questionnaire_done=False):
        super().__init__()

        self.patient_id = patient_id
        self.patient_name = self.get_patient_name(patient_id)
        self.questionnaire_done = questionnaire_done

        self.title(f"Patient Dashboard - {self.patient_name}")
        self.geometry("800x500")

        # layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ----- Sidebar -----
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.profile_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {self.patient_name}", font=("Arial", 14, "bold"))
        self.profile_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.show_home, width=140)
        self.home_button.grid(row=1, column=0, padx=10, pady=10)

        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", command=self.show_visual_data, width=140)
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        # ----- Main content -----
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#e6f0ff")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.show_home()

        self.mainloop()

    def show_home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Welcome to your Patient Portal",
            font=("Arial", 22, "bold"),
            text_color="#204080" 
            )
        title.pack(pady=20)

        # Buttons area
        self.questionnaire_button = ctk.CTkButton(self.main_frame, text=questionnaire_text, width=250,
                                                  command=self.open_questionnaire, state=questionnaire_state)
        self.questionnaire_button.pack(pady=15)

        self.visits_button = ctk.CTkButton(self.main_frame, text="Visits", width=250,
                                           command=self.open_visits)
        self.visits_button.pack(pady=15)

        self.medication_button = ctk.CTkButton(self.main_frame, text="Medication", width=250,
                                               command=self.open_medication)
        self.medication_button.pack(pady=15)

    def show_visual_data(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        title = ctk.CTkLabel(
            self.main_frame, text="Visual Data (coming soon)",             
            font=("Arial", 22, "bold"),
            text_color="#204080" 
            
            )
        title.pack(pady=20)

    def open_questionnaire(self):
        print("Open Questionnaire window")  # da collegare

    def open_visits(self):
        print("Open Visits window")  # da collegare

    def open_medication(self):
        print("Open Medication window")  # da collegare

    def get_patient_name(self, patient_id):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Name, Surname FROM Patients WHERE PatientID = ?", (patient_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return f"{result[0]} {result[1]}"
        else:
            return "Unknown Patient"

def open_questionnaire(self):
    self.current_question_index = 0
    self.answers = {}
    
    self.questions = [
        {"text": "How many times do you wake up during the night?", "type": "int", "key": "Q1"},
        {"text": "Did you sleep well", "type": "int", "key": "Q2"},
        {"text": "Nota: motivations of bad sleeping", "type": "text", "key": "Nota2"},
        {"text": "Have you encountered any problem with night measurements?", "type": "int", "key": "Q4"},
        {"text": "What kind of problem did you have?", "type": "int", "key": "Q4_1"},
        {"text": "Do you want to receive a daily reminder?", "type": "int", "key": "Q4_2"},
        # inserire alarm clock
        {"text": "Is technical support neeeded?", "type": "int", "key": "Q4_3"},+
        #technician is notified
        {"text": "Did you have any sleep apneas?", "type": "int", "key": "Q4_4"},
        {"text": "How many apneas did you have?", "type": "int", "key": "Q4_5"},
        #notifica al dottore
    ]
    
    self.show_question()

def show_question(self):
    for widget in self.main_frame.winfo_children():
        widget.destroy()

    question_data = self.questions[self.current_question_index]
    question_text = question_data["text"]
    question_type = question_data["type"]

    label = ctk.CTkLabel(self.main_frame, text=question_text, font=("Arial", 18), text_color="#204080")
    label.pack(pady=20)

    if question_type == "int":
        self.answer_var = ctk.IntVar()
        for i in range(1, 6):  # Opzioni da 1 a 5
            btn = ctk.CTkRadioButton(self.main_frame, text=str(i), variable=self.answer_var, value=i)
            btn.pack(anchor="w", padx=20)

    elif question_type == "text":
        self.answer_var = ctk.StringVar()
        self.text_entry = ctk.CTkEntry(self.main_frame, textvariable=self.answer_var, width=400)
        self.text_entry.pack(pady=10)

    # Pulsanti di navigazione
    nav_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
    nav_frame.pack(pady=30)

    if self.current_question_index > 0:
        back_button = ctk.CTkButton(nav_frame, text="Back", command=self.previous_question)
        back_button.grid(row=0, column=0, padx=10)

    next_text = "Finish" if self.current_question_index == len(self.questions) - 1 else "Next"
    next_button = ctk.CTkButton(nav_frame, text=next_text, command=self.next_question)
    next_button.grid(row=0, column=1, padx=10)

def next_question(self):
    question_key = self.questions[self.current_question_index]["key"]
    if isinstance(self.answer_var, ctk.IntVar):
        self.answers[question_key] = self.answer_var.get()
    elif isinstance(self.answer_var, ctk.StringVar):
        self.answers[question_key] = self.answer_var.get()

    if self.current_question_index < len(self.questions) - 1:
        self.current_question_index += 1
        self.show_question()
    else:
        self.save_answers_to_db()
        self.show_home()

def previous_question(self):
    self.current_question_index -= 1
    self.show_question()

def save_answers_to_db(self):
    import datetime
    conn = sqlite3.connect("quest.db")
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
    conn.close()
    self.questionnaire_done = True



