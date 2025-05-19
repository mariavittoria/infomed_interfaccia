import customtkinter as ctk
import sqlite3 
import datetime

DATABASE = "Database_proj.db"

class VisitView(ctk.CTk):
    def __init__(self, patient_id, patient_name):
        super().__init__()
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.current_start_date = datetime.date.today() + datetime.timedelta(days=1)

        self.selected_date = None
        self.selected_time = None
        self.slot_buttons = {}
        self.notification_count = self.get_notification_count()

        self.title("Visita")
        self.geometry("1000x600")
        self.center_window()

        # Layout principale
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.profile_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {patient_name}", anchor="w", font=("Arial", 14, "bold"))
        self.profile_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.show_home, width=140)
        self.home_button.grid(row=1, column=0, padx=10, pady=10)

        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", width=140, command=self.visual_data)
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        self.notification_button = ctk.CTkButton(
            self.sidebar_frame,
            text=f"Notifications ({self.notification_count})",
            width=140,
            command=self.show_notifications
        )
        self.notification_button.grid(row=3, column=0, padx=10, pady=10)

        # Main frame
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
        w = 1000
        h = 600
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def show_home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.main_frame, text="Visits", font=("Arial", 24, "bold"), text_color="#204080")
        title.grid(row=0, column=0, columnspan=2, pady=40)

        book_button = ctk.CTkButton(self.main_frame, text="Book a visit", width=150, fg_color="#9b59b6", command=self.book_visit)
        book_button.grid(row=1, column=0, padx=20)

        check_button = ctk.CTkButton(self.main_frame, text="Check appointments", width=150, fg_color="#b76ba3", command=self.check_appointment)
        check_button.grid(row=1, column=1, padx=20)

    def visual_data(self):
        print("Visual Data clicked")

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
        conn = sqlite3.connect(DATABASE)
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
        conn = sqlite3.connect(DATABASE)
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

    def book_visit(self):
        self.render_booking_interface()

    def render_booking_interface(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.main_frame, text="Book a Visit", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=7, pady=10)

        # Exit button
        close_button = ctk.CTkButton(self.main_frame, text="✕", width=30, fg_color="red", command=self.reset_view)
        close_button.grid(row=0, column=6, padx=10, sticky="e")

        # Navigation arrows
        left_arrow = ctk.CTkButton(self.main_frame, text="←", width=30, command=self.go_left_week)
        left_arrow.grid(row=1, column=0, padx=5)

        right_arrow = ctk.CTkButton(self.main_frame, text="→", width=30, command=self.go_right_week)
        right_arrow.grid(row=1, column=6, padx=5)

        self.slot_buttons.clear()

        # Show only weekdays (Monday to Friday)
        days = []
        current_date = self.current_start_date
        while len(days) < 5:  # We want 5 weekdays
            if current_date.weekday() < 5:  # 0-4 are Monday to Friday
                days.append(current_date)
            current_date += datetime.timedelta(days=1)

        slots = self.get_available_slots(days[0], days[-1])

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
        self.render_booking_interface()

    def go_right_week(self):
        self.current_start_date += datetime.timedelta(days=7)
        self.render_booking_interface()

    def get_available_slots(self, start_date, end_date):
        conn = sqlite3.connect(DATABASE)
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

        conn = sqlite3.connect(DATABASE)
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

        back_button = ctk.CTkButton(self.main_frame, text="Back to Home", command=self.reset_view)
        back_button.pack(pady=20)

    def reset_view(self):
        self.show_home()

    def get_notification_count(self):
        conn = sqlite3.connect(DATABASE)
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

        conn = sqlite3.connect(DATABASE)
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


if __name__ == "__main__":
    VisitView(patient_id="PAT001", patient_name="Luca Bianchi")
