"""
IssueInsight - AI-Powered GitHub Issue Analyzer
Advanced issue triage and analysis system powered by GPT-4
Created for intelligent project management and development workflow optimization
"""

import streamlit as st
import requests
import json
from typing import Optional
import time
from datetime import datetime


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="IssueInsight | AI-Powered GitHub Analysis",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/chetana7483/AI-Powered-GitHub-Issue-Assistant',
        'Report a bug': 'https://github.com/chetana7483/AI-Powered-GitHub-Issue-Assistant/issues',
        'About': "IssueInsight - Transform GitHub issues into actionable intelligence"
    }
)


# ============================================================================
# ADVANCED STYLING WITH MODERN UI/UX PRINCIPLES
# ============================================================================
st.markdown("""
<style>
    /* ===== FONT IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* ===== BASE THEME ===== */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        padding: 2rem 1rem;
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* ===== HEADER SECTION ===== */
    .header-container {
        text-align: center;
        padding: 4rem 1rem 3rem;
        margin-bottom: 3rem;
        position: relative;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, transparent, #3b82f6, transparent);
        border-radius: 2px;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 50%, #2563eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.75rem;
        letter-spacing: -2px;
        line-height: 1.2;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    
    /* ===== CARD COMPONENTS ===== */
    .card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        margin-bottom: 2rem;
        border: 2px solid rgba(59, 130, 246, 0.3);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5),
                    0 0 0 1px rgba(59, 130, 246, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }
    
    .card:hover {
        border-color: rgba(59, 130, 246, 0.5);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6),
                    0 0 0 1px rgba(59, 130, 246, 0.25),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }
    
    /* ===== BUTTONS ===== */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.05rem;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        letter-spacing: 0.3px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* ===== INPUT FIELDS ===== */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input {
        background: #1e293b !important;
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 500 !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15) !important;
        background: #1e293b !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #64748b !important;
        font-weight: 400 !important;
    }
    
    /* ===== LABELS ===== */
    label {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.75rem !important;
        letter-spacing: 0.3px !important;
    }
    
    /* ===== RESULTS SECTION ===== */
    .result-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(59, 130, 246, 0.4);
        position: relative;
    }
    
    .result-header:first-child {
        margin-top: 0;
    }
    
    .result-header::before {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 60px;
        height: 2px;
        background: #60a5fa;
    }
    
    .result-text {
        color: #e2e8f0;
        font-size: 1.05rem;
        line-height: 1.8;
        font-weight: 400;
        margin-bottom: 1rem;
    }
    
    /* ===== PRIORITY BADGES ===== */
    .priority {
        display: inline-block;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.3rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .priority:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
    }
    
    .p-5 { 
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: white;
        border: 2px solid rgba(220, 38, 38, 0.3);
    }
    
    .p-4 { 
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        border: 2px solid rgba(245, 158, 11, 0.3);
    }
    
    .p-3 { 
        background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
        color: #0a0e27;
        border: 2px solid rgba(234, 179, 8, 0.3);
    }
    
    .p-2 { 
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        border: 2px solid rgba(34, 197, 94, 0.3);
    }
    
    .p-1 { 
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: 2px solid rgba(59, 130, 246, 0.3);
    }
    
    /* ===== LABEL TAGS ===== */
    .label-tag {
        display: inline-block;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #60a5fa;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        margin: 0.4rem 0.3rem;
        font-size: 0.95rem;
        font-weight: 600;
        border: 1px solid rgba(59, 130, 246, 0.3);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.3px;
    }
    
    .label-tag:hover {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        border-color: rgba(59, 130, 246, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* ===== ALERTS ===== */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 12px !important;
        color: #86efac !important;
        padding: 1rem 1.5rem !important;
        font-weight: 500 !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
        color: #fca5a5 !important;
        padding: 1rem 1.5rem !important;
        font-weight: 500 !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
        color: #fcd34d !important;
        padding: 1rem 1.5rem !important;
        font-weight: 500 !important;
    }
    
    /* ===== DOWNLOAD BUTTON ===== */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.9rem 1.8rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5) !important;
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: #141b2d !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #1e293b !important;
        border-color: rgba(59, 130, 246, 0.4) !important;
    }
    
    /* ===== CODE BLOCKS ===== */
    .stCode {
        border-radius: 12px !important;
        background: #0f172a !important;
        border: 1px solid #1e293b !important;
        padding: 1rem !important;
    }
    
    /* ===== SPINNER ===== */
    .stSpinner > div {
        border-top-color: #3b82f6 !important;
        border-right-color: #3b82f6 !important;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        margin: 3rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent) !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0e27;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }
    
    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu, footer, [data-testid="stToolbar"], .stDeployButton {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .card {
            padding: 2rem 1.5rem;
        }
        
        .header-container {
            padding: 2rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# API CONFIGURATION
# ============================================================================
def get_api_url() -> str:
    """
    Get the backend API URL
    Returns the localhost URL by default, can be configured for production
    """
    return "http://localhost:8000"


# ============================================================================
# API COMMUNICATION FUNCTIONS
# ============================================================================
def analyze_issue(repo_url: str, issue_number: int) -> Optional[dict]:
    """
    Send issue analysis request to backend API
    
    Args:
        repo_url: Full GitHub repository URL
        issue_number: Issue number to analyze
        
    Returns:
        dict: Analysis results with summary, priority, labels, etc.
        None: If request fails
    """
    api_url = get_api_url()
    
    try:
        response = requests.post(
            f"{api_url}/analyze",
            json={
                "repo_url": repo_url,
                "issue_number": issue_number
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_detail = response.json().get("detail", "Unknown error occurred")
            st.error(f"❌ **Analysis Failed:** {error_detail}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("""
        ### 🔌 Backend Connection Error
        
        **The backend API server is not responding.**
        
        Please ensure the backend is running:
        
        ```bash
        cd backend
        python -m uvicorn main:app --reload
        ```
        
        The server should be accessible at `http://localhost:8000`
        """)
        return None
        
    except requests.exceptions.Timeout:
        st.error("""
        ### ⏱️ Request Timeout
        
        The analysis is taking longer than expected. This could be due to:
        - Large issue with many comments
        - High API load
        - Network connectivity issues
        
        Please try again in a moment.
        """)
        return None
        
    except Exception as e:
        st.error(f"❌ **Unexpected Error:** {str(e)}")
        return None


# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    """
    Main application entry point
    Renders the complete UI and handles user interactions
    """
    
    # ===== HEADER SECTION =====
    st.markdown("""
    <div class="header-container">
        <div class="main-title">IssueInsight</div>
        <div class="subtitle">AI-Powered GitHub Issue Analysis & Intelligence</div>
        <div style="margin-top: 1rem; color: #60a5fa; font-size: 0.95rem; font-weight: 600; letter-spacing: 1px;">
            🌱 SEEDLING LABS TASK
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== INPUT SECTION =====
    col1, col2 = st.columns([3, 1])
    
    with col1:
        repo_url = st.text_input(
            "📂 Repository URL",
            placeholder="https://github.com/facebook/react",
            help="Enter the complete GitHub repository URL",
            label_visibility="visible"
        )
    
    with col2:
        issue_number = st.number_input(
            "🔢 Issue Number",
            min_value=1,
            value=1,
            help="Issue number to analyze",
            label_visibility="visible"
        )
    
    # Spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Analyze button
    analyze_clicked = st.button("🚀 Analyze Issue")
    
    # ===== EXAMPLES SECTION =====
    with st.expander("💡 Try Example Issues"):
        st.markdown("<p style='color: #94a3b8; margin-bottom: 1rem;'>Click any example to load instantly:</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⚛️ React\n#28000", use_container_width=True, key="ex1"):
                st.session_state.ex = ("https://github.com/facebook/react", 28000)
                st.rerun()
        
        with col2:
            if st.button("💻 VS Code\n#190000", use_container_width=True, key="ex2"):
                st.session_state.ex = ("https://github.com/microsoft/vscode", 190000)
                st.rerun()
        
        with col3:
            if st.button("▲ Next.js\n#50000", use_container_width=True, key="ex3"):
                st.session_state.ex = ("https://github.com/vercel/next.js", 50000)
                st.rerun()
    
    # ===== HANDLE EXAMPLE SELECTION =====
    if 'ex' in st.session_state:
        repo_url, issue_number = st.session_state.ex
        del st.session_state.ex
        analyze_clicked = True
    
    # ===== PROCESS ANALYSIS REQUEST =====
    if analyze_clicked:
        # Validation
        if not repo_url:
            st.error("⚠️ Please enter a repository URL")
            return
        
        if "github.com" not in repo_url.lower():
            st.error("⚠️ Please enter a valid GitHub repository URL")
            return
        
        # Show progress
        with st.spinner("🔄 Fetching issue data from GitHub..."):
            time.sleep(0.5)
        
        with st.spinner("🧠 AI is analyzing the issue... This may take 15-30 seconds"):
            analysis = analyze_issue(repo_url, issue_number)
        
        # ===== DISPLAY RESULTS =====
        if analysis:
            st.success("✨ **Analysis Complete!**")
            
            # Priority Score - combine card opening with content
            priority_num = analysis["priority_score"].split()[0] if analysis["priority_score"] else "3"
            st.markdown(f"""
            <div class="card">
                <div class="result-header">📊 Priority Assessment</div>
                <div class="priority p-{priority_num}">
                    🎯 Priority: Level {priority_num}/5
                </div>
                <p class="result-text">{analysis.get("priority_score", "Priority information not available")}</p>
            """, unsafe_allow_html=True)
            
            # Summary
            st.markdown('<div class="result-header">📝 Executive Summary</div>', unsafe_allow_html=True)
            st.markdown(f'<p class="result-text">{analysis.get("summary", "No summary available")}</p>', unsafe_allow_html=True)
            
            # Type Classification
            st.markdown('<div class="result-header">🏷️ Issue Classification</div>', unsafe_allow_html=True)
            type_emoji = {
                "bug": "🐛",
                "feature_request": "✨",
                "documentation": "📚",
                "question": "❓",
                "enhancement": "⚡",
                "performance": "🚀"
            }
            issue_type = analysis.get("type", "unknown")
            emoji = type_emoji.get(issue_type.lower(), "📌")
            display_type = issue_type.replace("_", " ").title()
            st.markdown(f'<span class="label-tag">{emoji} {display_type}</span>', unsafe_allow_html=True)
            
            # Suggested Labels
            st.markdown('<div class="result-header">🎯 Recommended Labels</div>', unsafe_allow_html=True)
            labels = analysis.get("suggested_labels", [])
            if labels:
                labels_html = "".join([f'<span class="label-tag">{label}</span>' for label in labels])
                st.markdown(labels_html, unsafe_allow_html=True)
            else:
                st.markdown('<p class="result-text">No labels suggested</p>', unsafe_allow_html=True)
            
            # Impact Analysis
            st.markdown('<div class="result-header">💥 Impact Assessment</div>', unsafe_allow_html=True)
            st.markdown(f'<p class="result-text">{analysis.get("potential_impact", "Impact analysis not available")}</p>', unsafe_allow_html=True)
            
            # Export Section
            st.markdown('<div class="result-header">📦 Export Results</div>', unsafe_allow_html=True)
            json_data = json.dumps(analysis, indent=2)
            
            st.download_button(
                "💾 Download as JSON",
                data=json_data,
                file_name=f"issue_analysis_{issue_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Raw JSON viewer outside the card
            with st.expander("📋 View Raw JSON"):
                st.code(json_data, language="json")
    
    # ===== FOOTER =====
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 2rem 1rem;'>
        <p style='font-size: 1rem; margin-bottom: 0.5rem; font-weight: 500;'>
            ⚡ Powered by <strong style='color: #3b82f6;'>OpenAI GPT-4o-mini</strong>
        </p>
        <p style='font-size: 0.9rem; opacity: 0.8;'>
            Built with FastAPI • LangChain • Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    main()
