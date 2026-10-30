
import streamlit as st
import hashlib
import secrets
from django.contrib.auth.hashers import make_password, check_password

st.set_page_config(
    page_title="Password Hash Converter",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# CUSTOM DESIGN
# -------------------------------

st.markdown("""
<style>
#MainMenu, footer, header {
    visibility: hidden;
}

[data-testid="stHeader"] {
    height: 0px;
}

[data-testid="stToolbar"] {
    display: none;
}

.stApp {
    background: linear-gradient(135deg, #081225, #111c35);
    color: #ffffff;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(120deg, #172f59, #244d83);
    padding: 35px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid #355b91;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,.25);
}

.hero h1 {
    color: white;
    font-size: 36px;
    margin-bottom: 8px;
}

.hero p {
    color: #d4e4ff;
    font-size: 15px;
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
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 22px;
    transition: .2s;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: linear-gradient(90deg, #1d4ed8, #2563eb);
    border: none;
    color: white;
}

.info-card {
    background: #14243c;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #304967;
    margin: 12px 0;
}

.result-card {
    background: #102f2b;
    border: 1px solid #16866a;
    padding: 18px;
    border-radius: 12px;
    color: #d1fae5;
}

.footer {
    text-align: center;
    padding: 25px 10px;
    margin-top: 35px;
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


# -------------------------------
# HEADER
# -------------------------------

st.markdown("""
<div class="hero">
    <h1>🔐 Password Hash Converter</h1>
    <p>Generate, verify and understand password hashes securely.</p>
</div>
""", unsafe_allow_html=True)


# -------------------------------
# TABS
# -------------------------------

tab1, tab2, tab3 = st.tabs([
    "🔄 Normal → Hash",
    "🔍 Hash → Verify",
    "📚 Hash Information"
])


# -------------------------------
# NORMAL TO HASH
# -------------------------------

with tab1:

    st.markdown("### Generate Password Hash")

    st.markdown("""
    <div class="info-card">
        Convert your normal password into a cryptographic hash.
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
        ]
    )

    if st.button("⚡ Generate Hash", type="primary"):

        if not password:
            st.warning("Please enter a password.")

        else:

            if algorithm == "SHA-256":
                hashed = hashlib.sha256(
                    password.encode()
                ).hexdigest()

            elif algorithm == "SHA-512":
                hashed = hashlib.sha512(
                    password.encode()
                ).hexdigest()

            elif algorithm == "MD5":
                hashed = hashlib.md5(
                    password.encode()
                ).hexdigest()

            else:
                hashed = make_password(password)

            st.success("Hash generated successfully!")

            st.text_area(
                "Generated Hash",
                value=hashed,
                height=110,
                key="generated_hash"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    "⬇ Download Hash",
                    data=hashed,
                    file_name="password_hash.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with col2:
                st.button(
                    "✅ Hash Generated",
                    disabled=True,
                    use_container_width=True
                )


# -------------------------------
# HASH TO VERIFY
# -------------------------------

with tab2:

    st.markdown("### Verify Existing Password Hash")

    st.markdown("""
    <div class="info-card">
        Enter an existing hash and its suspected original password
        to check whether they match.
    </div>
    """, unsafe_allow_html=True)

    entered_hash = st.text_area(
        "Enter Existing Hash",
        placeholder="Paste your existing hash here...",
        height=110
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

    if st.button("🔍 Verify Password", type="primary"):

        if not entered_hash.strip() or not original_password:
            st.warning("Please fill in both fields.")

        else:

            try:

                if verify_algorithm == "SHA-256":
                    calculated = hashlib.sha256(
                        original_password.encode()
                    ).hexdigest()

                    result = secrets.compare_digest(
                        calculated,
                        entered_hash.strip().lower()
                    )

                elif verify_algorithm == "SHA-512":
                    calculated = hashlib.sha512(
                        original_password.encode()
                    ).hexdigest()

                    result = secrets.compare_digest(
                        calculated,
                        entered_hash.strip().lower()
                    )

                elif verify_algorithm == "MD5":
                    calculated = hashlib.md5(
                        original_password.encode()
                    ).hexdigest()

                    result = secrets.compare_digest(
                        calculated,
                        entered_hash.strip().lower()
                    )

                else:
                    result = check_password(
                        original_password,
                        entered_hash.strip()
                    )

                if result:
                    st.success("✅ Password Matched Successfully!")
                else:
                    st.error("❌ Password Does Not Match!")

            except Exception:
                st.error("Invalid hash format or verification error.")


# -------------------------------
# HASH INFORMATION
# -------------------------------

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
    | SHA-256 | 256-bit | Secure general-purpose hash |
    | SHA-512 | 512-bit | SHA-2 family |
    | Django PBKDF2 | Variable | Salted password hashing |

    #### Security Recommendations

    - Use Django PBKDF2 or Argon2 for password storage.
    - Avoid MD5 for password security.
    - Never store plain-text passwords.
    - Never share real production password hashes.
    """)

    st.warning(
        "Hashing is not encryption. A hash cannot be directly decrypted."
    )


# -------------------------------
# FOOTER
# -------------------------------

st.markdown("""
<div class="footer">
    <div>🔐 Password Hash Converter</div>
    <div>Designed & Built by <strong>Punit Jangir</strong></div>
    <div style="font-size:12px; margin-top:8px;">
        Secure Password Utilities | Streamlit
    </div>
</div>
""", unsafe_allow_html=True)
