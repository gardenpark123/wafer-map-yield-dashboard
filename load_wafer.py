import pandas as pd
import numpy as np
import sqlite3

# 데이터 로드
df = pd.read_pickle(
    "LSWMD.pkl"
)

# DB 연결
conn = sqlite3.connect(
    "wafer.db"
)

cursor = conn.cursor()

# 앞 100개만 저장
for i in range(100):

    wafer = df.iloc[i]["waferMap"]

    lot_name = str(
        df.iloc[i]["lotName"]
    )

    wafer_index = int(
        df.iloc[i]["waferIndex"]
    )

    defect_type = str(
        df.iloc[i]["failureType"]
    )

    # yield 계산
    good = np.sum(wafer == 1)

    bad = np.sum(wafer == 2)

    total = good + bad

    if total == 0:
        yield_rate = 0
    else:
        yield_rate = (
            good / total
        ) * 100

    # DB 저장
    cursor.execute("""

    INSERT INTO wafer_summary (

        lot_name,
        wafer_index,
        defect_type,

        good_chip,
        bad_chip,

        yield_rate

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """, (

        lot_name,
        wafer_index,
        defect_type,

        int(good),
        int(bad),

        float(yield_rate)

    ))

conn.commit()

conn.close()

print("100 wafers saved")