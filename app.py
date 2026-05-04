import streamlit as st
import pickle

st.set_page_config(page_title="COMSCA Credit Assessment", page_icon="🏦", layout="wide")

# 1. Sidebar
with st.sidebar:
    st.title("📂 COMSCA System")
    st.info("""
    **Evaluation Metrics:**
    * **Savings vs Loan:** Checks if the requested amount is proportional to savings.
    * **Behavioral Score:** Based on payments and meeting attendance.
    * **Debt Ratio:** Capacity to take on more debt.
    """)

# 2. Main Title
st.title("🏦 Member Loan Risk Analysis")

# 3. Load Model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Model not found. Please upload 'model.pkl'.")

# 4. Organized Input Fields
col1, col2 = st.columns(2)

with col1:
    st.subheader("Requested Loan Details")
    loan_amount = st.number_input("Loan Amount Requested (₱)", min_value=0, value=2000)
    savings = st.number_input("Current Member Savings (₱)", min_value=0, value=1000)
    debt_ratio = st.slider("Existing Debt Ratio (0.0 - 1.0)", 0.0, 1.0, 0.2)

with col2:
    st.subheader("Member Track Record")
    payments = st.slider("Payment Reliability (%)", 0, 100, 85)
    attendance = st.slider("Meeting Attendance (%)", 0, 100, 90)

st.markdown("---")

# 5. Prediction Logic
if st.button("🔍 Analyze Risk"):
    # ORDER MATTERS: Savings, LoanAmount, Payments, Attendance, DebtRatio
    features = [[savings, loan_amount, payments, attendance, debt_ratio]]
    prediction = model.predict(features)
    
    st.subheader("Analysis Result:")
    if prediction[0] == 'Low Risk':
        st.success(f"### Prediction: **{prediction[0]}** ✅")
        st.write("The member is eligible for this loan amount based on their profile.")
    else:
        st.error(f"### Prediction: **{prediction[0]}** ⚠️")
        st.write("This loan request is flagged as High Risk. Consider a lower amount or higher savings.")