import streamlit as st
import pickle
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="COMSCA Credit Assessment", page_icon="🏦", layout="wide")

# 2. Sidebar Information
with st.sidebar:
    st.title("📂 COMSCA System")
    st.info("""
    **Evaluation Metrics:**
    * **Savings vs Loan:** Checks if the requested amount is proportional to savings.
    * **Behavioral Score:** Based on payments and meeting attendance.
    * **Debt Ratio:** Capacity to take on more debt.
    """)

# 3. Load the Trained Model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Error: 'model.pkl' not found. Please run your training script first.")

# 4. Main Title
st.title("🏦 Member Loan Risk Analysis")
st.markdown("---")

# 5. Input Fields Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Requested Loan Details")
    loan_amount = st.number_input("Loan Amount Requested (₱)", min_value=0, value=2000, step=100)
    savings = st.number_input("Current Member Savings (₱)", min_value=0, value=1000, step=100)
    debt_ratio = st.slider("Existing Debt Ratio (0.0 - 1.0)", 0.0, 1.0, 0.20)

with col2:
    st.subheader("Member Track Record")
    payments = st.slider("Payment Reliability (%)", 0, 100, 85)
    attendance = st.slider("Meeting Attendance (%)", 0, 100, 90)

# 6. Prediction Logic
st.markdown("---")
if st.button("🔍 Analyze Risk"):
    # Prepare the input for the model (matching the training features order)
    # Order: ['Savings', 'LoanAmount', 'Payments', 'Attendance', 'DebtRatio']
    features = [[savings, loan_amount, payments, attendance, debt_ratio]]
    
    prediction = model.predict(features)
    result = prediction[0]

    # 7. Display Results
    if result == 'Low Risk':
        st.success(f"### Result: {result}")
        st.write("✅ This member is eligible for a loan based on their strong track record and financial standing.")
    else:
        st.error(f"### Result: {result}")
        st.write("⚠️ High risk detected. It is recommended to review the member's capacity to pay or require a co-maker.")

# 8. Visual Logic (Optional: Showing the inputs in a table)
if st.checkbox("Show Input Summary"):
    data_summary = {
        "Feature": ["Savings", "Loan Amount", "Payments", "Attendance", "Debt Ratio"],
        "Value": [f"₱{savings}", f"₱{loan_amount}", f"{payments}%", f"{attendance}%", debt_ratio]
    }
    st.table(pd.DataFrame(data_summary))
