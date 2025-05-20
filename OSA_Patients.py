import customtkinter
import os
from PIL import Image
import sqlite3
import tkinter.ttk as ttk
from patient_indexes_view import PatientIndexes
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

class OSAPatientsView(customtkinter.CTk):
    def __init__(self, parent_frame, user_id):
        # Titolo
        title = customtkinter.CTkLabel(parent_frame, text="OSA patients", font=("Arial", 20, "bold"), text_color="black")
        title.grid(row=0, column=0, columnspan=4, pady=20)

        # Recupera dati dal database
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM OSA_Patients")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()

        # Treeview style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#f0f4ff", foreground="black", rowheight=25, fieldbackground="#f0f4ff")
        style.map("Treeview", background=[('selected', '#4a7abc')])

        # Tabella
        self.tree = ttk.Treeview(parent_frame, columns=column_names, show='headings', height=12)
        self.tree.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        for col in column_names:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)

        for row in rows:
            self.tree.insert("", "end", values=row)

        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        # Get selected item
        item = self.tree.selection()[0]
        values = self.tree.item(item)['values']
        
        # Extract patient info
        self.patient_id = values[1]  # Assuming PatientID is the second column
        self.patient_name = f"{values[2]} {values[3]}"  # Assuming Name and Surname are the third and fourth columns
        
        # Create a new window for patient options
        self.options_window = customtkinter.CTkToplevel()
        self.options_window.title(f"Patient Options - {self.patient_name}")
        self.options_window.geometry("800x500")
        
        # Center the window
        w = 800
        h = 500
        x = (self.options_window.winfo_screenwidth() // 2) - (w // 2)
        y = (self.options_window.winfo_screenheight() // 2) - (h // 2)
        self.options_window.geometry(f"{w}x{h}+{x}+{y}")
        
        # Create main frame
        self.main_frame = customtkinter.CTkFrame(self.options_window, corner_radius=10, fg_color="#e6f0ff")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.show_main_menu()

    def show_main_menu(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add title
        title = customtkinter.CTkLabel(self.main_frame, text="Patient Trends", font=("Arial", 24, "bold"), text_color="#204080")
        title.pack(pady=(40, 20))
        
        # Add trend buttons frame
        trends_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        trends_frame.pack(pady=20)
        
        # Trend buttons
        ahi_btn = customtkinter.CTkButton(
            trends_frame,
            text="AHI Trend",
            width=200,
            fg_color="#c8b4e3",
            command=lambda: self.show_trend("AHI")
        )
        ahi_btn.pack(pady=15)
        
        odi_btn = customtkinter.CTkButton(
            trends_frame,
            text="ODI Trend",
            width=200,
            fg_color="#e0cda9",
            command=lambda: self.show_trend("ODI")
        )
        odi_btn.pack(pady=15)
        
        spo2_btn = customtkinter.CTkButton(
            trends_frame,
            text="SpO2 Trend",
            width=200,
            fg_color="#a8d5ba",
            command=lambda: self.show_trend("SpO2")
        )
        spo2_btn.pack(pady=15)
        
        # Add action buttons frame
        actions_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        actions_frame.pack(pady=(40, 20))
        
        # Action buttons
        visit_btn = customtkinter.CTkButton(
            actions_frame,
            text="Plan a Visit with the Patient",
            width=250,
            fg_color="#9b59b6",
            command=lambda: self.plan_visit(self.patient_id, self.patient_name)
        )
        visit_btn.pack(pady=15)
        
        therapy_btn = customtkinter.CTkButton(
            actions_frame,
            text="View/Modify Therapy",
            width=250,
            fg_color="#b76ba3",
            command=lambda: self.view_therapy(self.patient_id, self.patient_name)
        )
        therapy_btn.pack(pady=15)

    def show_trend(self, trend_type):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Add back button
        back_btn = customtkinter.CTkButton(
            self.main_frame,
            text="← Back",
            width=100,
            fg_color="#204080",
            command=self.show_main_menu
        )
        back_btn.pack(anchor="w", padx=20, pady=20)

        # Add title
        title = customtkinter.CTkLabel(self.main_frame, text=f"{trend_type} Trend", font=("Arial", 24, "bold"), text_color="#204080")
        title.pack(pady=20)

        # Get data from database
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        
        if trend_type == "AHI":
            cursor.execute("SELECT Date, ValueAHI FROM Indexes WHERE PatientID = ? ORDER BY Date DESC", (self.patient_id,))
        elif trend_type == "ODI":
            cursor.execute("SELECT Date, ValueODI FROM Indexes WHERE PatientID = ? ORDER BY Date DESC", (self.patient_id,))
        else:  # SpO2
            cursor.execute("SELECT Date, MeanSpO2 FROM Indexes WHERE PatientID = ? ORDER BY Date DESC", (self.patient_id,))
        
        data = cursor.fetchall()
        conn.close()

        if not data:
            no_data_label = customtkinter.CTkLabel(self.main_frame, text="No data available", font=("Arial", 16))
            no_data_label.pack(pady=20)
            return

        # Create plot frame
        plot_frame = customtkinter.CTkFrame(self.main_frame, height=350, width=700, fg_color="white")
        plot_frame.pack(pady=20)

        # Prepare data for plotting
        dates = [datetime.datetime.strptime(date_str, "%Y-%m-%d").date() for date_str, value in data]
        values = [value for date_str, value in data]

        # Create plot
        fig, ax = plt.subplots(figsize=(7, 3.5), dpi=100)
        ax.plot(dates, values, marker="o", markersize=5, linewidth=2, color="#3366cc")
        ax.set_title(f"{trend_type} values over time", fontsize=13, fontweight="bold")
        ax.set_xlabel("Date", fontsize=10)
        ax.set_ylabel(trend_type, fontsize=10)
        ax.grid(True, linestyle='--', linewidth=0.4, color='lightgray')
        ax.set_xticks(dates)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
        fig.autofmt_xdate(rotation=30)
        ax.set_ylim(min(values) - 0.5, max(values) + 0.5)

        # Add value labels
        for x, y in zip(dates, values):
            ax.text(x, y + 0.2, f"{y:.1f}", ha='center', fontsize=8, color='black')

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plan_visit(self, patient_id, patient_name):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Add back button
        back_btn = customtkinter.CTkButton(
            self.main_frame,
            text="← Back",
            width=100,
            fg_color="#204080",
            command=self.show_main_menu
        )
        back_btn.pack(anchor="w", padx=20, pady=20)

        # Add title
        title = customtkinter.CTkLabel(self.main_frame, text="Plan Visit", font=("Arial", 24, "bold"), text_color="#204080")
        title.pack(pady=20)

        # Create form frame
        form_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        form_frame.pack(pady=20)

        # Date selection
        date_label = customtkinter.CTkLabel(form_frame, text="Select Date:", font=("Arial", 14))
        date_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        date_entry = customtkinter.CTkEntry(form_frame, width=200)
        date_entry.grid(row=0, column=1, padx=20, pady=10)
        date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        # Time selection
        time_label = customtkinter.CTkLabel(form_frame, text="Select Time:", font=("Arial", 14))
        time_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        time_entry = customtkinter.CTkEntry(form_frame, width=200)
        time_entry.grid(row=1, column=1, padx=20, pady=10)
        time_entry.insert(0, "09:00")

        # Doctor selection
        doctor_label = customtkinter.CTkLabel(form_frame, text="Select Doctor:", font=("Arial", 14))
        doctor_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        doctor_entry = customtkinter.CTkEntry(form_frame, width=200)
        doctor_entry.grid(row=2, column=1, padx=20, pady=10)
        doctor_entry.insert(0, "Dr. Smith")

        # Submit button
        submit_btn = customtkinter.CTkButton(
            form_frame,
            text="Schedule Visit",
            width=200,
            fg_color="#9b59b6",
            command=lambda: self.schedule_visit(
                patient_id,
                patient_name,
                date_entry.get(),
                time_entry.get(),
                doctor_entry.get()
            )
        )
        submit_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def schedule_visit(self, patient_id, patient_name, date, time, doctor):
        # Add to appointments table
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO Appointments (date, time, doctor_name, status, patient_id, patient_name)
                VALUES (?, ?, ?, 'booked', ?, ?)
            """, (date, time, doctor, patient_id, patient_name))
            
            # Create notification for patient
            message = f"New appointment scheduled with {doctor} on {date} at {time}"
            cursor.execute("""
                INSERT INTO Notifications (PatientID, PatientName, Type, Message)
                VALUES (?, ?, 'APPOINTMENT', ?)
            """, (patient_id, patient_name, message))
            
            conn.commit()
            
            # Show success message
            success_label = customtkinter.CTkLabel(
                self.main_frame,
                text="Visit scheduled successfully!",
                font=("Arial", 16),
                text_color="green"
            )
            success_label.pack(pady=20)
            
        except sqlite3.Error as e:
            error_label = customtkinter.CTkLabel(
                self.main_frame,
                text=f"Error scheduling visit: {str(e)}",
                text_color="red"
            )
            error_label.pack(pady=20)
        finally:
            conn.close()

    def view_therapy(self, patient_id, patient_name):
        # Clear main frame
        for widget in self.main_frame2.winfo_children():
            widget.destroy()

        # Add back button
        back_btn = customtkinter.CTkButton(
            self.main_frame,
            text="← Back",
            width=100,
            fg_color="#204080",
            command=self.show_main_menu
        )
        back_btn.pack(anchor="w", padx=20, pady=20)

        # Add title
        title = customtkinter.CTkLabel(self.main_frame, text="Patient Therapy", font=("Arial", 24, "bold"), text_color="#204080")
        title.pack(pady=20)

        # Create main content frame
        content_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create table frame for drugs
        table_frame = customtkinter.CTkFrame(content_frame)
        table_frame.pack(fill="x", pady=(0, 20))

        # Table headers
        headers = ["Drug Information", "Start Date", "End Date"]
        for i, header in enumerate(headers):
            label = customtkinter.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"))
            label.grid(row=0, column=i, padx=20, pady=10, sticky="w")

        # Get drugs from database
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT Note, StartDate, EndDate
                FROM Drugs
                WHERE PatientID = ?
                ORDER BY StartDate DESC
            """, (patient_id,))
            
            drugs = cursor.fetchall()
            
            if not drugs:
                no_drugs_label = customtkinter.CTkLabel(table_frame, text="No medications found", font=("Arial", 14))
                no_drugs_label.grid(row=1, column=0, columnspan=3, pady=20)
            else:
                for i, (note, start_date, end_date) in enumerate(drugs, 1):
                    # Drug info
                    note_label = customtkinter.CTkLabel(table_frame, text=note, wraplength=300)
                    note_label.grid(row=i, column=0, padx=20, pady=5, sticky="w")
                    
                    # Dates
                    start_label = customtkinter.CTkLabel(table_frame, text=start_date)
                    start_label.grid(row=i, column=1, padx=20, pady=5, sticky="w")
                    
                    end_label = customtkinter.CTkLabel(table_frame, text=end_date)
                    end_label.grid(row=i, column=2, padx=20, pady=5, sticky="w")

            # Get current therapy
            cursor.execute("""
                SELECT Note
                FROM Therapy
                WHERE PatientID = ?
                ORDER BY ID DESC
                LIMIT 1
            """, (patient_id,))
            
            current_therapy = cursor.fetchone()
            
            # Create therapy input frame
            therapy_frame = customtkinter.CTkFrame(content_frame)
            therapy_frame.pack(fill="x", pady=20)
            
            therapy_label = customtkinter.CTkLabel(
                therapy_frame,
                text="Current Therapy:",
                font=("Arial", 14, "bold")
            )
            therapy_label.pack(anchor="w", padx=20, pady=(20, 10))
            
            # Therapy text input
            therapy_text = customtkinter.CTkTextbox(
                therapy_frame,
                height=100,
                width=600,
                font=("Arial", 12)
            )
            therapy_text.pack(padx=20, pady=10)
            
            if current_therapy:
                therapy_text.insert("1.0", current_therapy[0])
            
            # Save button
            save_btn = customtkinter.CTkButton(
                therapy_frame,
                text="Save Therapy",
                width=200,
                fg_color="#b76ba3",
                command=lambda: self.save_therapy(patient_id, patient_name, therapy_text.get("1.0", "end-1c"))
            )
            save_btn.pack(pady=20)
            
        except sqlite3.Error as e:
            error_label = customtkinter.CTkLabel(
                content_frame,
                text=f"Error loading data: {str(e)}",
                text_color="red"
            )
            error_label.pack(pady=20)
        finally:
            conn.close()

    def save_therapy(self, patient_id, patient_name, therapy_text):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        
        try:
            # Insert new therapy
            cursor.execute("""
                INSERT INTO Therapy (PatientID, Note)
                VALUES (?, ?)
            """, (patient_id, therapy_text))
            
            # Create notification for patient
            message = "Your therapy has been updated by your doctor"
            cursor.execute("""
                INSERT INTO Notifications (PatientID, PatientName, Type, Message)
                VALUES (?, ?, 'THERAPY', ?)
            """, (patient_id, patient_name, message))
            
            conn.commit()
            
            # Show success message
            success_label = customtkinter.CTkLabel(
                self.main_frame,
                text="Therapy updated successfully!",
                font=("Arial", 16),
                text_color="green"
            )
            success_label.pack(pady=20)
            
        except sqlite3.Error as e:
            error_label = customtkinter.CTkLabel(
                self.main_frame,
                text=f"Error saving therapy: {str(e)}",
                text_color="red"
            )
            error_label.pack(pady=20)
        finally:
            conn.close()

    def get_osa_patients(self):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM OSA_Patients")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()
        return column_names, rows

if __name__ == "__main__":
    app = OSAPatientsView(user_id=1)  # oppure un altro id valido
    app.mainloop()

