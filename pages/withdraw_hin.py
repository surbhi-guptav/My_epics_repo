import streamlit as st
import speech_recognition as sr
import re
from datetime import datetime
from googletrans import Translator

st.set_page_config(page_title="बैंक निकशी फॉर्म", layout="centered")

if "manual_input" not in st.session_state:
    st.session_state.manual_input = False
if "voice_input" not in st.session_state:
    st.session_state.voice_input = False
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

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

st.markdown('<p class="title">🏦 बैंक खाता निकशी फॉर्म</p>', unsafe_allow_html=True)

st.write("### इनपुट विधि चुनें:")
col1, col2 = st.columns(2)

if col1.button("📝 मैनुअल इनपुट"):
    st.session_state.manual_input = True
    st.session_state.voice_input = False

if col2.button("🎤 आवाज़ इनपुट करें"):
    st.session_state.voice_input = True
    st.session_state.manual_input = False
    st.info("🎙 बोलें, और आपके शब्द वास्तविक समय में दर्ज किए जाएंगे!")

if st.session_state.voice_input:
    st.subheader("🎤 आवाज़ इनपुट")
    st.info("उदाहरण: 'मेरा नाम राहुल है, मेरा फोन नंबर 9876543210 है, मेरा खाता नंबर 987667543210 है, मैं 500 रुपये निकालना चाहता हूं")
    def recognize_speech():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎙 सुन रहे हैं... बोलें! (15 सेकंड तक चुप रहने पर इनपुट बंद हो जाएगा)")
            recognizer.adjust_for_ambient_noise(source)

            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language="hi-IN")
                st.session_state.voice_text = text
                st.success("✅ आवाज़ सफलतापूर्वक दर्ज हो गई!")
            except sr.UnknownValueError:
                st.warning("⚠ क्षमा करें, मैं ऑडियो को समझ नहीं सका।")
            except sr.RequestError:
                st.error("🚫 स्पीच रिकॉग्निशन सेवा उपलब्ध नहीं है।")

    col3, col4, col5 = st.columns(3)
    
    if col3.button("🎙 सुनना शुरू करें"):
        st.session_state.recording = True
        recognize_speech()

    if col4.button("🛑 सुनना बंद करें"):
        st.session_state.recording = False

    if col5.button("🔁 रीसेट करें"):
        st.session_state.voice_text = ""
        st.session_state.translated_text = ""
        st.session_state.recording = False
    voice_text = st.text_area("आवाज़ डेटा (हिन्दी)", st.session_state.voice_text, height=100)

    def translate_text():
        if st.session_state.voice_text.strip():
            translator = Translator()
            translated = translator.translate(st.session_state.voice_text, src="hi", dest="en")
            st.session_state.translated_text = translated.text
            st.success("✅ टेक्स्ट सफलतापूर्वक अनुवादित हुआ!")
        else:
            st.warning("⚠ कोई आवाज़ डेटा दर्ज नहीं हुआ। कृपया पुनः प्रयास करें।")

    if st.button("🔄 अंग्रेज़ी में अनुवाद करें"):
        translate_text()

    translated_text = st.text_area("Translated Text (English)", st.session_state.translated_text, height=100)

# *मैनुअल इनपुट सेक्शन*
if st.session_state.manual_input:
    with st.form("deposit_form"):
        st.subheader("👤 व्यक्तिगत विवरण")

        # Fixed the text_input label issue
        full_name = st.text_input("पूरा नाम*", placeholder="पूरा नाम दर्ज करें")

        st.subheader("📞 संपर्क विवरण")
        contact_col1, contact_col2 = st.columns([1, 3])
        country_code = contact_col1.selectbox("देश कोड", ["+91", "+1", "+44", "+61"])
        phone_number = contact_col2.text_input("फोन नंबर", placeholder="10-अंकीय फोन नंबर दर्ज करें")

        st.subheader("🏧 खाता विवरण")
        account_number = st.text_input("🔑 खाता संख्या", placeholder="12-अंकीय खाता संख्या दर्ज करें")
        deposit_amount = st.text_input("💵 निकशी राशि", placeholder="राशि दर्ज करें (₹)")

        st.subheader("📅 निकशी करने की तारीख")
        deposit_date = st.date_input("तारीख चुनें", value=datetime.today())

        notes = st.text_area("📝 अतिरिक्त निर्देश (वैकल्पिक)", placeholder="कोई विशेष निर्देश")

        errors = []
        if not full_name or not re.match(r'^[\u0900-\u097F\sa-zA-Z]+$', full_name):
            errors.append("🔴 कृपया एक मान्य पूरा नाम दर्ज करें (केवल अक्षर और स्पेस की अनुमति है)।")
        if phone_number and (not phone_number.isdigit() or len(phone_number) != 10):
            errors.append("🔴 फोन नंबर बिल्कुल 10 अंकों का होना चाहिए।")
        if account_number and (not account_number.isdigit() or len(account_number) != 12):
            errors.append("🔴 खाता संख्या बिल्कुल 12 अंकों की होनी चाहिए।")
        if deposit_amount and not deposit_amount.isdigit():
            errors.append("🔴 निकशी राशि एक मान्य संख्या होनी चाहिए।")

        # Added the missing submit button
        submit = st.form_submit_button("✅ निकशी करें")

        if submit:
            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.success("✅ निकशी अनुरोध सफलतापूर्वक सबमिट किया गया!")
                st.write(f"खाताधारक: {full_name}")
                st.write(f"फोन: {country_code} {phone_number}")
                st.write(f"खाता संख्या: {account_number}")
                st.write(f"राशि: ₹{deposit_amount}")
                st.write(f"तारीख: {deposit_date}")
