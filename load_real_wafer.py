import pandas as pd
import sqlite3
import numpy as np

print("LSWMD 로딩 중...")

df = pd.read_pickle("LSWMD.pkl")

# 샘플 500개
df = df.sample(500, random_state=42)

conn = sqlite3.connect("wafer.db")

data_list = []

for idx, row in df.iterrows():

    wafer_map = row["waferMap"]

    rows = wafer_map.shape[0]
    cols = wafer_map.shape[1]

    wafer_str = np.array2string(wafer_map)

    total = np.sum(wafer_map > 0)
    good = np.sum(wafer_map == 2)

    if total == 0:
        yield_value = 0
    else:
        yield_value = round((good / total) * 100, 2)

    try:
        failure = row["failureType"][0][0]
    except:
        failure = "none"

    data_list.append([
        idx,
        row["lotName"][0][0],
        int(row["waferIndex"]),
        failure,
        yield_value,
        rows,
        cols,
        wafer_str
    ])

save_df = pd.DataFrame(data_list, columns=[
    "id",
    "lot_name",
    "wafer_index",
    "failure_type",
    "yield",
    "rows",
    "cols",
    "wafer_map"
])

save_df.to_sql(
    "real_wafer_data",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("DB 저장 완료")