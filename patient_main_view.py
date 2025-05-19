import sqlite3
import datetime
import customtkinter as ctk

class PatientInterface(ctk.CTk):
    def __init__(self, patient_id):
        super().__init__()

        self.patient_id = patient_id
        self.answers = {}
        self.questionnaire_done = self.check_if_questionnaire_done()

        if self.questionnaire_done:
            self.load_answers_from_db()

        self.patient_name = self.get_patient_name(patient_id)
        self.notification_count = self.get_notification_count()
        self.current_start_date = datetime.date.today() + datetime.timedelta(days=1)
        self.selected_date = None
        self.selected_time = None
        self.slot_buttons = {}

        self.title(f"Patient Dashboard - {self.patient_name}")
        self.geometry("1000x600")
        self.center_window()

        # Layout principale
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

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

        self.notification_button = ctk.CTkButton(
            self.sidebar_frame,
            text=f"Notifications ({self.notification_count})",
            command=self.show_notifications,
            width=140
        )
        self.notification_button.grid(row=3, column=0, padx=10, pady=10)

        # Main frame
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

    def center_window(self):
        w = 1000
        h = 600
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

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
            back_btn = ctk.CTkButton(nav, text="Back", command=self.previous_question, fg_color="gray", hover_color="#a9a9a9")
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

        # Center the main frame content
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(self.main_frame, text="Visits", font=("Arial", 24, "bold"), text_color="#204080")
        title.grid(row=0, column=0, columnspan=2, pady=40)

        # Create a frame for buttons to center them
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=2, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        book_button = ctk.CTkButton(button_frame, text="Book a visit", width=150, fg_color="#9b59b6", command=self.book_visit)
        book_button.grid(row=0, column=0, padx=20)

        check_button = ctk.CTkButton(button_frame, text="Check appointments", width=150, fg_color="#b76ba3", command=self.check_appointment)
        check_button.grid(row=0, column=1, padx=20)

    def book_visit(self):
        self.render_booking_interface()

    def render_booking_interface(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create main container frame
        container_frame = ctk.CTkFrame(self.main_frame)
        container_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(container_frame)
        scroll_frame.pack(fill="both", expand=True)

        # Title and close button in a frame
        title_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(title_frame, text="Book a Visit", font=("Arial", 20, "bold"))
        title.pack(side="left", padx=10)

        close_button = ctk.CTkButton(title_frame, text="✕", width=30, fg_color="red", command=self.show_home)
        close_button.pack(side="right", padx=10)

        # Navigation arrows in a frame
        nav_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(0, 20))

        left_arrow = ctk.CTkButton(nav_frame, text="←", width=30, command=self.go_left_week)
        left_arrow.pack(side="left", padx=10)

        right_arrow = ctk.CTkButton(nav_frame, text="→", width=30, command=self.go_right_week)
        right_arrow.pack(side="right", padx=10)

        # Create a frame for the calendar grid
        calendar_frame = ctk.CTkFrame(scroll_frame)
        calendar_frame.pack(fill="both", expand=True, padx=20)

        self.slot_buttons.clear()

        # Show only weekdays (Monday to Friday)
        days = []
        current_date = self.current_start_date
        while len(days) < 5:  # We want 5 weekdays
            if current_date.weekday() < 5:  # 0-4 are Monday to Friday
                days.append(current_date)
            current_date += datetime.timedelta(days=1)

        slots = self.get_available_slots(days[0], days[-1])

        # Configure grid weights for equal column widths
        for i in range(5):
            calendar_frame.grid_columnconfigure(i, weight=1)

        # Headers
        for i, date in enumerate(days):
            day_label = ctk.CTkLabel(
                calendar_frame,
                text=date.strftime("%A\n%d %b"),
                font=("Arial", 12, "bold")
            )
            day_label.grid(row=0, column=i, pady=(10, 20), padx=10)

        # Time slots
        max_slots = max(len(slots.get(date.isoformat(), [])) for date in days)
        for row in range(max_slots):
            for col, date in enumerate(days):
                day_slots = slots.get(date.isoformat(), [])
                if row < len(day_slots):
                    time = day_slots[row]
                    # Split time and doctor name
                    time_str, _, doctor_name = time.partition(" - Dr. ")
                    
                    # Create a frame for the time slot button
                    slot_frame = ctk.CTkFrame(calendar_frame, fg_color="transparent")
                    slot_frame.grid(row=row + 1, column=col, pady=5, padx=10)
                    
                    # Time button
                    time_btn = ctk.CTkButton(
                        slot_frame,
                        text=time_str,
                        width=120,
                        height=35,
                        fg_color="#e0e0e0",
                        text_color="black",
                        hover_color="#d0d0d0",
                        command=lambda d=date, t=time: self.select_slot(d, t)
                    )
                    time_btn.pack(pady=(0, 2))
                    
                    # Doctor name label
                    doctor_label = ctk.CTkLabel(
                        slot_frame,
                        text=f"Dr. {doctor_name}",
                        font=("Arial", 10),
                        text_color="gray"
                    )
                    doctor_label.pack()
                    
                    self.slot_buttons[(date, time)] = time_btn

        # Confirm button at the bottom
        confirm_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        confirm_frame.pack(fill="x", pady=20)

        confirm_btn = ctk.CTkButton(
            confirm_frame,
            text="Confirm",
            width=120,
            fg_color="green",
            command=self.confirm_booking
        )
        confirm_btn.pack(side="right", padx=20)

    def go_left_week(self):
        self.current_start_date -= datetime.timedelta(days=7)
        self.render_booking_interface()

    def go_right_week(self):
        self.current_start_date += datetime.timedelta(days=7)
        self.render_booking_interface()

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
        # Reset all buttons to default style
        for btn in self.slot_buttons.values():
            btn.configure(
                fg_color="#e0e0e0",
                text_color="black",
                hover_color="#d0d0d0"
            )

        self.selected_date = date
        self.selected_time = time_label
        selected_btn = self.slot_buttons.get((date, time_label))
        if selected_btn:
            selected_btn.configure(
                fg_color="#3498db",
                text_color="white",
                hover_color="#2980b9"
            )

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
            SET patient_id = ?, patient_name = ?, status = 'booked'
            WHERE date = ? AND time = ? AND doctor_name = ? AND status = 'available'
        """, (self.patient_id, self.patient_name, self.selected_date.isoformat(), time, doctor_name))

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

    def check_appointment(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.main_frame, text="Your Appointments", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        # Create a frame for the table
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Create headers
        headers = ["Date", "Time", "Doctor"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"))
            label.grid(row=0, column=i, padx=20, pady=10, sticky="w")

        # Get appointments from database
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT date, time, doctor_name
                FROM Appointments
                WHERE patient_id = ? AND status = 'booked'
                ORDER BY date ASC, time ASC
            """, (self.patient_id,))
            
            appointments = cursor.fetchall()
            
            if not appointments:
                no_appointments = ctk.CTkLabel(table_frame, text="No appointments found", font=("Arial", 14))
                no_appointments.grid(row=1, column=0, columnspan=3, pady=20)
            else:
                # Display appointments
                for i, (date, time, doctor) in enumerate(appointments, 1):
                    # Convert date string to datetime for comparison
                    appt_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                    today = datetime.date.today()
                    
                    # Check if appointment is tomorrow
                    if appt_date - today == datetime.timedelta(days=1):
                        self.create_notification(date, time, doctor)
                    
                    # Format date for display
                    formatted_date = appt_date.strftime("%A, %d %B %Y")
                    
                    # Create row with appointment details
                    date_label = ctk.CTkLabel(table_frame, text=formatted_date)
                    time_label = ctk.CTkLabel(table_frame, text=time)
                    doctor_label = ctk.CTkLabel(table_frame, text=f"Dr. {doctor}")
                    
                    # Add labels to grid
                    date_label.grid(row=i, column=0, padx=20, pady=5, sticky="w")
                    time_label.grid(row=i, column=1, padx=20, pady=5, sticky="w")
                    doctor_label.grid(row=i, column=2, padx=20, pady=5, sticky="w")
        except sqlite3.Error as e:
            error_label = ctk.CTkLabel(table_frame, text=f"Error loading appointments: {str(e)}", text_color="red")
            error_label.grid(row=1, column=0, columnspan=3, pady=20)
        finally:
            conn.close()

        # Add back button
        back_button = ctk.CTkButton(self.main_frame, text="Back to Home", command=self.show_home)
        back_button.pack(pady=20)

    def create_notification(self, date, time, doctor):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        
        # Check if notification already exists
        cursor.execute("""
            SELECT 1 FROM Notifications 
            WHERE PatientID = ? AND Type = 'REMINDER' 
            AND Message LIKE ?
        """, (self.patient_id, f"%{date}%"))
        
        if not cursor.fetchone():
            message = f"Reminder: You have an appointment tomorrow ({date}) at {time} with Dr. {doctor}"
            cursor.execute("""
                INSERT INTO Notifications (PatientID, PatientName, Type, Message)
                VALUES (?, ?, 'REMINDER', ?)
            """, (self.patient_id, self.patient_name, message))
            
            conn.commit()
        
        conn.close()

    def open_medication(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.main_frame, text="Medication Management", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        # Create buttons frame
        buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)

        # Modify Drugs button
        modify_drugs_button = ctk.CTkButton(
            buttons_frame,
            text="Modify Saved Drugs",
            width=200,
            command=self.show_drugs_table
        )
        modify_drugs_button.pack(side="left", padx=20)

        # View Therapy button
        view_therapy_button = ctk.CTkButton(
            buttons_frame,
            text="View Therapy",
            width=200,
            command=self.show_therapy
        )
        view_therapy_button.pack(side="left", padx=20)

        # Back button
        back_button = ctk.CTkButton(self.main_frame, text="Back to Home", command=self.show_home)
        back_button.pack(pady=20)

    def show_drugs_table(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.main_frame, text="Your Medications", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        # Create table frame
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.pack(padx=40, pady=20, fill="both", expand=True)

        # Headers
        headers = ["Drug Information", "Start Date", "End Date", "Actions"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"))
            label.grid(row=0, column=i, padx=20, pady=10, sticky="w")

        # Get drugs from database
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT ID, Note, StartDate, EndDate
                FROM Drugs
                WHERE PatientID = ?
                ORDER BY StartDate DESC
            """, (self.patient_id,))
            
            drugs = cursor.fetchall()
            
            if not drugs:
                no_drugs_label = ctk.CTkLabel(table_frame, text="No medications found", font=("Arial", 14))
                no_drugs_label.grid(row=1, column=0, columnspan=4, pady=20)
            else:
                for i, (drug_id, note, start_date, end_date) in enumerate(drugs, 1):
                    # Drug info
                    note_label = ctk.CTkLabel(table_frame, text=note, wraplength=300)
                    note_label.grid(row=i, column=0, padx=20, pady=5, sticky="w")
                    
                    # Dates
                    start_label = ctk.CTkLabel(table_frame, text=start_date)
                    start_label.grid(row=i, column=1, padx=20, pady=5, sticky="w")
                    
                    end_label = ctk.CTkLabel(table_frame, text=end_date)
                    end_label.grid(row=i, column=2, padx=20, pady=5, sticky="w")
                    
                    # Action buttons
                    actions_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
                    actions_frame.grid(row=i, column=3, padx=20, pady=5)
                    
                    edit_btn = ctk.CTkButton(
                        actions_frame,
                        text="Edit",
                        width=60,
                        command=lambda d=drug_id, n=note, s=start_date, e=end_date: self.edit_drug(d, n, s, e)
                    )
                    edit_btn.pack(side="left", padx=5)
                    
                    delete_btn = ctk.CTkButton(
                        actions_frame,
                        text="Delete",
                        width=60,
                        fg_color="red",
                        command=lambda d=drug_id: self.delete_drug(d)
                    )
                    delete_btn.pack(side="left", padx=5)
                
        except sqlite3.Error as e:
            error_label = ctk.CTkLabel(table_frame, text=f"Error loading medications: {str(e)}", text_color="red")
            error_label.grid(row=1, column=0, columnspan=4, pady=20)
        finally:
            conn.close()

        # Add new drug button
        add_button = ctk.CTkButton(
            self.main_frame,
            text="Add New Medication",
            width=200,
            command=lambda: self.edit_drug(None, "", "", "")
        )
        add_button.pack(pady=20)

        # Back button
        back_button = ctk.CTkButton(self.main_frame, text="Back to Medication", command=self.open_medication)
        back_button.pack(pady=20)

    def edit_drug(self, drug_id, note, start_date, end_date):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Edit Medication" if drug_id else "Add New Medication",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)

        # Create form frame
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(padx=40, pady=20, fill="both", expand=True)

        # Note label and text box
        note_label = ctk.CTkLabel(form_frame, text="Drug Information:", font=("Arial", 14))
        note_label.pack(pady=(20, 5))
        
        self.note_text = ctk.CTkTextbox(form_frame, width=400, height=100)
        self.note_text.pack(pady=10)
        if note:
            self.note_text.insert("1.0", note)

        # Date frame
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.pack(pady=20)

        # Start date
        start_label = ctk.CTkLabel(date_frame, text="Start Date:", font=("Arial", 14))
        start_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.start_date = ctk.CTkEntry(date_frame, placeholder_text="YYYY-MM-DD")
        self.start_date.grid(row=0, column=1, padx=20, pady=10)
        if start_date:
            self.start_date.insert(0, start_date)

        # End date
        end_label = ctk.CTkLabel(date_frame, text="End Date:", font=("Arial", 14))
        end_label.grid(row=1, column=0, padx=20, pady=10)
        
        self.end_date = ctk.CTkEntry(date_frame, placeholder_text="YYYY-MM-DD")
        self.end_date.grid(row=1, column=1, padx=20, pady=10)
        if end_date:
            self.end_date.insert(0, end_date)

        # Error label
        self.error_label = ctk.CTkLabel(form_frame, text="", text_color="red")
        self.error_label.pack(pady=10)

        # Buttons frame
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)

        # Back button (now first)
        back_button = ctk.CTkButton(
            buttons_frame,
            text="Back",
            width=120,
            command=self.show_drugs_table
        )
        back_button.pack(side="left", padx=10)

        # Save button (now second)
        save_button = ctk.CTkButton(
            buttons_frame,
            text="Save",
            width=120,
            command=lambda: self.save_drug(drug_id)
        )
        save_button.pack(side="left", padx=10)

    def save_drug(self, drug_id):
        note = self.note_text.get("1.0", "end-1c").strip()
        start_date = self.start_date.get().strip()
        end_date = self.end_date.get().strip()

        if not note or not start_date or not end_date:
            self.error_label.configure(text="Please fill in all fields")
            return

        try:
            # Validate dates
            datetime.datetime.strptime(start_date, "%Y-%m-%d")
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            self.error_label.configure(text="Invalid date format. Use YYYY-MM-DD")
            return

        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        
        try:
            if drug_id:  # Update existing drug
                cursor.execute("""
                    UPDATE Drugs
                    SET Note = ?, StartDate = ?, EndDate = ?
                    WHERE ID = ? AND PatientID = ?
                """, (note, start_date, end_date, drug_id, self.patient_id))
            else:  # Insert new drug
                cursor.execute("""
                    INSERT INTO Drugs (PatientID, Note, StartDate, EndDate)
                    VALUES (?, ?, ?, ?)
                """, (self.patient_id, note, start_date, end_date))
            
            conn.commit()
            self.show_drugs_table()  # Return to table view
            
        except sqlite3.Error as e:
            self.error_label.configure(text=f"Error saving data: {str(e)}")
        finally:
            conn.close()

    def delete_drug(self, drug_id):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                DELETE FROM Drugs
                WHERE ID = ? AND PatientID = ?
            """, (drug_id, self.patient_id))
            
            conn.commit()
            self.show_drugs_table()  # Refresh the table
            
        except sqlite3.Error as e:
            error_label = ctk.CTkLabel(self.main_frame, text=f"Error deleting medication: {str(e)}", text_color="red")
            error_label.pack(pady=20)
        finally:
            conn.close()

    def show_therapy(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.main_frame, text="Your Therapy", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        # Create therapy display frame
        therapy_frame = ctk.CTkFrame(self.main_frame)
        therapy_frame.pack(padx=40, pady=20, fill="both", expand=True)

        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT Note
                FROM Therapy
                WHERE PatientID = ?
                ORDER BY ID DESC
                LIMIT 1
            """, (self.patient_id,))
            
            result = cursor.fetchone()
            
            if result:
                therapy_text = result[0]
                therapy_label = ctk.CTkLabel(
                    therapy_frame,
                    text=therapy_text,
                    font=("Arial", 14),
                    wraplength=600,
                    justify="left"
                )
                therapy_label.pack(padx=20, pady=20)
            else:
                no_therapy_label = ctk.CTkLabel(
                    therapy_frame,
                    text="No therapy information available",
                    font=("Arial", 14)
                )
                no_therapy_label.pack(pady=20)
                
        except sqlite3.Error as e:
            error_label = ctk.CTkLabel(
                therapy_frame,
                text=f"Error loading therapy: {str(e)}",
                text_color="red"
            )
            error_label.pack(pady=20)
        finally:
            conn.close()

        # Back button
        back_button = ctk.CTkButton(self.main_frame, text="Back to Medication", command=self.open_medication)
        back_button.pack(pady=20)

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
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.main_frame, text="Notifications", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        # Create a frame for notifications
        notifications_frame = ctk.CTkFrame(self.main_frame)
        notifications_frame.pack(padx=20, pady=10, fill="both", expand=True)

        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT Message, Timestamp, Type
                FROM Notifications
                WHERE PatientID = ?
                ORDER BY Timestamp DESC
            """, (self.patient_id,))
            
            notifications = cursor.fetchall()
            
            if not notifications:
                no_notifications = ctk.CTkLabel(notifications_frame, text="No notifications", font=("Arial", 14))
                no_notifications.pack(pady=20)
            else:
                for message, timestamp, type in notifications:
                    # Create a frame for each notification
                    notification_frame = ctk.CTkFrame(notifications_frame)
                    notification_frame.pack(fill="x", padx=10, pady=5)
                    
                    # Format timestamp
                    timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    formatted_time = timestamp.strftime("%d %B %Y, %H:%M")
                    
                    # Create notification content
                    type_icon = "🔔" if type == "REMINDER" else "📋"
                    content = f"{type_icon} {message}\n{formatted_time}"
                    
                    notification_label = ctk.CTkLabel(
                        notification_frame,
                        text=content,
                        font=("Arial", 12),
                        justify="left",
                        wraplength=600
                    )
                    notification_label.pack(padx=10, pady=5, anchor="w")
            
            # Mark notifications as read
            cursor.execute("""
                UPDATE Notifications
                SET IsRead = 1
                WHERE PatientID = ? AND IsRead = 0
            """, (self.patient_id,))
            conn.commit()
            
            # Update notification count
            self.update_notification_button()
            
        except sqlite3.Error as e:
            error_label = ctk.CTkLabel(notifications_frame, text=f"Error loading notifications: {str(e)}", text_color="red")
            error_label.pack(pady=20)
        finally:
            conn.close()

        # Add back button
        back_button = ctk.CTkButton(self.main_frame, text="Back to Home", command=self.show_home)
        back_button.pack(pady=20)

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


if __name__ == "__main__":
    app = PatientInterface(patient_id="PAT001")
    app.mainloop() 