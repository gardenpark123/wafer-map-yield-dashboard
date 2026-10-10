# Wafer Map Visualization & Yield Analysis Dashboard

Python을 활용하여 반도체 웨이퍼 데이터를 시각화하고,
수율 및 결함 정보를 분석할 수 있도록 구현한 데이터 처리 프로젝트입니다.

웨이퍼별 정상/불량 영역을 시각적으로 확인하고,
불량 유형과 수율 조건에 따라 데이터를 필터링할 수 있도록 구성했습니다.

---

## Project Overview

본 프로젝트는 실제 반도체 웨이퍼 데이터를 기반으로
웨이퍼 상태와 수율 및 결함 정보를 직관적으로 확인할 수 있도록 구현한 분석 시스템입니다.

주요 목표는 다음과 같습니다.

- 웨이퍼별 정상/불량 영역 시각화
- 웨이퍼 번호 기반 데이터 조회
- 불량 유형별 데이터 필터링
- 수율 조건 기반 데이터 필터링
- 전체 평균 수율 계산
- 수율 분포 분석
- 불량 유형 비율 분석

---

## Main Features

### 1. Wafer Map Visualization

웨이퍼 번호를 선택하면 해당 웨이퍼 데이터를 원형 Wafer Map 형태로 시각화합니다.

- 웨이퍼 번호 검색 및 선택
- 선택한 웨이퍼 자동 시각화
- 정상 영역과 불량 영역 색상 구분
- 확대/축소 기능
- 초기 위치 Reset 기능

---

### 2. Data Filtering

불량 유형과 수율 조건을 이용하여 원하는 웨이퍼 데이터를 조회할 수 있도록 구현했습니다.

- 불량 유형 다중 선택
- 수율 기준 Slider 적용
- 선택 조건에 해당하는 웨이퍼 개수 표시
- 필터링 결과 실시간 업데이트

---

### 3. Yield Analysis

전체 웨이퍼 데이터를 기반으로 수율 정보를 분석할 수 있도록 구성했습니다.

- 전체 평균 수율 자동 계산
- 수율 분포 Histogram 제공
- 웨이퍼별 수율 비교
- 수율 조건 기반 데이터 분석

---

### 4. Defect Analysis

웨이퍼에서 발생하는 불량 유형을 분류하고
전체 데이터 및 불량 데이터 기준으로 결함 유형 비율을 분석합니다.

- 전체 불량 유형 비율 분석
- 정상 데이터를 제외한 불량 유형 비율 분석
- 결함 유형별 데이터 비교

---

## Project Structure

```text
wafer-map-yield-dashboard/
├── README.md
├── app.py
├── database.py
├── db.py
├── defect_page.py
├── load_lswmd.py
├── load_real_wafer.py
├── load_wafer.py
├── wafer.db
├── wafer_page.py
├── wafer_utils.py
└── yield_page.py
