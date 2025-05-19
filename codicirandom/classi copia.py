"""
Database relativo alle classi.
Vanno controllate le foreign key e le relazioni
per garantire il corretto funzionamento del sistema.
"""

# PATIENTS
c.execute("""
CREATE TABLE IF NOT EXISTS Patients (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Surname TEXT NOT NULL,
    dateOfBirth DATE,
    height REAL CHECK(height > 0),
    weight REAL CHECK(weight > 0),
    Age INTEGER CHECK(Age > 0),
    Gender CHAR(1) CHECK(Gender IN ('M', 'F', 'O')),
    Nationality TEXT DEFAULT 'Italian',
    ClinicalHistory TEXT,
    PatientID TEXT NOT NULL UNIQUE,
    PatientPassword TEXT,
    PhoneNumber TEXT UNIQUE
);
""")

# USER
c.execute("""
CREATE TABLE IF NOT EXISTS User (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    AppID TEXT NOT NULL,
    AppPassword TEXT NOT NULL,
    PhoneNumber TEXT UNIQUE
);
""")

# DOCTOR
c.execute("""
CREATE TABLE IF NOT EXISTS Doctor (
    doctorID TEXT PRIMARY KEY NOT NULL,
    Name TEXT NOT NULL,
    Surname TEXT NOT NULL,
    dateOfBirth DATE,
    hospital TEXT,
    DoctorPassword TEXT,
    PhoneNumber TEXT UNIQUE
);
""")

# APP
c.execute("""
CREATE TABLE IF NOT EXISTS App (
    AppID TEXT PRIMARY KEY,
    Name TEXT NOT NULL
);
""")

# TECHNICIAN
c.execute("""
CREATE TABLE IF NOT EXISTS Technicians (
    TechnicianID TEXT PRIMARY KEY AUTOINCREMENT,
    AppCredential TEXT NOT NULL,
    PhoneNumber TEXT NOT NULL
);
""")

# APNEA NOTIFICATIONS
c.execute("""
CREATE TABLE IF NOT EXISTS Apnea_Notifications (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Date DATE,
    NumberOfApneas INTEGER,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

# PATIENTS OK
c.execute("""
CREATE TABLE IF NOT EXISTS Patients_OK (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Date DATE,
    Days_since_last_OSA INTEGER,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

# PATIENTS FOLLOW UP
c.execute("""
CREATE TABLE IF NOT EXISTS Patients_Follow_up (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Date DATE,
    Days_since_last_OSA INTEGER,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

# SIGNALS
c.execute("""
CREATE TABLE IF NOT EXISTS Signals (
    SignalID TEXT PRIMARY KEY,
    PatientID TEXT NOT NULL,
    DeviceID TEXT NOT NULL,
    Timestamp DATETIME,
    Value REAL,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DeviceID) REFERENCES MedicalDevice(DeviceID)
);
""")

# MEDICAL DEVICE
c.execute("""
CREATE TABLE IF NOT EXISTS MedicalDevice (
    DeviceID TEXT PRIMARY KEY,
    Model TEXT
);
""")

# DRUGS
c.execute("""
CREATE TABLE IF NOT EXISTS Drugs (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Note TEXT,
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

# THERAPY
c.execute("""
CREATE TABLE IF NOT EXISTS Therapy (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Note TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

# QUESTIONNAIRE
c.execute("""
CREATE TABLE IF NOT EXISTS Questionnaire (
<<<<<<< HEAD
    QuestID INTEGER PRIMARY KEY AUTOINCREMENT,
=======
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> origin/main
    PatientID TEXT NOT NULL,
    Date DATE,
    Q1 INTEGER,
    Q2      
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

# VISIT
c.execute("""
CREATE TABLE IF NOT EXISTS Visit (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    DoctorID TEXT NOT NULL,
    Date DATE,
    Time TIME,
    Note TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(doctorID)
);
""")

# INDEXES
c.execute("""
CREATE TABLE IF NOT EXISTS Indexes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Date DATE,
    ValueAHI REAL,
    ValueODI REAL,
    MeanSpO2 REAL,
    MinSpO2 REAL,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")
