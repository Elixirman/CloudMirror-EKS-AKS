import os
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/appdb")
engine = create_engine(DB_URL)

SENSORS = [
    ("PRESS-01", "psi", 1400, 1600),
    ("TEMP-02", "°C", 60, 95),
    ("FLOW-03", "bbl/hr", 200, 450),
    ("VIB-04", "mm/s", 0.5, 4.0),
]

with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS readings (
            id SERIAL PRIMARY KEY,
            sensor_id VARCHAR(20),
            value NUMERIC,
            unit VARCHAR(10),
            recorded_at TIMESTAMP
        )
    """))
    now = datetime.utcnow()
    for i in range(20):
        sensor_id, unit, low, high in_ = SENSORS[i % len(SENSORS)][0], SENSORS[i % len(SENSORS)][1], SENSORS[i % len(SENSORS)][2], SENSORS[i % len(SENSORS)][3]
        value = round(random.uniform(low, in_), 2)
        conn.execute(
            text("INSERT INTO readings (sensor_id, value, unit, recorded_at) VALUES (:s, :v, :u, :t)"),
            {"s": sensor_id, "v": value, "u": unit, "t": now - timedelta(minutes=i*5)}
        )
print("Seeded 20 readings.")
