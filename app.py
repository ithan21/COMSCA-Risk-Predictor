import streamlit as st
import pickle
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="COMSCA Credit Risk Analyzer",
    page_icon="💰",
    layout="wide"
)

# 2. Sidebar for Logo and About Section
with st.sidebar:
    # Replace 'logo.png' with your actual logo filename in the folder
    st.title("📂 COMSCA System")
    st.info("""
    **About this AI:**
    This model is used to predict the credit risk of COMSCA members using Machine Learning (KNN Algorithm).
    """)
    st.markdown("---")
    st.write("🔧 **Developer Settings**")
    st.caption("Capstone Project 2026")

# 3. Main Interface Header
st.title("💰 Loan Risk Prediction & Analysis")
st.write("Please provide the information below to determine the borrower's risk level.")

# 4. Load the Model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Error: 'model.pkl' not found. Please ensure the model file and app.py are in the same folder.")

# 5. UI Layout using Columns for Inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("Financial Profile")
    income = st.number_input("Monthly Income (₱)", min_value=0, value=5000, help="Total gross income per month.")
    loan = st.number_input("Requested Loan Amount (₱)", min_value=0, value=2000)

with col2:
    st.subheader("Borrower Details")
    age = st.slider("Age of Borrower", 18, 80, 25)
    history = st.selectbox(
        "Credit History Status", 
        options=[0, 1], 
        format_func=lambda x: "Good (Existing payment record)" if x==1 else "Bad / No Existing Record"
    )

st.markdown("---")

# 6. Prediction Logic
if st.button("🔍 Run Risk Analysis"):
    # Ensure the order of features matches the training: Income, Loan, History, Age
    features = [[income, loan, history, age]]
    prediction = model.predict(features)
    
    # Visual Feedback for the Result
    st.subheader("Prediction Result:")
    if prediction[0] == 'Low Risk':
        st.success(f"### Result: **{prediction[0]}** ✅")
        st.write("The borrower has a high probability of paying on time. This loan is recommended for approval.")
    else:
        st.error(f"### Result: **{prediction[0]}** ⚠️")
        st.write("Warning: This borrower is considered high risk. Proceed with caution and conduct further verification.")
