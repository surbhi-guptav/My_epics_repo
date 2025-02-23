import streamlit as st
import speech_recognition as sr  # For voice recognition
import re  # For validation
from datetime import datetime

# Set Page Config
st.set_page_config(page_title="Bank Deposit Form", layout="centered")

# Initialize session state variables
if "manual_input" not in st.session_state:
    st.session_state.manual_input = False
if "voice_input" not in st.session_state:
    st.session_state.voice_input = False
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""  # Store spoken words

# Custom CSS for Styling
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: white;
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(90deg, #87CEEB, #4682B4);
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header (Enlarged)
st.markdown('<p class="title">🏦 Bank Account Deposit Form</p>', unsafe_allow_html=True)

# Toggle Buttons for Input Method
st.write("### Select Input Method:")
col1, col2 = st.columns(2)

if col1.button("📝 Manual Input"):
    st.session_state.manual_input = True
    st.session_state.voice_input = False

if col2.button("🎤 Use Voice Input"):
    st.session_state.voice_input = True
    st.session_state.manual_input = False
    st.info("🎙 Speak, and your words will be captured in real-time!")

# *Manual Input Section*
if st.session_state.manual_input:
    with st.form("deposit_form"):
        st.subheader("👤 Personal Details")
        
        name = st.text_input("Full Name*", placeholder="Enter your full name")
        
        st.subheader("📞 Contact Details")
        contact_col1, contact_col2 = st.columns([1, 3])
        country_code = contact_col1.selectbox("Country Code", ["+91", "+1", "+44", "+61"])
        phone_number = contact_col2.text_input("Phone Number", placeholder="Enter 10-digit phone number")
        
        st.subheader("🏧 Account Details")
        account_number = st.text_input("🔑 Account Number", placeholder="Enter 12-digit account number")
        deposit_amount = st.text_input("💵 Deposit Amount", placeholder="Enter amount (₹)")
        
        st.subheader("📅 Date of Deposit")
        deposit_date = st.date_input("Select Date", value=datetime.today())
        
        notes = st.text_area("📝 Additional Notes (Optional)", placeholder="Any special instructions")
        
        # Validation
        errors = []
        if not name or not re.match(r"^[A-Za-z\s]+$", name):
            errors.append("🔴 Please enter a valid name (letters only).")
        if phone_number and (not phone_number.isdigit() or len(phone_number) != 10):
            errors.append("🔴 Phone number must be exactly 10 digits.")
        if account_number and (not account_number.isdigit() or len(account_number) != 12):
            errors.append("🔴 Account number must be exactly 12 digits.")
        if deposit_amount and not deposit_amount.isdigit():
            errors.append("🔴 Deposit amount must be a valid number.")

        # Submit button
        submit = st.form_submit_button("✅ Submit Deposit")

        if submit:
            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.success("✅ Deposit request submitted successfully!")
                st.write(f"Account Holder: {name}")
                st.write(f"Phone: {country_code} {phone_number}")
                st.write(f"Account Number: {account_number}")
                st.write(f"Amount: ₹{deposit_amount}")
                st.write(f"Date: {deposit_date}")

# *Voice Input Section*
if st.session_state.voice_input:
    st.subheader("🎤 Voice Input")
    st.info("Example: 'My name is Rahul, my phone number is 9876543210, my account number is 987667543210, I want to deposit 500 rupees.'")

    # Voice Recognition Function
    def recognize_speech():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎙 Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                st.session_state.voice_text = text
                st.success("✅ Voice captured successfully!")
            except sr.UnknownValueError:
                st.warning("⚠ Sorry, I couldn't understand the audio.")
            except sr.RequestError:
                st.error("🚫 Speech Recognition service is unavailable.")

    col3, col4, col5 = st.columns(3)

    if col3.button("🎙 Start Recording"):
        st.session_state.recording = True
        recognize_speech()
        st.session_state.recording = False

    if col4.button("🛑 Stop Recording"):
        st.session_state.recording = False

    if col5.button("🔄 Reset"):
        st.session_state.voice_text = ""
        st.success("🔁 Voice input reset!")

    voice_text = st.text_area("Voice Data", st.session_state.voice_text, height=100)

    if st.button("Process Voice Data"):
        if voice_text.strip():
            st.success("✅ Extracted Text:")
            st.write(f"🔹 {voice_text}")
        else:
            st.warning("⚠ No voice data captured. Please try again.")
