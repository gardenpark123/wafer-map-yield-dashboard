import sys
import types

import pandas as pd

# -----------------------------------
# pandas.indexes 호환 패치
# -----------------------------------

indexes_module = types.ModuleType(
    "pandas.indexes"
)

sys.modules["pandas.indexes"] = (
    indexes_module
)

# 하위 모듈 생성
base_module = types.ModuleType(
    "pandas.indexes.base"
)

sys.modules[
    "pandas.indexes.base"
] = base_module

# Index 연결
base_module.Index = pd.Index

# -----------------------------------
# pickle 읽기
# -----------------------------------

df = pd.read_pickle("LSWMD.pkl")

print(df.head())

print("\n컬럼:")
print(df.columns)

print("\n데이터 개수:")
print(len(df))