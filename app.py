import os
from dotenv import load_dotenv

# load environment variables before importing anything else that may
# rely on OPENAI_API_KEY. Streamlit spawns worker processes that import
# this module at startup, so we want the key available as early as
# possible.
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment")

import streamlit as st
from src.vectorstore import load_index, rebuild_index_from_dir
from src.rag_chain import build_rag
from src.uploader import save_uploaded_file

# ─────────────────────────────────────────────
# Page Config  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Folio · Document Intelligence",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# Global CSS — dark clinical aesthetic
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@300;400;500;600&display=swap');

    /* ── Base ─────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: #0b0f14;
        color: #e8eaf0;
    }

    /* ── Hide default Streamlit chrome ────── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Hero banner ──────────────────────── */
    .hero {
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 3rem 0 1.5rem;
    }
    .hero-icon {
        font-size: 3.2rem;
        line-height: 1;
        filter: drop-shadow(0 0 16px #3ecfcf88);
    }
    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.9rem;
        font-weight: 400;
        letter-spacing: -0.02em;
        color: #f0f4ff;
        line-height: 1.1;
        margin: 0;
    }
    .hero-title span { color: #3ecfcf; font-style: italic; }
    .hero-sub {
        font-size: 0.85rem;
        color: #7a8499;
        margin-top: 0.3rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    /* ── Divider ──────────────────────────── */
    .hr { border: none; border-top: 1px solid #1e2535; margin: 0.5rem 0 2rem; }

    /* ── Card containers ──────────────────── */
    .card {
        background: #111620;
        border: 1px solid #1e2535;
        border-radius: 14px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
    }
    .card-accent { border-left: 3px solid #3ecfcf; }

    /* ── Section labels ───────────────────── */
    .section-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #3ecfcf;
        margin-bottom: 0.6rem;
    }

    /* ── Streamlit text_input override ────── */
    .stTextInput > div > div > input {
        background: #0d1117 !important;
        border: 1px solid #2a3347 !important;
        border-radius: 10px !important;
        color: #e8eaf0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: border-color 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3ecfcf !important;
        box-shadow: 0 0 0 3px #3ecfcf22 !important;
    }

    /* ── File uploader ────────────────────── */
    .stFileUploader > div {
        background: #0d1117 !important;
        border: 1px dashed #2a3347 !important;
        border-radius: 10px !important;
        color: #7a8499 !important;
    }
    .stFileUploader > div:hover {
        border-color: #3ecfcf !important;
    }

    /* ── Buttons ─────────────────────────── */
    .stButton > button {
        background: #3ecfcf !important;
        color: #0b0f14 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.55rem 1.4rem !important;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: #5adcdc !important;
        box-shadow: 0 0 16px #3ecfcf55 !important;
        transform: translateY(-1px);
    }

    /* ── Answer block ─────────────────────── */
    .answer-box {
        background: linear-gradient(135deg, #111e2a 0%, #0d1821 100%);
        border: 1px solid #1e3a4a;
        border-left: 4px solid #3ecfcf;
        border-radius: 12px;
        padding: 1.6rem 1.8rem;
        font-size: 1.02rem;
        line-height: 1.75;
        color: #d4e0f0;
        margin: 1rem 0;
    }

    /* ── Source pill ─────────────────────── */
    .source-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #151c2b;
        border: 1px solid #2a3347;
        border-radius: 20px;
        padding: 4px 14px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        color: #8fa8cc;
        margin: 4px 4px 4px 0;
    }

    /* ── Spinner override ─────────────────── */
    .stSpinner > div { border-top-color: #3ecfcf !important; }

    /* ── Info / warning strip ─────────────── */
    .notice-strip {
        background: #0d1821;
        border: 1px solid #1e3a4a;
        border-radius: 10px;
        padding: 0.75rem 1.2rem;
        font-size: 0.82rem;
        color: #6b8aaa;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 2rem;
    }

    /* ── Upload count badge ───────────────── */
    .badge {
        background: #1c2d3f;
        color: #3ecfcf;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        border-radius: 6px;
        padding: 2px 8px;
        margin-left: 8px;
    }

    /* ── History entry ────────────────────── */
    .history-entry {
        border-left: 2px solid #1e2535;
        padding-left: 1rem;
        margin-bottom: 1.2rem;
        opacity: 0.7;
        transition: opacity 0.2s;
    }
    .history-entry:hover { opacity: 1; border-left-color: #3ecfcf88; }
    .history-q {
        font-size: 0.8rem;
        color: #7a8499;
        font-family: 'IBM Plex Mono', monospace;
        margin-bottom: 0.3rem;
    }
    .history-a { font-size: 0.88rem; color: #b0bdd0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Session state init
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []          # list of {q, answer, sources}
if "upload_slots" not in st.session_state:
    st.session_state.upload_slots = 1      # number of upload widgets shown
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "index_version" not in st.session_state:
    st.session_state.index_version = 0

# ─────────────────────────────────────────────
# Load RAG system
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_system(version):
    db = load_index()
    retriever = db.as_retriever(search_kwargs={"k": 4})
    rag = build_rag(retriever)
    return rag

rag = load_system(st.session_state.index_version)

# ─────────────────────────────────────────────
# Layout  —  2 columns (main | sidebar panel)
# ─────────────────────────────────────────────
col_main, col_side = st.columns([3, 1], gap="large")

# ══════════════════════════════════════════════
#  LEFT — Main Panel
# ══════════════════════════════════════════════
with col_main:

    # Hero
    st.markdown(
        """
        <div class="hero">
            <div class="hero-icon">📚</div>
            <div>
                <div class="hero-title">Fo<span>lio</span></div>
                <div class="hero-sub">Document Intelligence Assistant</div>
            </div>
        </div>
        <hr class="hr">
        """,
        unsafe_allow_html=True,
    )

    # Disclaimer strip
    st.markdown(
        """
        <div class="notice-strip">
            ⚕️&nbsp; Answers are grounded exclusively in the uploaded documents.
            This tool is <strong>not</strong> a substitute for professional medical advice.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Query card ────────────────────────────
    st.markdown('<div class="card card-accent">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">01 · Ask a Question</div>', unsafe_allow_html=True)

    query = st.text_input(
        label="query",
        placeholder="e.g. What are the contraindications for ibuprofen in elderly patients?",
        label_visibility="collapsed",
        key="query_input",
    )

    run_btn = st.button("Search Knowledge Base →", use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Answer ───────────────────────────────
    if run_btn and query:
        with st.spinner("Retrieving and synthesising…"):
            result = rag(query)

        answer  = result.get("answer", "No answer returned.")
        sources = list(set(s for s in result.get("sources", []) if s))

        # Persist to history
        st.session_state.history.insert(0, {"q": query, "answer": answer, "sources": sources})

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">02 · Answer</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

        if sources:
            st.markdown('<div class="section-label" style="margin-top:1rem">03 · Sources</div>', unsafe_allow_html=True)
            pills_html = "".join(
                f'<span class="source-pill">📄 {s}</span>' for s in sources
            )
            st.markdown(pills_html, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    elif run_btn and not query:
        st.warning("Please enter a question before searching.")

    # ── History ───────────────────────────────
    if st.session_state.history:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Query History</div>', unsafe_allow_html=True)

        # Show at most 5 previous (skip the first/current one)
        past = st.session_state.history[1:6]
        for item in past:
            truncated_a = item["answer"][:220] + "…" if len(item["answer"]) > 220 else item["answer"]
            src_str = ", ".join(item["sources"][:2]) if item["sources"] else "—"
            st.markdown(
                f"""
                <div class="history-entry">
                    <div class="history-q">Q: {item['q']}</div>
                    <div class="history-a">{truncated_a}</div>
                    <div class="history-q" style="margin-top:4px">📄 {src_str}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

# ══════════════════════════════════════════════
#  RIGHT — Upload Panel
# ══════════════════════════════════════════════
with col_side:
    st.markdown("<br><br><br>", unsafe_allow_html=True)   # align with main content
    st.markdown(
        f'<div class="section-label">Documents'
        f'<span class="badge">{st.session_state.upload_slots} slot(s)</span></div>',
        unsafe_allow_html=True,
    )

    all_uploaded = []

    for i in range(st.session_state.upload_slots):
        uploaded = st.file_uploader(
            label=f"File {i + 1}",
            type=["pdf", "txt", "docx", "csv", "md"],
            key=f"file_upload_{i}",
            label_visibility="collapsed",
        )
        if uploaded:
            all_uploaded.append(uploaded)

    # handle new uploads by saving and rebuilding index
    for file_obj in all_uploaded:
        if file_obj.name not in st.session_state.uploaded_files:
            save_uploaded_file(file_obj)
            st.session_state.uploaded_files.append(file_obj.name)
            with st.spinner("Indexing uploaded documents…"):
                rebuild_index_from_dir("data")
            st.session_state.index_version += 1
            st.rerun()

    # Add new slot if the last one is filled
    if (
        st.session_state.upload_slots <= 8
        and len(all_uploaded) == st.session_state.upload_slots
        and all_uploaded  # at least one file
    ):
        st.session_state.upload_slots += 1
        st.rerun()

    # Summary of what's loaded
    if all_uploaded:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Loaded Files</div>', unsafe_allow_html=True)
        for f in all_uploaded:
            size_kb = round(f.size / 1024, 1)
            st.markdown(
                f'<div class="source-pill" style="display:flex;margin:4px 0;width:fit-content">'
                f'📄 {f.name} <span style="color:#4a5a70;margin-left:6px">{size_kb} KB</span>'
                f"</div>",
                unsafe_allow_html=True,
            )

        if st.button("➕ Add Another Slot"):
            if st.session_state.upload_slots < 10:
                st.session_state.upload_slots += 1
                st.rerun()

        if st.button("🗑 Reset Uploads"):
            st.session_state.upload_slots = 1
            st.session_state.uploaded_files = []
            # optionally clear data directory or rebuild
            st.rerun()

    # Tips card
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card" style="font-size:0.8rem;color:#6b8aaa;line-height:1.6">
            <div class="section-label">Tips</div>
            📌 Upload PDFs, TXT, DOCX, or CSV<br>
            🔍 Be specific in your questions<br>
            📄 Cite document names for targeted retrieval<br>
            ⚡ Up to 10 documents per session
        </div>
        """,
        unsafe_allow_html=True,
    ) 
