import streamlit as st
import pickle
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="COMSCA Credit Risk Analyzer",
    page_icon="💰",
    layout="wide"
)

# 2. Sidebar para sa Logo at About Section
with st.sidebar:
    # Palitan ang 'logo.png' ng actual filename ng logo niyo sa folder
    st.title("📂 COMSCA System")
    st.info("""
    **About this AI:**
    Ang model na ito ay ginagamit para i-predict ang credit risk ng mga miyembro ng COMSCA gamit ang Machine Learning (KNN Algorithm).
    """)
    st.markdown("---")
    st.write("🔧 **Developer Settings**")
    st.caption("Capstone Project 2026")

# 3. Main Interface Header
st.title("💰 Loan Risk Prediction & Analysis")
st.write("Punan ang mga impormasyon sa ibaba para malaman ang risk level ng borrower.")

# 4. Load the Model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Error: 'model.pkl' not found. Pakisigurado na nasa iisang folder ang model at app.py.")

# 5. UI Layout gamit ang Columns para sa Inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("Financial Profile")
    income = st.number_input("Monthly Income (₱)", min_value=0, value=5000, help="Kabuuang kita sa loob ng isang buwan.")
    loan = st.number_input("Requested Loan Amount (₱)", min_value=0, value=2500)

with col2:
    st.subheader("Borrower Details")
    age = st.slider("Age of Borrower", 18, 80, 25)
    history = st.selectbox(
        "Credit History Status", 
        options=[0, 1], 
        format_func=lambda x: "Good (May record ng pagbabayad)" if x==1 else "Bad/No Record"
    )

st.markdown("---")

# 6. Prediction Logic
if st.button("🔍 Run Risk Analysis"):
    # Siguraduhin na ang order ng features ay tugma sa training: Income, Loan, History, Age
    features = [[income, loan, history, age]]
    prediction = model.predict(features)
    
    # Visual Feedback para sa Resulta
    st.subheader("Prediction Result:")
    if prediction[0] == 'Low Risk':
        st.success(f"### Result: **{prediction[0]}** ✅")
        st.write("Ang borrower ay may mataas na posibilidad na makapagbayad sa tamang oras.")
    else:
        st.error(f"### Result: **{prediction[0]}** ⚠️")
        st.write("Babala: Ang borrower na ito ay itinuturing na high risk. Mag-ingat sa pag-approve.")