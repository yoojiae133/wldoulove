pip install matplotlib
import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# ------------------------------
# 연핑크 배경 적용
st.markdown(
    """
    <style>
        .stApp {
            background-color: #ffe6f0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
st.title("🐷 핑크 돼지 용돈 관리 앱 💖")

# ------------------------------
# 세션 초기화
if 'allowance' not in st.session_state:
    st.session_state.allowance = 0
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['날짜', '항목', '금액', '카테고리'])

# ------------------------------
# 초기 용돈 입력
if st.session_state.allowance == 0:
    st.header("💵 처음 받은 용돈을 입력해 주세요!")
    initial = st.number_input("받은 용돈 (원)", min_value=0, step=100)
    if st.button("⏳ 저장하고 시작하기"):
        if initial > 0:
            st.session_state.allowance = initial
            st.success("✅ 저장 완료! 지출을 입력해 보세요.")
        else:
            st.warning("용돈은 0보다 커야 해요!")
    st.stop()

# ------------------------------
# 지출 입력
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
# 지출 내역 표시
st.header("📋 지출 내역")
st.dataframe(st.session_state.data)

# ------------------------------
# 총 지출, 남은 돈 계산
total_spent = st.session_state.data['금액'].sum()
remaining = st.session_state.allowance - total_spent

st.subheader("💰 요약 정보")
col1, col2, col3 = st.columns(3)
col1.metric("총 용돈", f"{int(st.session_state.allowance):,} 원")
col2.metric("총 지출", f"{int(total_spent):,} 원")
col3.metric("남은 돈", f"{int(remaining):,} 원 🐷")

# ------------------------------
# 📊 카테고리별 소비 분석 (matplotlib 사용!)
st.header("📊 카테고리별 소비 분석")
if not st.session_state.data.empty:
    category_sum = st.session_state.data.groupby('카테고리')['금액'].sum()
    categories = category_sum.index.tolist()
    values = category_sum.values.tolist()

    pink_palette = ['#ffb6c1', '#ffc0cb', '#ff69b4', '#f08080', '#ffa6c9']

    fig, ax = plt.subplots()
    bars = ax.bar(categories, values, color=pink_palette[:len(categories)])

    # 금액 텍스트 표시
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height):,}원',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom')

    ax.set_title("카테고리별 지출 (연핑크 톤)")
    ax.set_ylabel("지출 금액 (원)")
    st.pyplot(fig)

# ------------------------------
# 초기화 버튼
if st.button("🔄 전체 초기화"):
    st.session_state.allowance = 0
    st.session_state.data = pd.DataFrame(columns=['날짜', '항목', '금액', '카테고리'])
    st.success("데이터가 초기화되었습니다! 🎉")
