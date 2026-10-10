import sqlite3

conn = sqlite3.connect(
    "wafer.db"
)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS wafer_summary (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    lot_name TEXT,
    wafer_index INTEGER,

    defect_type TEXT,

    good_chip INTEGER,
    bad_chip INTEGER,

    yield_rate REAL

)

""")

conn.commit()

conn.close()

print("DB Ready")