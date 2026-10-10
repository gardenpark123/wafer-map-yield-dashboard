import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sqlite3
import numpy as np

# -------------------------
# DB 로드
# -------------------------
conn = sqlite3.connect("wafer.db")

df = pd.read_sql_query(
    "SELECT * FROM real_wafer_data",
    conn
)

conn.close()

# -------------------------
# 문자열 → wafer map 변환
# -------------------------
def convert_map(map_str, rows, cols):

    cleaned = map_str.replace("[", "")
    cleaned = cleaned.replace("]", "")

    numbers = np.fromstring(cleaned, sep=' ')

    wafer_map = numbers.reshape(rows, cols)

    return wafer_map

# -------------------------
# 원형 마스킹
# -------------------------
def mask_circle(wafer_map):

    rows, cols = wafer_map.shape

    center_x = cols / 2
    center_y = rows / 2

    radius = min(rows, cols) / 2

    masked = wafer_map.astype(float)

    for y in range(rows):
        for x in range(cols):

            dist = np.sqrt(
                (x - center_x) ** 2 +
                (y - center_y) ** 2
            )

            if dist > radius:
                masked[y][x] = np.nan

    return masked

# -------------------------
# Figure 생성
# -------------------------
def create_figure(wafer_map):

    masked_map = mask_circle(wafer_map)

    fig = go.Figure(
        data=go.Heatmap(
            z=masked_map,
            colorscale=[
                [0.0, "black"],
                [0.5, "green"],
                [1.0, "red"]
            ],
            showscale=True
        )
    )

    fig.update_layout(
        width=650,
        height=650,
        title="웨이퍼 맵"
    )

    return fig

# -------------------------
# 첫 웨이퍼
# -------------------------
first_row = df.iloc[0]

first_map = convert_map(
    first_row["wafer_map"],
    first_row["rows"],
    first_row["cols"]
)

# -------------------------
# Failure Type 목록
# -------------------------
failure_options = sorted(df["failure_type"].unique())

# -------------------------
# Yield Histogram
# -------------------------
hist_fig = px.histogram(
    df,
    x="yield",
    nbins=20,
    title="수율 분포"
)

# -------------------------
# Pie Chart (전체)
# -------------------------
pie_fig = px.pie(
    df,
    names="failure_type",
    title="전체 불량 유형 비율"
)

pie_fig.update_layout(height=300)

# -------------------------
# Pie Chart (불량만)
# -------------------------
df_defect_only = df[df["failure_type"] != "none"]

defect_pie_fig = px.pie(
    df_defect_only,
    names="failure_type",
    title="불량 유형 비율 (정상 제외)"
)

defect_pie_fig.update_layout(height=300)

# -------------------------
# Dash 앱
# -------------------------
app = dash.Dash(__name__)

# -------------------------
# Layout
# -------------------------
app.layout = html.Div([

    html.H1(
        "웨이퍼 맵 시각화 및 수율 분석 시스템",
        style={"textAlign": "center"}
    ),

    html.Div([

        # ====================================================
        # LEFT
        # ====================================================
        html.Div([

            html.H2("웨이퍼 조회"),

            dcc.Dropdown(
                id="wafer-dropdown",
                options=[
                    {"label": f"웨이퍼 {row['id']}", "value": row["id"]}
                    for _, row in df.iterrows()
                ],
                value=first_row["id"]
            ),

            html.Br(),

            html.Div(id="yield-text",
                     style={"fontSize": "20px", "fontWeight": "bold"}),

            html.Div(id="failure-text",
                     style={"fontSize": "20px", "fontWeight": "bold"}),

            html.Br(),

            dcc.Graph(
                id="wafer-graph",
                figure=create_figure(first_map)
            )

        ],
        style={"width": "60%", "padding": "20px"}),

        # ====================================================
        # RIGHT
        # ====================================================
        html.Div([

            html.H2("분석 대시보드"),

            # 평균 수율
            html.Div([
                html.H3(f"전체 평균 수율 : {round(df['yield'].mean(),2)} %")
            ]),

            html.Br(),

            # 필터
            html.H4("불량 유형 필터"),

            dcc.Dropdown(
                id="failure-filter",
                options=[{"label": i, "value": i} for i in failure_options],
                multi=True
            ),

            html.Br(),

            html.H4("수율 필터"),

            dcc.Slider(
                id="yield-slider",
                min=0,
                max=100,
                step=5,
                value=80,
                marks={i: str(i) for i in range(0, 101, 20)}
            ),

            html.Br(),

            html.Div(
                id="filtered-count",
                style={"fontSize": "18px", "fontWeight": "bold"}
            ),

            html.Br(),

            html.Div(
                id="filtered-wafer-list",
                style={
                    "height": "250px",
                    "overflowY": "scroll",
                    "border": "1px solid lightgray",
                    "padding": "10px"
                }
            ),

            html.Br(),

            # =========================
            # 그래프 1: 전체 불량 비율
            # =========================
            dcc.Graph(
                figure=pie_fig,
                style={"height": "320px"}
            ),

            # =========================
            # 그래프 2: 불량만
            # =========================
            dcc.Graph(
                figure=defect_pie_fig,
                style={"height": "320px"}
            ),

            # =========================
            # 히스토그램
            # =========================
            dcc.Graph(figure=hist_fig)

        ],
        style={
            "width": "40%",
            "padding": "20px",
            "borderLeft": "2px solid lightgray"
        })

    ],
    style={"display": "flex"})

])

# -------------------------
# 웨이퍼 업데이트
# -------------------------
@app.callback(
    [
        Output("wafer-graph", "figure"),
        Output("yield-text", "children"),
        Output("failure-text", "children")
    ],
    Input("wafer-dropdown", "value")
)
def update_wafer(selected_id):

    row = df[df["id"] == selected_id].iloc[0]

    wafer_map = convert_map(
        row["wafer_map"],
        row["rows"],
        row["cols"]
    )

    fig = create_figure(wafer_map)

    return (
        fig,
        f"수율 : {row['yield']} %",
        f"불량 유형 : {row['failure_type']}"
    )

# -------------------------
# 필터 기능
# -------------------------
@app.callback(
    [
        Output("filtered-count", "children"),
        Output("filtered-wafer-list", "children")
    ],
    [
        Input("failure-filter", "value"),
        Input("yield-slider", "value")
    ]
)
def update_filter(failure_values, yield_value):

    filtered_df = df.copy()

    if failure_values and len(failure_values) > 0:
        filtered_df = filtered_df[
            filtered_df["failure_type"].isin(failure_values)
        ]

    filtered_df = filtered_df[
        filtered_df["yield"] <= yield_value
    ]

    wafer_list = []

    for _, row in filtered_df.head(100).iterrows():

        wafer_list.append(
            html.Div([
                html.B(f"웨이퍼 {row['id']}"),
                html.Br(),
                f"수율 : {row['yield']} %",
                html.Br(),
                f"불량 유형 : {row['failure_type']}",
                html.Hr()
            ])
        )

    return f"필터된 웨이퍼 개수 : {len(filtered_df)}", wafer_list

# -------------------------
# 실행
# -------------------------
if __name__ == "__main__":
    app.run(debug=False)