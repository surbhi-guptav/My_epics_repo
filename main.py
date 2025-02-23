import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Set page configuration
st.set_page_config(layout="wide")

# Apply background color and styling
st.markdown(
    """
    <style>
        body {
            background-color: #0d1b2a;
        }
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #e0e1dd;
            text-align: center;
            background: linear-gradient(to right, #457b9d, #1d3557);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .subtitle {
            font-size: 30px;
            font-weight: bold;
            color: #f4a261;
            text-align: center;
            margin-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Store language and option selection in session state
if "language" not in st.session_state:
    st.session_state.language = None
if "option" not in st.session_state:
    st.session_state.option = None

# Language selection screen
if st.session_state.language is None:
    st.markdown("<div class='title'>🎙 Voice Activated Form Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>🌍 भाषा चुनें / Select a Language / ଭାଷା ଚୟନ କରନ୍ତୁ</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        col_lang1, col_lang2, col_lang3 = st.columns(3)
        
        with col_lang1:
            if st.button("English", key="english_button", use_container_width=True):
                st.session_state.language = "English"
                st.rerun()
        
        with col_lang2:
            if st.button("हिन्दी", key="hindi_button", use_container_width=True):
                st.session_state.language = "हिन्दी"
                st.rerun()
        
        with col_lang3:
            if st.button("ଓଡ଼ିଆ", key="odia_button", use_container_width=True):
                st.session_state.language = "ଓଡ଼ିଆ"
                st.rerun()

# Display deposit/withdraw options in the selected language
else:
    translations = {
        "English": {"deposit": "Deposit", "withdraw": "Withdraw", "select_option": "Select an option"},
        "हिन्दी": {"deposit": "जमा करें", "withdraw": "निकालें", "select_option": "एक विकल्प चुनें"},
        "ଓଡ଼ିଆ": {"deposit": "ଜମା କରନ୍ତୁ", "withdraw": "ଉତ୍ତୋଳନ କରନ୍ତୁ", "select_option": "ଏକ ବିକଳ୍ପ ଚୟନ କରନ୍ତୁ"}
    }

    selected_lang = st.session_state.language
    st.markdown(f"### {translations[selected_lang]['select_option']}", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"💰 {translations[selected_lang]['deposit']}", key="deposit_button", use_container_width=True):
            st.session_state.option = "Deposit"
            st.rerun()

    with col2:
        if st.button(f"💸 {translations[selected_lang]['withdraw']}", key="withdraw_button", use_container_width=True):
            st.session_state.option = "Withdraw"
            st.rerun()

    # Switch to the correct page
    if st.session_state.option:
        page_map = {
            "Deposit": {
                "English": "Deposit_eng",
                "हिन्दी": "Deposit_hin",
                "ଓଡ଼ିଆ": "Deposit_odia"
            },
            "Withdraw": {
                "English": "withdraw_eng",
                "हिन्दी": "withdraw_hin",
                "ଓଡ଼ିଆ": "withdraw_odia"
            }
        }

        selected_page = page_map[st.session_state.option][selected_lang]

        # Load the correct page
        switch_page(selected_page)
