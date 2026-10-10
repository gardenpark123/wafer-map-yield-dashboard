import sqlite3
import pandas as pd

# SQLite DB 연결
conn = sqlite3.connect("wafer.db")

# CSV 읽기
df = pd.read_csv("test.csv")

# 테이블 저장
df.to_sql(
    "wafer_map",
    conn,
    if_exists="replace",
    index=False
)

print("DB 저장 완료")

# 저장 확인
result = pd.read_sql(
    "SELECT * FROM wafer_map",
    conn
)

print(result)

# 연결 종료
conn.close()