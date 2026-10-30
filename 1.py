
import streamlit as st
import hashlib
import secrets
import base64
import hmac


st.set_page_config(
    page_title="Password Hash Converter",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================
# PASSWORD FUNCTIONS
# =====================================

def make_password(password):
    salt = secrets.token_urlsafe(12)
    iterations = 600000

    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations
    )

    encoded = base64.b64encode(dk).decode("ascii")

    return f"pbkdf2_sha256${iterations}${salt}${encoded}"


def check_password(password, encoded):
    try:
        algorithm, iterations, salt, stored_hash = encoded.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations)

        if iterations <= 0 or iterations > 10000000:
            return False

        dk = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations
        )

        calculated = base64.b64encode(dk).decode("ascii")

        return hmac.compare_digest(calculated, stored_hash)

    except (ValueError, TypeError, OverflowError):
        return False


def generate_hash(password, algorithm):

    if algorithm == "MD5":
        return hashlib.md5(password.encode()).hexdigest()

    elif algorithm == "SHA-256":
        return hashlib.sha256(password.encode()).hexdigest()

    elif algorithm == "SHA-512":
        return hashlib.sha512(password.encode()).hexdigest()

    elif algorithm == "Django PBKDF2":
        return make_password(password)


def verify_hash(password, hashed, algorithm):

    hashed = hashed.strip()

    if algorithm == "MD5":
        calculated = hashlib.md5(password.encode()).hexdigest()

        return hmac.compare_digest(calculated, hashed.lower())

    elif algorithm == "SHA-256":
        calculated = hashlib.sha256(password.encode()).hexdigest()

        return hmac.compare_digest(calculated, hashed.lower())

    elif algorithm == "SHA-512":
        calculated = hashlib.sha512(password.encode()).hexdigest()

        return hmac.compare_digest(calculated, hashed.lower())

    elif algorithm == "Django PBKDF2":
        return check_password(password, hashed)

    return False


# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

/* Main background */

.stApp {
    background: #0b1426 !important;
    color: #ffffff !important;
}

[data-testid="stAppViewContainer"] {
    background: #0b1426 !important;
}

[data-testid="stMain"] {
    background: transparent !important;
}

.block-container {
    max-width: 1100px;
    padding: 2rem 2rem 1rem 2rem;
}

/* Hide unnecessary top controls */

#MainMenu,
footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* All normal text */

.stApp p,
.stApp label,
.stApp span,
.stApp li,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp small {
    color: #f1f5f9;
}

/* Hero header */

.hero-container {
    background: linear-gradient(135deg, #172f59, #2563a6);
    border: 1px solid #365d91;
    border-radius: 18px;
    padding: 32px 20px;
    text-align: center;
    margin-bottom: 28px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
}

.hero-title {
    font-size: 32px;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
}

.hero-subtitle {
    color: #dbeafe;
    font-size: 15px;
    margin-top: 10px;
}

/* Tabs */

.stTabs [data-baseweb="tab-list"] {
    background: #14233b;
    border: 1px solid #263c5b;
    border-radius: 12px;
    padding: 8px;
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    padding: 12px 18px;
    color: #ffffff !important;
}

.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span {
    color: #ffffff !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #2563eb !important;
    border-radius: 8px;
}

.stTabs [data-baseweb="tab-highlight"] {
    background: #60a5fa;
}

.stTabs [data-baseweb="tab-panel"] {
    padding-top: 28px;
}

/* Input labels */

.stTextInput label,
.stTextArea label,
.stSelectbox label {
    color: #f8fafc !important;
    font-weight: 600;
}

/* Input fields */

.stTextInput input,
.stTextArea textarea {
    background: #172943 !important;
    color: #ffffff !important;
    border: 1px solid #3b5577 !important;
    border-radius: 9px !important;
    caret-color: white !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #a9bad0 !important;
}

/* Select box */

.stSelectbox [data-baseweb="select"] > div {
    background: #172943 !important;
    color: #ffffff !important;
    border: 1px solid #3b5577 !important;
    border-radius: 9px !important;
}

.stSelectbox [data-baseweb="select"] * {
    color: #ffffff !important;
}

/* Dropdown menu */

[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="select"] ul {
    background: #172943 !important;
}

[data-baseweb="menu"] li {
    color: white !important;
}

/* Buttons */

.stButton button,
.stDownloadButton button {
    background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    min-height: 43px;
    transition: 0.2s;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: #1d4ed8 !important;
    color: white !important;
    border: none !important;
    transform: translateY(-1px);
}

.stButton button:disabled {
    background: #334155 !important;
    color: #cbd5e1 !important;
}

/* Information cards */

.info-card {
    background: #14243c;
    border: 1px solid #304967;
    border-radius: 12px;
    padding: 17px 20px;
    margin: 12px 0 24px 0;
    color: #e2e8f0 !important;
    line-height: 1.7;
}

/* Result card */

.result-card {
    background: #10352f;
    border: 1px solid #16866a;
    padding: 18px;
    border-radius: 12px;
    color: #ecfdf5 !important;
    margin: 15px 0;
}

/* Alerts */

[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Code block */

.stCode,
[data-testid="stCode"] {
    background: #172943 !important;
    border-radius: 10px;
}

/* Download area */

[data-testid="stDownloadButton"] button {
    width: 100%;
}

/* Dividers */

hr {
    border-color: #30415b !important;
}

/* Footer */

.footer {
    text-align: center;
    border-top: 1px solid #30415b;
    margin-top: 40px;
    padding: 25px 10px;
    color: #cbd5e1;
    line-height: 2;
}

.footer-name {
    color: #60a5fa;
    font-weight: 700;
}

/* Mobile responsive */

@media (max-width: 640px) {

    .block-container {
        padding: 1rem 1rem;
    }

    .hero-container {
        padding: 25px 12px;
    }

    .hero-title {
        font-size: 23px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 9px 7px;
        font-size: 12px;
    }

}

</style>
""", unsafe_allow_html=True)


# =====================================
# HEADER
# =====================================

st.markdown("""
<div class="hero-container">
    <div class="hero-title">🔐 Password Hash Converter</div>
    <div class="hero-subtitle">
        Generate, verify and understand password hashes securely.
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================
# TABS
# =====================================

tab1, tab2, tab3 = st.tabs([
    "🔄 Normal → Hash",
    "🔍 Hash → Verify",
    "📚 Hash Information"
])


# =====================================
# TAB 1 - NORMAL TO HASH
# =====================================

with tab1:

    st.subheader("Generate Password Hash")

    st.markdown("""
    <div class="info-card">
        Convert your normal password into a cryptographic hash.
        Select your preferred algorithm and generate the result.
    </div>
    """, unsafe_allow_html=True)

    password = st.text_input(
        "Enter Normal Password",
        type="password",
        placeholder="Enter your password...",
        key="normal_password"
    )

    algorithm = st.selectbox(
        "Select Hash Algorithm",
        ["SHA-256", "SHA-512", "MD5", "Django PBKDF2"],
        key="generate_algorithm"
    )

    if st.button(
        "⚡ Generate Hash",
        type="primary",
        use_container_width=True
    ):

        if not password:
            st.warning("Please enter a password.")

        else:

            hashed = generate_hash(password, algorithm)

            st.session_state["generated_hash"] = hashed

            st.success("Hash generated successfully!")

    if st.session_state.get("generated_hash"):

        st.markdown("#### Generated Hash")

        st.text_area(
            "Your Hash",
            value=st.session_state["generated_hash"],
            height=110,
            key="hash_output"
        )

        st.download_button(
            "⬇ Download Hash",
            data=st.session_state["generated_hash"],
            file_name="password_hash.txt",
            mime="text/plain",
            use_container_width=True
        )


# =====================================
# TAB 2 - HASH TO VERIFY
# =====================================

with tab2:

    st.subheader("Verify Existing Password Hash")

    st.markdown("""
    <div class="info-card">
        Enter an existing hash and the suspected original password
        to check whether they match.
    </div>
    """, unsafe_allow_html=True)

    entered_hash = st.text_area(
        "Enter Existing Hash",
        placeholder="Paste your existing hash here...",
        height=110,
        key="existing_hash"
    )

    original_password = st.text_input(
        "Enter Password to Verify",
        type="password",
        placeholder="Enter password...",
        key="verify_password"
    )

    verify_algorithm = st.selectbox(
        "Select Hash Algorithm",
        ["SHA-256", "SHA-512", "MD5", "Django PBKDF2"],
        key="verify_algorithm"
    )

    if st.button(
        "🔍 Verify Password",
        type="primary",
        use_container_width=True
    ):

        if not entered_hash.strip() or not original_password:

            st.warning("Please fill in both fields.")

        else:

            result = verify_hash(
                original_password,
                entered_hash,
                verify_algorithm
            )

            if result:

                st.success("✅ Password Matched Successfully!")

                st.markdown("""
                <div class="result-card">
                    <b>Verification Successful</b><br>
                    The entered password matches the provided hash.
                </div>
                """, unsafe_allow_html=True)

            else:

                st.error("❌ Password Does Not Match!")


# =====================================
# TAB 3 - HASH INFORMATION
# =====================================

with tab3:

    st.subheader("Understanding Password Hashes")

    st.markdown("""
    <div class="info-card">
        A cryptographic hash is a one-way mathematical function.
        It cannot normally be converted back into its original password.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    | Algorithm | Hash Size | Description |
    |:---|:---:|:---|
    | MD5 | 128-bit | Legacy hash |
    | SHA-256 | 256-bit | SHA-2 family |
    | SHA-512 | 512-bit | SHA-2 family |
    | Django PBKDF2 | Variable | Salted password hashing |
    """)

    st.markdown("### Security Recommendations")

    st.markdown("""
    - Use Django PBKDF2 or Argon2 for password storage.
    - Avoid MD5 for password security.
    - Never store plain-text passwords.
    - Never share production password hashes.
    """)

    st.warning(
        "Hashing is not encryption. A hash cannot be directly decrypted."
    )


# =====================================
# FOOTER
# =====================================

st.markdown("""
<div class="footer">
    <div>🔐 Password Hash Converter</div>
    <div>
        Designed & Built by
        <span class="footer-name">Punit Jangir</span>
    </div>
    <div style="font-size:12px;">
        Secure Password Utilities | Streamlit
    </div>
</div>
""", unsafe_allow_html=True)
