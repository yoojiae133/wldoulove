import streamlit as st
st.title('나의 첫 웹 서비스 만들기!!') 
import streamlit as st
import pandas as pd
import datetime

# ------------------------------
# 앱 제목
st.title("💸 나만의 용돈 관리 앱")

# ------------------------------
# 데이터 불러오기 or 새로 만들기
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['날짜', '항목', '금액', '카테고리'])

# ------------------------------
# 입력 폼
st.header("📥 지출 입력하기")

with st.form("expense_form"):
    date = st.date_input("날짜", datetime.date.today())
    item = st.text_input("지출 항목 (예: 편의점, 버스 등)")
    amount = st.number_input("금액 (원)", min_value=0, step=100)
    category = st.selectbox("카테고리", ["식비", "교통", "쇼핑", "취미", "기타"])
    submitted = st.form_submit_button("저장하기")

    if submitted and item and amount > 0:
        new_row = pd.DataFrame([[date, item, amount, category]], columns=st.session_state.data.columns)
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.success("✅ 저장되었습니다!")

# ------------------------------
# 데이터 출력
st.header("📋 지출 내역")
st.dataframe(st.session_state.data)

# ------------------------------
# 총 지출 금액
total = st.session_state.data['금액'].sum()
st.metric("💰 총 지출 금액", f"{int(total):,} 원")

# ------------------------------
# 카테고리별 분석
st.header("📊 카테고리별 소비 분석")
if not st.session_state.data.empty:
    category_sum = st.session_state.data.groupby('카테고리')['금액'].sum()
    st.bar_chart(category_sum)

# ------------------------------
# 리셋 버튼
if st.button("🔄 전체 초기화"):
    st.session_state.data = pd.DataFrame(columns=['날짜', '항목', '금액', '카테고리'])
    st.success("모든 데이터가 초기화되었습니다.")
