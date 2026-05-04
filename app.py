import streamlit as st
import pickle

# 1. Page Setup
st.set_page_config(page_title="COMSCA Credit Scoring", page_icon="⚖️", layout="wide")

# 2. Sidebar Information
with st.sidebar:
    st.title("📂 COMSCA System")
    st.info("""
    **Risk Parameters:**
    This AI evaluates risk based on member behavior:
    *   **Savings:** Total capital build-up.
    *   **Payments:** On-time payment history.
    *   **Attendance:** Participation in meetings.
    *   **Debt Ratio:** Current debt vs income.
    """)

# 3. Main Interface
st.title("⚖️ Member Risk Assessment")
st.write("Input the member's data to analyze creditworthiness.")

# 4. Load Model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Model file not found. Please upload 'model.pkl'.")

# 5. Input Fields
col1, col2 = st.columns(2)

with col1:
    st.subheader("Financial Standing")
    savings = st.number_input("Total Savings (₱)", min_value=0, value=1000)
    debt_ratio = st.slider("Debt Ratio (0.0 to 1.0)", 0.0, 1.0, 0.3, help="Higher means more existing debt.")

with col2:
    st.subheader("Member Behavior")
    payments = st.slider("Payment Reliability (%)", 0, 100, 80)
    attendance = st.slider("Meeting Attendance (%)", 0, 100, 90)

st.markdown("---")

# 6. Analysis Logic
if st.button("🔍 Analyze Member Risk"):
    # Must match training order: Savings, Payments, Attendance, DebtRatio
    features = [[savings, payments, attendance, debt_ratio]]
    prediction = model.predict(features)
    
    st.subheader("Analysis Result:")
    if prediction[0] == 'Low Risk':
        st.success(f"### Result: **{prediction[0]}** ✅")
        st.write("This member shows strong financial habits and reliability.")
    else:
        st.error(f"### Result: **{prediction[0]}** ⚠️")
        st.write("This member is flagged as high risk. Review debt ratio and attendance.")