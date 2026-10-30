
import streamlit as st
import hashlib
import secrets
import base64
import hmac


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Password Hash Converter",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# PASSWORD HASH FUNCTIONS
# ==========================================

def make_password(password):
    """Generate Django-compatible PBKDF2 SHA256 hash."""

    salt = secrets.token_urlsafe(12)
    iterations = 600000

    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations
    )

    encoded = base64.b64encode(dk).decode("ascii").strip()

    return f"pbkdf2_sha256${iterations}${salt}${encoded}"


def check_password(password, encoded):
    """Verify Django-compatible PBKDF2 SHA256 hash."""

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

        calculated = base64.b64encode(dk).decode("ascii").strip()

        return hmac.compare_digest(
            calculated,
            stored_hash
        )

    except (ValueError, TypeError, OverflowError):
        return False


def generate_hash(password, algorithm):

    if algorithm == "MD5":
        return hashlib.md5(
            password.encode("utf-8")
        ).hexdigest()

    elif algorithm == "SHA-256":
        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    elif algorithm == "SHA-512":
        return hashlib.sha512(
            password.encode("utf-8")
        ).hexdigest()

    elif algorithm == "Django PBKDF2":
        return make_password(password)

    return None


def verify_hash(password, hashed, algorithm):

    hashed = hashed.strip()

    if algorithm == "MD5":
        calculated = hashlib.md5(
            password.encode("utf-8")
        ).hexdigest()

        return hmac.compare_digest(
            calculated,
            hashed.lower()
        )

    elif algorithm == "SHA-256":
        calculated = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        return hmac.compare_digest(
            calculated,
            hashed.lower()
        )

    elif algorithm == "SHA-512":
        calculated = hashlib.sha512(
            password.encode("utf-8")
        ).hexdigest()

        return hmac.compare_digest(
            calculated,
            hashed.lower()
        )

    elif algorithm == "Django PBKDF2":
        return check_password(password, hashed)

    return False


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

#MainMenu,
footer,
header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stHeader"] {
    height: 0 !important;
    background: transparent !important;
}

.stApp {
    background: linear-gradient(
        135deg,
        #081225,
        #101e36,
        #142847
    );
    color: #ffffff;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(
        120deg,
        #172f59,
        #244d83
    );
    padding: 38px 20px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid #355b91;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,.25);
}

.hero h1 {
    color: #ffffff;
    font-size: 35px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    color: #d4e4ff;
    font-size: 15px;
    margin-bottom: 0;
}

.info-card {
    background: #14243c;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #304967;
    margin: 12px 0 22px 0;
    color: #dbeafe;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: #14233e;
    padding: 10px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    color: #dbeafe;
    border-radius: 9px;
    padding: 12px 20px;
}

.stTabs [aria-selected="true"] {
    background: #2563eb;
    color: white;
}

.stTextInput label,
.stTextArea label,
.stSelectbox label {
    color: #e2e8f0 !important;
    font-weight: 600;
}

.stTextInput input,
.stTextArea textarea {
    background: #172943 !important;
    color: white !important;
    border: 1px solid #385273 !important;
    border-radius: 10px !important;
}

.stSelectbox [data-baseweb="select"] > div {
    background: #172943;
    color: white;
    border-radius: 10px;
}

.stButton button,
.stDownloadButton button {
    background: linear-gradient(
        90deg,
        #2563eb,
        #3b82f6
    );
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 11px 20px;
    transition: .2s;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: #1d4ed8;
    color: white;
    border: none;
}

.result-card {
    background: #102f2b;
    border: 1px solid #16866a;
    padding: 18px;
    border-radius: 12px;
    color: #d1fae5;
    margin-top: 15px;
}

.footer {
    text-align: center;
    padding: 25px 10px;
    margin-top: 40px;
    color: #9fb4d0;
    border-top: 1px solid #30415b;
}

.footer strong {
    color: #60a5fa;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">

    <h1>🔐 Password Hash Converter</h1>

    <p>
        Generate, verify and understand password hashes securely.
    </p>

</div>
""", unsafe_allow_html=True)


# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3 = st.tabs([
    "🔄 Normal → Hash",
    "🔍 Hash → Verify",
    "📚 Hash Information"
])


# ==========================================
# TAB 1: NORMAL TO HASH
# ==========================================

with tab1:

    st.markdown("### Generate Password Hash")

    st.markdown("""
    <div class="info-card">
        Enter your normal password and select an algorithm
        to generate its hash.
    </div>
    """, unsafe_allow_html=True)

    password = st.text_input(
        "Enter Normal Password",
        type="password",
        key="normal_password",
        placeholder="Enter your password..."
    )

    algorithm = st.selectbox(
        "Select Hash Algorithm",
        [
            "SHA-256",
            "SHA-512",
            "MD5",
            "Django PBKDF2"
        ],
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

            with st.spinner("Generating hash..."):

                hashed = generate_hash(
                    password,
                    algorithm
                )

                st.session_state["generated_hash"] = hashed

                st.session_state["generated_algorithm"] = algorithm

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


# ==========================================
# TAB 2: HASH TO VERIFY
# ==========================================

with tab2:

    st.markdown("### Verify Existing Password Hash")

    st.markdown("""
    <div class="info-card">
        Paste an existing password hash and enter the password
        you want to verify.
    </div>
    """, unsafe_allow_html=True)

    entered_hash = st.text_area(
        "Enter Existing Hash",
        placeholder="Paste your existing hash here...",
        height=120,
        key="existing_hash"
    )

    original_password = st.text_input(
        "Enter Password to Verify",
        type="password",
        key="verify_password",
        placeholder="Enter password..."
    )

    verify_algorithm = st.selectbox(
        "Select Hash Algorithm",
        [
            "SHA-256",
            "SHA-512",
            "MD5",
            "Django PBKDF2"
        ],
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

            with st.spinner("Verifying password..."):

                result = verify_hash(
                    original_password,
                    entered_hash,
                    verify_algorithm
                )

            if result:

                st.success("✅ Password Matched Successfully!")

                st.markdown("""
                <div class="result-card">
                    <h4>Verification Successful</h4>
                    The entered password matches the provided hash.
                </div>
                """, unsafe_allow_html=True)

            else:

                st.error("❌ Password Does Not Match!")


# ==========================================
# TAB 3: HASH INFORMATION
# ==========================================

with tab3:

    st.markdown("### Understanding Password Hashes")

    st.info(
        "Cryptographic password hashes are one-way functions. "
        "They cannot normally be converted back into their original passwords."
    )

    st.markdown("""
    | Algorithm | Hash Size | Description |
    |---|---:|---|
    | MD5 | 128-bit | Legacy hash |
    | SHA-256 | 256-bit | SHA-2 family |
    | SHA-512 | 512-bit | SHA-2 family |
    | Django PBKDF2 | Variable | Salted password hashing |

    ### Security Recommendations

    - Use Django PBKDF2 or Argon2 for password storage.
    - Avoid MD5 for password security.
    - Never store plain-text passwords.
    - Never share production password hashes.
    """)

    st.warning(
        "Hashing is not encryption. A hash cannot be directly decrypted."
    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">

    <div>🔐 Password Hash Converter</div>

    <div style="margin-top:8px;">
        Designed & Built by
        <strong>Punit Jangir</strong>
    </div>

    <div style="font-size:12px; margin-top:8px;">
        Secure Password Utilities | Streamlit
    </div>

</div>
""", unsafe_allow_html=True)
