import sqlite3

# Assicurati di usare il database giusto: quest.db o Database_proj.db
conn = sqlite3.connect("Database_proj.db")
cursor = conn.cursor()

# Cancella tutte le righe dalla tabella Questionnaire
cursor.execute("DELETE FROM Questionnaire;")

# Salva i cambiamenti
conn.commit()
conn.close()

