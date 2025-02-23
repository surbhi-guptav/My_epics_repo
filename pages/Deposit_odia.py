import streamlit as st
import speech_recognition as sr  # For voice recognition
from googletrans import Translator  # Import Translator for language conversion
import re  # For validation
from datetime import datetime

# Set Page Config
st.set_page_config(page_title="ବ୍ୟାଙ୍କ ଜମା ଫର୍ମ", layout="centered")

# Initialize session state variables
if "manual_input" not in st.session_state:
    st.session_state.manual_input = False
if "voice_input" not in st.session_state:
    st.session_state.voice_input = False
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""  # Store spoken words
translator = Translator()

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
        .stButton>button {
            width: 180px;
            height: 45px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            transition: 0.3s;
            background: #87CEEB;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background: #4682B4;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header (Enlarged)
st.markdown('<p class="title">🏦 ବ୍ୟାଙ୍କ ଖାତା ଜମା ଫର୍ମ</p>', unsafe_allow_html=True)

# Toggle Buttons for Input Method
st.write("### ଇନପୁଟ ପ୍ରକାର ବାଛନ୍ତୁ:")
col1, col2 = st.columns(2)

if col1.button("📝 ହସ୍ତକୃତ ଇନପୁଟ"):
    st.session_state.manual_input = True
    st.session_state.voice_input = False

if col2.button("🎤 ଧ୍ୱନି ଇନପୁଟ ବ୍ୟବହାର କରନ୍ତୁ"):
    st.session_state.voice_input = True
    st.session_state.manual_input = False
    st.info("🎙 କଥା କରନ୍ତୁ, ଏବଂ ଆପଣଙ୍କ ଶବ୍ଦ ଧରାହେବ!")

# *Manual Input Section*
if st.session_state.manual_input:
    with st.form("deposit_form"):
        st.subheader("👤 ବ୍ୟକ୍ତିଗତ ବିବରଣୀ")


        # Single name field
        full_name = st.text_input("ପୁରା ନାମ*", placeholder="ପୁରା ନାମ ଭରନ୍ତୁ")

        st.subheader("📞 ଯୋଗାଯୋଗ ବିବରଣୀ")
        contact_col1, contact_col2 = st.columns([1, 3])
        country_code = contact_col1.selectbox("ଦେଶ କୋଡ୍", ["+91", "+1", "+44", "+61"])
        phone_number = contact_col2.text_input("ଫୋନ ନମ୍ବର", placeholder="10 ଡିଜିଟ ଫୋନ ନମ୍ବର ଭରନ୍ତୁ")

        st.subheader("🏧 ଖାତା ବିବରଣୀ")
        account_number = st.text_input("🔑 ଖାତା ନମ୍ବର", placeholder="12-ଡିଜିଟ ଖାତା ନମ୍ବର ଭରନ୍ତୁ")
        deposit_amount = st.text_input("💵 ଜମା ରାଶି", placeholder="ମୁଲ୍ୟ ଭରନ୍ତୁ (₹)")

        st.subheader("📅 ଜମା ତାରିଖ")
        deposit_date = st.date_input("ତାରିଖ ବାଛନ୍ତୁ", value=datetime.today())

        notes = st.text_area("📝 ଅତିରିକ୍ତ ଟିପ୍ପଣୀ (ଐଛିକ)", placeholder="କୌଣସି ବିଶେଷ ନିର୍ଦ୍ଦେଶ ଦିଅନ୍ତୁ")

        # Validation
        errors = []
        if not full_name:
            errors.append("🔴 ଦୟାକରି ପୁରା ନାମ ଭରନ୍ତୁ।")
        if phone_number and (not phone_number.isdigit() or len(phone_number) != 10):
            errors.append("🔴 ଫୋନ ନମ୍ବର 10 ଡିଜିଟ ହୋଇଥିବା ଉଚିତ।")
        if account_number and (not account_number.isdigit() or len(account_number) != 12):
            errors.append("🔴 ଖାତା ନମ୍ବର 12 ଡିଜିଟ ହୋଇଥିବା ଉଚିତ।")
        if deposit_amount and not deposit_amount.isdigit():
            errors.append("🔴 ଜମା ରାଶି ଏକ ବୈଧ ସଂଖ୍ୟା ହୋଇଥିବା ଉଚିତ।")

        # Submit button
        submit = st.form_submit_button("✅ ଜମା କରନ୍ତୁ")

        if submit:
            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.success("✅ ଜମା ଅନୁରୋଧ ସଫଳ ଭାବରେ ପ୍ରେରିତ ହେଲା!")
                st.write(f"ଖାତାଧାରୀ: {full_name}")
                st.write(f"ଫୋନ: {country_code} {phone_number}")
                st.write(f"ଖାତା ନମ୍ବର: {account_number}")
                st.write(f"ମୁଲ୍ୟ: ₹{deposit_amount}")
                st.write(f"ତାରିଖ: {deposit_date}")

# *Voice Input Section*
if st.session_state.voice_input:
    st.subheader("🎤 ଧ୍ବନି ଇନପୁଟ")

    def recognize_speech():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎙 ଶୁଣୁଛି... କହନ୍ତୁ!")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=None)
                text = recognizer.recognize_google(audio, language='or-IN')
                st.session_state.voice_text = text
                st.success("✅ ଧ୍ୱନି ଧରାଗଲା!")
            except sr.UnknownValueError:
                st.warning("⚠ ଧ୍ୱନି ଉଦ୍ଧାର ହେଲା ନାହିଁ।")
            except sr.RequestError:
                st.error("🚫 ଧ୍ୱନି ଜଣା ଅସମ୍ଭବ।")

    col3, col4, col5 = st.columns(3)

    if col3.button("🎙 ଶୁଣିବା ଆରମ୍ଭ କରନ୍ତୁ"):
        st.session_state.recording = True
        recognize_speech()

    if col4.button("⏹ ରୋକନ୍ତୁ"):
        st.session_state.recording = False

    if col5.button("🔄 ରିସେଟ୍ କରନ୍ତୁ"):
        st.session_state.voice_text = ""
        st.session_state.recording = False
        st.warning("🔃 ଡାଟା ଡିଲିଟ୍ ହେଲା।")

    voice_text = st.text_area("ଧ୍ୱନି ଡାଟା", st.session_state.voice_text, height=100)

    if st.button("🔄 ଇଂରାଜୀକୁ ଅନୁବାଦ କରନ୍ତୁ"):
        if voice_text.strip():
            try:
                translated_text = translator.translate(voice_text, src='or', dest='en').text
                st.success("✅ ଅନୁବାଦ ସଫଳ ହେଲା:")
                st.text_area("ଅନୁବାଦିତ ପାଠ୍ୟ (English)", translated_text, height=100)
            except Exception as e:
                st.error(f"🚫 ଅନୁବାଦରେ ଅସୁବିଧା: {str(e)}")
        else:
            st.warning("⚠ ଅନୁବାଦ ପାଇଁ କୌଣସି ଡାଟା ମିଳିଲା ନାହିଁ।")
